# Contributing to AutoDevCore 🚀

Thank you for your interest in contributing to AutoDevCore! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 🐛 Reporting Bugs
- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Provide environment information
- Check existing issues first

### 💡 Suggesting Features
- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Describe the problem and proposed solution
- Include use cases and impact assessment
- Check existing feature requests first

### ❓ Asking Questions
- Use the [Question template](.github/ISSUE_TEMPLATE/question.md)
- Search existing issues and discussions first
- Provide clear context and what you've tried

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request

## 🛠 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Ollama (for GPT-OSS models)

### Local Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AutoDevCore.git
cd AutoDevCore

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Pull GPT-OSS model
ollama pull gpt-oss:20b
```

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use Flake8 for linting
- Add type hints where appropriate

```bash
# Format code
black .

# Check linting
flake8 .

# Run tests
pytest
```

## 🏗️ Project Structure

```
AutoDevCore/
├── agents/              # AI Agent modules
├── modes/               # CLI operation modes
├── integrations/        # External integrations
├── plugins/             # Custom plugins
├── profiles/            # Scoring templates
├── cli.py              # Main CLI entry point
└── requirements.txt    # Python dependencies
```

## 🔌 Plugin Development

### Creating a Plugin
1. Create a new Python file in `plugins/`
2. Implement a `run(context=None)` function
3. Return a dictionary with results
4. Add documentation and tests

### Plugin Template
```python
def run(context=None):
    """
    Plugin description.

    Args:
        context: Optional context data

    Returns:
        dict: Plugin results
    """
    try:
        # Your plugin logic here
        result = "Plugin executed successfully"

        return {
            "status": "success",
            "message": result,
            "data": {"timestamp": "2024-01-01"}
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": {}
        }
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_compose.py

# Run with coverage
pytest --cov=agents --cov=modes

# Run integration tests
pytest tests/integration/
```

### Writing Tests
- Use pytest framework
- Test both success and error cases
- Mock external dependencies
- Test with and without GPT-OSS models

## 📝 Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google docstring format
- Include examples where helpful

### README Updates
- Update README.md for new features
- Add usage examples
- Update installation instructions
- Include breaking changes

## 🔒 Security

### Guidelines
- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Validate all user inputs
- Follow secure coding practices

### Reporting Security Issues
- Email security issues to maintainers
- Don't create public issues for security problems
- Provide detailed information about the vulnerability

## 🚀 Release Process

### Versioning
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version in code and documentation
- Create release notes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Release notes written
- [ ] GitHub release created

## 📊 Performance Guidelines

### Code Performance
- Optimize for readability first
- Profile code for bottlenecks
- Consider memory usage
- Test with large datasets

### GPT-OSS Integration
- Handle timeouts gracefully
- Implement fallback mechanisms
- Optimize prompt engineering
- Cache results when appropriate

## 🤝 Community Guidelines

### Communication
- Be respectful and inclusive
- Use clear and constructive language
- Help others learn and grow
- Follow the project's code of conduct

### Code Review
- Review code thoroughly
- Provide constructive feedback
- Test changes locally
- Approve only when satisfied

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/MissyMedina/AutoDevCore/issues)
- **Discussions**: [GitHub Discussions](https://github.com/MissyMedina/AutoDevCore/discussions)
- **Documentation**: [Wiki](https://github.com/MissyMedina/AutoDevCore/wiki)

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to AutoDevCore! 🚀
