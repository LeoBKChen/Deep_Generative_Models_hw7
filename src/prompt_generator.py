from __future__ import annotations

from .llm_client import generate_text
from .rag import format_references, format_retrieved_context, retrieve
from .turtle_profile import format_profile


DESIGN_SYSTEM_PROMPT = """You are TurtleCare AI, a turtle tank design assistant.
Generate safe, realistic turtle tank design prompts.
Do not provide veterinary diagnosis.
The generated image prompt is for visualization only, not an engineering blueprint."""


def _parse_design_response(text: str) -> dict:
    sections = {
        "image_prompt": "",
        "negative_prompt": "",
        "materials": "",
        "safety_notes": "",
    }
    current = None
    aliases = {
        "english image prompt": "image_prompt",
        "image prompt": "image_prompt",
        "negative prompt": "negative_prompt",
        "suggested materials": "materials",
        "materials": "materials",
        "safety notes": "safety_notes",
    }
    for raw_line in text.splitlines():
        line = raw_line.strip()
        key = aliases.get(line.lower().rstrip(":"))
        if key:
            current = key
            continue
        for label, mapped in aliases.items():
            prefix = f"{label}:"
            if line.lower().startswith(prefix):
                current = mapped
                sections[current] += line[len(prefix):].strip() + "\n"
                break
        else:
            if current:
                sections[current] += raw_line + "\n"

    if not sections["image_prompt"]:
        sections["image_prompt"] = text
    if not sections["negative_prompt"]:
        sections["negative_prompt"] = "sharp decorations, unstable rocks, small gravel, dirty water, overcrowded layout, unsafe ramp"
    if not sections["materials"]:
        sections["materials"] = "Stable basking platform, non-slip ramp, UVB light, heat lamp, strong filter, thermometer, safe decorations."
    if not sections["safety_notes"]:
        sections["safety_notes"] = "Generated designs are for visualization only. Confirm real equipment safety before setup."
    return {key: value.strip() for key, value in sections.items()}


def generate_design_prompt(profile: dict) -> dict:
    query = (
        f"{profile.get('species', '')} turtle tank basking ramp UVB filter "
        f"{profile.get('desired_style', '')} {profile.get('required_elements', '')}"
    )
    chunks = retrieve(query)
    prompt = f"""User requirements:
{format_profile(profile)}

Relevant turtle care knowledge:
{format_retrieved_context(chunks)}

Task:
Generate:
1. A diffusion-ready English image prompt
2. A negative prompt
3. A practical material list
4. Safety notes

The design must prioritize turtle safety, stable basking access, clean water, realistic tank layout, and accessible dry basking area.
Use clear section labels:
English image prompt:
Negative prompt:
Suggested materials:
Safety notes:"""
    response = generate_text(DESIGN_SYSTEM_PROMPT, prompt)
    parsed = _parse_design_response(response)
    parsed["references"] = chunks
    parsed["references_text"] = format_references(chunks)
    return parsed
