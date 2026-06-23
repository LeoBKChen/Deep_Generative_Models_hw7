# agent.md

# TurtleCare AI: RAG-based Turtle Keeping and Tank Design Assistant

## 0. Agent Role

You are a coding agent helping implement **TurtleCare AI**, a final project for the course **Deep Generative Models**.

Your job is to assist with:

* Project scaffolding
* Architecture implementation
* RAG knowledge base construction
* LLM integration
* Rule-based turtle care risk checking
* Gradio UI implementation
* Debugging
* README writing
* Workflow log writing
* Demo preparation

The final result must be a complete, runnable generative AI application with an interactive user interface.

The project must demonstrate an **Agent-driven workflow**, meaning that the agent should assist throughout planning, architecture design, code generation, debugging, UI integration, and documentation.

---

## 1. Project Summary

**TurtleCare AI** is an interactive turtle keeping assistant.

It helps users:

1. Ask turtle care questions.
2. Evaluate turtle tank conditions.
3. Identify potential turtle care risks.
4. Generate personalized tank improvement reports.
5. Generate diffusion-ready turtle tank design prompts.

The system combines:

* A local Markdown turtle care knowledge base
* A RAG retrieval pipeline
* A rule-based risk checker
* An OpenAI-compatible LLM backend
* A Gradio-based interactive App
* Optional future diffusion image generation support

The project should stay simple, modular, and reliable.

---

## 2. Assignment Context

This project is for the final assignment of the course **Deep Generative Models**.

The assignment requires a generative AI App that demonstrates at least one of the following:

* Large Language Models, also known as LLMs
* Diffusion Models
* Flow Matching Models

TurtleCare AI satisfies the requirements through:

| Assignment Requirement              | TurtleCare AI Implementation                                     |
| ----------------------------------- | ---------------------------------------------------------------- |
| Generative AI App                   | Interactive turtle care assistant                                |
| LLM usage                           | Q&A, report generation, tank design prompt generation            |
| RAG architecture                    | Local Markdown turtle care knowledge base retrieval              |
| Diffusion / Flow Matching relevance | Diffusion-ready tank design prompt generator                     |
| Agent-driven workflow               | Coding agent used for planning, coding, debugging, documentation |
| Interactive UI                      | Gradio App                                                       |
| Source code                         | GitHub repository                                                |
| Documentation                       | README.md and workflow_log.md                                    |
| Demo material                       | Screenshot or video of the running App                           |

---

## 3. Project Scope

### 3.1 MVP Scope

The MVP must include:

1. Gradio interactive UI
2. Turtle Care Q&A tab
3. Tank Environment Diagnosis tab
4. Tank Design Prompt Generator tab
5. Local Markdown knowledge base
6. Basic RAG retriever
7. Rule-based turtle care risk checker
8. OpenAI-compatible LLM API client
9. Fallback mock response mode when no API key is available
10. README.md
11. workflow_log.md
12. Demo screenshot or video

---

### 3.2 Out of Scope for MVP

Do not implement these unless explicitly requested later:

* User login system
* Cloud database
* Mobile App deployment
* Real veterinary diagnosis
* Web crawling
* Large-scale vector database service
* Complex fine-tuning
* Real-time camera analysis
* Full medical triage system
* Mandatory image generation backend
* Payment or subscription system

The MVP should prioritize a working local App over ambitious but fragile features.

---

## 4. Core Design Principle

The project must be:

* Easy to run locally
* Easy to explain in README
* Easy to demonstrate in a video
* Modular enough for future extension
* Safe in health-related responses
* Clearly aligned with the course assignment

Prefer a simple working system over a complex unfinished system.

---

## 5. Recommended Technical Stack

### 5.1 Frontend / UI

Use:

```text
Gradio
```

Reason:

* Fast to implement
* Easy to demo
* Suitable for AI Apps
* Works well with Python backend

---

### 5.2 Backend Language

Use:

```text
Python
```

Recommended Python version:

```text
Python 3.10+
```

---

### 5.3 RAG Retriever

MVP option:

```text
TF-IDF retrieval using scikit-learn
```

Reason:

* Lightweight
* No GPU required
* No model download required
* Easy to debug
* Suitable for small Markdown knowledge base

Optional advanced version:

```text
sentence-transformers + FAISS
```

Only implement the advanced version if the MVP is already stable.

---

### 5.4 LLM Backend

Implement a generic OpenAI-compatible API client.

Support environment variables:

```text
OPENAI_API_KEY=
OPENAI_BASE_URL=
OPENAI_MODEL=
```

The client should work with OpenAI-compatible providers such as:

* OpenRouter
* Ollama OpenAI-compatible API
* Big Pickle through OpenCode-compatible endpoint
* Other OpenAI-compatible inference services

Important:

* Do not hard-code private API keys.
* Provide `.env.example`.
* Provide fallback mock mode if no API key is available.

---

### 5.5 Dependency File

Use:

```text
requirements.txt
```

Suggested dependencies:

```text
gradio
python-dotenv
openai
scikit-learn
numpy
markdown
```

Add additional dependencies only when necessary.

---

## 6. Required Project Structure

Create the following structure:

```text
turtlecare-ai/
├── agent.md
├── app.py
├── requirements.txt
├── README.md
├── workflow_log.md
├── .env.example
├── data/
│   └── knowledge_base/
│       ├── turtle_species.md
│       ├── tank_setup.md
│       ├── water_quality.md
│       ├── lighting_and_basking.md
│       ├── feeding.md
│       ├── common_health_issues.md
│       ├── mixed_species_warning.md
│       └── emergency_warning.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── rag.py
│   ├── llm_client.py
│   ├── turtle_profile.py
│   ├── risk_checker.py
│   ├── report_generator.py
│   └── prompt_generator.py
├── assets/
│   └── demo_screenshot.png
├── examples/
│   └── sample_cases.md
└── docs/
    └── project_outline.md
```

The exact structure may be adjusted only if there is a clear reason. Keep the repository easy to inspect.

---

## 7. Module Responsibilities

### 7.1 `app.py`

Main Gradio App entry point.

Responsibilities:

* Launch the UI
* Define three main tabs
* Collect user inputs
* Call backend functions
* Display generated outputs
* Display retrieved references
* Display risk results

Required tabs:

1. Turtle Care Q&A
2. Tank Environment Diagnosis
3. Tank Design Prompt Generator

---

### 7.2 `src/config.py`

Responsibilities:

* Load environment variables
* Define default paths
* Define LLM settings
* Define RAG settings

Expected settings:

```python
KNOWLEDGE_BASE_DIR
OPENAI_API_KEY
OPENAI_BASE_URL
OPENAI_MODEL
LLM_TEMPERATURE
RETRIEVAL_TOP_K
MOCK_MODE
```

---

### 7.3 `src/rag.py`

Responsibilities:

* Load Markdown files from `data/knowledge_base/`
* Split Markdown documents into chunks
* Build a simple TF-IDF retrieval index
* Retrieve top-k relevant chunks
* Return retrieved chunks with source filenames

Required behavior:

* If knowledge files are missing, return a clear error message.
* Keep retrieval simple and deterministic.
* Include source names in returned references.

---

### 7.4 `src/llm_client.py`

Responsibilities:

* Provide one function for LLM calls
* Use OpenAI-compatible API format
* Handle missing API key
* Handle API errors
* Provide fallback mock responses

Required behavior:

* Never expose API keys.
* If no API key exists, return mock output that still allows the demo to run.
* Keep the interface simple for other modules.

Suggested function:

```python
generate_text(system_prompt: str, user_prompt: str) -> str
```

---

### 7.5 `src/turtle_profile.py`

Responsibilities:

* Convert UI inputs into a structured turtle profile
* Normalize missing fields
* Format the profile as readable text for prompts

Profile fields may include:

* Turtle species
* Shell length
* Number of turtles
* Tank length
* Tank width
* Tank height
* Water depth
* Basking area availability
* UVB light availability
* Heating equipment
* Filtration method
* Feeding content
* Mixed-species condition
* Current concern

---

### 7.6 `src/risk_checker.py`

Responsibilities:

* Apply deterministic rule-based care checks
* Return risk level and explanation
* Support environment diagnosis report generation

Required checks:

1. No basking area
2. No UVB light
3. Mixed-species housing
4. Weak or missing filtration
5. Deep water without resting area
6. Unclear or unbalanced feeding
7. Health-related warning symptoms

Example rule:

```text
If basking_area == false:
    risk_level = "high"
    message = "Aquatic and semi-aquatic turtles need a completely dry basking area."
```

The risk checker should not claim medical certainty.

---

### 7.7 `src/report_generator.py`

Responsibilities:

* Build RAG Q&A prompts
* Build environment diagnosis prompts
* Combine user profile, retrieved chunks, and risk results
* Call `llm_client.generate_text`
* Return formatted care advice or report

Required outputs:

For Q&A:

* Direct answer
* Practical suggestions
* Safety warning when needed
* Retrieved reference summary

For environment diagnosis:

* Overall assessment
* Current strengths
* Potential risks
* Priority improvement checklist
* Daily care checklist
* Weekly care checklist
* Safety warnings

---

### 7.8 `src/prompt_generator.py`

Responsibilities:

* Generate diffusion-ready turtle tank design prompts
* Generate negative prompts
* Generate practical material suggestions
* Generate safety notes

Required outputs:

1. English image generation prompt
2. Negative prompt
3. Suggested materials
4. Safety notes

The design must prioritize:

* Turtle safety
* Stable basking access
* Clean water
* Realistic layout
* Easy climbing ramps
* Safe resting areas
* UVB and heat lamp placement

---

## 8. Knowledge Base Requirements

Create a local Markdown knowledge base under:

```text
data/knowledge_base/
```

Required files:

```text
turtle_species.md
tank_setup.md
water_quality.md
lighting_and_basking.md
feeding.md
common_health_issues.md
mixed_species_warning.md
emergency_warning.md
```

---

### 8.1 `turtle_species.md`

Include basic information about:

* Taiwan stripe-necked turtle
* Red-eared slider
* African side-necked turtle
* Musk turtle
* Map turtle

For each species, include:

* General behavior
* Aquatic or semi-aquatic tendency
* Tank needs
* Diet notes
* Basking needs
* Compatibility notes
* Common risks

---

### 8.2 `tank_setup.md`

Include:

* Tank size
* Water depth
* Dry basking area
* Ramps
* Resting areas
* Substrate
* Decorations
* Escape prevention
* Safety concerns

---

### 8.3 `water_quality.md`

Include:

* Filtration
* Partial water changes
* Dechlorination
* Ammonia
* Nitrite
* Nitrate
* Water temperature
* Cleaning after feeding

---

### 8.4 `lighting_and_basking.md`

Include:

* UVB light
* UVA light
* Heat lamp
* Basking temperature
* Light distance
* Lighting schedule
* Bulb replacement

---

### 8.5 `feeding.md`

Include:

* Juvenile turtle feeding
* Adult turtle feeding
* Commercial pellets
* Vegetables
* Animal protein
* Calcium
* Overfeeding risks

---

### 8.6 `common_health_issues.md`

Include beginner-level warning signs:

* Refusing food
* Swollen eyes
* Floating abnormally
* Shell softness
* Skin lesions
* Wounds
* Breathing difficulty

Mandatory disclaimer:

```text
TurtleCare AI does not provide veterinary diagnosis.
If symptoms are severe, persistent, or rapidly worsening, consult a qualified reptile veterinarian.
```

---

### 8.7 `mixed_species_warning.md`

Include:

* Mixed-species housing risks
* Size differences
* Feeding competition
* Biting
* Territorial stress
* Quarantine
* Separation plans

---

### 8.8 `emergency_warning.md`

Include warning signs requiring professional help:

* Serious injury
* Long-term refusal to eat
* Abnormal floating or imbalance
* Noisy breathing
* Eyes unable to open
* Severe shell or skin infection
* Bleeding

---

## 9. UI Requirements

The Gradio App must include three tabs.

---

### 9.1 Tab 1: Turtle Care Q&A

Inputs:

* Turtle species
* Shell length
* User question

Outputs:

* Generated answer
* Retrieved knowledge references

Expected behavior:

* Retrieve relevant knowledge chunks.
* Generate a helpful answer.
* Include safety warnings for health-related questions.

---

### 9.2 Tab 2: Tank Environment Diagnosis

Inputs:

* Turtle species
* Number of turtles
* Shell length
* Tank length
* Tank width
* Tank height
* Water depth
* Basking area availability
* UVB light availability
* Heating equipment
* Filtration method
* Feeding content
* Mixed-species condition
* Current concern

Outputs:

* Environment diagnosis report
* Risk summary
* Priority improvement checklist
* Retrieved references

Expected behavior:

* Run rule-based risk checker.
* Retrieve related knowledge.
* Generate a structured report.

---

### 9.3 Tab 3: Tank Design Prompt Generator

Inputs:

* Turtle species
* Tank size
* Water depth
* Desired tank style
* Required elements
* Elements to avoid

Outputs:

* Diffusion-ready English image prompt
* Negative prompt
* Suggested materials
* Safety notes

Expected behavior:

* Generate a realistic and safe turtle tank design prompt.
* Keep the prompt suitable for image generation models.

---

## 10. RAG Pipeline Requirements

The RAG pipeline should follow this flow:

```text
User query
  ↓
Load Markdown knowledge base
  ↓
Split documents into chunks
  ↓
Build TF-IDF index
  ↓
Retrieve top-k relevant chunks
  ↓
Inject retrieved context into LLM prompt
  ↓
Generate grounded answer
```

Required implementation details:

* Use source filenames for references.
* Keep chunk size simple.
* Rebuild index at startup for MVP.
* Avoid external database dependency in MVP.
* Return retrieved context even in mock mode.

---

## 11. Prompt Templates

### 11.1 System Prompt

Use this general system prompt for LLM calls:

```text
You are TurtleCare AI, a turtle keeping assistant.
Use the provided context and user profile to generate practical, beginner-friendly advice.
Do not provide veterinary diagnosis.
For severe, persistent, or rapidly worsening symptoms, recommend consulting a qualified reptile veterinarian.
Prioritize animal safety, water quality, basking access, UVB lighting, heating, filtration, and species compatibility.
If information is missing, state assumptions clearly.
Provide structured recommendations and actionable next steps.
```

---

### 11.2 RAG Q&A Prompt Template

```text
Retrieved turtle care knowledge:
{retrieved_context}

User turtle profile:
{turtle_profile}

User question:
{question}

Task:
Answer the user's question using the retrieved knowledge and the turtle profile.
Give practical advice.
Mention uncertainty when needed.
Do not provide veterinary diagnosis.
If the question involves health symptoms, include a safety warning when appropriate.
```

---

### 11.3 Environment Diagnosis Prompt Template

```text
Retrieved turtle care knowledge:
{retrieved_context}

User turtle and tank profile:
{turtle_profile}

Rule-based risk results:
{risk_results}

Task:
Generate a structured turtle tank environment diagnosis report.

The report must include:
1. Overall assessment
2. Current strengths
3. Potential risks
4. Priority improvement checklist
5. Daily care checklist
6. Weekly care checklist
7. Safety warnings
```

---

### 11.4 Tank Design Prompt Template

```text
User requirements:
{design_requirements}

Relevant turtle care knowledge:
{retrieved_context}

Task:
Generate:
1. A diffusion-ready English image prompt
2. A negative prompt
3. A practical material list
4. Safety notes

The design must prioritize turtle safety, stable basking access, clean water, realistic tank layout, and accessible dry basking area.
```

---

## 12. Safety Rules

The App must follow these safety rules.

### 12.1 Health-related Safety

* Do not provide veterinary diagnosis.
* Do not claim that a symptom has one definite cause.
* For severe, persistent, or worsening symptoms, recommend a reptile veterinarian.
* Use cautious language for health issues.
* Provide husbandry checks rather than medical treatment instructions.

Example wording:

```text
This may be related to husbandry, stress, water quality, infection, or other causes.
TurtleCare AI cannot diagnose the condition.
If the symptom is severe, persistent, or worsening, please consult a qualified reptile veterinarian.
```

---

### 12.2 Tank Design Safety

* Do not recommend sharp decorations.
* Do not recommend unstable rock piles.
* Do not recommend small gravel that may be swallowed.
* Deep water must include resting or climbing access.
* Basking platform must allow complete drying.
* Mixed-species housing should be treated as a risk.

---

### 12.3 API and Privacy Safety

* Do not hard-code API keys.
* Do not commit `.env`.
* Provide `.env.example`.
* Avoid collecting unnecessary personal information.
* Do not store user conversations unless explicitly implemented and documented.

---

## 13. README.md Requirements

Generate a complete `README.md`.

It must include:

* Project title
* Course assignment context
* Overview
* Motivation
* Features
* System architecture
* Technology stack
* Folder structure
* Installation steps
* Environment variable setup
* How to run the App
* Example usage
* Demo screenshot or video section
* Limitations
* Future work
* Agent usage summary

Suggested README sections:

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

## Demo

## Limitations

## Future Work

## Agent-driven Development
```

---

## 14. Workflow Log Requirements

Generate an independent file:

```text
workflow_log.md
```

It must document the Agent-assisted development process.

Required sections:

```markdown
# Agent Collaboration Workflow Log

## 1. Tools Used

## 2. Phase 1: Ideation and Planning

### Prompt Used

### Agent Output Summary

### Human Decision

## 3. Phase 2: Architecture Design and Task Decomposition

### Prompt Used

### Agent Output Summary

### Human Decision

## 4. Phase 3: Knowledge Base Construction

### Prompt Used

### Generated Files

### Human Review Notes

## 5. Phase 4: Code Generation and Implementation

### Prompt Used

### Generated Components

### Debugging Records

## 6. Phase 5: UI Integration

### Prompt Used

### Generated Components

## 7. Phase 6: Documentation and Finalization

### Prompt Used

### Generated Files

## 8. Technical Bottlenecks and Resolutions

## 9. Reflection on Agent Collaboration
```

The workflow log should mention:

* Key prompts used
* Agent tools used
* LLM backend used
* Generated modules
* Debugging problems
* How the agent helped solve them
* Final reflection

---

## 15. Demo Requirements

Prepare at least one demo material:

```text
<StudentID>_HW7.mp4
```

or

```text
<StudentID>_HW7.png
```

The demo should show:

1. App successfully starts.
2. Turtle Care Q&A works.
3. Environment Diagnosis works.
4. Tank Design Prompt Generator works.
5. Generated output appears in the UI.

Suggested demo case:

```text
Species: Taiwan stripe-necked turtle
Shell length: 7 cm
Tank size: 100 x 80 x 100 cm
Water depth: 60 cm
Basking area: yes
UVB light: no
Filtration: external canister filter
Mixed species: yes, African side-necked turtle
Current concern: Is deep water and mixed housing safe?
```

---

## 16. Submission Requirements

Final submission requires two files.

### 16.1 Repository Link TXT

Create:

```text
<StudentID>_HW7.txt
```

The TXT file should contain:

* Public GitHub repository link

The repository must include:

* Source code
* `README.md`
* `workflow_log.md`
* `requirements.txt`
* Demo material or demo instructions

If GitHub cannot be public, use Google Drive sharing and set permission to:

```text
Anyone with the link
```

---

### 16.2 Demo Material

Create:

```text
<StudentID>_HW7.<ext>
```

Examples:

```text
314832001_HW7.mp4
314832001_HW7.png
```

---

## 17. Implementation Order

Follow this order.

### Step 1: Create Project Structure

Create all folders and placeholder files.

---

### Step 2: Implement Knowledge Base

Create the eight Markdown knowledge files.

Keep the content:

* Concise
* Beginner-friendly
* Practical
* Safety-aware
* Non-diagnostic

---

### Step 3: Implement RAG Retriever

Use TF-IDF for MVP.

Required functions:

```python
load_documents()
split_documents()
build_index()
retrieve(query, top_k=3)
format_retrieved_context()
```

---

### Step 4: Implement LLM Client

Use OpenAI-compatible API.

Required functions:

```python
generate_text(system_prompt, user_prompt)
```

Required behavior:

* If API key exists, call real LLM backend.
* If API key is missing, return mock response.
* If API call fails, return readable error message or fallback.

---

### Step 5: Implement Turtle Profile Formatter

Convert UI inputs into structured profile text.

---

### Step 6: Implement Risk Checker

Implement deterministic risk rules.

Return:

* Risk category
* Risk level
* Explanation
* Suggested action

---

### Step 7: Implement Report Generator

Combine:

* Turtle profile
* Retrieved context
* Risk results
* LLM prompt templates

Generate:

* Q&A answer
* Diagnosis report

---

### Step 8: Implement Tank Design Prompt Generator

Generate:

* English diffusion-ready prompt
* Negative prompt
* Materials
* Safety notes

---

### Step 9: Implement Gradio UI

Create three tabs.

Test all three tabs.

---

### Step 10: Write README and Workflow Log

Make documentation complete enough for assignment submission.

---

### Step 11: Prepare Demo

Create screenshot or video.

---

## 18. Validation Checklist

Before final submission, verify:

```text
[ ] The App starts successfully with `python app.py`.
[ ] Gradio UI opens locally.
[ ] Q&A tab returns an answer.
[ ] Environment Diagnosis tab returns a report.
[ ] Tank Design Prompt Generator returns a prompt.
[ ] RAG retrieves relevant knowledge chunks.
[ ] Retrieved source filenames are displayed.
[ ] Mock mode works without an API key.
[ ] Real LLM mode works when API key is configured.
[ ] Health-related answers include proper safety warnings.
[ ] README.md is complete.
[ ] workflow_log.md is complete.
[ ] requirements.txt is included.
[ ] .env.example is included.
[ ] No private API key is committed.
[ ] Demo screenshot or video is prepared.
[ ] GitHub or Google Drive link is accessible.
[ ] <StudentID>_HW7.txt is prepared.
[ ] <StudentID>_HW7.<ext> is prepared.
```

---

## 19. Coding Style Rules

Follow these rules:

* Keep code readable and modular.
* Prefer simple functions over complex abstractions.
* Avoid unnecessary dependencies.
* Use type hints where helpful.
* Add comments only for non-obvious logic.
* Handle missing files and missing API keys gracefully.
* Keep UI text clear and beginner-friendly.
* Do not create hidden external service dependencies.
* Do not implement features that are outside MVP unless explicitly requested.

---

## 20. Agent Behavior Rules

When acting as the coding agent:

1. Read this `agent.md` before making changes.
2. Keep the project aligned with TurtleCare AI.
3. Do not change the project scope without explanation.
4. Do not remove safety disclaimers.
5. Do not hard-code API keys.
6. Do not make veterinary diagnosis claims.
7. Prefer working MVP over complex extensions.
8. Update `README.md` when implementation changes.
9. Update `workflow_log.md` with important prompts, generated files, and debugging notes.
10. When fixing bugs, explain the cause and the fix.
11. When generating code, make sure the project remains runnable.
12. When adding dependencies, update `requirements.txt`.

---

## 21. Suggested Initial Prompt for Codex Agent

Use this prompt to start implementation:

```text
Read agent.md carefully and implement the TurtleCare AI MVP.

Create the full project structure and generate the initial files:
- app.py
- requirements.txt
- README.md
- workflow_log.md
- .env.example
- data/knowledge_base/*.md
- src/config.py
- src/rag.py
- src/llm_client.py
- src/turtle_profile.py
- src/risk_checker.py
- src/report_generator.py
- src/prompt_generator.py
- docs/project_outline.md
- examples/sample_cases.md

Use Gradio for the UI.
Use a simple local Markdown RAG retriever with TF-IDF for the MVP.
Use an OpenAI-compatible LLM API interface.
Include a fallback mock response mode when no API key is provided.
Implement three UI tabs:
1. Turtle Care Q&A
2. Tank Environment Diagnosis
3. Tank Design Prompt Generator

Keep the implementation simple, modular, safety-aware, and runnable locally.
After implementation, update README.md and workflow_log.md.
```

---

## 22. Suggested Debugging Prompt for Codex Agent

Use this prompt when the App has an error:

```text
The TurtleCare AI App has the following error:

[paste error message here]

Please inspect the relevant files, explain the cause, and fix the bug.
Keep the project aligned with agent.md.
Do not remove existing safety disclaimers.
After fixing the bug, update workflow_log.md with the debugging record.
```

---

## 23. Suggested Finalization Prompt for Codex Agent

Use this prompt before submission:

```text
Review the TurtleCare AI project for final submission.

Check:
1. The App runs with python app.py.
2. The Gradio UI has three working tabs.
3. RAG retrieval works.
4. Mock mode works without an API key.
5. README.md is complete.
6. workflow_log.md documents the Agent-driven process.
7. requirements.txt includes all dependencies.
8. .env.example is present.
9. No private API keys are committed.
10. The project satisfies the Deep Generative Models HW7 requirements.

Fix any issues you find and provide a final checklist.
```

---

## 24. Final Project Definition

The completed project should be describable as:

```text
TurtleCare AI is a RAG-based turtle keeping and tank design assistant. 
It uses a local Markdown knowledge base, a TF-IDF retrieval pipeline, rule-based risk checking, and an OpenAI-compatible LLM backend to generate personalized turtle care answers and tank environment diagnosis reports. 
It also generates diffusion-ready tank design prompts for visual planning. 
The system is packaged as a Gradio App and developed through an Agent-driven workflow.
```


# agent.md Update: OpenRouter Image Generation Extension

## Optional Image Generation Extension

TurtleCare AI must keep the **Tank Design Prompt Generator** as a required MVP feature.

In addition, the project should reserve an optional text-to-image generation feature using **OpenRouter image generation models**. This extension should use the same OpenRouter API infrastructure as the text LLM backend whenever possible.

The MVP must not depend on image generation. If image generation is disabled, unsupported, or unavailable, the App must still work completely in prompt-only mode.

---

## 1. Finalized Image Generation Strategy

Use the following priority:

```text
Required MVP:
Generate diffusion-ready turtle tank design prompts.

Optional extension:
Generate turtle tank layout images through OpenRouter image generation models.

Fallback:
If image generation is disabled or fails, show the generated prompt only.
```

The project should not use a separate OpenAI Image API key for the MVP.
Both text generation and optional image generation should be configured through OpenRouter-compatible settings.

---

## 2. Environment Variables

Update `.env.example` with the following variables:

```env
# Primary text LLM backend: OpenRouter
OPENAI_API_KEY=
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4o-mini

# Optional image generation through OpenRouter
IMAGE_GENERATION_ENABLED=false
OPENROUTER_IMAGE_MODEL=
OPENROUTER_IMAGE_SIZE=1024x1024
```

Notes:

* `OPENAI_API_KEY` is the OpenRouter API key.
* `OPENAI_BASE_URL` should point to the OpenRouter OpenAI-compatible endpoint.
* `OPENAI_MODEL` is used for text generation.
* `OPENROUTER_IMAGE_MODEL` is used only when image generation is enabled.
* `IMAGE_GENERATION_ENABLED=false` must be the default.
* The App must work even when `OPENROUTER_IMAGE_MODEL` is empty.

Optional example:

```env
IMAGE_GENERATION_ENABLED=true
OPENROUTER_IMAGE_MODEL=openai/gpt-5-image
OPENROUTER_IMAGE_SIZE=1024x1024
```

The actual image model should remain configurable because OpenRouter model availability, pricing, and model IDs may change over time.

---

## 3. Required Behavior

### 3.1 Prompt-only Mode

If:

```text
IMAGE_GENERATION_ENABLED=false
```

then the App should:

* Generate the English image prompt.
* Generate the negative prompt.
* Generate suggested materials.
* Generate safety notes.
* Not call any image generation model.
* Display a clear status message:

```text
圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。
```

---

### 3.2 Image Generation Enabled but Not Configured

If:

```text
IMAGE_GENERATION_ENABLED=true
```

but `OPENROUTER_IMAGE_MODEL` or `OPENAI_API_KEY` is missing, then the App should:

* Not crash.
* Still show the generated prompt.
* Still show materials and safety notes.
* Display a clear status message:

```text
圖片生成功能已啟用，但缺少 OpenRouter API key 或 image model 設定。目前僅顯示圖片生成 Prompt。
```

---

### 3.3 Image Generation Success

If image generation succeeds, the App should:

* Save the generated image under:

```text
outputs/images/
```

* Return the generated image path.
* Display the image in the Gradio UI.
* Still display the text prompt, negative prompt, materials, and safety notes.

Recommended output folder:

```text
outputs/
└── images/
```

Recommended filename format:

```text
turtle_tank_YYYYMMDD_HHMMSS.png
```

---

### 3.4 Image Generation Failure

If image generation fails, the App should:

* Not crash.
* Display a user-friendly error message.
* Keep showing the generated prompt.
* Keep showing the negative prompt, materials, and safety notes.

Example message:

```text
圖片生成失敗，可能是模型不支援圖片輸出、API 額度不足，或 OpenRouter 回應格式不同。目前保留 Prompt-only 結果。
```

---

## 4. New Module: `src/image_generator.py`

Add a new optional module:

```text
src/image_generator.py
```

Responsibilities:

* Check whether image generation is enabled.
* Check whether OpenRouter API settings are available.
* Call an OpenRouter image-capable model when configured.
* Parse generated image data if available.
* Save generated image files to `outputs/images/`.
* Return image path and status message.
* Gracefully fallback to prompt-only mode.

Suggested function:

```python
generate_tank_image(prompt: str) -> tuple[str | None, str]
```

Return format:

```python
(image_path, status_message)
```

Examples:

```python
(None, "圖片生成功能未啟用。目前僅顯示圖片生成 Prompt。")
```

or:

```python
("outputs/images/turtle_tank_20260623_153000.png", "圖片生成成功。")
```

---

## 5. OpenRouter Image Generation Implementation Notes

OpenRouter image generation support may depend on the selected model.

The implementation should be defensive:

* Do not assume every model supports image output.
* Do not assume the response format is identical across all providers.
* Prefer a small helper function to extract base64 image data from common response formats.
* If no image data is found, return a fallback message instead of crashing.
* Keep generated prompt visible even when image generation fails.

Possible request design:

```python
response = client.chat.completions.create(
    model=image_model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    modalities=["image", "text"],
)
```

Important:

* This is a planned optional extension.
* If the selected OpenRouter model requires a different parameter format, update only `src/image_generator.py`.
* The rest of the App should not depend on image provider details.

---

## 6. Gradio UI Update

Rename the third tab from:

```text
龜缸設計 Prompt 生成
```

to:

```text
龜缸設計與圖片生成
```

The tab must still work in prompt-only mode.

### Inputs

Keep the existing inputs:

```text
烏龜種類
水缸長度（cm）
水缸寬度（cm）
水缸高度（cm）
水深（cm）
想要的風格
必要元素
避免元素
```

Add one option:

```text
是否產生圖片
```

Options:

```text
否
是
```

Internal normalization:

```text
否 → false
是 → true
```

The UI should only attempt image generation when both conditions are true:

```text
IMAGE_GENERATION_ENABLED=true
```

and

```text
是否產生圖片 = 是
```

---

### Outputs

The third tab should output:

```text
英文圖片生成 Prompt
Negative Prompt
建議材料
安全提醒
圖片生成狀態
生成圖片（如果可用）
```

If no image is generated, the image output can remain empty.

---

## 7. Project Structure Update

Update the project structure:

```text
turtlecare-ai/
├── outputs/
│   └── images/
├── src/
│   ├── prompt_generator.py
│   └── image_generator.py
```

Full relevant structure:

```text
turtlecare-ai/
├── agent.md
├── app.py
├── requirements.txt
├── README.md
├── workflow_log.md
├── .env.example
├── data/
│   └── knowledge_base/
├── outputs/
│   └── images/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── rag.py
│   ├── llm_client.py
│   ├── turtle_profile.py
│   ├── risk_checker.py
│   ├── report_generator.py
│   ├── prompt_generator.py
│   └── image_generator.py
├── examples/
│   └── sample_cases.md
└── docs/
    └── project_outline.md
```

Add an empty `.gitkeep` file under `outputs/images/` if needed.

---

## 8. README Update Requirements

The README must explain:

1. OpenRouter is the primary backend for text generation.
2. Mock mode allows the full App to run without an API key.
3. OpenRouter image generation is optional.
4. The MVP works in prompt-only mode.
5. Image generation requires an OpenRouter image-capable model.
6. Image generation may fail depending on model availability, pricing, or provider response format.
7. The generated image is for visualization only, not an engineering blueprint or veterinary recommendation.

Suggested README section:

````markdown
## Optional Image Generation

The MVP always generates a diffusion-ready turtle tank design prompt.

Optionally, users can enable image generation through OpenRouter image-capable models. This allows the App to generate a turtle tank layout image from the generated prompt.

Image generation is disabled by default.

```env
IMAGE_GENERATION_ENABLED=false
OPENROUTER_IMAGE_MODEL=
OPENROUTER_IMAGE_SIZE=1024x1024
````

To enable image generation:

```env
IMAGE_GENERATION_ENABLED=true
OPENROUTER_IMAGE_MODEL=your-openrouter-image-model
OPENROUTER_IMAGE_SIZE=1024x1024
```

The App still works if image generation is disabled or unavailable. In that case, it shows the generated prompt only.

````

---

## 9. Workflow Log Update Requirements

The workflow log must mention this design decision:

```text
The project keeps OpenRouter as the unified API backend.
Text generation uses an OpenRouter text model.
Optional image generation uses an OpenRouter image-capable model.
The MVP remains prompt-only by default to ensure stable local demonstration.
````

Also record:

* Why image generation is optional.
* Why prompt-only mode is required.
* How the App handles missing image model configuration.
* How the App handles image generation failure.

---

## 10. Updated Assignment Mapping

Update the assignment mapping:

| Assignment Requirement       | TurtleCare AI Implementation                                                                         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| LLM                          | OpenRouter text model for Q&A and reports                                                            |
| RAG                          | Local Markdown turtle care knowledge base with TF-IDF retrieval                                      |
| Diffusion / Image Generation | Tank design prompt generator and optional OpenRouter image generation                                |
| Interactive App              | Gradio UI with Traditional Chinese labels                                                            |
| Agent workflow               | Codex Agent-assisted planning, implementation, debugging, and documentation                          |
| Demo                         | Prompt-only demo always works; image generation can be shown if OpenRouter image model is configured |

---

## 11. Updated Codex Agent Prompt

Use this prompt after updating `agent.md`.

```text
Read agent.md carefully and update the TurtleCare AI MVP.

Important finalized decisions:
1. Use OpenRouter as the primary text LLM backend through an OpenAI-compatible API.
2. Implement mock mode fallback so the full App works without an API key.
3. Use Traditional Chinese labels in the Gradio UI.
4. README.md and workflow_log.md must be written in English.
5. Generated answers should follow the user's input language.
6. RAG must use TF-IDF retrieval with Markdown heading/paragraph chunking.
7. Retrieval top-k must be 3.
8. Retrieved source filename and chunk preview must be displayed.
9. Add optional image generation through OpenRouter image-capable models.
10. Do not use a separate OpenAI image API key.
11. Image generation must be disabled by default.
12. The Tank Design tab must work in prompt-only mode even when image generation is unavailable.
13. Add src/image_generator.py.
14. Add outputs/images/ for generated images.
15. Update .env.example with IMAGE_GENERATION_ENABLED, OPENROUTER_IMAGE_MODEL, and OPENROUTER_IMAGE_SIZE.
16. Update README.md and workflow_log.md to document the optional image generation design.

Keep the implementation simple, modular, safety-aware, and runnable locally.
Do not make image generation required for the MVP.
```

---

## 12. Updated Validation Checklist

Before final submission, verify:

```text
[ ] The App starts with python app.py.
[ ] The Gradio UI uses Traditional Chinese labels.
[ ] README.md is written in English.
[ ] workflow_log.md is written in English.
[ ] OpenRouter text generation works when API key is configured.
[ ] Mock mode works when API key is missing.
[ ] RAG uses TF-IDF.
[ ] Retrieval top-k is 3.
[ ] Retrieved references show source filename and preview.
[ ] Tank Design tab generates an English image prompt.
[ ] Tank Design tab works when image generation is disabled.
[ ] IMAGE_GENERATION_ENABLED=false is the default.
[ ] Optional image generation uses OpenRouter settings.
[ ] No separate OpenAI image API key is required.
[ ] src/image_generator.py exists.
[ ] outputs/images/ exists.
[ ] Image generation failure does not crash the App.
[ ] Generated image is displayed if image generation succeeds.
[ ] Prompt-only result is displayed if image generation fails.
[ ] Health-related answers avoid veterinary diagnosis claims.
[ ] Demo cases still work without image generation.
```
