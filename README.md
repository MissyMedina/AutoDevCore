# 🚀 AutoDevCore - The Core of Intelligent Development

**Modular AI agents that build smarter, score deeper**

AutoDevCore is a comprehensive development platform that combines AI-powered code generation, intelligent scoring, project management, and collaboration tools into a unified ecosystem. Built for modern development teams who demand excellence, efficiency, and innovation.

## 🌐 **Active Web Services & Interfaces**

### **Primary Web Interfaces**
- **🖥️ Streamlit GUI**: `http://localhost:8501` - Visual Development Hub
- **🔗 REST API**: `http://localhost:8080` - Core API Services
- **🔌 WebSocket Server**: `ws://localhost:8765` - Real-time Collaboration
- **📊 Monitoring Dashboard**: Integrated in GUI - Performance & Analytics

### **Service Endpoints**
- **API Health Check**: `http://localhost:8080/health`
- **Authentication**: `http://localhost:8080/auth/login`
- **User Profile**: `http://localhost:8080/api/user/profile`
- **System Status**: `http://localhost:8080/api/status`

### **Quick Start Web Access**
```bash
# Launch GUI (Primary Interface)
python3 run_gui.py
# Access: http://localhost:8501

# Start API Server
python3 integrations/web_api.py
# Access: http://localhost:8080

# Start WebSocket Server
python3 collaboration/websocket_server.py
# Access: ws://localhost:8765
```

## 🌟 Key Features

### 🤖 **AI-Powered Development**
- **Multi-Provider AI Integration**: OpenAI, Anthropic, Google AI, Cohere, Mistral, Perplexity, and Local GPT-OSS
- **Intelligent Code Generation**: Context-aware code creation with best practices
- **Real-time AI Assistant**: Interactive chat for development guidance
- **Advanced AI Lab**: Test and compare different AI models and prompts

### 📊 **Enhanced Code Quality Analysis**
- **Intelligent Scoring System**: AI-powered code quality assessment across 5 dimensions
- **Beautiful HTML Reports**: Professional-grade reports with interactive charts
- **Robust Fallback System**: Works reliably even when AI models are unavailable
- **Radar Chart Visualization**: Visual representation of code quality metrics
- **Template-Based Analysis**: Industry-specific scoring templates (FinTech, Healthcare, E-commerce)

### 🎯 **Role-Based Dashboards**
- **Developer Dashboard**: Code generation, debugging, and development tools
- **Project Manager Dashboard**: Project tracking, team management, and reporting
- **DevOps Engineer Dashboard**: Deployment, monitoring, and infrastructure management
- **Stakeholder Dashboard**: Business intelligence, ROI analysis, and strategic insights
- **Admin Dashboard**: System administration, security, and user management
- **New Developer Dashboard**: Learning resources and onboarding tools

### 👥 **Enterprise User Management & SSO**
- **Multi-User System**: Role-based access control and permissions
- **SSO Integration**: Azure AD, AWS IAM, Google Workspace, Okta, OneLogin, Auth0
- **Team Collaboration**: Real-time collaboration with WebSocket communication
- **Group Management**: Organize users into teams and departments
- **Security & Compliance**: Audit logs, compliance reporting, and security policies

### 📈 **Business Intelligence & Analytics**
- **Real-time Analytics**: KPIs, performance metrics, and trend analysis
- **ROI Analysis**: Cost-benefit analysis and business impact assessment
- **Predictive Analytics**: 30-day forecasts and trend predictions
- **Performance Benchmarks**: Industry comparison and best practices
- **Custom Analytics**: Configurable metrics and reporting

### 🔧 **Advanced Project Management**
- **Project Templates**: Pre-built templates for common project types
- **Budget Management**: Cost tracking, budget allocation, and financial reporting
- **Team Management**: Workload distribution, task assignment, and progress tracking
- **Risk Assessment**: Automated risk identification and mitigation strategies
- **Milestone Tracking**: Project timeline management and deadline monitoring

### 🛡️ **Enterprise Security**
- **Security Auditing**: Automated security scanning and vulnerability assessment
- **Compliance Framework**: SOC 2, GDPR, HIPAA, and industry-specific compliance
- **Access Control**: Fine-grained permissions and role-based security
- **Data Protection**: Encryption, secure storage, and privacy controls
- **Audit Logging**: Comprehensive activity tracking and compliance reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (recommended)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/autodevcore.git
cd autodevcore

# Create and activate virtual environment
python -m venv gui_env
source gui_env/bin/activate  # On Windows: gui_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install GUI dependencies
cd gui
pip install -r requirements.txt
cd ..
```

### Running the Application

#### Option 1: Streamlit GUI (Recommended)
```bash
# Start the main GUI
python run_gui.py

# Or directly with Streamlit
streamlit run gui/main.py --server.port 8501
```

#### Option 2: Flask GUI (Alternative)
```bash
# Start the Flask-based GUI
python simple_gui.py
```

#### Option 3: Command Line Interface
```bash
# Run CLI commands
python cli.py --help

# Generate an application
python cli.py --mode compose --idea "A task management app" --output-dir output/my_app

# Score code quality
python cli.py --mode score --app-dir my_app --template profiles/fintech.yaml
```

## 📊 Enhanced HTML Reports

AutoDevCore generates beautiful, professional HTML reports for code quality analysis:

### Features:
- **Interactive Charts**: Chart.js radar charts with hover effects
- **Responsive Design**: Works on desktop and mobile devices
- **Professional Styling**: Modern gradient design with Font Awesome icons
- **Real-time Data**: Extracts actual scoring values from analysis
- **Export Options**: Save reports for sharing and documentation

### Accessing Reports:
1. **Run scoring analysis** from the GUI or CLI
2. **View current report** with "🌐 View Full Report" button
3. **Browse previous reports** in the Reports page
4. **Open in new window** for full-screen viewing
5. **Share via URL** for team collaboration

## 🎯 Scoring System

### Quality Dimensions:
- **Security (75%)**: Authentication, input validation, data protection
- **Performance (80%)**: Code efficiency, optimization, resource usage
- **Code Quality (85%)**: Readability, maintainability, best practices
- **Architecture (70%)**: Design patterns, structure, scalability
- **DevOps (75%)**: Deployment readiness, monitoring, CI/CD

### Templates Available:
- **FinTech**: Banking and financial services focus
- **Healthcare**: Medical and health data compliance
- **E-commerce**: Online retail and payment processing
- **Custom**: Create your own scoring templates

## 🔧 Configuration

### API Keys Setup
1. Navigate to **Settings** → **API Configuration**
2. Configure keys for your preferred AI providers:
   - OpenAI API Key
   - Anthropic API Key
   - Google AI API Key
   - Cohere API Key
   - Mistral API Key
   - Perplexity API Key
   - Local GPT-OSS Configuration

### User Management
1. Access **User Management** from the sidebar
2. Configure SSO providers (Azure AD, AWS IAM, etc.)
3. Create user groups and assign roles
4. Set up security policies and access controls

## 📁 Project Structure

```
OpnAI_Hackathon/
├── gui/                    # Streamlit GUI application
│   ├── main.py            # Main GUI application
│   └── requirements.txt   # GUI dependencies
├── agents/                # AI agent modules
├── integrations/          # External service integrations
├── modes/                 # CLI operation modes
├── plugins/               # Extensible plugin system
├── profiles/              # Scoring templates
├── reports/               # Generated HTML reports
├── security/              # Security and authentication
├── utils/                 # Utility functions
├── cli.py                 # Command-line interface
├── simple_gui.py          # Flask-based GUI
└── requirements.txt       # Main dependencies
```

## 🛠️ Development

### Adding New Features
1. **Plugin System**: Extend functionality with custom plugins
2. **Custom Templates**: Create industry-specific scoring templates
3. **AI Integration**: Add new AI providers to the multi-provider system
4. **Dashboard Extensions**: Enhance role-based dashboards

### Testing
```bash
# Run tests
python run_tests.py

# Run specific test suites
pytest tests/test_core.py
pytest tests/test_collaboration_platform.py
```

## 📈 Performance & Monitoring

### System Health
- **Real-time Monitoring**: CPU, memory, disk, and network usage
- **Performance Metrics**: Response times, throughput, and error rates
- **Health Checks**: Service status and availability monitoring
- **Alerting**: Proactive notification of issues

### Analytics Dashboard
- **Usage Statistics**: User activity and feature adoption
- **Performance Trends**: Historical performance data
- **Cost Analysis**: AI usage costs and optimization opportunities
- **ROI Tracking**: Business impact and value generation

## 🔒 Security & Compliance

### Security Features
- **Authentication**: Multi-factor authentication and SSO
- **Authorization**: Role-based access control
- **Data Protection**: Encryption at rest and in transit
- **Audit Logging**: Comprehensive activity tracking
- **Vulnerability Scanning**: Automated security assessments

### Compliance Frameworks
- **SOC 2**: Security and availability controls
- **GDPR**: Data privacy and protection
- **HIPAA**: Healthcare data security
- **Industry Standards**: Custom compliance requirements

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [CLI Help](docs/CLI_HELP.md)
- [GUI Help](docs/GUI_HELP.md)

### Getting Help
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions
- **Documentation**: Comprehensive guides and tutorials
- **Examples**: Sample projects and use cases

## 🎉 Acknowledgments

- **AI Providers**: OpenAI, Anthropic, Google AI, Cohere, Mistral, Perplexity
- **Open Source**: Built on amazing open-source libraries
- **Community**: Contributors and users who make this project better

---

**AutoDevCore** - The core of intelligent development 🚀

*Transform ideas into fully functional applications in minutes, not weeks*
