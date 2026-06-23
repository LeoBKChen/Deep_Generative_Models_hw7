以下是 **TurtleCare AI** 的整體基底大綱文件，可直接放進 `docs/project_outline.md`，也可以作為後續交給 Codex Agent 的專案規劃依據。

# TurtleCare AI: RAG-based Turtle Keeping and Tank Design Assistant

## 1. Project Overview

**TurtleCare AI** is an interactive generative AI application designed to assist turtle keepers in evaluating turtle care environments, asking husbandry-related questions, and generating personalized tank improvement suggestions.

The system combines a **Retrieval-Augmented Generation, also known as RAG, pipeline** with a **Large Language Model, also known as LLM**, to provide more grounded and context-aware responses. The application retrieves relevant turtle care knowledge from a local Markdown knowledge base and uses the retrieved context, together with user-provided turtle profiles and tank conditions, to generate personalized care reports.

The project also includes a **tank design prompt generator**, which produces diffusion-ready prompts for visualizing turtle tank layouts. This allows the system to demonstrate both LLM-based reasoning and generative design support.

This project is developed under an **Agent-driven workflow**, where AI coding agents are used for ideation, architecture design, task decomposition, code generation, debugging, UI integration, and documentation.

---

## 2. Project Motivation

Many beginner turtle keepers face difficulties in setting up a safe and healthy environment for aquatic or semi-aquatic turtles. Common problems include insufficient basking areas, poor water quality, inappropriate water depth, lack of UVB lighting, unsuitable feeding habits, and risky mixed-species housing.

General online information is often scattered, inconsistent, or not personalized to the keeper's actual tank conditions. TurtleCare AI aims to provide a structured assistant that can:

* Collect turtle and tank information from the user.
* Retrieve relevant turtle care knowledge from a local knowledge base.
* Generate personalized care suggestions.
* Identify possible environmental risks.
* Produce a clear improvement checklist.
* Generate tank layout prompts for image generation models.

The system is not intended to replace veterinarians or professional reptile experts. Instead, it serves as a beginner-friendly care assistant and educational support tool.

---

## 3. Project Objectives

The main objectives of TurtleCare AI are:

1. Build an interactive generative AI App for turtle keeping assistance.
2. Demonstrate practical use of LLMs in a domain-specific assistant.
3. Implement a local RAG pipeline using a Markdown turtle care knowledge base.
4. Generate personalized turtle care and tank improvement reports.
5. Provide tank design prompts suitable for diffusion-based image generation.
6. Use an Agent-driven development process and document the workflow.
7. Produce a complete GitHub-ready project with source code, README, workflow log, and demo material.

---

## 4. Target Users

The target users are:

* Beginner turtle keepers.
* Pet owners setting up a turtle tank.
* Students learning generative AI application development.
* Users who want structured turtle care suggestions.
* Users who want tank setup design references.

---

## 5. Core Features

### 5.1 Turtle Care Q&A

The user can ask turtle care questions such as:

* How deep should the water be?
* Does my turtle need UVB light?
* What should I feed my turtle?
* Is it safe to keep two turtle species together?
* Why does my turtle refuse to eat?
* What should I check if my turtle floats abnormally?

The system retrieves relevant knowledge base chunks and generates an answer using an LLM.

---

### 5.2 Turtle and Tank Profile Input

The user can provide structured information, including:

* Turtle species
* Shell length
* Number of turtles
* Tank length, width, and height
* Water depth
* Basking platform availability
* UVB light availability
* Heating equipment
* Filtration method
* Feeding content
* Mixed-species housing condition
* Current problem or concern

This profile is used to personalize the generated response.

---

### 5.3 RAG-based Knowledge Retrieval

The system uses a local turtle care knowledge base stored as Markdown files.

The RAG process includes:

1. Load Markdown documents.
2. Split documents into smaller chunks.
3. Convert chunks into searchable representations.
4. Retrieve the most relevant chunks based on the user query.
5. Inject retrieved context into the LLM prompt.
6. Generate a grounded response.

The MVP version may use BM25 or TF-IDF keyword retrieval for simplicity. A more advanced version may use sentence-transformer embeddings and FAISS or Chroma.

---

### 5.4 Environment Diagnosis Report

The system generates a structured turtle tank diagnosis report.

The report should include:

* Current environment summary
* Positive aspects
* Potential risks
* Priority improvement items
* Suggested equipment
* Daily care checklist
* Weekly care checklist
* Safety warnings

Example risk categories:

* Water quality risk
* Basking area risk
* UVB and lighting risk
* Filtration risk
* Mixed-species housing risk
* Feeding imbalance risk
* Health warning risk

---

### 5.5 Tank Design Prompt Generator

The system generates a diffusion-ready prompt for turtle tank visualization.

The generated prompt may describe:

* Tank size
* Turtle species
* Water depth
* Basking platform
* Ramp design
* Filter placement
* UVB and heat lamp position
* Natural rocks or plants
* Safe resting areas
* Visual style

Example output:

```text
A realistic indoor aquatic turtle tank setup for a Taiwan stripe-necked turtle, 
large deep-water aquarium, stable dry basking platform with gentle ramp, 
UVB lamp above the basking area, external canister filter, clear water, 
safe resting rocks, natural aquatic plants, educational aquarium design, 
realistic lighting, clean and practical layout.
```

The MVP version generates only the prompt. An extended version may connect to a diffusion API or local image generation pipeline.

---

## 6. Core Generative AI Technologies

### 6.1 Large Language Model

The LLM is used for:

* Care question answering
* Report generation
* Risk explanation
* Personalized improvement suggestions
* Tank design prompt generation
* Natural language formatting

Possible LLM backends:

* OpenRouter API
* Ollama local model
* OpenAI-compatible API endpoint
* Big Pickle through OpenCode-compatible API
* Other compatible LLM provider

---

### 6.2 Retrieval-Augmented Generation

RAG is used to reduce hallucination and improve domain grounding.

Instead of relying only on the LLM's internal knowledge, the system retrieves relevant care information from a local curated knowledge base.

The retrieved context is included in the prompt so the answer is more consistent with the project knowledge base.

---

### 6.3 Diffusion / Image Generation Extension

The core MVP does not require direct image generation. However, the project includes a tank design prompt generator that prepares prompts for diffusion-based models.

Possible extension:

* Stable Diffusion
* ControlNet
* LoRA-enhanced image generation
* ComfyUI API
* Hugging Face Diffusers
* OpenRouter image model

This extension can be described as future work or implemented if time allows.

---

## 7. System Architecture

### 7.1 High-level Architecture

```text
User
  ↓
Gradio / Streamlit UI
  ↓
Input Parser
  ↓
Turtle Profile Builder
  ↓
RAG Retriever ───── Local Markdown Knowledge Base
  ↓
Risk Rule Checker
  ↓
LLM Prompt Builder
  ↓
LLM Backend
  ↓
Care Report / Q&A Answer / Tank Design Prompt
  ↓
UI Output
```

---

### 7.2 Module Responsibilities

#### UI Layer

Responsible for:

* Collecting user inputs
* Displaying generated answers
* Displaying care reports
* Displaying retrieved references
* Displaying tank design prompts

Recommended framework:

* Gradio for fast prototyping
* Streamlit as an alternative

---

#### RAG Layer

Responsible for:

* Loading knowledge base files
* Splitting documents into chunks
* Building retrieval index
* Searching relevant chunks
* Returning top-k references

Possible implementations:

* MVP: BM25 or TF-IDF
* Advanced: sentence-transformers + FAISS
* Advanced: Chroma vector database

---

#### Rule-based Diagnosis Layer

Responsible for simple deterministic risk checks.

Examples:

* If no basking area exists, mark basking risk as high.
* If no UVB light exists, mark lighting risk as medium or high.
* If mixed species are housed together, mark compatibility risk as medium or high.
* If water depth is high but no resting platform exists, mark drowning or fatigue risk as high.
* If filtration is weak, mark water quality risk as medium or high.

This layer helps the system generate more consistent reports.

---

#### LLM Generation Layer

Responsible for:

* Combining user profile, retrieved context, and risk results
* Creating final prompts
* Calling the LLM backend
* Returning structured natural language outputs

The LLM should be instructed to:

* Be practical and beginner-friendly.
* Avoid unsupported medical diagnosis.
* Provide clear priorities.
* Mention when veterinary help is needed.
* Separate facts, suggestions, and warnings.
* Avoid overconfident claims.

---

## 8. Knowledge Base Design

### 8.1 Recommended Folder Structure

```text
data/
└── knowledge_base/
    ├── turtle_species.md
    ├── tank_setup.md
    ├── water_quality.md
    ├── lighting_and_basking.md
    ├── feeding.md
    ├── common_health_issues.md
    ├── mixed_species_warning.md
    └── emergency_warning.md
```

---

### 8.2 Knowledge Base Topics

#### `turtle_species.md`

Contains general species notes, such as:

* Taiwan stripe-necked turtle
* Red-eared slider
* African side-necked turtle
* Musk turtle
* Map turtle

Each species section should include:

* General behavior
* Aquatic or semi-aquatic tendency
* Tank needs
* Diet notes
* Basking needs
* Compatibility notes
* Common risks

---

#### `tank_setup.md`

Contains information about:

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

#### `water_quality.md`

Contains information about:

* Filtration
* Partial water changes
* Dechlorination
* Ammonia
* Nitrite
* Nitrate
* Water temperature
* Cleaning after feeding

---

#### `lighting_and_basking.md`

Contains information about:

* UVB light
* UVA light
* Heat lamp
* Basking temperature
* Light distance
* Lighting schedule
* Bulb replacement

---

#### `feeding.md`

Contains information about:

* Juvenile turtle feeding
* Adult turtle feeding
* Commercial pellets
* Vegetables
* Animal protein
* Calcium
* Overfeeding risks

---

#### `common_health_issues.md`

Contains beginner-level warning signs, such as:

* Refusing food
* Swollen eyes
* Floating abnormally
* Shell softness
* Skin lesions
* Wounds
* Breathing difficulty

This document must clearly state that the system does not provide veterinary diagnosis.

---

#### `mixed_species_warning.md`

Contains information about:

* Mixed-species housing risks
* Size differences
* Feeding competition
* Biting
* Territorial stress
* Quarantine
* Separation plans

---

#### `emergency_warning.md`

Contains warning signs that require professional help, such as:

* Serious injury
* Long-term refusal to eat
* Abnormal floating or imbalance
* Noisy breathing
* Eyes unable to open
* Severe shell or skin infection
* Bleeding

---

## 9. Data Flow

### 9.1 Care Q&A Flow

```text
User question
  ↓
Query preprocessing
  ↓
Retrieve relevant knowledge chunks
  ↓
Build LLM prompt with retrieved context
  ↓
Generate answer
  ↓
Display answer and references
```

---

### 9.2 Environment Diagnosis Flow

```text
Structured turtle and tank profile
  ↓
Rule-based risk checker
  ↓
Retrieve related care knowledge
  ↓
Build diagnosis prompt
  ↓
Generate structured care report
  ↓
Display diagnosis report
```

---

### 9.3 Tank Design Prompt Flow

```text
Tank requirements and user preferences
  ↓
Retrieve tank setup knowledge
  ↓
Build design prompt request
  ↓
Generate diffusion-ready prompt
  ↓
Display prompt and material suggestions
```

---

## 10. Recommended Project Structure

```text
turtlecare-ai/
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

---

## 11. Suggested Python Modules

### `app.py`

Main entry point of the interactive App.

Responsibilities:

* Launch Gradio or Streamlit UI.
* Define tabs and input components.
* Connect UI inputs to backend functions.
* Display generated outputs.

---

### `src/config.py`

Responsibilities:

* Load environment variables.
* Store model settings.
* Store retrieval settings.
* Define default paths.

Example settings:

* LLM provider
* API base URL
* Model name
* Temperature
* Top-k retrieval count
* Knowledge base directory

---

### `src/rag.py`

Responsibilities:

* Load Markdown files.
* Split documents into chunks.
* Build retrieval index.
* Retrieve relevant chunks.
* Return retrieved text with source names.

MVP option:

* Use TF-IDF or BM25 retrieval.

Advanced option:

* Use sentence-transformers with FAISS.

---

### `src/llm_client.py`

Responsibilities:

* Provide a unified LLM call interface.
* Support OpenAI-compatible APIs.
* Handle API errors.
* Support fallback output when no API key is available.

---

### `src/turtle_profile.py`

Responsibilities:

* Convert UI inputs into a structured turtle profile.
* Normalize missing fields.
* Format the profile for prompts.

---

### `src/risk_checker.py`

Responsibilities:

* Apply deterministic risk rules.
* Return risk levels and explanations.
* Provide structured results to the report generator.

Example risks:

* No basking area
* No UVB light
* Mixed species
* Weak filtration
* Deep water without resting area
* Unbalanced feeding

---

### `src/report_generator.py`

Responsibilities:

* Build prompts for care reports.
* Combine user profile, retrieved context, and risk results.
* Call LLM client.
* Return formatted diagnosis report.

---

### `src/prompt_generator.py`

Responsibilities:

* Build prompts for turtle tank design.
* Generate diffusion-ready image prompts.
* Generate material suggestions.
* Return prompt in English for image generation models.

---

## 12. User Interface Design

The App should contain three main tabs.

---

### Tab 1: Turtle Care Q&A

Inputs:

* Turtle species
* Shell length
* User question

Outputs:

* Generated answer
* Retrieved knowledge references

Purpose:

* Provide RAG-based turtle care question answering.

---

### Tab 2: Tank Environment Diagnosis

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

Purpose:

* Generate personalized care and environment improvement recommendations.

---

### Tab 3: Tank Design Prompt Generator

Inputs:

* Turtle species
* Tank size
* Water depth
* Desired tank style
* Required elements
* Elements to avoid

Outputs:

* Diffusion-ready image prompt
* Negative prompt
* Suggested materials
* Safety notes

Purpose:

* Generate visual design prompts for turtle tank layout planning.

---

## 13. Prompt Design

### 13.1 General System Instruction

The LLM should follow these rules:

```text
You are TurtleCare AI, a turtle keeping assistant.
Use the provided context and user profile to generate practical, beginner-friendly advice.
Do not provide veterinary diagnosis.
For severe, persistent, or rapidly worsening symptoms, recommend consulting a reptile veterinarian.
Prioritize animal safety, water quality, basking access, UVB lighting, and species compatibility.
If information is missing, state assumptions clearly.
Provide structured recommendations and actionable next steps.
```

---

### 13.2 RAG Q&A Prompt Template

```text
System:
You are TurtleCare AI, a turtle keeping assistant.

Retrieved knowledge:
{retrieved_context}

User turtle profile:
{turtle_profile}

User question:
{question}

Task:
Answer the user's question using the retrieved knowledge and profile.
Give practical advice.
Mention uncertainty when needed.
Do not provide veterinary diagnosis.
If the question involves health symptoms, include a safety warning when appropriate.
```

---

### 13.3 Environment Diagnosis Prompt Template

```text
System:
You are TurtleCare AI, a turtle keeping assistant.

Retrieved knowledge:
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

### 13.4 Tank Design Prompt Template

```text
System:
You are TurtleCare AI, a turtle tank design assistant.

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

The design must prioritize turtle safety, stable basking access, clean water, and realistic tank layout.
```

---

## 14. Risk Checking Rules

The MVP should include simple rule-based checks.

Example rules:

```text
If basking_area == false:
    risk = high
    message = "A completely dry basking area is required for aquatic and semi-aquatic turtles."

If uvb_light == false:
    risk = medium_to_high
    message = "UVB lighting is important for calcium metabolism and shell health."

If mixed_species == true:
    risk = medium_to_high
    message = "Mixed-species housing can cause stress, biting, competition, and injury."

If filtration_method is weak or missing:
    risk = medium
    message = "Turtles produce heavy waste, so stronger filtration and regular water changes are recommended."

If water_depth is high and no resting area exists:
    risk = high
    message = "Deep water should include accessible ramps or resting areas so the turtle can reach the surface safely."
```

The rule-based output should not replace LLM reasoning. It should provide stable signals for the final report.

---

## 15. Minimum Viable Product

The MVP should include:

* Gradio or Streamlit UI
* Turtle care Q&A tab
* Tank environment diagnosis tab
* Tank design prompt generator tab
* Local Markdown knowledge base
* Basic RAG retriever
* LLM backend through OpenAI-compatible API or local Ollama
* Rule-based risk checker
* `README.md`
* `workflow_log.md`
* Demo screenshot or video

The MVP does not need:

* Real-time image generation
* Full user account system
* Database login system
* Mobile app deployment
* Real veterinary diagnosis
* Large-scale web scraping

---

## 16. Possible Extensions

If time allows, the following features can be added:

1. Direct image generation through Stable Diffusion or another image model.
2. Turtle or tank image upload with vision model analysis.
3. FAISS vector retrieval with sentence-transformers.
4. Persistent care history with SQLite.
5. Export care report as Markdown or PDF.
6. Multi-language support for English and Traditional Chinese.
7. Species-specific care profiles.
8. More detailed water quality tracking.
9. Feeding schedule generator.
10. Weekly turtle care report generation.

---

## 17. Safety and Limitation Statement

TurtleCare AI is an educational and husbandry support tool. It does not provide veterinary diagnosis, medical treatment, or emergency care.

For severe, persistent, or rapidly worsening symptoms, users should consult a qualified reptile veterinarian.

The system may produce incomplete or imperfect suggestions. The generated tank design prompt is intended for visualization and planning support only, not as a precise engineering or veterinary standard.

---

## 18. Assignment Requirement Mapping

| Assignment Requirement            | TurtleCare AI Implementation                                            |
| --------------------------------- | ----------------------------------------------------------------------- |
| Generative AI App                 | Interactive turtle care assistant                                       |
| LLM usage                         | Personalized care reports, Q&A, design prompt generation                |
| RAG architecture                  | Local Markdown turtle care knowledge base retrieval                     |
| Diffusion / Flow Matching support | Tank design prompt generator, optional image generation                 |
| Agent-driven workflow             | Codex Agent used for planning, implementation, debugging, documentation |
| Interactive UI                    | Gradio or Streamlit App                                                 |
| Source code                       | GitHub repository                                                       |
| Dependency file                   | `requirements.txt`                                                      |
| README                            | Project overview, architecture, setup, execution                        |
| Workflow log                      | Key prompts, tools, debugging records                                   |
| Demo material                     | Screenshot or video of running App                                      |

---

## 19. Recommended Development Phases

### Phase 1: Project Planning

Tasks:

* Confirm project title.
* Confirm MVP scope.
* Define target users.
* Define required features.
* Create this project outline.

Expected output:

* `docs/project_outline.md`

---

### Phase 2: Architecture and Task Decomposition

Tasks:

* Design folder structure.
* Define modules.
* Define UI tabs.
* Define RAG pipeline.
* Define LLM prompt templates.
* Define risk checking rules.

Expected output:

* `agent.md`
* `docs/architecture.md`
* Task checklist

---

### Phase 3: Knowledge Base Construction

Tasks:

* Create Markdown knowledge base files.
* Draft concise turtle care content.
* Review health-related safety wording.
* Prepare sample user cases.

Expected output:

* `data/knowledge_base/*.md`
* `examples/sample_cases.md`

---

### Phase 4: Core Implementation

Tasks:

* Implement RAG retriever.
* Implement LLM client.
* Implement turtle profile formatter.
* Implement risk checker.
* Implement report generator.
* Implement tank design prompt generator.

Expected output:

* `src/*.py`

---

### Phase 5: UI Implementation

Tasks:

* Build Gradio or Streamlit interface.
* Create Q&A tab.
* Create environment diagnosis tab.
* Create tank design prompt tab.
* Connect UI to backend modules.

Expected output:

* `app.py`

---

### Phase 6: Testing and Debugging

Tasks:

* Test App startup.
* Test Q&A retrieval.
* Test report generation.
* Test missing API key behavior.
* Test sample cases.
* Fix runtime errors.

Expected output:

* Working local App
* Debug records in `workflow_log.md`

---

### Phase 7: Documentation and Submission

Tasks:

* Write `README.md`.
* Write `workflow_log.md`.
* Prepare demo screenshot or video.
* Upload to GitHub.
* Create `<StudentID>_HW7.txt`.
* Prepare `<StudentID>_HW7.<ext>` demo file.

Expected output:

* Final GitHub repository
* Submission TXT file
* Demo material

---

## 20. Suggested First Prompt for Codex Agent

```text
Read docs/project_outline.md and help me implement the TurtleCare AI project.

First, create the project folder structure and generate the initial files:
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

Use Gradio for the UI.
Use a simple local Markdown RAG retriever for the MVP.
Use an OpenAI-compatible LLM API interface, but include a fallback mock response mode when no API key is provided.
Keep the implementation simple, modular, and runnable locally.
```

---

## 21. Final Project Summary

TurtleCare AI is a RAG-based turtle keeping and tank design assistant. It helps users evaluate turtle care conditions, ask turtle husbandry questions, and generate tank improvement suggestions. The system uses a local turtle care knowledge base, rule-based risk checking, and LLM-based generation to produce personalized care reports. It also generates diffusion-ready tank design prompts for visual planning.

The project satisfies the assignment requirements by integrating LLMs, RAG, generative prompt design, an interactive UI, and a documented Agent-driven development workflow.
