# 🖥️ AutoDevCore CLI Help Documentation

**Complete guide to AutoDevCore's command-line interface and automation capabilities**

AutoDevCore provides a powerful command-line interface for automated development, project generation, and system management. This guide covers all CLI features and usage patterns.

## 🚀 **Quick Start**

### **Basic Usage**
```bash
# Generate an application from an idea
python cli.py --mode compose --idea "AI-powered task manager"

# Analyze a codebase
python cli.py --mode journal --path ./my-project

# Score an application
python cli.py --mode score --path ./my-app

# Use a plugin
python cli.py --mode plugin --name security-scanner
```

### **Help and Information**
```bash
# Show general help
python cli.py --help

# Show mode-specific help
python cli.py --mode compose --help
python cli.py --mode journal --help
python cli.py --mode score --help
python cli.py --mode plugin --help
```

---

## 🎯 **Available Modes**

### **1. Compose Mode**
**Purpose**: Generate complete applications from natural language descriptions

#### **Basic Usage**
```bash
python cli.py --mode compose --idea "AI-powered task manager"
```

#### **Advanced Options**
```bash
# Generate with specific template
python cli.py --mode compose --idea "E-commerce platform" --template ecommerce

# Generate with specific AI provider
python cli.py --mode compose --idea "FinTech application" --provider anthropic

# Generate with verbose output
python cli.py --mode compose --idea "Mobile app" --verbose

# Generate with custom configuration
python cli.py --mode compose --idea "API service" --config custom_config.json
```

#### **Available Templates**
- `web-app`: Full-stack web application
- `mobile-app`: Cross-platform mobile application
- `api-service`: RESTful API service
- `data-analytics`: Data processing and visualization
- `ecommerce`: E-commerce platform
- `saas`: Software-as-a-Service application

#### **Example Commands**
```bash
# Generate a web application
python cli.py --mode compose --idea "Project management tool with user authentication" --template web-app

# Generate a mobile app
python cli.py --mode compose --idea "Fitness tracking app with social features" --template mobile-app

# Generate an API service
python cli.py --mode compose --idea "Payment processing API with Stripe integration" --template api-service

# Generate with specific AI provider
python cli.py --mode compose --idea "AI-powered chatbot" --provider openai --verbose
```

### **2. Journal Mode**
**Purpose**: Analyze codebases and generate comprehensive insights

#### **Basic Usage**
```bash
python cli.py --mode journal --path ./my-project
```

#### **Advanced Options**
```bash
# Analyze with specific output format
python cli.py --mode journal --path ./my-project --format json

# Analyze with custom output file
python cli.py --mode journal --path ./my-project --output analysis_report.md

# Analyze with specific analysis depth
python cli.py --mode journal --path ./my-project --depth detailed

# Analyze with AI insights
python cli.py --mode journal --path ./my-project --ai-insights
```

#### **Output Formats**
- `markdown`: Human-readable markdown report
- `json`: Machine-readable JSON format
- `html`: Interactive HTML report
- `pdf`: PDF report (requires additional dependencies)

#### **Analysis Types**
- `basic`: Basic code structure analysis
- `detailed`: Comprehensive code analysis
- `security`: Security-focused analysis
- `performance`: Performance optimization analysis
- `ai-enhanced`: AI-powered code insights

#### **Example Commands**
```bash
# Basic code analysis
python cli.py --mode journal --path ./my-project --output basic_analysis.md

# Detailed analysis with AI insights
python cli.py --mode journal --path ./my-project --depth detailed --ai-insights --output detailed_report.html

# Security analysis
python cli.py --mode journal --path ./my-project --analysis-type security --output security_report.md

# Performance analysis
python cli.py --mode journal --path ./my-project --analysis-type performance --output performance_report.md
```

### **3. Blueprint Mode**
**Purpose**: Create project blueprints and architecture designs

#### **Basic Usage**
```bash
python cli.py --mode blueprint --idea "Microservices architecture for e-commerce"
```

#### **Advanced Options**
```bash
# Create blueprint with specific complexity
python cli.py --mode blueprint --idea "Distributed system" --complexity enterprise

# Create blueprint with custom output
python cli.py --mode blueprint --idea "Cloud-native application" --output architecture.json

# Create blueprint with specific technology stack
python cli.py --mode blueprint --idea "Real-time application" --tech-stack nodejs,redis,websockets
```

#### **Complexity Levels**
- `simple`: Basic architecture for small projects
- `medium`: Standard architecture for typical applications
- `complex`: Advanced architecture for large systems
- `enterprise`: Enterprise-grade architecture with scalability

#### **Example Commands**
```bash
# Simple web application blueprint
python cli.py --mode blueprint --idea "Blog platform" --complexity simple --output blog_blueprint.md

# Enterprise microservices blueprint
python cli.py --mode blueprint --idea "Banking system" --complexity enterprise --output banking_blueprint.json

# Cloud-native blueprint
python cli.py --mode blueprint --idea "IoT platform" --tech-stack kubernetes,docker,mqtt --output iot_blueprint.md
```

### **4. Score Mode**
**Purpose**: Evaluate applications against industry standards and best practices

#### **Basic Usage**
```bash
python cli.py --mode score --path ./my-app
```

#### **Advanced Options**
```bash
# Score against specific template
python cli.py --mode score --path ./my-app --template saas

# Score with custom criteria
python cli.py --mode score --path ./my-app --criteria security,performance,accessibility

# Score with detailed report
python cli.py --mode score --path ./my-app --detailed --output score_report.md

# Score with AI analysis
python cli.py --mode score --path ./my-app --ai-analysis
```

#### **Scoring Templates**
- `web-app`: Web application standards
- `mobile-app`: Mobile application standards
- `api-service`: API service standards
- `saas`: SaaS application standards
- `enterprise`: Enterprise application standards

#### **Scoring Criteria**
- `security`: Security best practices and vulnerabilities
- `performance`: Performance optimization and efficiency
- `accessibility`: Accessibility standards and compliance
- `maintainability`: Code maintainability and structure
- `scalability`: Scalability and architecture quality
- `documentation`: Documentation quality and completeness

#### **Example Commands**
```bash
# Basic scoring
python cli.py --mode score --path ./my-app --output score_report.md

# Detailed scoring with AI analysis
python cli.py --mode score --path ./my-app --detailed --ai-analysis --output detailed_score.html

# Security-focused scoring
python cli.py --mode score --path ./my-app --criteria security --output security_score.md

# Enterprise scoring
python cli.py --mode score --path ./my-app --template enterprise --detailed --output enterprise_score.json
```

### **5. Plugin Mode**
**Purpose**: Manage and execute custom plugins and extensions

#### **Basic Usage**
```bash
python cli.py --mode plugin --name security-scanner
```

#### **Advanced Options**
```bash
# List available plugins
python cli.py --mode plugin --list

# Install a plugin
python cli.py --mode plugin --install security-scanner

# Execute plugin with parameters
python cli.py --mode plugin --name security-scanner --params '{"target": "./my-app"}'

# Update a plugin
python cli.py --mode plugin --update security-scanner

# Remove a plugin
python cli.py --mode plugin --remove security-scanner
```

#### **Available Plugins**
- `security-scanner`: Automated security vulnerability scanning
- `performance-analyzer`: Performance analysis and optimization
- `code-formatter`: Code formatting and style enforcement
- `dependency-checker`: Dependency analysis and updates
- `test-generator`: Automated test case generation

#### **Example Commands**
```bash
# List all plugins
python cli.py --mode plugin --list

# Install security scanner
python cli.py --mode plugin --install security-scanner

# Run security scan
python cli.py --mode plugin --name security-scanner --params '{"target": "./my-app", "level": "detailed"}'

# Update all plugins
python cli.py --mode plugin --update-all
```

---

## 🔧 **Configuration Options**

### **Global Configuration**
```bash
# Set configuration file
python cli.py --config /path/to/config.json

# Set log level
python cli.py --log-level DEBUG

# Set output directory
python cli.py --output-dir /path/to/output

# Enable verbose mode
python cli.py --verbose
```

### **AI Provider Configuration**
```bash
# Use specific AI provider
python cli.py --provider openai

# Use local AI only
python cli.py --local-only

# Set AI model
python cli.py --model gpt-4

# Set AI temperature
python cli.py --temperature 0.7
```

### **Output Configuration**
```bash
# Set output format
python cli.py --format json

# Set output file
python cli.py --output report.md

# Enable detailed output
python cli.py --detailed

# Enable progress tracking
python cli.py --progress
```

---

## 📊 **Output Formats**

### **Markdown Output**
```markdown
# Project Analysis Report

## Overview
- **Project Name**: My Application
- **Analysis Date**: 2024-01-15
- **Total Files**: 150
- **Lines of Code**: 5,234

## Code Quality
- **Overall Score**: 85/100
- **Maintainability**: Good
- **Performance**: Excellent
- **Security**: Good

## Recommendations
1. Add more comprehensive error handling
2. Implement input validation
3. Add unit tests for critical functions
```

### **JSON Output**
```json
{
  "project_name": "My Application",
  "analysis_date": "2024-01-15",
  "metrics": {
    "total_files": 150,
    "lines_of_code": 5234,
    "overall_score": 85,
    "maintainability": "good",
    "performance": "excellent",
    "security": "good"
  },
  "recommendations": [
    "Add more comprehensive error handling",
    "Implement input validation",
    "Add unit tests for critical functions"
  ]
}
```

### **HTML Output**
Interactive HTML reports with:
- **Charts and Graphs**: Visual representation of metrics
- **Interactive Elements**: Expandable sections and filters
- **Navigation**: Table of contents and search functionality
- **Export Options**: Download reports in various formats

---

## 🤖 **AI Integration**

### **AI Provider Selection**
```bash
# Use OpenAI
python cli.py --provider openai --model gpt-4

# Use Anthropic
python cli.py --provider anthropic --model claude-3-sonnet

# Use local GPT-OSS
python cli.py --provider gpt-oss --model gpt-oss:20b

# Use automatic selection
python cli.py --provider auto
```

### **AI Parameters**
```bash
# Set temperature (creativity)
python cli.py --temperature 0.7

# Set max tokens
python cli.py --max-tokens 2000

# Set top-p
python cli.py --top-p 0.9

# Set frequency penalty
python cli.py --frequency-penalty 0.1
```

### **AI-Enhanced Features**
- **Code Generation**: AI-powered code generation from descriptions
- **Code Analysis**: AI-powered code review and optimization
- **Architecture Design**: AI-powered architecture recommendations
- **Security Analysis**: AI-powered security vulnerability detection
- **Performance Optimization**: AI-powered performance recommendations

---

## 🔒 **Security Features**

### **Security Scanning**
```bash
# Basic security scan
python cli.py --mode plugin --name security-scanner

# Detailed security scan
python cli.py --mode plugin --name security-scanner --params '{"level": "detailed"}'

# Security scan with specific focus
python cli.py --mode plugin --name security-scanner --params '{"focus": "authentication"}'
```

### **Security Checks**
- **Vulnerability Scanning**: Automated vulnerability detection
- **Dependency Analysis**: Security analysis of dependencies
- **Code Review**: Security-focused code review
- **Configuration Audit**: Security configuration validation
- **Compliance Check**: Security compliance validation

---

## 📈 **Performance Analysis**

### **Performance Monitoring**
```bash
# Basic performance analysis
python cli.py --mode plugin --name performance-analyzer

# Detailed performance analysis
python cli.py --mode plugin --name performance-analyzer --params '{"level": "detailed"}'

# Performance analysis with recommendations
python cli.py --mode plugin --name performance-analyzer --params '{"recommendations": true}'
```

### **Performance Metrics**
- **Response Time**: Application response time analysis
- **Memory Usage**: Memory consumption optimization
- **CPU Usage**: CPU utilization analysis
- **Database Performance**: Database query optimization
- **Network Performance**: Network efficiency analysis

---

## 🚀 **Automation and Scripting**

### **Batch Processing**
```bash
# Process multiple projects
for project in project1 project2 project3; do
    python cli.py --mode journal --path ./$project --output ${project}_analysis.md
done

# Generate multiple applications
python cli.py --mode compose --idea "Task manager" --output task_manager
python cli.py --mode compose --idea "Blog platform" --output blog_platform
python cli.py --mode compose --idea "API service" --output api_service
```

### **Integration with CI/CD**
```yaml
# GitHub Actions example
name: AutoDevCore Analysis
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AutoDevCore Analysis
        run: |
          python cli.py --mode journal --path . --output analysis_report.md
          python cli.py --mode score --path . --output score_report.md
```

### **Scheduled Analysis**
```bash
# Cron job for daily analysis
0 2 * * * cd /path/to/project && python cli.py --mode journal --path . --output daily_analysis_$(date +\%Y\%m\%d).md
```

---

## 🔧 **Advanced Usage**

### **Custom Templates**
```bash
# Use custom template
python cli.py --mode compose --idea "Custom application" --template /path/to/custom_template.json

# Create custom template
python cli.py --mode blueprint --idea "Template structure" --output custom_template.json
```

### **Plugin Development**
```python
# Plugin structure
class SecurityScannerPlugin:
    def __init__(self, config):
        self.config = config

    def execute(self, target_path):
        # Plugin implementation
        return {
            "vulnerabilities": [],
            "recommendations": [],
            "score": 85
        }
```

### **Custom Output Formats**
```python
# Custom formatter
class CustomFormatter:
    def format_report(self, data):
        # Custom formatting logic
        return formatted_report
```

---

## 🆘 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version

# Check virtual environment
which python
```

#### **AI Provider Issues**
```bash
# Check API keys
cat config/api_keys.json

# Test AI connection
python -c "from integrations.multi_provider_ai import MultiProviderAI; print(MultiProviderAI().get_provider_status())"

# Check Ollama (for local AI)
ollama list
```

#### **Permission Issues**
```bash
# Check file permissions
ls -la

# Fix permissions
chmod +x cli.py

# Check directory access
ls -la /path/to/project
```

### **Debug Mode**
```bash
# Enable debug mode
python cli.py --debug

# Verbose output
python cli.py --verbose

# Log to file
python cli.py --log-file debug.log
```

### **Performance Issues**
```bash
# Profile execution
python -m cProfile -o profile.stats cli.py --mode compose --idea "test"

# Memory profiling
python -m memory_profiler cli.py --mode compose --idea "test"

# Time execution
time python cli.py --mode compose --idea "test"
```

---

## 📚 **Examples and Use Cases**

### **Web Application Development**
```bash
# Generate a complete web application
python cli.py --mode compose --idea "Social media platform with user authentication, posts, and comments" --template web-app --verbose

# Analyze the generated application
python cli.py --mode journal --path ./social_media_platform --output analysis.md

# Score the application
python cli.py --mode score --path ./social_media_platform --template web-app --output score.md
```

### **API Service Development**
```bash
# Generate an API service
python cli.py --mode compose --idea "RESTful API for e-commerce with product management, orders, and payments" --template api-service

# Create architecture blueprint
python cli.py --mode blueprint --idea "Microservices architecture for e-commerce API" --complexity enterprise --output architecture.md

# Security scan the API
python cli.py --mode plugin --name security-scanner --params '{"target": "./ecommerce_api", "focus": "api_security"}'
```

### **Mobile Application Development**
```bash
# Generate a mobile app
python cli.py --mode compose --idea "Fitness tracking app with workout plans, progress tracking, and social features" --template mobile-app

# Performance analysis
python cli.py --mode plugin --name performance-analyzer --params '{"target": "./fitness_app", "platform": "mobile"}'

# Accessibility analysis
python cli.py --mode score --path ./fitness_app --criteria accessibility --output accessibility_score.md
```

---

## 📞 **Support and Resources**

### **Documentation**
- **User Guide**: `docs/USER_GUIDE.md` - Comprehensive user manual
- **API Reference**: `docs/API_REFERENCE.md` - Technical API documentation
- **GUI Help**: `docs/GUI_HELP.md` - Interface-specific guidance

### **Community**
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Join community discussions and Q&A
- **Contributing**: Guidelines for contributing to the project

### **Getting Help**
1. **Check Documentation**: Review relevant documentation first
2. **Search Issues**: Look for similar issues in GitHub
3. **Ask Community**: Post questions in discussions
4. **Report Bugs**: Create detailed bug reports with steps to reproduce

---

**AutoDevCore CLI - Powerful command-line interface for automated development and project management.**
