# RAG Module Spec

## Purpose

定義 `src/rag.py` 的 local Markdown RAG retriever。MVP 使用 TF-IDF，不依賴外部 vector database 或下載 embedding model。

## Responsibilities

- Load Markdown files from `data/knowledge_base/`.
- Split Markdown documents by headings and paragraphs.
- Build a deterministic TF-IDF index at startup or first use.
- Retrieve top 3 relevant chunks.
- Return source filename, heading, content, preview, and score.
- Format retrieved context for LLM prompts.

## Inputs

- Knowledge base directory path.
- User query string.
- Optional `top_k`, default 3.

## Outputs

Retrieved chunk list:

```python
[
    {
        "source": "tank_setup.md",
        "heading": "Basking Area",
        "content": "...",
        "preview": "...",
        "score": 0.42,
    }
]
```

Formatted context string for prompts.

## Data Format

Chunk object:

```python
{
    "source": str,
    "heading": str,
    "content": str,
    "preview": str,
    "score": float,
}
```

Recommended functions:

```python
load_documents() -> list[dict]
split_documents(documents: list[dict]) -> list[dict]
build_index(chunks: list[dict]) -> object
retrieve(query: str, top_k: int = 3) -> list[dict]
format_retrieved_context(chunks: list[dict]) -> str
format_references(chunks: list[dict]) -> str
```

## Error / Fallback Behavior

- If the knowledge base directory is missing, return a clear error chunk or message.
- If no Markdown files are found, return a clear error chunk or message.
- If query is empty, retrieve using a generic turtle care query or return broad references.
- Retrieval should not crash mock mode.

## Safety Requirements

- Retrieved knowledge should include health disclaimers when health topics are involved.
- Do not present retrieved text as veterinary diagnosis.

## Implementation Checklist

- [ ] Read all `.md` files from `data/knowledge_base/`.
- [ ] Preserve source filenames.
- [ ] Split documents by Markdown headings and paragraph blocks.
- [ ] Create chunk previews.
- [ ] Build `TfidfVectorizer` matrix.
- [ ] Retrieve top 3 chunks by cosine similarity.
- [ ] Return chunk dictionaries.
- [ ] Format retrieved context for prompt injection.
- [ ] Format references for UI display.

## Completion Checklist

- [ ] Retrieval works when all knowledge files exist.
- [ ] Missing knowledge files produce a clear message.
- [ ] Top-k defaults to 3.
- [ ] Retrieved references include filename and preview.
- [ ] Retrieved context is available even in mock mode.
- [ ] Retrieval results are deterministic for the same query and knowledge base.
