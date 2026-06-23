# TurtleCare AI

## Overview

TurtleCare AI is an agent-developed generative AI application for the Deep Generative Models final assignment. It is a RAG-based turtle care and tank design assistant that helps users ask husbandry questions, evaluate turtle tank conditions, identify deterministic care risks, and generate diffusion-ready turtle tank design prompts.

The project combines:

- Large Language Models through API-based text generation.
- RAG with a local Markdown turtle care knowledge base.
- Rule-based safety and risk checking.
- Prompt engineering for image generation.
- Optional image generation through multiple providers.
- A Traditional Chinese Gradio user interface.

TurtleCare AI is an educational assistant. It does not provide veterinary diagnosis. Severe, persistent, or rapidly worsening symptoms should be handled by a qualified reptile veterinarian.

## System Architecture

```text
User
  -> Gradio UI
  -> Turtle profile builder
  -> TF-IDF RAG retriever
  -> Rule-based risk checker
  -> Report / prompt builders
  -> Text provider router
  -> OpenRouter / OpenAI / Google Gemini
  -> UI text outputs

Tank design prompt
  -> Optional image provider router
  -> OpenRouter / OpenAI / Google Gemini / Stability AI
  -> outputs/images/
```

The frontend and backend are integrated directly through Gradio event handlers. There is no separate web API server. The app calls Python backend functions directly and displays generated answers, diagnosis reports, prompt sections, retrieved references, risk summaries, image status messages, and optional generated image paths.

## Features

- Turtle Care Q&A with retrieved knowledge references.
- Tank Environment Diagnosis with deterministic risk checking.
- Tank Design Prompt Generator with English image prompt, negative prompt, materials, and safety notes.
- Multi-provider text fallback: OpenRouter -> OpenAI -> Google Gemini.
- Optional multi-provider image fallback: OpenRouter -> OpenAI -> Google Gemini -> Stability AI.
- Mock mode when no text API key is configured.
- Prompt-only image design mode for stable demonstrations.
- Traditional Chinese UI labels.

## Technology Stack

- Python 3.11
- Gradio
- scikit-learn TF-IDF retrieval
- OpenAI Python SDK for OpenRouter-compatible and OpenAI APIs
- Google Gen AI SDK for Gemini APIs
- requests for Stability AI image generation
- python-dotenv
- Local Markdown knowledge base

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── 314831018_HW7.txt
├── 314831018_HW7.png
├── data/knowledge_base/
├── docs/
│   ├── architecture.md
│   ├── debugging_process.md
│   ├── development_status.md
│   └── specs/
├── examples/
├── outputs/images/
├── scripts/
└── src/
```

## Installation

Recommended setup with the existing conda environment:

```powershell
cd "C:\Users\邦亢\Desktop\BK\NYCU\Deep Generative Models\Deep_Generative_Models_hw7"
conda activate DGM
python -m pip install -r requirements.txt
```

If PowerShell does not resolve the correct `python`, use the DGM interpreter directly:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip install -r requirements.txt
```

Optional screenshot helper dependencies:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip install -r requirements-dev.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill only the providers you want to use.

```env
TEXT_PROVIDER_ORDER=openrouter,openai,google
IMAGE_PROVIDER_ORDER=openrouter,openai,google,stability
PROVIDER_TIMEOUT_SECONDS=45

OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_TEXT_MODEL=openai/gpt-4o-mini
OPENROUTER_IMAGE_MODEL=
OPENROUTER_IMAGE_SIZE=1024x1024

OPENAI_API_KEY=
OPENAI_TEXT_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_IMAGE_SIZE=1024x1024

GEMINI_API_KEY=
GOOGLE_TEXT_MODEL=gemini-3.5-flash
GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image
GOOGLE_IMAGE_ASPECT_RATIO=1:1

STABILITY_API_KEY=
STABILITY_IMAGE_ENDPOINT=https://api.stability.ai/v2beta/stable-image/generate/sd3
STABILITY_OUTPUT_FORMAT=jpeg

LLM_TEMPERATURE=0.3
RETRIEVAL_TOP_K=3
IMAGE_GENERATION_ENABLED=false
```

If all text provider API keys are empty, the app runs in mock mode. Legacy OpenRouter `.env` files using `OPENAI_API_KEY` with `OPENAI_BASE_URL=https://openrouter.ai/api/v1` remain compatible when `OPENROUTER_API_KEY` is not set, but new configuration should use `OPENROUTER_API_KEY`.

## How To Run

Start the Gradio app:

```powershell
C:\miniconda3\envs\DGM\python.exe app.py
```

Open the local URL shown in the terminal. The verified local URL during development was:

```text
http://127.0.0.1:7860
```

## Validation

Run the backend smoke test:

```powershell
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
```

Run dependency health check:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip check
```

Run syntax compilation check:

```powershell
C:\miniconda3\envs\DGM\python.exe -m compileall app.py src scripts
```

The smoke test supports both mock mode and real API mode. If image generation is enabled, it may call configured external image providers and consume provider quota.

## Optional Image Generation

The MVP always generates a diffusion-ready turtle tank design prompt. Image generation is optional and disabled by default.

To enable image generation, configure at least one image provider:

```env
IMAGE_GENERATION_ENABLED=true
IMAGE_PROVIDER_ORDER=stability,openrouter,openai,google

STABILITY_API_KEY=your-stability-api-key
STABILITY_IMAGE_ENDPOINT=https://api.stability.ai/v2beta/stable-image/generate/sd3
STABILITY_OUTPUT_FORMAT=jpeg
```

If image generation is disabled, unsupported, misconfigured, quota-limited, or fails, the app keeps showing the generated prompt, negative prompt, materials, and safety notes.

Generated images are for visualization only. They are not engineering blueprints or veterinary recommendations.

## RAG Knowledge Base

The RAG knowledge base is located at:

```text
data/knowledge_base/
```

It contains eight curated Markdown files covering turtle species, tank setup, water quality, lighting, feeding, common health warnings, mixed-species housing, and emergency warnings. The retriever in `src/rag.py` loads these files, splits them by Markdown headings and paragraphs, builds a TF-IDF index, and returns the top 3 chunks with source filename, heading, preview, and score.

The current knowledge base is a local educational knowledge base created for this assignment. It is not a citation-based veterinary database.

## Demo And Submission

Submission files:

```text
314831018_HW7.txt
314831018_HW7.png
```

- `314831018_HW7.txt` contains the repository or shared drive link.
- `314831018_HW7.png` is the screenshot demonstration material.

Prompt-only mode is acceptable for the screenshot demo because the core assignment requirements are satisfied by the interactive LLM/RAG app and image-generation prompt workflow. Optional real image generation depends on provider quota and billing status.

## Agent-driven Development

This project was developed with Codex Agent assistance. The agent helped with ideation, architecture design, task decomposition, code generation, debugging, UI integration, provider migration, and documentation.

Detailed records:

- `workflow_log.md`
- `docs/architecture.md`
- `docs/debugging_process.md`
- `docs/development_status.md`
- `docs/specs/`

## Limitations

- TurtleCare AI does not provide veterinary diagnosis.
- The knowledge base is small and educational.
- TF-IDF retrieval is simple and keyword-based.
- Optional image generation depends on provider model availability, pricing, quota, and response format.
- Real API behavior may change when providers update model names or endpoint requirements.
