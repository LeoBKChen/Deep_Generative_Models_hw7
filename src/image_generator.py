from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import datetime

import requests
from openai import OpenAI

from .config import (
    GEMINI_API_KEY,
    GOOGLE_IMAGE_ASPECT_RATIO,
    GOOGLE_IMAGE_MODEL,
    IMAGE_GENERATION_ENABLED,
    IMAGE_PROVIDER_ORDER,
    OPENAI_API_KEY,
    OPENAI_IMAGE_MODEL,
    OPENAI_IMAGE_SIZE,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_IMAGE_MODEL,
    OPENROUTER_IMAGE_SIZE,
    OUTPUT_IMAGES_DIR,
    PROVIDER_TIMEOUT_SECONDS,
    STABILITY_API_KEY,
    STABILITY_IMAGE_ENDPOINT,
    STABILITY_OUTPUT_FORMAT,
)


SUPPORTED_IMAGE_PROVIDERS = {"openrouter", "openai", "google", "stability"}

DISABLED_STATUS = "圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。"
MISSING_CONFIG_STATUS = "圖片生成功能已啟用，但所有圖片 provider 都缺少必要設定。目前僅顯示圖片生成 Prompt。"
FAILURE_STATUS = "圖片生成失敗，已保留 Prompt-only 結果。"
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
        for key in ("b64_json", "base64", "image_base64", "data"):
            value = node.get(key)
            if isinstance(value, str) and len(value) > 100:
                return value.split(",", 1)[-1]
        url = node.get("url") or node.get("image_url")
        if isinstance(url, str) and url.startswith("data:image"):
            return url.split(",", 1)[-1]
    return None


def _save_base64_image(image_b64: str, provider: str, extension: str = "png") -> str:
    OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_bytes = base64.b64decode(image_b64)
    filename = f"turtle_tank_{provider}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    path = OUTPUT_IMAGES_DIR / filename
    path.write_bytes(image_bytes)
    return str(path)


def _save_image_bytes(image_bytes: bytes, provider: str, extension: str) -> str:
    OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"turtle_tank_{provider}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    path = OUTPUT_IMAGES_DIR / filename
    path.write_bytes(image_bytes)
    return str(path)


def _safe_error(exc: Exception) -> str:
    message = str(exc).replace("\n", " ").replace("\r", " ").strip()
    if len(message) > 180:
        message = f"{message[:177]}..."
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


def _post_openrouter_image(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{OPENROUTER_BASE_URL.rstrip('/')}/images",
        data=body,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=PROVIDER_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc


def _generate_openrouter_image(prompt: str) -> str:
    if not OPENROUTER_API_KEY or not OPENROUTER_IMAGE_MODEL:
        raise ValueError("OpenRouter API key or image model is not configured.")
    response = _post_openrouter_image(
        {
            "model": OPENROUTER_IMAGE_MODEL,
            "prompt": f"Generate a safe realistic turtle tank layout image at {OPENROUTER_IMAGE_SIZE}.\n\n{prompt}",
            "size": OPENROUTER_IMAGE_SIZE,
        }
    )
    image_b64 = _extract_base64_image(response)
    if not image_b64:
        raise ValueError("OpenRouter response did not include base64 image data.")
    return _save_base64_image(image_b64, "openrouter")


def _generate_openai_image(prompt: str) -> str:
    if not OPENAI_API_KEY or not OPENAI_IMAGE_MODEL:
        raise ValueError("OpenAI API key or image model is not configured.")
    client = OpenAI(api_key=OPENAI_API_KEY, timeout=PROVIDER_TIMEOUT_SECONDS)
    response = client.images.generate(
        model=OPENAI_IMAGE_MODEL,
        prompt=prompt,
        size=OPENAI_IMAGE_SIZE,
        n=1,
    )
    image_b64 = _extract_base64_image(response)
    if not image_b64:
        raise ValueError("OpenAI image response did not include base64 image data.")
    return _save_base64_image(image_b64, "openai")


def _extract_google_image(response) -> str | None:
    output_image = getattr(response, "output_image", None)
    data = getattr(output_image, "data", None)
    if isinstance(data, str) and len(data) > 100:
        return data.split(",", 1)[-1]
    return _extract_base64_image(response)


def _generate_google_image(prompt: str) -> str:
    if not GEMINI_API_KEY or not GOOGLE_IMAGE_MODEL:
        raise ValueError("Gemini API key or image model is not configured.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("google-genai is not installed.") from exc

    client = genai.Client(api_key=GEMINI_API_KEY)
    if not hasattr(client, "interactions"):
        raise RuntimeError("Installed google-genai package does not expose image interactions.")

    response = client.interactions.create(
        model=GOOGLE_IMAGE_MODEL,
        input=prompt,
        response_format={
            "type": "image",
            "mime_type": "image/jpeg",
            "aspect_ratio": GOOGLE_IMAGE_ASPECT_RATIO,
            "image_size": "1K",
        },
    )
    image_b64 = _extract_google_image(response)
    if not image_b64:
        raise ValueError("Google image response did not include base64 image data.")
    return _save_base64_image(image_b64, "google", "jpg")


def _generate_stability_image(prompt: str) -> str:
    if not STABILITY_API_KEY or not STABILITY_IMAGE_ENDPOINT:
        raise ValueError("Stability AI API key or image endpoint is not configured.")

    output_format = STABILITY_OUTPUT_FORMAT.lower() or "jpeg"
    response = requests.post(
        STABILITY_IMAGE_ENDPOINT,
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": prompt,
            "output_format": output_format,
        },
        timeout=PROVIDER_TIMEOUT_SECONDS,
    )
    if response.status_code != 200:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Stability AI HTTP {response.status_code}: {detail}")

    extension = "jpg" if output_format == "jpeg" else output_format
    return _save_image_bytes(response.content, "stability", extension)


IMAGE_PROVIDER_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "openrouter": _generate_openrouter_image,
    "openai": _generate_openai_image,
    "google": _generate_google_image,
    "stability": _generate_stability_image,
}


def _provider_has_minimum_image_config(provider: str) -> bool:
    if provider == "openrouter":
        return bool(OPENROUTER_API_KEY and OPENROUTER_IMAGE_MODEL)
    if provider == "openai":
        return bool(OPENAI_API_KEY and OPENAI_IMAGE_MODEL)
    if provider == "google":
        return bool(GEMINI_API_KEY and GOOGLE_IMAGE_MODEL)
    if provider == "stability":
        return bool(STABILITY_API_KEY and STABILITY_IMAGE_ENDPOINT)
    return False


def generate_tank_image(prompt: str) -> tuple[str | None, str]:
    if not IMAGE_GENERATION_ENABLED:
        return None, DISABLED_STATUS

    configured_providers = [
        provider
        for provider in IMAGE_PROVIDER_ORDER
        if provider in SUPPORTED_IMAGE_PROVIDERS and _provider_has_minimum_image_config(provider)
    ]
    if not configured_providers:
        return None, MISSING_CONFIG_STATUS

    failures: list[str] = []
    for provider in IMAGE_PROVIDER_ORDER:
        if provider not in SUPPORTED_IMAGE_PROVIDERS:
            failures.append(f"{provider}: unsupported provider")
            continue
        if not _provider_has_minimum_image_config(provider):
            failures.append(f"{provider}: missing config")
            continue
        try:
            return IMAGE_PROVIDER_FUNCTIONS[provider](prompt), SUCCESS_STATUS
        except Exception as exc:  # noqa: BLE001 - image generation must be optional
            failures.append(f"{provider}: {_safe_error(exc)}")

    failure_summary = "; ".join(failures) if failures else "no provider was configured"
    return None, f"{FAILURE_STATUS} Provider failures: {failure_summary}"
