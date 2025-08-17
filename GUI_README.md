# 🎨 AutoDevCore GUI Documentation

**Comprehensive guide to AutoDevCore's dual GUI architecture**

AutoDevCore provides two powerful GUI interfaces designed for different use cases and user preferences. Both interfaces offer full access to AutoDevCore's AI-powered development capabilities with role-based dashboards and enterprise features.

## 🚀 Quick Start

### Streamlit GUI (Primary Interface)
```bash
# Launch the comprehensive Streamlit GUI
python run_gui.py

# Or directly with Streamlit
streamlit run gui/main.py --server.port 8501

# Access at: http://localhost:8501
```

### Flask GUI (Alternative Interface)
```bash
# Launch the Flask-based GUI
python simple_gui.py

# Access at: http://localhost:8502
```

## 🎯 GUI Comparison

| Feature | Streamlit GUI | Flask GUI |
|---------|---------------|-----------|
| **Interface Type** | Web-based dashboard | Web-based with modals |
| **Port** | 8501 | 8502 |
| **Best For** | Full-featured development | Quick access and simple tasks |
| **Role-Based Dashboards** | ✅ Complete | ✅ Basic |
| **AI Integration** | ✅ Multi-provider | ✅ GPT-OSS |
| **Project Management** | ✅ Comprehensive | ✅ Basic |
| **Reports** | ✅ Enhanced HTML | ✅ Basic |
| **User Management** | ✅ Full SSO | ❌ Limited |
| **Analytics** | ✅ Business Intelligence | ❌ Basic |

## 🌟 Streamlit GUI Features

### 🎯 Role-Based Dashboards

#### **Developer Dashboard**
- **Code Editor**: Syntax-highlighted code editing with AI assistance
- **AI Code Generation**: Multi-provider AI for code creation and optimization
- **Debug Analysis**: Syntax validation, code quality assessment, security scanning
- **File Management**: Upload/download capabilities for code files and folders
- **Real-time Chat**: AI assistant for development guidance

#### **Project Manager Dashboard**
- **Project Templates**: 5 pre-configured templates (Web App, Mobile App, API, Data Analytics, E-commerce)
- **Comprehensive Tracking**: Progress, budget, team allocation, risk assessment
- **Milestone Management**: Key milestone tracking with automated status updates
- **Team Management**: Workload distribution and resource allocation
- **Budget Control**: Real-time budget tracking with alerts and forecasting
- **Project Analytics**: Performance metrics and trend analysis

#### **DevOps Engineer Dashboard**
- **System Monitoring**: Real-time infrastructure health monitoring
- **Deployment Management**: Simulated deployment with status tracking
- **Security Scanning**: Automated vulnerability assessment and security analysis
- **Performance Metrics**: System performance and application metrics
- **Infrastructure Health**: CPU, memory, disk, and network usage monitoring

#### **Stakeholder Dashboard**
- **Business Intelligence**: Real-time analytics and business metrics
- **ROI Analysis**: Investment tracking, cost savings, revenue generation
- **Performance Monitoring**: Project performance and business impact
- **Strategic Insights**: Executive-level reporting and decision support
- **Competitive Analysis**: Market positioning and benchmark comparisons

#### **Admin Dashboard**
- **User Management**: Multi-user system with role-based access control
- **SSO Configuration**: Azure AD, AWS IAM, Google Workspace, Okta, OneLogin, Auth0
- **Security Policies**: Access control, data protection, and compliance settings
- **System Administration**: Infrastructure health, auditing, and reporting
- **Compliance Management**: SOC 2, GDPR, HIPAA, ISO 27001 compliance tracking

#### **New Developer Dashboard**
- **Learning Resources**: Onboarding guides and development tutorials
- **Quick Start Tools**: Simplified interface for new team members
- **AI Assistant**: Guided development with AI-powered suggestions
- **Project Templates**: Pre-built templates for common development tasks
- **Progress Tracking**: Learning progress and skill development metrics

### 📊 Enhanced HTML Reports

#### **Report Generation**
- **Automatic Creation**: Reports generated after each scoring analysis
- **Professional Styling**: Modern gradient design with Font Awesome icons
- **Interactive Charts**: Chart.js radar charts with hover effects
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Data**: Extracts actual scoring values from analysis

#### **Report Access**
- **Current Report**: Immediately available after scoring analysis
- **Previous Reports**: Browse all historical reports with timestamps
- **New Window Opening**: Reports open in full-screen browser windows
- **Direct Links**: Shareable URLs for team collaboration
- **Export Options**: Save reports for documentation and sharing

#### **Report Features**
- **Overall Score**: Prominent display of code quality score
- **Metrics Grid**: 5 cards showing Security, Performance, Code Quality, Architecture, DevOps
- **Interactive Radar Chart**: Visual representation of quality dimensions
- **Detailed Analysis**: Comprehensive scoring report with recommendations
- **Information Section**: Template used, analysis date, method details

### 🤖 AI Integration

#### **Multi-Provider AI**
- **7 AI Providers**: OpenAI, Anthropic, Google AI, Cohere, Mistral, Perplexity, GPT-OSS
- **Intelligent Fallback**: Automatic provider switching on failure
- **Cost Optimization**: Smart provider selection based on task requirements
- **Health Monitoring**: Real-time availability checking for all providers
- **Performance Tracking**: Response times, success rates, and cost analysis

#### **AI Lab**
- **Model Testing**: Test and compare different AI models
- **Prompt Engineering**: Advanced prompt template selection and customization
- **Performance Analysis**: Response time, cost, and quality metrics
- **Provider Comparison**: Side-by-side comparison of AI providers
- **Custom Parameters**: Temperature, max tokens, top_p, frequency penalty

### 👥 User Management & SSO

#### **Multi-User System**
- **Role-Based Access**: Developer, Project Manager, DevOps, Stakeholder, Admin
- **Permission Management**: Fine-grained access control and permissions
- **User Profiles**: Personal settings and preferences
- **Team Organization**: Group management and team hierarchies
- **Activity Tracking**: User activity and engagement metrics

#### **SSO Integration**
- **Multi-Provider SSO**: Azure AD, AWS IAM, Google Workspace, Okta, OneLogin, Auth0
- **Configuration Management**: Easy setup and configuration of SSO providers
- **Security Policies**: Password policies, MFA, session management
- **Compliance Support**: SOC 2, GDPR, HIPAA compliance tracking
- **Audit Logging**: Comprehensive activity tracking and reporting

### 📈 Business Intelligence

#### **Real-time Analytics**
- **Project Metrics**: Progress tracking, budget utilization, team performance
- **AI Performance**: Response times, success rates, cost analysis
- **User Activity**: Engagement metrics, feature usage, adoption rates
- **System Health**: Infrastructure monitoring, service status, performance metrics

#### **Advanced Analytics**
- **ROI Analysis**: Investment tracking, cost savings, revenue generation
- **Trend Analysis**: Performance trends, usage patterns, market positioning
- **Predictive Analytics**: 30-day forecasting, risk assessment, trend predictions
- **Competitive Analysis**: Benchmark comparisons, industry standards, best practices

## 🎨 Flask GUI Features

### **Lightweight Interface**
- **Modal Dialogs**: Clean, focused interface with popup dialogs
- **Quick Actions**: Fast access to common development tasks
- **AI Chat Integration**: Real-time AI assistant for development guidance
- **File Management**: Upload and manage code files and folders
- **Project Creation**: Simple project creation and management

### **Core Functionality**
- **Code Generation**: AI-powered code creation with best practices
- **Debug Analysis**: Syntax validation and code quality assessment
- **Deployment Simulation**: Simulated deployment with status tracking
- **Settings Management**: Configuration and customization options
- **Status Monitoring**: System health and AI service status

## 🔧 Configuration

### **API Keys Setup**
1. Navigate to **Settings** → **API Configuration**
2. Configure keys for your preferred AI providers:
   - OpenAI API Key
   - Anthropic API Key
   - Google AI API Key
   - Cohere API Key
   - Mistral API Key
   - Perplexity API Key
   - Local GPT-OSS Configuration

### **User Management**
1. Access **User Management** from the sidebar
2. Configure SSO providers (Azure AD, AWS IAM, etc.)
3. Create user groups and assign roles
4. Set up security policies and access controls

### **Theme and Appearance**
- **Dark/Light Mode**: Toggle between dark and light themes
- **Custom Styling**: Professional color schemes and typography
- **Responsive Design**: Optimized for desktop and mobile devices
- **Accessibility**: High contrast and keyboard navigation support

## 📊 Reports Management

### **Current Report**
- **Immediate Access**: View the most recent scoring report
- **Enhanced HTML**: Professional-grade report with interactive charts
- **New Window Opening**: Full-screen viewing experience
- **Direct Links**: Shareable URLs for team collaboration

### **Previous Reports**
- **Historical Access**: Browse all previous scoring reports
- **Timestamp Information**: Creation date and time for each report
- **File Size**: Report size and metadata information
- **Management Tools**: Clear, refresh, and organize reports

### **Report Features**
- **Interactive Charts**: Chart.js radar charts with hover effects
- **Metrics Visualization**: Visual representation of code quality scores
- **Detailed Analysis**: Comprehensive scoring breakdown and recommendations
- **Professional Styling**: Modern design with Font Awesome icons
- **Export Options**: Save and share reports for documentation

## 🛠️ Development Tools

### **Code Generation**
- **AI-Powered**: Multi-provider AI for intelligent code creation
- **Template-Based**: Industry-specific templates and best practices
- **Context-Aware**: Understanding of project requirements and constraints
- **Quality Assurance**: Built-in code quality and security checks

### **Debug Analysis**
- **Syntax Validation**: Automatic detection of syntax errors
- **Code Quality**: Assessment of readability and maintainability
- **Security Scanning**: Vulnerability detection and security analysis
- **Performance Analysis**: Code efficiency and optimization suggestions

### **File Management**
- **Upload Capabilities**: Support for code files and folders
- **Version Control**: Git integration for project management
- **Collaboration**: Real-time collaboration and sharing
- **Backup and Recovery**: Automatic backup and version management

## 🔒 Security Features

### **Authentication & Authorization**
- **Multi-Factor Authentication**: Enhanced security with MFA
- **Role-Based Access Control**: Fine-grained permissions and access
- **Session Management**: Secure session handling and timeout
- **Password Policies**: Strong password requirements and policies

### **Data Protection**
- **Encryption**: Data encryption at rest and in transit
- **Privacy Controls**: User data protection and privacy settings
- **Audit Logging**: Comprehensive activity tracking and reporting
- **Compliance**: SOC 2, GDPR, HIPAA compliance support

## 📈 Performance & Monitoring

### **System Health**
- **Real-time Monitoring**: CPU, memory, disk, and network usage
- **Performance Metrics**: Response times, throughput, and error rates
- **Health Checks**: Service status and availability monitoring
- **Alerting**: Proactive notification of issues and problems

### **Analytics Dashboard**
- **Usage Statistics**: User activity and feature adoption metrics
- **Performance Trends**: Historical performance data and analysis
- **Cost Analysis**: AI usage costs and optimization opportunities
- **ROI Tracking**: Business impact and value generation metrics

## 🚀 Deployment

### **Local Development**
```bash
# Start Streamlit GUI
python run_gui.py

# Start Flask GUI
python simple_gui.py

# Access interfaces
# Streamlit: http://localhost:8501
# Flask: http://localhost:8502
```

### **Production Deployment**
```bash
# Docker deployment
docker-compose up -d

# Environment variables
export AUTODEV_API_KEYS_PATH=/path/to/api_keys.json
export AUTODEV_LOG_LEVEL=INFO
export AUTODEV_ENVIRONMENT=production
```

## 📚 Documentation

### **User Guides**
- **User Guide**: `docs/USER_GUIDE.md` - Comprehensive user manual
- **Interactive Tutorial**: `docs/INTERACTIVE_TUTORIAL.md` - Step-by-step learning
- **Judge Reference**: `docs/JUDGE_QUICK_REFERENCE.md` - Evaluation guide

### **Technical Documentation**
- **API Reference**: `docs/API_REFERENCE.md` - Technical API documentation
- **CLI Help**: `docs/CLI_HELP.md` - Command-line interface guide
- **Role Hierarchy**: `docs/ROLE_HIERARCHY.md` - User role definitions

## 🆘 Support

### **Common Issues**
1. **Port Conflicts**: Check if ports 8501/8502 are available
2. **API Keys**: Configure API keys for AI providers
3. **Dependencies**: Ensure all requirements are installed
4. **Browser Compatibility**: Use modern browsers for best experience

### **Getting Help**
- **Documentation**: Check the `docs/` directory for comprehensive guides
- **Issues**: Report bugs and feature requests via GitHub issues
- **Discussions**: Join community discussions for questions and ideas

---

**AutoDevCore GUI** - Professional interfaces for intelligent development 🎨

*Choose the interface that best fits your workflow and team needs*
