# Image Generator Module Spec

## Purpose

定義 optional `src/image_generator.py`。此模組透過 provider fallback 嘗試生成龜缸設計圖片，支援 OpenRouter、OpenAI、Google Gemini 與 Stability AI，但不得成為 MVP 的必要條件。

## Responsibilities

- Check whether image generation is enabled.
- Read configured image provider order.
- Skip providers missing API key or image model.
- Try OpenRouter, OpenAI, Google, and Stability AI image providers in order.
- Extract base64 image data from common response formats.
- Save generated image files under `outputs/images/`.
- Return image path and status message.
- Fall back to prompt-only mode gracefully.

## Inputs

```python
prompt: str
```

## Outputs

```python
(image_path, status_message)
```

Where:

- `image_path` is `str | None`.
- `status_message` is a Traditional Chinese user-facing message.

## Data Format

Required function:

```python
generate_tank_image(prompt: str) -> tuple[str | None, str]
```

Successful image path format:

```text
outputs/images/turtle_tank_<provider>_YYYYMMDD_HHMMSS.<ext>
```

OpenRouter request shape:

```python
requests.post(
    f"{OPENROUTER_BASE_URL}/images",
    headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
    json={"model": OPENROUTER_IMAGE_MODEL, "prompt": prompt, "size": OPENROUTER_IMAGE_SIZE},
)
```

OpenAI request shape:

```python
client.images.generate(
    model=OPENAI_IMAGE_MODEL,
    prompt=prompt,
    size=OPENAI_IMAGE_SIZE,
    n=1,
)
```

Google request shape:

```python
client.interactions.create(
    model=GOOGLE_IMAGE_MODEL,
    input=prompt,
    response_format={
        "type": "image",
        "mime_type": "image/jpeg",
        "aspect_ratio": GOOGLE_IMAGE_ASPECT_RATIO,
        "image_size": "1K",
    },
)
```

Stability AI request shape:

```python
requests.post(
    STABILITY_IMAGE_ENDPOINT,
    headers={"authorization": f"Bearer {STABILITY_API_KEY}", "accept": "image/*"},
    files={"none": ""},
    data={"prompt": prompt, "output_format": STABILITY_OUTPUT_FORMAT},
)
```

## Error / Fallback Behavior

Disabled:

```text
圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。
```

Enabled but missing all provider config:

```text
圖片生成功能已啟用，但所有圖片 provider 都缺少必要設定。目前僅顯示圖片生成 Prompt。
```

Failure:

```text
圖片生成失敗，已保留 Prompt-only 結果。
```

Success:

```text
圖片生成成功。
```

## Safety Requirements

- Do not require image generation for the MVP.
- Do not expose API keys.
- Generated image is only for visualization, not a construction plan or veterinary recommendation.
- Provider errors shown to the UI may include provider names and exception types only.

## Implementation Checklist

- [x] Read image generation config from `src/config.py`.
- [x] Return disabled status when `IMAGE_GENERATION_ENABLED=false`.
- [x] Return missing config status when no image provider has minimum config.
- [x] Create `outputs/images/` if needed.
- [x] Call OpenRouter image model defensively.
- [x] Call OpenAI Images API defensively.
- [x] Call Google Gemini image API defensively.
- [x] Call Stability AI SD3 image API defensively.
- [x] Implement helper to extract base64 image data.
- [x] Save successful image as PNG, JPG, or provider-selected output format.
- [x] Catch image generation exceptions and continue fallback chain.

## Completion Checklist

- [ ] Default disabled mode returns `(None, disabled_status)`.
- [ ] Missing API key or image model does not crash.
- [ ] Failed provider response falls back to the next provider.
- [ ] Total provider failure falls back to prompt-only status.
- [ ] Successful generation saves image under `outputs/images/`.
- [ ] Function always returns `tuple[str | None, str]`.
- [ ] Rest of App does not depend on provider-specific image response details.
