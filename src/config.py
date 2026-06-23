from pathlib import Path
import os

from dotenv import dotenv_values, load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH, override=True)
_ENV_FILE_VALUES = dotenv_values(ENV_PATH)


def _env(name: str, default: str = "") -> str:
    if name in _ENV_FILE_VALUES:
        value = _ENV_FILE_VALUES.get(name)
        return "" if value is None else str(value)
    return os.getenv(name, default)


def _env_bool(name: str, default: bool = False) -> bool:
    value = _env(name, "")
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_float(name: str, default: float) -> float:
    try:
        return float(_env(name, str(default)))
    except (TypeError, ValueError):
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(_env(name, str(default)))
    except (TypeError, ValueError):
        return default


KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"
OUTPUT_IMAGES_DIR = PROJECT_ROOT / "outputs" / "images"

TEXT_PROVIDER_ORDER = [
    provider.strip().lower()
    for provider in _env("TEXT_PROVIDER_ORDER", "openrouter,openai,google").split(",")
    if provider.strip()
]
IMAGE_PROVIDER_ORDER = [
    provider.strip().lower()
    for provider in _env("IMAGE_PROVIDER_ORDER", "openrouter,openai,google,stability").split(",")
    if provider.strip()
]
PROVIDER_TIMEOUT_SECONDS = _env_float("PROVIDER_TIMEOUT_SECONDS", 45.0)

LEGACY_OPENAI_API_KEY = _env("OPENAI_API_KEY", "").strip()
LEGACY_OPENAI_BASE_URL = _env("OPENAI_BASE_URL", "").strip()
LEGACY_OPENAI_MODEL = _env("OPENAI_MODEL", "").strip()
LEGACY_OPENROUTER_MODE = bool(LEGACY_OPENAI_API_KEY and "openrouter.ai" in LEGACY_OPENAI_BASE_URL)

OPENROUTER_API_KEY = _env("OPENROUTER_API_KEY", "").strip()
OPENROUTER_BASE_URL = _env("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
OPENROUTER_TEXT_MODEL = _env("OPENROUTER_TEXT_MODEL", "openai/gpt-4o-mini").strip()
USING_LEGACY_OPENROUTER = not OPENROUTER_API_KEY and LEGACY_OPENROUTER_MODE
if USING_LEGACY_OPENROUTER:
    OPENROUTER_API_KEY = LEGACY_OPENAI_API_KEY
    OPENROUTER_BASE_URL = LEGACY_OPENAI_BASE_URL
    OPENROUTER_TEXT_MODEL = LEGACY_OPENAI_MODEL or OPENROUTER_TEXT_MODEL

OPENAI_API_KEY = "" if USING_LEGACY_OPENROUTER else LEGACY_OPENAI_API_KEY
OPENAI_TEXT_MODEL = _env("OPENAI_TEXT_MODEL", "gpt-4o-mini").strip()
OPENAI_IMAGE_MODEL = _env("OPENAI_IMAGE_MODEL", "gpt-image-1").strip()
OPENAI_IMAGE_SIZE = _env("OPENAI_IMAGE_SIZE", "1024x1024").strip()

GEMINI_API_KEY = _env("GEMINI_API_KEY", "").strip()
GOOGLE_TEXT_MODEL = _env("GOOGLE_TEXT_MODEL", "gemini-3.5-flash").strip()
GOOGLE_IMAGE_MODEL = _env("GOOGLE_IMAGE_MODEL", "gemini-3.1-flash-image").strip()
GOOGLE_IMAGE_ASPECT_RATIO = _env("GOOGLE_IMAGE_ASPECT_RATIO", "1:1").strip()

STABILITY_API_KEY = _env("STABILITY_API_KEY", "").strip()
STABILITY_IMAGE_ENDPOINT = _env(
    "STABILITY_IMAGE_ENDPOINT",
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
).strip()
STABILITY_OUTPUT_FORMAT = _env("STABILITY_OUTPUT_FORMAT", "jpeg").strip()

LLM_TEMPERATURE = _env_float("LLM_TEMPERATURE", 0.3)
RETRIEVAL_TOP_K = _env_int("RETRIEVAL_TOP_K", 3)
MOCK_MODE = not any([OPENROUTER_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY])

IMAGE_GENERATION_ENABLED = _env_bool("IMAGE_GENERATION_ENABLED", False)
OPENROUTER_IMAGE_MODEL = _env("OPENROUTER_IMAGE_MODEL", "").strip()
OPENROUTER_IMAGE_SIZE = _env("OPENROUTER_IMAGE_SIZE", "1024x1024").strip()
