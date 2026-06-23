from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import KNOWLEDGE_BASE_DIR, RETRIEVAL_TOP_K


@dataclass
class RagIndex:
    chunks: list[dict]
    vectorizer: TfidfVectorizer | None
    matrix: object | None
    error: str | None = None


_INDEX: RagIndex | None = None


QUERY_EXPANSIONS = {
    "烏龜": "turtle aquatic semi-aquatic",
    "龜": "turtle",
    "紅耳": "red-eared slider",
    "斑龜": "Taiwan stripe-necked turtle",
    "麝香": "musk turtle",
    "地圖": "map turtle",
    "側頸": "African side-necked turtle",
    "水": "water depth water quality aquarium",
    "水深": "water depth resting area ramp",
    "水質": "water quality ammonia nitrite nitrate filtration",
    "過濾": "filtration filter water quality",
    "曬台": "basking area dry platform ramp",
    "曬背": "basking area heat lamp dry shell",
    "uvb": "UVB lighting calcium shell health",
    "燈": "UVB heat lamp lighting basking",
    "加溫": "heating temperature heat lamp",
    "餵": "feeding diet pellets vegetables protein calcium",
    "吃": "feeding refusing food diet health warning",
    "不吃": "refusing food stress temperature water quality veterinarian",
    "混養": "mixed species stress biting competition separation",
    "浮": "abnormal floating imbalance health warning veterinarian",
    "眼睛": "swollen eyes health warning veterinarian",
    "受傷": "wounds injury bleeding emergency veterinarian",
}


SOURCE_BOOSTS = [
    (("uvb", "燈", "照明"), "lighting_and_basking.md", 0.35),
    (("曬台", "曬背", "basking"), "tank_setup.md", 0.25),
    (("水質", "過濾", "ammonia", "nitrite", "filter"), "water_quality.md", 0.3),
    (("餵", "吃", "feeding", "diet"), "feeding.md", 0.25),
    (("混養", "mixed"), "mixed_species_warning.md", 0.3),
    (("受傷", "流血", "呼吸", "emergency"), "emergency_warning.md", 0.35),
]


def load_documents(kb_dir: Path = KNOWLEDGE_BASE_DIR) -> list[dict]:
    if not kb_dir.exists():
        return []
    documents = []
    for path in sorted(kb_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        documents.append({"source": path.name, "content": text})
    return documents


def split_documents(documents: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    for doc in documents:
        source = doc["source"]
        content = doc["content"]
        current_heading = "General"
        buffer: list[str] = []

        def flush() -> None:
            text = "\n".join(buffer).strip()
            if text:
                preview = re.sub(r"\s+", " ", text)[:220]
                chunks.append(
                    {
                        "source": source,
                        "heading": current_heading,
                        "content": text,
                        "preview": preview,
                        "score": 0.0,
                    }
                )
            buffer.clear()

        for line in content.splitlines():
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading_match:
                flush()
                current_heading = heading_match.group(2).strip()
                continue
            if not line.strip():
                flush()
                continue
            buffer.append(line)
        flush()
    return chunks


def build_index() -> RagIndex:
    documents = load_documents()
    if not documents:
        return RagIndex(
            chunks=[],
            vectorizer=None,
            matrix=None,
            error="Knowledge base files were not found. Please create Markdown files under data/knowledge_base/.",
        )

    chunks = split_documents(documents)
    if not chunks:
        return RagIndex(
            chunks=[],
            vectorizer=None,
            matrix=None,
            error="Knowledge base files exist, but no searchable chunks were created.",
        )

    vectorizer = TfidfVectorizer(stop_words="english")
    searchable_texts = [f"{chunk.get('heading', '')}\n{chunk['content']}" for chunk in chunks]
    matrix = vectorizer.fit_transform(searchable_texts)
    return RagIndex(chunks=chunks, vectorizer=vectorizer, matrix=matrix)


def get_index() -> RagIndex:
    global _INDEX
    if _INDEX is None:
        _INDEX = build_index()
    return _INDEX


def expand_query(query: str) -> str:
    expanded_terms = []
    lowered = query.lower()
    for keyword, expansion in QUERY_EXPANSIONS.items():
        if keyword.lower() in lowered:
            expanded_terms.append(expansion)
    if expanded_terms:
        return f"{query} {' '.join(expanded_terms)}"
    return query


def score_boost(query: str, chunk: dict) -> float:
    lowered = query.lower()
    source = chunk.get("source", "")
    boost = 0.0
    for keywords, target_source, value in SOURCE_BOOSTS:
        if source == target_source and any(keyword.lower() in lowered for keyword in keywords):
            boost += value
    return boost


def retrieve(query: str, top_k: int = RETRIEVAL_TOP_K) -> list[dict]:
    index = get_index()
    if index.error:
        return [
            {
                "source": "knowledge_base",
                "heading": "Knowledge base unavailable",
                "content": index.error,
                "preview": index.error,
                "score": 0.0,
            }
        ]
    assert index.vectorizer is not None and index.matrix is not None
    search_query = expand_query(query.strip()) or "turtle care tank setup water quality basking UVB feeding"
    query_vector = index.vectorizer.transform([search_query])
    scores = cosine_similarity(query_vector, index.matrix).flatten()
    for idx, chunk in enumerate(index.chunks):
        scores[idx] += score_boost(search_query, chunk)
    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked:
        chunk = dict(index.chunks[int(idx)])
        chunk["score"] = float(scores[int(idx)])
        results.append(chunk)
    return results


def format_retrieved_context(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(
            f"[{i}] Source: {chunk['source']} | Heading: {chunk.get('heading', 'General')}\n"
            f"{chunk['content']}"
        )
    return "\n\n".join(lines)


def format_references(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        score = chunk.get("score", 0.0)
        lines.append(
            f"{i}. {chunk['source']} - {chunk.get('heading', 'General')} "
            f"(score: {score:.3f})\n{chunk.get('preview', '')}"
        )
    return "\n\n".join(lines)
