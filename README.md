# TurtleCare AI

## Overview

TurtleCare AI is a RAG-based turtle keeping and tank design assistant for the Deep Generative Models final assignment. It helps users ask turtle care questions, evaluate tank conditions, identify husbandry risks, and generate diffusion-ready turtle tank design prompts.

The app uses a local Markdown knowledge base, TF-IDF retrieval, rule-based risk checking, and a multi-provider LLM client with OpenRouter, OpenAI, and Google Gemini fallback. It also includes optional multi-provider image generation, disabled by default so the MVP remains stable in prompt-only mode.

## Features

- Turtle Care Q&A with retrieved references.
- Tank Environment Diagnosis with deterministic risk checking.
- Tank Design Prompt Generator with English image prompt, negative prompt, materials, and safety notes.
- Optional OpenRouter, OpenAI, Google Gemini, or Stability AI image generation.
- Mock mode when no API key is configured.
- Traditional Chinese Gradio UI.

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
├── .env.example
├── data/knowledge_base/
├── docs/
├── examples/
├── outputs/images/
└── src/
```

## Installation

Recommended conda setup for this project:

```powershell
conda activate DGM
pip install -r requirements.txt
```

If `conda` is not initialized in PowerShell, use the environment Python directly:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip install -r requirements.txt
```

Alternative virtualenv setup:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill values if needed.

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

If all provider API keys are empty, the app runs in mock mode. This allows the full Gradio demo to work without external API access.

Legacy OpenRouter `.env` files using `OPENAI_API_KEY` with `OPENAI_BASE_URL=https://openrouter.ai/api/v1` remain compatible when `OPENROUTER_API_KEY` is not set, but new configuration should use `OPENROUTER_API_KEY`.

## How To Run

```powershell
C:\miniconda3\envs\DGM\python.exe app.py
```

Open the local Gradio URL shown in the terminal.

## Smoke Test

Run the backend smoke test before recording the demo screenshot:

```powershell
C:\miniconda3\envs\DGM\python.exe scripts\smoke_test.py
```

The test checks mock mode, RAG retrieval, Q&A generation, diagnosis risks, design prompt generation, and disabled image-generation fallback.

Optional dependency check:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip check
```

## Optional Image Generation

The MVP always generates a diffusion-ready turtle tank design prompt. Image generation is optional and disabled by default.

To enable image generation, configure at least one image-capable provider:

```env
IMAGE_GENERATION_ENABLED=true
IMAGE_PROVIDER_ORDER=openrouter,openai,google,stability

OPENROUTER_IMAGE_MODEL=your-openrouter-image-model
OPENROUTER_IMAGE_SIZE=1024x1024

OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_IMAGE_SIZE=1024x1024

GOOGLE_IMAGE_MODEL=gemini-3.1-flash-image
GOOGLE_IMAGE_ASPECT_RATIO=1:1

STABILITY_API_KEY=your-stability-api-key
STABILITY_IMAGE_ENDPOINT=https://api.stability.ai/v2beta/stable-image/generate/sd3
STABILITY_OUTPUT_FORMAT=jpeg
```

If image generation is disabled, unsupported, misconfigured, or fails, the app keeps showing the generated prompt, negative prompt, materials, and safety notes.

Generated images are for visualization only. They are not engineering blueprints or veterinary recommendations.

## Demo

The planned submission demo format is a screenshot named `314831018_HW7.png`.

Recommended screenshot content:

- Running Gradio UI.
- At least one generated output from the Tank Design tab or Diagnosis tab.
- Prompt-only mode is acceptable and expected for stable demo submission.

Current verified local URL:

```text
http://127.0.0.1:7860
```

See `docs/development_status.md` for the current implementation and validation status.

Optional local screenshot helper:

```powershell
C:\miniconda3\envs\DGM\python.exe -m pip install -r requirements-dev.txt
C:\miniconda3\envs\DGM\python.exe scripts\capture_demo_screenshot.py
```

This helper assumes the Gradio app is already running at `http://127.0.0.1:7860`.

## Limitations

- TurtleCare AI does not provide veterinary diagnosis.
- The knowledge base is small and educational.
- TF-IDF retrieval is simple and keyword-based.
- Optional image generation depends on provider model availability, pricing, quota, and response format.

## Agent-driven Development

This project is developed with Codex Agent assistance. The documentation includes planning files, architecture specs, module specs, implementation notes, and a workflow log to show the agent-driven process.
