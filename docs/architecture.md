# TurtleCare AI Architecture

本文件將 `docs/agent.md` 的專案願景整理成可實作、可驗收的工程架構與任務清單。`agent.md` 仍是最高層級的專案規格來源；本文件負責定義系統架構、前後端介接方式、資料交換格式，以及未來實作的總確認清單。

## 1. Project Goal

TurtleCare AI 是 Deep Generative Models 期末作業的互動式生成式 AI App。系統協助使用者詢問烏龜飼養問題、診斷龜缸環境風險、產生改善建議，並生成適合 diffusion / image generation model 的龜缸設計 prompt。

核心目標：

- 建立可本地執行的 Gradio App。
- 使用 local Markdown knowledge base 與 TF-IDF RAG 提供 grounded responses。
- 使用 multi-provider LLM backend 產生 Q&A、診斷報告與設計 prompt，預設順序為 OpenRouter -> OpenAI -> Google Gemini。
- 使用 rule-based risk checker 提供穩定、安全的飼養風險訊號。
- 預留 optional multi-provider image generation，但 MVP 必須在 prompt-only mode 下完整可用。
- README 與 workflow log 必須支援作業提交與 Agent-driven workflow 證明。

## 2. Assignment Mapping

| Assignment Requirement | TurtleCare AI Implementation |
| --- | --- |
| Generative AI App | Gradio-based interactive turtle care assistant |
| LLM | Multi-provider text generation through OpenRouter, OpenAI, and Google Gemini fallback |
| RAG | Local Markdown knowledge base with TF-IDF retrieval |
| Diffusion / Image Generation | Diffusion-ready tank design prompt generator and optional multi-provider image generation |
| Interactive UI | Traditional Chinese Gradio interface |
| Agent Workflow | `agent.md`, architecture docs, module specs, README, and workflow log |
| Source Code | Python modules under `src/`, plus `app.py` |
| Documentation | English `README.md` and `workflow_log.md` |
| Demo | Screenshot or video showing the running App |

## 3. MVP And Optional Extension Boundary

MVP required:

- Gradio UI with three tabs:
  - Turtle Care Q&A
  - Tank Environment Diagnosis
  - Tank Design Prompt Generator
- Local Markdown knowledge base.
- TF-IDF RAG with `top_k = 3`.
- Rule-based turtle care risk checker.
- Multi-provider LLM client with OpenRouter, OpenAI, and Google Gemini fallback.
- Mock mode when no API key is available.
- Traditional Chinese UI labels.
- English README and workflow log.
- Prompt-only tank design generation.

Optional extension:

- OpenRouter, OpenAI, or Google Gemini image-capable model integration.
- `src/image_generator.py`.
- `outputs/images/` for generated images.
- Image displayed in Gradio only when generation succeeds.

Hard boundary:

- Image generation must be disabled by default.
- Prompt-only mode must work even when API key, image model, quota, or provider response format is unavailable.
- Image generation remains optional and can use any configured provider.
- The system must not provide veterinary diagnosis.

## 4. High-level System Architecture

```text
User
  ↓
Gradio UI
  ↓
UI input dictionary
  ↓
Turtle profile builder
  ↓
RAG retriever ───── Local Markdown knowledge base
  ↓
Rule-based risk checker
  ↓
Prompt builders
  ↓
Provider router
  ↓
OpenRouter / OpenAI / Google Gemini
  ↓
Care answer / diagnosis report / tank design prompt
  ↓
Optional image generator / provider router
  ↓
UI outputs
```

Primary module flow:

- `app.py` collects inputs and calls backend functions.
- `src/turtle_profile.py` normalizes structured user inputs.
- `src/rag.py` loads Markdown knowledge files and retrieves relevant chunks.
- `src/risk_checker.py` produces deterministic risk results.
- `src/report_generator.py` builds Q&A and diagnosis prompts and calls the LLM client.
- `src/prompt_generator.py` builds tank design prompt outputs.
- `src/image_generator.py` optionally calls configured image providers and saves images.
- `src/llm_client.py` handles text provider fallback and mock fallback.
- `src/config.py` centralizes paths, environment variables, and default settings.

## 5. Frontend / Backend Integration Model

The frontend is Gradio. There is no separate web API server in the MVP.

Integration pattern:

- Gradio components collect user input.
- Button click handlers call Python functions directly.
- Backend functions return strings, structured lists, and optional image paths.
- Gradio output components display generated text, retrieved references, risk summaries, image status, and optional image output.

This keeps the MVP simple, demo-friendly, and easy to debug.

## 6. Data Exchange Formats

### 6.1 UI Input Dictionaries

Q&A input:

```python
{
    "species": str,
    "shell_length_cm": float | None,
    "question": str,
}
```

Diagnosis input:

```python
{
    "species": str,
    "number_of_turtles": int | None,
    "shell_length_cm": float | None,
    "tank_length_cm": float | None,
    "tank_width_cm": float | None,
    "tank_height_cm": float | None,
    "water_depth_cm": float | None,
    "has_basking_area": bool,
    "has_uvb_light": bool,
    "heating_equipment": str,
    "filtration_method": str,
    "feeding_content": str,
    "mixed_species": bool,
    "current_concern": str,
}
```

Design input:

```python
{
    "species": str,
    "tank_length_cm": float | None,
    "tank_width_cm": float | None,
    "tank_height_cm": float | None,
    "water_depth_cm": float | None,
    "desired_style": str,
    "required_elements": str,
    "elements_to_avoid": str,
    "user_wants_image": bool,
}
```

### 6.2 Turtle Profile Structure

```python
{
    "species": str,
    "shell_length_cm": float | None,
    "number_of_turtles": int | None,
    "tank_size_cm": {
        "length": float | None,
        "width": float | None,
        "height": float | None,
    },
    "water_depth_cm": float | None,
    "has_basking_area": bool | None,
    "has_uvb_light": bool | None,
    "heating_equipment": str,
    "filtration_method": str,
    "feeding_content": str,
    "mixed_species": bool | None,
    "current_concern": str,
}
```

### 6.3 RAG Retrieved Chunk Structure

```python
{
    "source": str,
    "heading": str,
    "content": str,
    "preview": str,
    "score": float,
}
```

Required display:

- Source filename.
- Short chunk preview.
- Optional relevance score for debugging.

### 6.4 Risk Result Structure

```python
{
    "category": str,
    "level": "low" | "medium" | "high",
    "message": str,
    "suggested_action": str,
}
```

Rules must use cautious language and must not claim medical certainty.

### 6.5 Report Generation I/O

Q&A function input:

```python
{
    "profile": dict,
    "question": str,
    "retrieved_chunks": list[dict],
}
```

Q&A function output:

```python
{
    "answer": str,
    "references": list[dict],
}
```

Diagnosis function input:

```python
{
    "profile": dict,
    "risk_results": list[dict],
    "retrieved_chunks": list[dict],
}
```

Diagnosis function output:

```python
{
    "report": str,
    "risk_summary": str,
    "references": list[dict],
}
```

### 6.6 Prompt Generation Output

```python
{
    "image_prompt": str,
    "negative_prompt": str,
    "materials": str,
    "safety_notes": str,
    "references": list[dict],
}
```

`image_prompt` must be English and suitable for diffusion-style image generation.

### 6.7 Optional Image Generation Output

```python
{
    "image_path": str | None,
    "status_message": str,
}
```

Equivalent function interface:

```python
generate_tank_image(prompt: str) -> tuple[str | None, str]
```

## 7. Environment Variables

Provider fallback variables:

```env
TEXT_PROVIDER_ORDER=openrouter,openai,google
IMAGE_PROVIDER_ORDER=openrouter,openai,google,stability
PROVIDER_TIMEOUT_SECONDS=45
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_TEXT_MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=
OPENAI_TEXT_MODEL=gpt-4o-mini
GEMINI_API_KEY=
GOOGLE_TEXT_MODEL=gemini-3.5-flash
```

Optional image generation variables:

```env
IMAGE_GENERATION_ENABLED=false
OPENROUTER_IMAGE_MODEL=
OPENROUTER_IMAGE_SIZE=1024x1024
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_IMAGE_SIZE=1024x1024
GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image
GOOGLE_IMAGE_ASPECT_RATIO=1:1
STABILITY_API_KEY=
STABILITY_IMAGE_ENDPOINT=https://api.stability.ai/v2beta/stable-image/generate/sd3
STABILITY_OUTPUT_FORMAT=jpeg
```

Default behavior:

- If all provider API keys are empty, text generation uses mock mode.
- Provider calls follow the configured order and try the next provider after recoverable failure.
- If `IMAGE_GENERATION_ENABLED=false`, do not call image generation.
- If image generation is enabled but no provider has image model and API key configured, return prompt-only status.

## 8. Global Implementation Checklist

- [ ] Create root project files: `app.py`, `requirements.txt`, `.env.example`, `README.md`, `workflow_log.md`.
- [ ] Create package directory `src/` with `__init__.py`.
- [ ] Implement `src/config.py`.
- [ ] Implement `src/rag.py`.
- [ ] Implement `src/llm_client.py`.
- [ ] Implement `src/turtle_profile.py`.
- [ ] Implement `src/risk_checker.py`.
- [ ] Implement `src/report_generator.py`.
- [ ] Implement `src/prompt_generator.py`.
- [ ] Implement optional `src/image_generator.py`.
- [ ] Create `data/knowledge_base/` with eight required Markdown files.
- [ ] Create `examples/sample_cases.md`.
- [ ] Create `outputs/images/` and optional `.gitkeep`.
- [ ] Build Gradio UI with three tabs and Traditional Chinese labels.
- [ ] Display retrieved source filenames and previews.
- [ ] Ensure mock mode works without API key.
- [ ] Ensure prompt-only mode works when image generation is disabled.
- [ ] Write English README.
- [ ] Write English workflow log.
- [ ] Prepare demo screenshot or video.
- [ ] Prepare `<StudentID>_HW7.txt` containing repository or shared drive link.
- [ ] Prepare `<StudentID>_HW7.<ext>` demo material.

## 9. Validation Checklist

- [ ] `python app.py` starts the App successfully.
- [ ] Gradio UI opens locally.
- [ ] UI labels are Traditional Chinese.
- [ ] Q&A tab returns an answer.
- [ ] Diagnosis tab returns a structured report.
- [ ] Tank design tab returns English image prompt, negative prompt, materials, and safety notes.
- [ ] RAG uses TF-IDF retrieval.
- [ ] Retrieval top-k is 3.
- [ ] Retrieved references show source filename and preview.
- [ ] Mock mode works when API key is missing.
- [ ] OpenRouter text generation works when API key is configured.
- [ ] OpenAI text generation works when API key is configured.
- [ ] Google Gemini text generation works when API key is configured.
- [ ] Text provider fallback tries the next provider when one service fails.
- [ ] `IMAGE_GENERATION_ENABLED=false` is the default.
- [ ] Tank design tab works when image generation is disabled.
- [ ] Optional image generation does not crash when model or API key is missing.
- [ ] Image provider fallback tries the next provider when one service fails.
- [ ] Generated image is saved under `outputs/images/` if image generation succeeds.
- [ ] Image generation failure falls back to prompt-only output.
- [ ] Health-related answers avoid veterinary diagnosis claims.
- [ ] README is complete and written in English.
- [ ] workflow log is complete and written in English.
- [ ] No private API keys are committed.
- [ ] Demo material verifies the running App.
