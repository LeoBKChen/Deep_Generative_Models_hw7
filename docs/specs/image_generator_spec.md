# Image Generator Module Spec

## Purpose

定義 optional `src/image_generator.py`。此模組透過 OpenRouter image-capable models 嘗試生成龜缸設計圖片，但不得成為 MVP 的必要條件。

## Responsibilities

- Check whether image generation is enabled.
- Check whether OpenRouter API key and image model are configured.
- Call OpenRouter image-capable model when allowed.
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
outputs/images/turtle_tank_YYYYMMDD_HHMMSS.png
```

Possible request shape:

```python
response = client.chat.completions.create(
    model=OPENROUTER_IMAGE_MODEL,
    messages=[{"role": "user", "content": prompt}],
    modalities=["image", "text"],
)
```

## Error / Fallback Behavior

Disabled:

```text
圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。
```

Enabled but missing config:

```text
圖片生成功能已啟用，但缺少 OpenRouter API key 或 image model 設定。目前僅顯示圖片生成 Prompt。
```

Failure:

```text
圖片生成失敗，可能是模型不支援圖片輸出、API 額度不足，或 OpenRouter 回應格式不同。目前保留 Prompt-only 結果。
```

Success:

```text
圖片生成成功。
```

## Safety Requirements

- Do not require image generation for the MVP.
- Do not use a separate OpenAI Image API key.
- Do not expose API keys.
- Generated image is only for visualization, not a construction plan or veterinary recommendation.

## Implementation Checklist

- [ ] Read image generation config from `src/config.py`.
- [ ] Return disabled status when `IMAGE_GENERATION_ENABLED=false`.
- [ ] Return missing config status when API key or image model is empty.
- [ ] Create `outputs/images/` if needed.
- [ ] Call OpenRouter image model defensively.
- [ ] Implement helper to extract base64 image data.
- [ ] Save successful image as PNG.
- [ ] Catch all image generation exceptions.

## Completion Checklist

- [ ] Default disabled mode returns `(None, disabled_status)`.
- [ ] Missing API key or image model does not crash.
- [ ] Failed provider response falls back to prompt-only status.
- [ ] Successful generation saves image under `outputs/images/`.
- [ ] Function always returns `tuple[str | None, str]`.
- [ ] Rest of App does not depend on provider-specific image response details.
