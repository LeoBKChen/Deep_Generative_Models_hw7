from __future__ import annotations

from collections.abc import Callable

from openai import OpenAI

from .config import (
    GEMINI_API_KEY,
    GOOGLE_TEXT_MODEL,
    LLM_TEMPERATURE,
    MOCK_MODE,
    OPENAI_API_KEY,
    OPENAI_TEXT_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_TEXT_MODEL,
    PROVIDER_TIMEOUT_SECONDS,
    TEXT_PROVIDER_ORDER,
)


SUPPORTED_TEXT_PROVIDERS = {"openrouter", "openai", "google"}


def _looks_chinese(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def _mock_response(user_prompt: str) -> str:
    lower = user_prompt.lower()
    use_chinese = _looks_chinese(user_prompt)
    if "diffusion-ready" in lower or "image prompt" in lower:
        return (
            "English image prompt:\n"
            "A realistic indoor aquatic turtle tank setup, clean clear water, stable dry basking platform "
            "with a gentle ramp, UVB and heat lamp above the basking area, strong external filter, safe resting "
            "areas, natural aquatic plants, practical educational aquarium layout, realistic lighting.\n\n"
            "Negative prompt:\n"
            "sharp decorations, unstable rocks, tiny gravel, dirty water, overcrowded tank, unsafe ramp, fantasy layout.\n\n"
            "Suggested materials:\n"
            "Large aquarium, secure basking platform, non-slip ramp, UVB lamp, heat lamp, strong filter, thermometer.\n\n"
            "Safety notes:\n"
            "This design is for visualization only. Confirm real equipment dimensions and prioritize turtle safety."
        )
    if "structured turtle tank environment diagnosis report" in lower or "rule-based risk results" in lower:
        if use_chinese:
            return (
                "Mock environment diagnosis report:\n"
                "1. 整體評估：請優先確認乾燥曬台、UVB 燈、乾淨水質與穩定過濾。\n"
                "2. 目前優點：若已有過濾、加溫或穩固平台，請持續維護並定期檢查。\n"
                "3. 潛在風險：請先處理 rule-based risk summary 中標示為 high 的項目。\n"
                "4. 優先改善清單：補足曬台、UVB、強力過濾與安全上下岸路徑。\n"
                "5. 每日照護：觀察活動力、水色、溫度、曬背狀況與剩餘食物。\n"
                "6. 每週照護：局部換水、檢查濾材、清潔設備並確認燈具仍正常。\n"
                "7. 安全提醒：TurtleCare AI 不能提供獸醫診斷；若症狀嚴重、持續或惡化，請諮詢爬蟲類獸醫。"
            )
        return (
            "Mock diagnosis report:\n"
            "1. Overall assessment: The setup should prioritize dry basking access, UVB lighting, clean water, and filtration.\n"
            "2. Current strengths: Any existing filtration, heating, or stable platform should be maintained.\n"
            "3. Potential risks: Review the rule-based risk summary below and fix high-priority items first.\n"
            "4. Priority improvement checklist: Add/verify basking area, UVB light, strong filtration, and safe resting access.\n"
            "5. Daily care checklist: Check behavior, water clarity, temperature, basking access, and feeding leftovers.\n"
            "6. Weekly care checklist: Partial water changes, filter inspection, equipment check, and tank cleaning.\n"
            "7. Safety warnings: TurtleCare AI cannot provide veterinary diagnosis. Severe or worsening symptoms require a reptile veterinarian."
        )
    if use_chinese:
        return (
            "Mock TurtleCare AI answer:\n"
            "根據本地知識庫，請優先確認乾淨水質、完全乾燥且容易上下的曬台、UVB 燈、合適加溫、"
            "足夠過濾與符合物種需求的飼養空間。TurtleCare AI 不能提供獸醫診斷；如果症狀嚴重、"
            "持續或惡化，請諮詢合格的爬蟲類獸醫。"
        )
    return (
        "Mock TurtleCare AI answer:\n"
        "Based on the local knowledge context, prioritize clean water, a completely dry basking area, UVB lighting, "
        "appropriate heating, strong filtration, and species-safe housing. TurtleCare AI cannot provide veterinary "
        "diagnosis. If symptoms are severe, persistent, or worsening, consult a qualified reptile veterinarian."
    )


def _extract_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        content = None
    if isinstance(content, str) and content.strip():
        return content.strip()

    raise ValueError("Provider returned an empty text response.")


def _generate_openrouter_text(system_prompt: str, user_prompt: str) -> str:
    if not OPENROUTER_API_KEY or not OPENROUTER_TEXT_MODEL:
        raise ValueError("OpenRouter API key or text model is not configured.")
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        timeout=PROVIDER_TIMEOUT_SECONDS,
    )
    response = client.chat.completions.create(
        model=OPENROUTER_TEXT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=LLM_TEMPERATURE,
    )
    return _extract_text(response)


def _generate_openai_text(system_prompt: str, user_prompt: str) -> str:
    if not OPENAI_API_KEY or not OPENAI_TEXT_MODEL:
        raise ValueError("OpenAI API key or text model is not configured.")
    client = OpenAI(api_key=OPENAI_API_KEY, timeout=PROVIDER_TIMEOUT_SECONDS)
    response = client.responses.create(
        model=OPENAI_TEXT_MODEL,
        instructions=system_prompt,
        input=user_prompt,
        temperature=LLM_TEMPERATURE,
    )
    return _extract_text(response)


def _generate_google_text(system_prompt: str, user_prompt: str) -> str:
    if not GEMINI_API_KEY or not GOOGLE_TEXT_MODEL:
        raise ValueError("Gemini API key or text model is not configured.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("google-genai is not installed.") from exc

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"{system_prompt}\n\nUser request:\n{user_prompt}"

    if hasattr(client, "interactions"):
        response = client.interactions.create(model=GOOGLE_TEXT_MODEL, input=prompt)
    else:
        response = client.models.generate_content(model=GOOGLE_TEXT_MODEL, contents=prompt)
    return _extract_text(response)


TEXT_PROVIDER_FUNCTIONS: dict[str, Callable[[str, str], str]] = {
    "openrouter": _generate_openrouter_text,
    "openai": _generate_openai_text,
    "google": _generate_google_text,
}


def generate_text(system_prompt: str, user_prompt: str) -> str:
    if MOCK_MODE:
        return _mock_response(user_prompt)

    failures: list[str] = []
    for provider in TEXT_PROVIDER_ORDER:
        if provider not in SUPPORTED_TEXT_PROVIDERS:
            failures.append(f"{provider}: unsupported provider")
            continue
        try:
            return TEXT_PROVIDER_FUNCTIONS[provider](system_prompt, user_prompt)
        except Exception as exc:  # noqa: BLE001 - provider fallback must be demo-safe
            failures.append(f"{provider}: {type(exc).__name__}")

    failure_summary = "; ".join(failures) if failures else "no provider was configured"
    return (
        "The LLM provider fallback chain failed, so TurtleCare AI is returning a safe mock response.\n"
        f"Provider failures: {failure_summary}\n\n"
        f"{_mock_response(user_prompt)}"
    )
