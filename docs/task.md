HomeworkaFinal : Agent-Driven Integration Project
I. Assignment Overview
This assignment serves as the capstone project for the "Deep Generative Models" course, evaluating students' comprehensive understanding of Large Language Models (LLMs) and Diffusion Models or Flow Matching technologies. The project must rely heavily on AI Agents and code generation tools, covering the full development lifecycle from ideation and system architecture design to task decomposition and code implementation. The final deliverable must be a fully functional generative AI application (App) with an interactive user interface.

II. Core Technical Requirements
The project must incorporate concrete applications of the following technologies (incorporating at least one is required; combining both is highly encouraged):

Large Language Models (LLMs): May include Prompt Engineering, RAG architectures, API integrations, or local open-weights model inference.

Diffusion / Flow Matching Models: Covering image, audio, or 3D generation. May include ControlNet, LoRA weight integration, customized pipelines, or inference acceleration.

III. Tools and Resources
To support the Agentic Workflow and model inference, the following tools and computing resources are recommended or permitted:

Ollama: A local inference framework used to rapidly deploy and run quantized open-weights LLMs (e.g., GGUF format). It provides an OpenAI-compatible REST API, suitable for offline development verification and edge-computing integration.

NVIDIA NIM (NVIDIA Inference Microservices): A containerized microservice inference platform. It includes optimized inference engines like TensorRT-LLM and supports standard API integration, ideal for environments requiring maximum utilization of enterprise-grade GPU memory bandwidth and compute power.

OpenRouter: A model API aggregation service. It provides a single endpoint to access models from various providers (e.g., Anthropic, OpenAI) and the open-source community, facilitating seamless model switching and Context Window management during development.

Big Pickle: An experimental, free large language model endpoint provided by the OpenCode platform (underlying model: Zhipu AI GLM-4.6, MoE architecture, 355B total / 32B active parameters). Featuring a 200k Context Window and an OpenAI-compatible API (Model ID: opencode/big-pickle), it is specifically optimized for code generation tasks and driving programming agents.

Agent / CLI Tools: Including claude-cli, codex-cli, antigravity-cli, open-code, etc. Students can use these command-line tools to interact with the inference backends mentioned above, automating code generation and project scaffolding directly via the terminal.

 
IV. Project Execution Steps (Agent Workflow)
Please follow this Agent-assisted development process and thoroughly document your interaction and generation history:

Phase 1: Ideation and Planning Provide the Agent with initial context to generate project proposals. Define the project objective, core features, and the intended technology stack.

Phase 2: Architecture Design and Task Decomposition Utilize the Agent to break down the selected proposal into actionable implementation tasks. Define the system architecture, frontend-backend integration methods, and API data exchange formats.

Phase 3: Code Generation and Implementation Use CLI tools or IDE-based Agents to implement the core logic. The developer must assume the role of an architect, providing precise context (e.g., specific framework versions or environment dependencies) to guide the Agent in writing training, fine-tuning, or inference scripts, and managing the debugging process.

Phase 4: Interface Encapsulation and Finalization Instruct the Agent to rapidly generate a UI using Gradio, Streamlit, or frontend frameworks. Integrate the model inference backend into an interactive App, and use the Agent to assist in drafting the technical documentation.

V. Deliverables
Source Code (GitHub Repository): Must include the complete source code and a dependency environment list (requirements.txt or environment.yml).

Project Documentation (README.md): Must include the project title, system architecture overview, and detailed instructions for local execution.

Agent Collaboration Log (Workflow Log): An independent Markdown file documenting the development process. It must detail the key prompts used, the combinations of tools applied, and the specific technical bottlenecks resolved with the Agent's assistance.

Demonstration Materials: A short video recording of the App in operation or key screenshots verifying that the system successfully runs.

Submission Requirements:
Please submit the following two files:

Please provide a public GitHub repository link. The repository must include the source code, README.md, and Workflow Log. Paste the link into a TXT file and name the file <StudentID>_HW7.txt.
(If it is inconvenient to make the GitHub repository public, you may alternatively use Google Drive sharing. Please make sure the sharing setting is set to “Anyone with the link”.)

Demonstration Materials, named as: <StudentID>_HW7.<ext> (e.g., 314832001_HW7.mp4, 314832001_HW7.png)
