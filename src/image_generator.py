from __future__ import annotations

import base64
from datetime import datetime

from openai import OpenAI

from .config import (
    IMAGE_GENERATION_ENABLED,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENROUTER_IMAGE_MODEL,
    OPENROUTER_IMAGE_SIZE,
    OUTPUT_IMAGES_DIR,
)


DISABLED_STATUS = "圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。"
MISSING_CONFIG_STATUS = "圖片生成功能已啟用，但缺少 OpenRouter API key 或 image model 設定。目前僅顯示圖片生成 Prompt。"
FAILURE_STATUS = "圖片生成失敗，可能是模型不支援圖片輸出、API 額度不足，或 OpenRouter 回應格式不同。目前保留 Prompt-only 結果。"
SUCCESS_STATUS = "圖片生成成功。"


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _walk(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk(item)


def _extract_base64_image(response) -> str | None:
    data = response.model_dump() if hasattr(response, "model_dump") else response
    for node in _walk(data):
        for key in ("b64_json", "base64", "image_base64"):
            value = node.get(key)
            if isinstance(value, str) and len(value) > 100:
                return value.split(",", 1)[-1]
        url = node.get("url") or node.get("image_url")
        if isinstance(url, str) and url.startswith("data:image"):
            return url.split(",", 1)[-1]
    return None


def generate_tank_image(prompt: str) -> tuple[str | None, str]:
    if not IMAGE_GENERATION_ENABLED:
        return None, DISABLED_STATUS
    if not OPENAI_API_KEY or not OPENROUTER_IMAGE_MODEL:
        return None, MISSING_CONFIG_STATUS

    try:
        OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model=OPENROUTER_IMAGE_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate a safe realistic turtle tank layout image at {OPENROUTER_IMAGE_SIZE}.\n\n"
                        f"{prompt}"
                    ),
                }
            ],
            modalities=["image", "text"],
        )
        image_b64 = _extract_base64_image(response)
        if not image_b64:
            return None, FAILURE_STATUS

        image_bytes = base64.b64decode(image_b64)
        filename = f"turtle_tank_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = OUTPUT_IMAGES_DIR / filename
        path.write_bytes(image_bytes)
        return str(path), SUCCESS_STATUS
    except Exception:
        return None, FAILURE_STATUS
