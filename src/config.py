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

OPENAI_API_KEY = _env("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = _env("OPENAI_BASE_URL", "https://openrouter.ai/api/v1").strip()
OPENAI_MODEL = _env("OPENAI_MODEL", "openai/gpt-4o-mini").strip()
LLM_TEMPERATURE = _env_float("LLM_TEMPERATURE", 0.3)
RETRIEVAL_TOP_K = _env_int("RETRIEVAL_TOP_K", 3)
MOCK_MODE = not bool(OPENAI_API_KEY)

IMAGE_GENERATION_ENABLED = _env_bool("IMAGE_GENERATION_ENABLED", False)
OPENROUTER_IMAGE_MODEL = _env("OPENROUTER_IMAGE_MODEL", "").strip()
OPENROUTER_IMAGE_SIZE = _env("OPENROUTER_IMAGE_SIZE", "1024x1024").strip()
