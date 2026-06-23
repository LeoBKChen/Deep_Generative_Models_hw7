from __future__ import annotations

from openai import OpenAI

from .config import (
    LLM_TEMPERATURE,
    MOCK_MODE,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
)


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
                "1. 整體評估：目前環境應優先確認乾燥曬台、UVB、乾淨水質與足夠過濾。\n"
                "2. 現有優點：若已有穩定加溫、過濾或平台，請持續維護並定期檢查。\n"
                "3. 潛在風險：請先處理 rule-based risk summary 中的 high risk 項目。\n"
                "4. 優先改善清單：補足曬台、UVB、強過濾與安全休息點。\n"
                "5. 每日照護：觀察活動力、食慾、水質、溫度與是否能順利上岸曬背。\n"
                "6. 每週照護：部分換水、清理過濾器、檢查燈具與平台穩定性。\n"
                "7. 安全提醒：TurtleCare AI 不能提供獸醫診斷；若症狀嚴重、持續或惡化，請諮詢合格爬蟲類獸醫。"
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
            "根據本地知識庫脈絡，請優先確認乾淨水質、完全乾燥的曬台、UVB 照明、合適加溫、"
            "足夠過濾，以及是否避免不安全混養。TurtleCare AI 不能提供獸醫診斷；"
            "如果症狀嚴重、持續或惡化，請諮詢合格爬蟲類獸醫。"
        )
    return (
        "Mock TurtleCare AI answer:\n"
        "Based on the local knowledge context, prioritize clean water, a completely dry basking area, UVB lighting, "
        "appropriate heating, strong filtration, and species-safe housing. TurtleCare AI cannot provide veterinary "
        "diagnosis. If symptoms are severe, persistent, or worsening, consult a qualified reptile veterinarian."
    )


def generate_text(system_prompt: str, user_prompt: str) -> str:
    if MOCK_MODE:
        return _mock_response(user_prompt)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=LLM_TEMPERATURE,
        )
        content = response.choices[0].message.content
        if not content:
            return "The model returned an empty response. Please try again."
        return content
    except Exception as exc:  # noqa: BLE001 - user-facing fallback for demo stability
        return (
            "The LLM request failed, so TurtleCare AI is returning a safe fallback response.\n"
            f"Error type: {type(exc).__name__}\n\n"
            f"{_mock_response(user_prompt)}"
        )
