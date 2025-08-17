
# 🚀 AutoDevCore

**Modular AI agents that build smarter, score deeper.**
*The core of intelligent development.*

AutoDevCore is a local-first CLI platform that transforms prompts into scaffolded apps, tracks agent reasoning, scores each build against industry templates, and supports modular plugins—all offline.

## 🧭 Table of Contents
- [Features](#features)
- [Why It Matters](#why-it-matters)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Modes & Usage](#supported-modes--usage)
- [Architecture & Folder Structure](#architecture--folder-structure)
- [Developer Requirements](#developer-requirements)
- [Security & UX Considerations](#security--ux-considerations)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

| Feature | Description |
|--------|-------------|
| 🛠 AutoComposer | Transform ideas into app scaffolds (PRD, code, README) with modular agents |
| 🧠 OmniMind Tools | Journal or analyze codebases for tasks, improvement suggestions, and structure |
| 🧩 Plugin Loader | Drop-in `.py` agents to extend AutoDevCore (diagrams, code search, weather, etc.) |
| 📊 App Personality Scoring | Compare generated apps against enterprise-weighted templates and custom profiles |
| 🚨 Agent Thought Trail | JSON logging of agent steps; exportable as visual graph (Mermaid/D3.js) |
| 🔒 Offline-Only Operation | Runs with local gpt‑oss models via Ollama or vLLM—no tokens, no cloud |

## ✨ Why It Matters

AutoDevCore solves the gap between prototype and production by combining:
- Explainable generation — clearly shows how the AI made choices
- Enterprise-aligned scoring — gives clients the confidence to adopt AI-built scaffolds
- Extensibility and transparency — plugin-friendly and traceable reasoning
- Offline capability — perfect for secure, local, or air-gapped environments

## ⚙️ Installation

```bash
git clone https://github.com/<your-org>/AutoDevCore.git
cd AutoDevCore
pip install -r requirements.txt
```

Ensure your Ollama daemon or vLLM server is running before use.

## 🚀 Quick Start

Run the splash screen:
```bash
./autodevcore --help
```

To build an app:
```bash
./autodevcore --mode compose --idea "Build a contract management app with role-based access"
```

## 🧠 Modes & Commands

### Compose
```bash
./autodevcore --mode compose --idea "restaurant inventory manager"
```

### Journal
```bash
./autodevcore --mode journal
```

### Blueprint
```bash
./autodevcore --mode blueprint --path ./legacy_codebase
```

### Score
```bash
./autodevcore --mode score --template profiles/fintech.yaml
```

### Plugin
```bash
./autodevcore --mode plugin --name ascii_weather
```

## 🗂️ Architecture & Folder Layout

```plaintext
AutoDevCore/
├── agents/
├── modes/
├── profiles/
├── plugins/
├── logs/
├── output/
├── cli.py
├── splash.py
└── requirements.txt
```

## 🛠 Developer Requirements
- Python 3.11+
- Ollama or vLLM
- 16GB+ RAM
- Optional: Node.js or browser for Mermaid charts

## 🔐 Security & UX Considerations
- Sandbox plugin execution
- Optional AES encryption for logs
- CLI-native UI with splash banner and verbose toggle
- Logs and outputs remain local and self-contained

## 🤝 Contributing
Drop a `.py` file into `/plugins` with a `run(input_text)` function. Done!

## 📜 License
MIT — free to modify, extend, and distribute.
