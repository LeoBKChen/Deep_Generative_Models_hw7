# Debugging Process

This document summarizes the major debugging steps completed during TurtleCare AI development. It is written as supporting evidence for the agent-driven development process required by the assignment.

## 1. Python Environment

### Problem

The default `python` command did not reliably point to the intended project environment. In some cases it resolved to the Windows Store Python stub or a different conda environment.

### Diagnosis

The agent inspected the available interpreter and verified the `DGM` conda environment.

### Resolution

Use the explicit DGM Python path for validation and execution:

```powershell
C:\miniconda3\envs\DGM\python.exe app.py
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
```

## 2. Dependency Installation

### Problem

The project needed both runtime dependencies and optional development-only screenshot dependencies.

### Resolution

Runtime dependencies were placed in:

```text
requirements.txt
```

Screenshot helper dependencies were placed in:

```text
requirements-dev.txt
```

Validation command:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip check
```

Result:

```text
No broken requirements found.
```

## 3. Mock Mode And Real API Mode

### Problem

The first smoke test assumed the default `.env` had no API keys and therefore expected `MOCK_MODE=True`. After the human filled real API keys into `.env`, the test failed with:

```text
AssertionError: Expected mock mode with the default local .env.
```

### Resolution

The smoke test was updated to support both modes:

- In mock mode, it checks mock-specific output text.
- In real API mode, it checks that generated outputs are non-empty and that references/risk summaries are still returned.

This made `scripts/smoke_test.py` useful for both local no-key demos and real API validation.

## 4. RAG Retrieval For Chinese Queries

### Problem

The UI uses Traditional Chinese labels and users may ask Chinese questions, but the knowledge base is written mainly in English. This reduced TF-IDF retrieval quality.

### Resolution

The agent added query expansion in `src/rag.py`, mapping common Chinese turtle-care terms to English retrieval keywords.

Examples:

| Chinese query term | Added retrieval keywords |
| --- | --- |
| `曬台` | `basking area dry platform ramp` |
| `水質` | `water quality ammonia nitrite nitrate filtration` |
| `混養` | `mixed species stress biting competition separation` |
| `不吃` | `refusing food stress temperature water quality veterinarian` |

## 5. Image Generation Provider Failures

### Problem

When image generation was enabled, all configured image providers initially failed.

Observed UI status:

```text
圖片生成失敗，已保留 Prompt-only 結果。
Provider failures: openrouter: APIStatusError; openai: BadRequestError; google: BadRequestError
```

### Diagnosis

The agent inspected non-secret provider configuration values and then performed targeted provider debugging. No API keys were printed.

Provider findings:

- OpenRouter account did not have enough credits.
- OpenAI account reached the billing hard limit.
- Google initially rejected `image/png` for Gemini image output.

### Resolution

- OpenRouter image generation was changed to the dedicated `/api/v1/images` endpoint.
- Google Gemini image generation was changed to request `image/jpeg`.
- Error summaries were made more readable while avoiding secret leakage.
- Prompt-only fallback remained the stable demo path.

## 6. Stability AI Provider Addition

### Problem

The human wanted another image provider option and supplied official Stability AI SD3 sample code, but requested that the agent not directly test the API to avoid consuming credits.

### Resolution

The agent added a Stability AI image provider using the supplied API shape:

```python
requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": f"Bearer {STABILITY_API_KEY}",
        "accept": "image/*",
    },
    files={"none": ""},
    data={
        "prompt": prompt,
        "output_format": "jpeg",
    },
)
```

Validation was done with a local monkeypatch mock only. No live Stability AI API request was sent.

## 7. Encoding Cleanup

### Problem

Some earlier Traditional Chinese fallback/status strings displayed as mojibake in PowerShell output.

### Resolution

The affected runtime messages were rewritten as clean UTF-8 Traditional Chinese strings.

Examples:

```text
圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。
圖片生成成功。
圖片生成失敗，已保留 Prompt-only 結果。
```

## 8. Final Validation Commands

The following commands were used throughout debugging:

```powershell
C:\miniconda3\envs\DGM\python.exe -m compileall app.py src scripts
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
C:\miniconda3\envs\DGM\python.exe -m pip check
```

Stability AI local mock validation:

```text
stability provider local mock passed
```

## 9. Current Stable Demo Strategy

Because real image generation depends on external provider credits, billing, quota, and model availability, the stable demo strategy is:

```env
IMAGE_GENERATION_ENABLED=false
```

This keeps the Tank Design tab fully functional in prompt-only mode. The app still demonstrates LLM/RAG interaction, deterministic risk checking, and diffusion-ready prompt generation without depending on image provider availability.
