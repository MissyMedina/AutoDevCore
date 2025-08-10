
# Product Requirements Document (PRD): AutoDevCore

## 1. Purpose
AutoDevCore is a portable, local-first developer platform powered by modular AI agents. It enables users to generate entire applications from a prompt, analyze and summarize codebases, and evaluate applications against industry-specific scoring templates. Designed for enterprise developers, consultants, and teams working in offline or secure environments, AutoDevCore empowers users with explainable, customizable, and extensible agent-based development.

## 2. Background
Developers, especially in regulated or air-gapped environments, often lack the benefits of AI-assisted automation. Most solutions are cloud-based, have limited explainability, or don't provide industry-specific performance evaluations. AutoDevCore addresses this with modular, transparent, offline-capable AI tooling.

## 3. Assumptions
- Users are familiar with CLI tools and Python.
- Ollama or vLLM is pre-installed for local model support.
- Most enterprise users will value explainability and compliance over speed.

## 4. Requirements

### Functional Requirements
- Convert prompt into scaffolded project folder
- Generate PRD, README, and core codebase
- Log agent steps in structured JSON format
- Summarize developer thoughts and notes
- Analyze legacy codebases (blueprint mode)
- Score projects using industry templates (App Personality Scoring)
- Support plugin architecture for custom tools

### Non-functional Requirements
- Fully offline capable
- Lightweight and portable (Mac/Linux)
- Runs on CPU/GPU with local model serving

### UI/UX Requirements
- ASCII splash banner branding
- Verbose output stream of agent thoughts (toggle)
- Radar chart and logs in output folder

### Security Requirements
- Sandbox plugin execution
- Optional AES encryption for logs
- No network communication

## 5. Success Metrics
- Can generate and score an app from prompt in < 2 minutes
- Runs completely offline on standard MacBook Pro M1/M2
- Plug-and-play plugins execute without error
- Thought trail renders without manual correction

## 6. User Stories
- As a developer, I want to describe my idea in one sentence and get a fully scaffolded project I can start coding.
- As a consultant, I want to evaluate the maturity of an app using an enterprise scoring rubric.
- As an enterprise PM, I want to see how an AI agent made a development decision in a visual diagram.

## 7. Stakeholders
- AI Developers
- Enterprise Security Architects
- DevOps Engineers
- Freelancers and PMs

## 8. Timeline (Hackathon Sprint)
- Week 1: CLI & Agent system scaffold
- Week 2: Compose + Thought Trail complete
- Week 3: App Scoring & Plugin Framework
- Week 4: Final UX polish + diagrams + README

## 9. Open Questions
- Will encryption be a feature in MVP or backlog?
- Should we visualize the scoring using a UI or rely on exports only?
