# Config Module Spec

## Purpose

定義 `src/config.py` 的設定集中管理方式，讓 paths、multi-provider text/image backend、mock mode、RAG top-k 與 optional image generation 設定都能從單一模組取得。

## Responsibilities

- Load `.env` using `python-dotenv`.
- Define project root paths.
- Define knowledge base and output image directories.
- Read OpenRouter, OpenAI, and Google Gemini text generation settings.
- Read Stability AI image generation settings.
- Read optional image generation settings.
- Read provider fallback order settings.
- Support legacy OpenRouter `.env` settings.
- Provide safe defaults for local demo.
- Determine mock mode when API key is unavailable.

## Inputs

Environment variables:

- `TEXT_PROVIDER_ORDER`
- `IMAGE_PROVIDER_ORDER`
- `PROVIDER_TIMEOUT_SECONDS`
- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `OPENROUTER_TEXT_MODEL`
- `OPENROUTER_IMAGE_MODEL`
- `OPENROUTER_IMAGE_SIZE`
- `OPENAI_API_KEY`
- `OPENAI_TEXT_MODEL`
- `OPENAI_IMAGE_MODEL`
- `OPENAI_IMAGE_SIZE`
- `GEMINI_API_KEY`
- `GOOGLE_TEXT_MODEL`
- `GOOGLE_IMAGE_MODEL`
- `GOOGLE_IMAGE_ASPECT_RATIO`
- `STABILITY_API_KEY`
- `STABILITY_IMAGE_ENDPOINT`
- `STABILITY_OUTPUT_FORMAT`
- `LLM_TEMPERATURE`
- `RETRIEVAL_TOP_K`
- `IMAGE_GENERATION_ENABLED`

## Outputs

Module-level constants:

- `PROJECT_ROOT`
- `KNOWLEDGE_BASE_DIR`
- `OUTPUT_IMAGES_DIR`
- `TEXT_PROVIDER_ORDER`
- `IMAGE_PROVIDER_ORDER`
- `PROVIDER_TIMEOUT_SECONDS`
- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `OPENROUTER_TEXT_MODEL`
- `OPENROUTER_IMAGE_MODEL`
- `OPENROUTER_IMAGE_SIZE`
- `OPENAI_API_KEY`
- `OPENAI_TEXT_MODEL`
- `OPENAI_IMAGE_MODEL`
- `OPENAI_IMAGE_SIZE`
- `GEMINI_API_KEY`
- `GOOGLE_TEXT_MODEL`
- `GOOGLE_IMAGE_MODEL`
- `GOOGLE_IMAGE_ASPECT_RATIO`
- `STABILITY_API_KEY`
- `STABILITY_IMAGE_ENDPOINT`
- `STABILITY_OUTPUT_FORMAT`
- `LLM_TEMPERATURE`
- `RETRIEVAL_TOP_K`
- `MOCK_MODE`
- `IMAGE_GENERATION_ENABLED`

## Data Format

Suggested defaults:

```python
TEXT_PROVIDER_ORDER = ["openrouter", "openai", "google"]
IMAGE_PROVIDER_ORDER = ["openrouter", "openai", "google", "stability"]
PROVIDER_TIMEOUT_SECONDS = 45.0
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_TEXT_MODEL = "openai/gpt-4o-mini"
OPENAI_TEXT_MODEL = "gpt-4o-mini"
OPENAI_IMAGE_MODEL = "gpt-image-1"
GOOGLE_TEXT_MODEL = "gemini-3.5-flash"
GOOGLE_IMAGE_MODEL = "gemini-3.1-flash-image"
STABILITY_IMAGE_ENDPOINT = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
STABILITY_OUTPUT_FORMAT = "jpeg"
LLM_TEMPERATURE = 0.3
RETRIEVAL_TOP_K = 3
IMAGE_GENERATION_ENABLED = False
OPENROUTER_IMAGE_MODEL = ""
OPENROUTER_IMAGE_SIZE = "1024x1024"
OPENAI_IMAGE_SIZE = "1024x1024"
GOOGLE_IMAGE_ASPECT_RATIO = "1:1"
MOCK_MODE = not any([OPENROUTER_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY])
```

Boolean normalization:

- `"true"`, `"1"`, `"yes"` -> `True`
- Anything else -> `False`

## Error / Fallback Behavior

- Missing `.env` is allowed.
- Missing all provider API keys activates mock mode.
- Missing image model or API key for a provider causes that provider to be skipped.
- If old `.env` uses `OPENAI_API_KEY` with `OPENAI_BASE_URL` containing `openrouter.ai` and no `OPENROUTER_API_KEY` is set, treat it as legacy OpenRouter config.
- Directories should be created by implementation or checked before use.

## Safety Requirements

- Never print or expose API keys.
- Do not store secrets in committed files.
- `.env.example` must include empty key placeholders only.

## Implementation Checklist

- [ ] Import `Path`, `os`, and `load_dotenv`.
- [ ] Load `.env`.
- [ ] Define root and data paths.
- [ ] Parse provider fallback order environment variables.
- [ ] Parse OpenRouter environment variables.
- [ ] Parse OpenAI environment variables.
- [ ] Parse Google Gemini environment variables.
- [ ] Parse Stability AI environment variables.
- [ ] Support legacy OpenRouter settings.
- [ ] Parse retrieval settings with default `top_k = 3`.
- [ ] Parse optional image generation variables.
- [ ] Compute `MOCK_MODE`.
- [ ] Provide helper for boolean environment parsing.

## Completion Checklist

- [ ] Config works when `.env` is absent.
- [ ] Mock mode becomes true when API key is empty.
- [ ] OpenRouter base URL defaults correctly.
- [ ] Provider order defaults to OpenRouter, OpenAI, Google, and Stability for images.
- [ ] Retrieval top-k defaults to 3.
- [ ] Image generation defaults to disabled.
- [ ] Legacy OpenRouter `.env` remains compatible.
- [ ] No secret values are hard-coded.
