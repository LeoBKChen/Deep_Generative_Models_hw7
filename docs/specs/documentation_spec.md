# Documentation Spec

## Purpose

定義 final submission 需要的 English `README.md` 與 `workflow_log.md`，並確保文件能清楚展示 Agent-driven development process。

## Responsibilities

- Write complete English README.
- Write independent English workflow log.
- Explain architecture, setup, environment variables, mock mode, and optional image generation.
- Document prompts, tools, generated modules, debugging records, and human decisions.
- Keep documentation aligned with implemented behavior.

## Inputs

- `docs/agent.md`.
- `docs/architecture.md`.
- Module specs under `docs/specs/`.
- Final implemented code.
- Debugging records and demo notes.

## Outputs

Required files:

```text
README.md
workflow_log.md
```

Optional supporting files:

```text
examples/sample_cases.md
assets/demo_screenshot.png
```

## Data Format

README required sections:

```markdown
# TurtleCare AI

## Overview
## Motivation
## Features
## System Architecture
## Technology Stack
## Project Structure
## Installation
## Environment Variables
## How to Run
## Example Usage
## Optional Image Generation
## Demo
## Limitations
## Future Work
## Agent-driven Development
```

Workflow log required sections:

```markdown
# Agent Collaboration Workflow Log

## 1. Tools Used
## 2. Phase 1: Ideation and Planning
## 3. Phase 2: Architecture Design and Task Decomposition
## 4. Phase 3: Knowledge Base Construction
## 5. Phase 4: Code Generation and Implementation
## 6. Phase 5: UI Integration
## 7. Phase 6: Documentation and Finalization
## 8. Technical Bottlenecks and Resolutions
## 9. Reflection on Agent Collaboration
```

## Error / Fallback Behavior

- If optional image generation is not configured, README must still explain prompt-only usage.
- If real API was not used during demo, README and workflow log must explain mock mode.
- If screenshots are not available yet, README may include a placeholder demo section before final submission.

## Safety Requirements

- Documentation must state TurtleCare AI does not provide veterinary diagnosis.
- Documentation must state generated images are visualization only.
- Do not include API keys, private repository credentials, or private user data.

## Implementation Checklist

- [ ] Write English README.
- [ ] Include assignment context.
- [ ] Include architecture overview.
- [ ] Include local installation steps.
- [ ] Include `.env.example` explanation.
- [ ] Explain mock mode.
- [ ] Explain multi-provider text and image fallback.
- [ ] Write English workflow log.
- [ ] Record key prompts and agent outputs.
- [ ] Record technical bottlenecks and fixes.
- [ ] Record final validation results.

## Completion Checklist

- [ ] README can guide a new user to run the App.
- [ ] README explains OpenRouter, OpenAI, and Google Gemini provider fallback.
- [ ] README explains image generation is optional and disabled by default.
- [ ] workflow log clearly documents Agent-driven workflow.
- [ ] workflow log includes human decisions.
- [ ] No secrets are included.
- [ ] Documentation matches actual implemented behavior.
