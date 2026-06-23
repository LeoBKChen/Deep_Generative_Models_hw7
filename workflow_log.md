# Agent Collaboration Workflow Log

## 1. Tools Used

- Codex Agent in the IDE for planning, code generation, debugging, and documentation.
- PowerShell for local inspection and validation commands.
- Python 3.11 in the `DGM` conda environment.
- Gradio for the interactive UI.
- OpenAI Python SDK for OpenRouter-compatible and OpenAI APIs.
- Google Gen AI SDK for Gemini APIs.
- requests for Stability AI image generation.
- Playwright as a development-only screenshot helper.

## 2. Phase 1: Ideation And Planning

### Human Prompt

The human asked the agent to read the homework requirements and propose a generative AI application that demonstrates an agent-driven workflow.

### Agent Output

The agent proposed TurtleCare AI: a turtle care, tank diagnosis, and tank design assistant combining LLM generation, local RAG, deterministic risk checks, and image-generation prompt engineering.

### Human Decision

The human accepted TurtleCare AI as the project topic and continued the project around a Gradio-based interactive app.

## 3. Phase 2: Architecture Design And Task Decomposition

### Human Prompt

The human asked the agent to read `docs/agent.md`, explain the project direction, and determine whether the architecture design and task decomposition requirement had been completed.

### Agent Output

The agent identified that the project still needed an implementation-ready architecture checklist and module-level specs.

### Generated Documentation

- `docs/architecture.md`
- `docs/specs/app_ui_spec.md`
- `docs/specs/config_spec.md`
- `docs/specs/rag_spec.md`
- `docs/specs/llm_client_spec.md`
- `docs/specs/turtle_profile_spec.md`
- `docs/specs/risk_checker_spec.md`
- `docs/specs/report_generator_spec.md`
- `docs/specs/prompt_generator_spec.md`
- `docs/specs/image_generator_spec.md`
- `docs/specs/knowledge_base_spec.md`
- `docs/specs/documentation_spec.md`
- `docs/specs/demo_submission_spec.md`

### Human Decisions

- Use Python 3.11.
- Use Student ID `314831018`.
- Submit a screenshot demo.
- Keep image generation optional.
- Keep prompt-only mode reliable for demonstration.

## 4. Phase 3: Code Generation And Implementation

### Human Prompt

The human asked the agent to create `requirements.txt`, `.env`, image generation support, README, workflow log, and begin project implementation.

### Generated Components

- `app.py`
- `src/config.py`
- `src/rag.py`
- `src/llm_client.py`
- `src/turtle_profile.py`
- `src/risk_checker.py`
- `src/report_generator.py`
- `src/prompt_generator.py`
- `src/image_generator.py`
- `scripts/smoke_test.py`
- `scripts/capture_demo_screenshot.py`
- `requirements.txt`
- `requirements-dev.txt`
- `.env.example`
- `examples/sample_cases.md`
- `data/knowledge_base/*.md`
- `outputs/images/.gitkeep`

### Implementation Summary

The agent implemented a three-tab Gradio app:

- Turtle Care Q&A.
- Tank Environment Diagnosis.
- Tank Design Prompt Generator.

The backend uses local Markdown RAG, TF-IDF retrieval, turtle profile normalization, deterministic risk checking, LLM prompt construction, and optional image generation.

## 5. Phase 4: Knowledge Base And RAG

### Human Prompt

The human asked whether the RAG database was complete and what its sources were.

### Agent Output

The agent verified that the MVP RAG database was complete with eight local Markdown files under `data/knowledge_base/`.

### Knowledge Base Files

- `turtle_species.md`
- `tank_setup.md`
- `water_quality.md`
- `lighting_and_basking.md`
- `feeding.md`
- `common_health_issues.md`
- `mixed_species_warning.md`
- `emergency_warning.md`

### Source Clarification

The knowledge base is a local curated educational knowledge base generated for the assignment from project requirements, beginner turtle care topics, and safety rules. It is not a citation-based veterinary database.

## 6. Phase 5: API Provider Evolution

### Initial Design

The first implementation used OpenRouter-compatible text generation and optional OpenRouter image generation.

### Human Prompt

The human requested keeping OpenRouter while adding OpenAI and Google AI API support so the app could try another service if one provider failed.

### Agent Output

The agent implemented a provider fallback architecture:

- Text fallback order: `openrouter,openai,google`.
- Image fallback order: `openrouter,openai,google`.
- Existing public functions remained unchanged:
  - `generate_text(system_prompt, user_prompt) -> str`
  - `generate_tank_image(prompt) -> tuple[str | None, str]`

### Later Extension

The human provided official Stability AI SD3 sample code and requested adding Stability AI without testing the live API to avoid consuming quota.

The agent added Stability AI as an image-only provider:

- `STABILITY_API_KEY`
- `STABILITY_IMAGE_ENDPOINT`
- `STABILITY_OUTPUT_FORMAT`
- `IMAGE_PROVIDER_ORDER=stability,openrouter,openai,google`

The Stability implementation was validated with a local monkeypatch mock only, not a real API call.

## 7. Phase 6: Debugging Records

### Environment Debugging

Problem:

The default `python` command pointed to a Windows Store stub or the wrong interpreter.

Resolution:

The agent verified the `DGM` conda environment and used:

```powershell
C:\miniconda3\envs\DGM\python.exe
```

### Mock Mode Debugging

Problem:

The original smoke test expected `MOCK_MODE=True`, but after the human filled `.env` with real API keys, the test failed.

Resolution:

The smoke test was updated to support both mock mode and real API mode. It now checks non-empty outputs when real providers are configured and keeps mock-specific assertions only when `MOCK_MODE=True`.

### RAG Debugging

Problem:

Chinese UI questions retrieved less relevant English knowledge-base chunks.

Resolution:

The agent added Chinese keyword expansion in `src/rag.py`, mapping terms such as `曬台`, `水質`, `混養`, and `UVB` to English retrieval keywords.

### Image Provider Debugging

Problem:

Image generation failed across OpenRouter, OpenAI, and Google.

Observed provider responses:

- OpenRouter: insufficient credits.
- OpenAI: billing hard limit reached.
- Google: invalid `image/png` response format, later quota limitation.

Resolution:

- OpenRouter image generation was updated to use the dedicated `/api/v1/images` endpoint.
- Google image generation was updated to use `image/jpeg`.
- Prompt-only fallback remained the stable demo path.
- Stability AI was added as an additional optional image provider.

### Encoding Debugging

Problem:

Some earlier Chinese fallback/status strings displayed as mojibake in PowerShell.

Resolution:

The agent replaced broken strings with clean UTF-8 Traditional Chinese status messages in the runtime modules.

## 8. Phase 7: UI Integration And Demo Preparation

### Generated UI

The agent created a Gradio app with Traditional Chinese labels and three tabs:

- `烏龜照護問答`
- `龜缸環境診斷`
- `龜缸設計與圖片生成`

### Demo Files

- `314831018_HW7.txt`
- `314831018_HW7.png`

### Screenshot Helper

The agent added `scripts/capture_demo_screenshot.py` and `requirements-dev.txt` for optional screenshot automation.

## 9. Validation Summary

Validation commands used during development:

```powershell
C:\miniconda3\envs\DGM\python.exe -m compileall app.py src scripts
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
C:\miniconda3\envs\DGM\python.exe -m pip check
```

Validated behavior:

- Python syntax compile checks passed.
- Smoke test passed in mock mode and later real-provider mode.
- RAG retrieves top 3 chunks.
- Chinese keyword expansion improves retrieval.
- Q&A, diagnosis, and design prompt flows return outputs.
- Image generation disabled fallback works.
- Multi-provider fallback handles provider errors without crashing the app.
- Stability AI provider was validated with a local mock, not a live API call.

## 10. Technical Bottlenecks And Resolutions

| Bottleneck | Resolution |
| --- | --- |
| Wrong Python interpreter | Use explicit DGM interpreter path |
| Missing API keys | Implement mock mode |
| Provider quota and billing failures | Keep prompt-only fallback and provider failover |
| Provider-specific image formats | Normalize image extraction and save provider-specific output formats |
| Google image format rejection | Use `image/jpeg` for Gemini image generation |
| OpenRouter image endpoint mismatch | Use `/api/v1/images` for image generation |
| Chinese query retrieval weakness | Add Chinese-to-English keyword expansion |
| API testing cost concern | Use local mocks for Stability AI provider validation |

## 11. Reflection On Agent Collaboration

The agent helped convert the homework requirements into a concrete application, design the architecture, break the work into module specs, scaffold the codebase, implement the Gradio UI, add provider fallback logic, debug environment and API issues, and prepare final documentation.

The human guided the major product and engineering decisions, including project topic, Python version, Student ID, screenshot demo format, API provider preferences, and the decision not to live-test Stability AI to avoid consuming image generation credits.
