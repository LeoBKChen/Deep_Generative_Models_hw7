from __future__ import annotations

from .llm_client import generate_text
from .rag import format_references, format_retrieved_context, retrieve
from .risk_checker import check_risks, format_risk_summary
from .turtle_profile import format_profile


SYSTEM_PROMPT = """You are TurtleCare AI, a turtle keeping assistant.
Use the provided context and user profile to generate practical, beginner-friendly advice.
Do not provide veterinary diagnosis.
For severe, persistent, or rapidly worsening symptoms, recommend consulting a qualified reptile veterinarian.
Prioritize animal safety, water quality, basking access, UVB lighting, heating, filtration, and species compatibility.
If information is missing, state assumptions clearly.
Provide structured recommendations and actionable next steps."""


def answer_question(profile: dict, question: str) -> dict:
    query = f"{profile.get('species', '')} {question}"
    chunks = retrieve(query)
    prompt = f"""Retrieved turtle care knowledge:
{format_retrieved_context(chunks)}

User turtle profile:
{format_profile(profile)}

User question:
{question}

Task:
Answer the user's question using the retrieved knowledge and the turtle profile.
Give practical advice.
Mention uncertainty when needed.
Do not provide veterinary diagnosis.
If the question involves health symptoms, include a safety warning when appropriate.
Follow the user's input language when possible."""
    return {
        "answer": generate_text(SYSTEM_PROMPT, prompt),
        "references": chunks,
        "references_text": format_references(chunks),
    }


def generate_diagnosis_report(profile: dict) -> dict:
    risks = check_risks(profile)
    risk_summary = format_risk_summary(risks)
    query = f"{profile.get('species', '')} tank setup water quality UVB basking feeding {profile.get('current_concern', '')}"
    chunks = retrieve(query)
    prompt = f"""Retrieved turtle care knowledge:
{format_retrieved_context(chunks)}

User turtle and tank profile:
{format_profile(profile)}

Rule-based risk results:
{risk_summary}

Task:
Generate a structured turtle tank environment diagnosis report.

The report must include:
1. Overall assessment
2. Current strengths
3. Potential risks
4. Priority improvement checklist
5. Daily care checklist
6. Weekly care checklist
7. Safety warnings

Follow the user's input language when possible."""
    return {
        "report": generate_text(SYSTEM_PROMPT, prompt),
        "risk_summary": risk_summary,
        "references": chunks,
        "references_text": format_references(chunks),
    }
