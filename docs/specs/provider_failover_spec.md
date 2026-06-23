# Provider Failover Spec

## Purpose

定義 TurtleCare AI 的 multi-provider API fallback 設計，讓文字生成可以保留 OpenRouter，同時額外支援 OpenAI 與 Google Gemini；optional image generation 另外支援 OpenRouter、OpenAI、Google Gemini 與 Stability AI。

## Responsibilities

- Maintain independent provider orders for text and image generation.
- Try providers in configured order until one succeeds.
- Skip providers with missing keys, missing models, or unsupported names.
- Preserve existing public module interfaces.
- Keep demo-safe fallback behavior when all providers fail.
- Avoid exposing API keys or raw sensitive payloads.

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
- `IMAGE_GENERATION_ENABLED`

Runtime inputs:

```python
generate_text(system_prompt: str, user_prompt: str) -> str
generate_tank_image(prompt: str) -> tuple[str | None, str]
```

## Outputs

Text generation:

```python
generated_text: str
```

Image generation:

```python
(image_path, status_message)
```

Where:

- `image_path` is `str | None`.
- `status_message` is a Traditional Chinese user-facing message.

## Data Format

Default provider order:

```env
TEXT_PROVIDER_ORDER=openrouter,openai,google
IMAGE_PROVIDER_ORDER=openrouter,openai,google,stability
```

Text providers:

| Provider | SDK / API shape | Required config |
| --- | --- | --- |
| OpenRouter | OpenAI-compatible chat completions | `OPENROUTER_API_KEY`, `OPENROUTER_TEXT_MODEL` |
| OpenAI | OpenAI Responses API | `OPENAI_API_KEY`, `OPENAI_TEXT_MODEL` |
| Google | `google-genai` Gemini API | `GEMINI_API_KEY`, `GOOGLE_TEXT_MODEL` |

Image providers:

| Provider | SDK / API shape | Required config |
| --- | --- | --- |
| OpenRouter | Dedicated `/api/v1/images` endpoint | `OPENROUTER_API_KEY`, `OPENROUTER_IMAGE_MODEL` |
| OpenAI | OpenAI Images API | `OPENAI_API_KEY`, `OPENAI_IMAGE_MODEL` |
| Google | `google-genai` image interaction | `GEMINI_API_KEY`, `GOOGLE_IMAGE_MODEL` |
| Stability AI | `stable-image/generate/sd3` multipart request | `STABILITY_API_KEY`, `STABILITY_IMAGE_ENDPOINT` |

Legacy compatibility:

- New OpenRouter settings use `OPENROUTER_API_KEY`.
- If old `.env` uses `OPENAI_API_KEY` with `OPENAI_BASE_URL` containing `openrouter.ai` and no `OPENROUTER_API_KEY` is set, treat that key as legacy OpenRouter config.
- Do not use the legacy OpenRouter key for official OpenAI calls.

## Error / Fallback Behavior

- If no text provider key is configured, `MOCK_MODE=True`.
- If a text provider fails, try the next provider.
- If every text provider fails, return a safe mock response with provider error types only.
- If image generation is disabled, return disabled status immediately.
- If image generation is enabled but no image provider has minimum config, return missing-config status.
- If every image provider fails, return `(None, status_message)` and keep prompt-only output usable.

## Safety Requirements

- Never print or return API keys.
- Do not expose full provider request payloads in UI errors.
- Generated content must keep the no-veterinary-diagnosis boundary.
- Generated images are visualization only, not real construction plans.

## Implementation Checklist

- [x] Add provider order settings in `src/config.py`.
- [x] Add OpenRouter-specific API key and model settings.
- [x] Add OpenAI text and image model settings.
- [x] Add Gemini text and image model settings.
- [x] Add Stability AI image settings.
- [x] Add legacy OpenRouter compatibility for old `.env` files.
- [x] Implement text fallback in `src/llm_client.py`.
- [x] Implement image fallback in `src/image_generator.py`.
- [x] Add `google-genai` to `requirements.txt`.
- [x] Add `requests` to `requirements.txt`.
- [x] Update `.env.example`.
- [ ] Test real OpenRouter call with a valid key.
- [ ] Test real OpenAI call with a valid key.
- [ ] Test real Gemini call with a valid key.
- [ ] Test real Stability AI image call with a valid key.

## Completion Checklist

- [ ] Mock mode still works without API keys.
- [ ] Disabled image generation returns prompt-only status.
- [ ] Invalid provider names do not crash the app.
- [ ] Provider failures do not expose secrets.
- [ ] Text fallback tries the next configured provider after failure.
- [ ] Image fallback tries the next configured provider after failure.
- [ ] Successful image generation saves under `outputs/images/`.
- [ ] README and architecture docs describe the multi-provider setup.
