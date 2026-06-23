# TurtleCare AI Development Status

本文件記錄目前實作與驗證狀態。`docs/agent.md` 仍是最高層級規格來源，`docs/architecture.md` 與 `docs/specs/` 是工程拆解文件。

## Environment

- Target Python version: Python 3.11
- Verified conda environment: `DGM`
- Verified interpreter: `C:\miniconda3\envs\DGM\python.exe`
- Verified Python version: Python 3.11.15

Installed core packages:

```text
gradio==6.19.0
gradio_client==2.5.0
openai==2.43.0
google-genai==2.9.0
scikit-learn==1.9.0
numpy==2.4.6
python-dotenv==1.2.2
Markdown==3.10.2
```

Installed local screenshot helper package:

```text
playwright==1.60.0
```

Dependency health:

```text
python -m pip check
No broken requirements found.
```

## Implemented

- [x] `requirements.txt`
- [x] `requirements-dev.txt`
- [x] `.env.example`
- [x] Local `.env` for mock-mode development
- [x] `.gitignore`
- [x] `app.py`
- [x] `src/config.py`
- [x] `src/rag.py`
- [x] `src/llm_client.py`
- [x] `src/turtle_profile.py`
- [x] `src/risk_checker.py`
- [x] `src/report_generator.py`
- [x] `src/prompt_generator.py`
- [x] `src/image_generator.py`
- [x] Multi-provider text fallback settings and implementation
- [x] Multi-provider image fallback settings and implementation
- [x] Stability AI image provider support added without live API test
- [x] `docs/specs/provider_failover_spec.md`
- [x] `data/knowledge_base/*.md`
- [x] `outputs/images/.gitkeep`
- [x] `examples/sample_cases.md`
- [x] `README.md`
- [x] `workflow_log.md`
- [x] `scripts/smoke_test.py`
- [x] `scripts/capture_demo_screenshot.py`
- [x] `314831018_HW7.txt` with GitHub repository link

## Verified

- [x] DGM Python can run.
- [x] Dependencies installed in DGM.
- [x] `pip check` reports no broken requirements.
- [x] Python syntax compile check passes for `app.py`, `src/`, and `scripts/`.
- [x] `scripts/smoke_test.py` passes.
- [x] RAG retrieves top 3 chunks.
- [x] Chinese care questions use keyword expansion for better English knowledge-base retrieval.
- [x] Mock mode is active when local `.env` has an empty `OPENAI_API_KEY`.
- [x] Mock Q&A and diagnosis responses follow Chinese input when applicable.
- [x] Q&A flow returns an answer and references.
- [x] Diagnosis flow returns report, risk summary, and references.
- [x] Tank design flow returns English prompt, negative prompt, materials, safety notes, status, and references.
- [x] Image generation disabled fallback returns no image path and a user-facing status message.
- [x] Text generation still supports mock mode when no provider key is configured.
- [x] Optional image generation still supports prompt-only fallback when disabled.
- [x] Gradio server starts and responds at `http://127.0.0.1:7860`.
- [x] Gradio API endpoints `/handle_qa`, `/handle_diagnosis`, and `/handle_design` have been called successfully.

## Remaining Manual Submission Tasks

- [x] Fill `314831018_HW7.txt` with the final public GitHub repository link or shared Google Drive link.
- [x] Capture demo screenshot as `314831018_HW7.png`.
- [x] Demo screenshot includes a Chinese Q&A input, generated Chinese mock answer, and retrieved references.
- [ ] Optionally configure a real OpenRouter API key in `.env` for real LLM testing.
- [ ] Optionally configure a real OpenAI API key in `.env` for real LLM/image testing.
- [ ] Optionally configure a real Gemini API key in `.env` for real LLM/image testing.
- [ ] Optionally configure a real Stability AI API key in `.env` for real image testing.
- [ ] Optionally configure `IMAGE_GENERATION_ENABLED=true` and at least one image provider model for real image generation testing.
- [ ] Review README and workflow log before final submission.

## Recommended Next Commands

Run smoke test:

```powershell
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
```

Start app:

```powershell
C:\miniconda3\envs\DGM\python.exe app.py
```

Open:

```text
http://127.0.0.1:7860
```

Capture demo screenshot after starting the app:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip install -r requirements-dev.txt
C:\miniconda3\envs\DGM\python.exe scripts\capture_demo_screenshot.py
```
