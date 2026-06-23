# Config Module Spec

## Purpose

定義 `src/config.py` 的設定集中管理方式，讓 paths、OpenRouter text backend、mock mode、RAG top-k 與 optional image generation 設定都能從單一模組取得。

## Responsibilities

- Load `.env` using `python-dotenv`.
- Define project root paths.
- Define knowledge base and output image directories.
- Read OpenRouter / OpenAI-compatible text generation settings.
- Read optional image generation settings.
- Provide safe defaults for local demo.
- Determine mock mode when API key is unavailable.

## Inputs

Environment variables:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `LLM_TEMPERATURE`
- `RETRIEVAL_TOP_K`
- `IMAGE_GENERATION_ENABLED`
- `OPENROUTER_IMAGE_MODEL`
- `OPENROUTER_IMAGE_SIZE`

## Outputs

Module-level constants:

- `PROJECT_ROOT`
- `KNOWLEDGE_BASE_DIR`
- `OUTPUT_IMAGES_DIR`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `LLM_TEMPERATURE`
- `RETRIEVAL_TOP_K`
- `MOCK_MODE`
- `IMAGE_GENERATION_ENABLED`
- `OPENROUTER_IMAGE_MODEL`
- `OPENROUTER_IMAGE_SIZE`

## Data Format

Suggested defaults:

```python
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_MODEL = "openai/gpt-4o-mini"
LLM_TEMPERATURE = 0.3
RETRIEVAL_TOP_K = 3
IMAGE_GENERATION_ENABLED = False
OPENROUTER_IMAGE_MODEL = ""
OPENROUTER_IMAGE_SIZE = "1024x1024"
MOCK_MODE = not bool(OPENAI_API_KEY)
```

Boolean normalization:

- `"true"`, `"1"`, `"yes"` -> `True`
- Anything else -> `False`

## Error / Fallback Behavior

- Missing `.env` is allowed.
- Missing `OPENAI_API_KEY` activates mock mode.
- Missing `OPENROUTER_IMAGE_MODEL` disables actual image call even if image generation is enabled.
- Directories should be created by implementation or checked before use.

## Safety Requirements

- Never print or expose API keys.
- Do not store secrets in committed files.
- `.env.example` must include empty key placeholders only.

## Implementation Checklist

- [ ] Import `Path`, `os`, and `load_dotenv`.
- [ ] Load `.env`.
- [ ] Define root and data paths.
- [ ] Parse text backend environment variables.
- [ ] Parse retrieval settings with default `top_k = 3`.
- [ ] Parse optional image generation variables.
- [ ] Compute `MOCK_MODE`.
- [ ] Provide helper for boolean environment parsing.

## Completion Checklist

- [ ] Config works when `.env` is absent.
- [ ] Mock mode becomes true when API key is empty.
- [ ] OpenRouter base URL defaults correctly.
- [ ] Retrieval top-k defaults to 3.
- [ ] Image generation defaults to disabled.
- [ ] No secret values are hard-coded.
