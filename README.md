# AutoDevCore 🚀

> **Modular AI agents that build smarter, score deeper**

AutoDevCore is a portable, local-first developer platform powered by modular AI agents. It enables users to generate entire applications from a prompt, analyze and summarize codebases, and evaluate applications against industry-specific scoring templates.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GPT-OSS](https://img.shields.io/badge/GPT--OSS-20B-orange.svg)](https://github.com/openai/gpt-oss)

## 🌟 Features

### 🤖 **AutoComposer**
- Generate complete applications from natural language descriptions
- Intelligent tech stack selection (Python/FastAPI, Node.js/Express)
- Comprehensive project scaffolding with PRD, README, and codebase

### 🧠 **OmniMind Tools**
- **Journal Mode**: Analyze codebases and generate insights
- **Blueprint Mode**: Create architecture diagrams from existing code
- **Score Mode**: Evaluate applications against industry templates
- **Plugin Mode**: Extensible plugin system for custom functionality

### 📊 **App Personality Scoring**
- Industry-specific evaluation templates (FinTech, Healthcare, etc.)
- Radar charts and detailed scoring reports
- Customizable scoring criteria and weights

### 🔍 **Agent Thought Trail**
- JSON logging of all agent reasoning steps
- Exportable as visual graphs (Mermaid/D3.js)
- Transparent AI decision-making process

### 🔌 **Plugin Loader**
- Sandboxed plugin execution
- Easy plugin development and distribution
- Built-in plugin discovery and management

### 🛡️ **Offline-Only Operation**
- Complete local execution with GPT-OSS models
- No cloud dependencies or data transmission
- Secure, air-gapped environment support

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** (for local GPT-OSS models)
3. **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/MissyMedina/AutoDevCore.git
cd AutoDevCore

# Install dependencies
pip install -r requirements.txt

# Install and start Ollama
# Visit https://ollama.ai for installation instructions

# Pull GPT-OSS model
ollama pull gpt-oss:20b
```

### Basic Usage

```bash
# Generate a complete application
python cli.py --mode compose --idea "task management app" --output-dir ./myapp

# Analyze an existing codebase
python cli.py --mode blueprint --path ./legacy_codebase --output-dir ./analysis

# Score an application
python cli.py --mode score --app-dir ./myapp --template fintech

# Run a custom plugin
python cli.py --mode plugin --name ascii_weather
```

## 📖 Supported Modes

### 🎯 **Compose Mode**
Generate complete applications from ideas:
```bash
python cli.py --mode compose --idea "restaurant inventory manager" --output-dir ./inventory-app
```

**Outputs:**
- Complete application scaffold
- Product Requirements Document (PRD)
- Comprehensive README
- Thought trail and architecture diagrams

### 📝 **Journal Mode**
Analyze codebases and generate insights:
```bash
python cli.py --mode journal --path ./my-codebase --output-dir ./analysis
```

### 🏗️ **Blueprint Mode**
Create architecture diagrams from code:
```bash
python cli.py --mode blueprint --path ./legacy-system --output-dir ./blueprints
```

### 📊 **Score Mode**
Evaluate applications against industry templates:
```bash
python cli.py --mode score --app-dir ./myapp --template fintech
```

### 🔌 **Plugin Mode**
Execute custom plugins:
```bash
python cli.py --mode plugin --name my_custom_plugin
```

## 🏗️ Architecture

```
AutoDevCore/
├── cli.py                 # Main CLI entry point
├── splash.py              # ASCII art and help display
├── agents/                # AI Agent modules
│   ├── composer.py        # App idea analysis and planning
│   ├── prd_writer.py      # PRD generation
│   ├── code_generator.py  # Codebase generation
│   └── readme_writer.py   # README generation
├── modes/                 # Operation modes
│   ├── base.py           # Base mode functionality
│   ├── compose.py        # Application composition
│   ├── journal.py        # Codebase analysis
│   ├── blueprint.py      # Architecture diagrams
│   ├── score.py          # Application scoring
│   └── plugin.py         # Plugin execution
├── integrations/          # External integrations
│   └── gpt_oss.py        # GPT-OSS model integration
├── plugins/               # Custom plugins
├── profiles/              # Scoring templates
└── requirements.txt       # Python dependencies
```

## 🤖 GPT-OSS Integration

AutoDevCore leverages OpenAI's GPT-OSS models for intelligent reasoning:

- **Local Execution**: Runs completely offline via Ollama
- **Harmony Format**: Native tool calling and structured reasoning
- **Fallback System**: Graceful degradation when models are unavailable
- **Optimized Performance**: Configurable parameters for speed vs. quality

### Model Requirements

- **Recommended**: `gpt-oss:20b` (13GB, balanced performance)
- **Alternative**: `gpt-oss:120b` (larger, higher quality)
- **Hardware**: 16GB+ RAM, modern CPU/GPU

## 🔌 Plugin Development

Create custom plugins by adding Python files to the `plugins/` directory:

```python
# plugins/my_plugin.py
def run(context=None):
    """Plugin entry point."""
    return {
        "status": "success",
        "message": "Hello from my plugin!",
        "data": {"timestamp": "2024-01-01"}
    }
```

## 📊 Scoring Templates

AutoDevCore includes industry-specific scoring templates:

- **FinTech**: Security, compliance, performance, scalability
- **Healthcare**: HIPAA compliance, data integrity, audit trails
- **E-commerce**: User experience, payment processing, inventory
- **Custom**: Create your own templates in YAML format

## 🛡️ Security

- **Sandboxed Execution**: Plugins run in isolated environments
- **No Network Access**: Completely offline operation
- **Optional Encryption**: AES encryption for sensitive logs
- **Audit Trails**: Complete logging of all operations

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Test specific mode
python cli.py --mode compose --idea "test app" --verbose

# Test plugin system
python cli.py --mode plugin --name ascii_weather
```

## 📈 Performance

- **Application Generation**: < 2 minutes (with GPT-OSS)
- **Code Analysis**: < 30 seconds per 1000 lines
- **Scoring**: < 10 seconds per application
- **Memory Usage**: < 2GB RAM (excluding model)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/MissyMedina/AutoDevCore.git
cd AutoDevCore
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run code formatting
black .
flake8 .

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI GPT-OSS](https://github.com/openai/gpt-oss) for the powerful local AI models
- [Ollama](https://ollama.ai) for local model serving
- The open-source community for inspiration and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/MissyMedina/AutoDevCore/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MissyMedina/AutoDevCore/discussions)
- **Documentation**: [Wiki](https://github.com/MissyMedina/AutoDevCore/wiki)

---

**AutoDevCore** - The core of intelligent development 🚀
