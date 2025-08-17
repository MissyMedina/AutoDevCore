# 🔌 AutoDevCore API Reference

**Comprehensive API documentation for AutoDevCore's production-ready development platform**

This document provides detailed technical information about AutoDevCore's APIs, integrations, and development interfaces.

## 🌐 **Active API Services** (Updated 2025-08-15)

### **Base URL & Endpoints**
- **REST API**: `http://localhost:8080`
- **WebSocket**: `ws://localhost:8765`
- **Health Check**: `http://localhost:8080/health`
- **API Version**: v1.0.0

### **Service Status**
- ✅ **REST API Server**: Active on port 8080
- ✅ **WebSocket Server**: Active on port 8765
- ✅ **Authentication**: JWT-based with CORS support
- ✅ **Rate Limiting**: Implemented with security headers

### **Quick Start**
```bash
# Start API Server
python3 integrations/web_api.py

# Test Health Endpoint
curl http://localhost:8080/health

# Login (Default Credentials)
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## 🚀 **Quick Reference**

### **Core Components**
- **Streamlit GUI**: `gui/main.py` - Comprehensive web interface
- **Flask GUI**: `simple_gui.py` - Lightweight alternative interface
- **CLI Interface**: `cli.py` - Command-line automation
- **AI Integration**: `integrations/` - Multi-provider AI system
- **Project Management**: Role-based dashboards and project tracking

---

## 🎨 **GUI Architecture**

### **Streamlit GUI (`gui/main.py`)**
**Primary Interface**: Comprehensive web-based development environment

#### **Core Functions**
```python
def main():
    """Main Streamlit application entry point"""
    # Initialize session state
    # Setup role-based navigation
    # Render appropriate dashboard

def dashboard_page():
    """Main dashboard with role-based views"""
    # Role-based dashboard routing
    # Developer, Project Manager, DevOps, Stakeholder, Admin views

def sidebar_navigation():
    """Role-based sidebar navigation"""
    # User profile and team status
    # Role selection and navigation
    # Quick chat interface
```

#### **Role-Based Dashboards**
```python
def developer_dashboard():
    """Developer dashboard with code tools and AI assistance"""
    # Code editor and file management
    # AI code generation and debugging
    # Development tools and deployment

def project_manager_dashboard():
    """Project management dashboard with comprehensive tracking"""
    # Project creation and templates
    # Progress tracking and analytics
    # Team management and budget control

def devops_dashboard():
    """DevOps dashboard with system monitoring and security"""
    # System health monitoring
    # Deployment management
    # Security scanning and compliance

def stakeholder_dashboard():
    """Business intelligence dashboard for stakeholders"""
    # Business metrics and analytics
    # ROI analysis and reporting
    # Strategic KPIs and trends

def admin_dashboard():
    """System administration dashboard"""
    # User management and SSO
    # Security configuration
    # System health and auditing
```

### **Flask GUI (`simple_gui.py`)**
**Alternative Interface**: Lightweight web interface with modal dialogs

#### **Core Endpoints**
```python
@app.route("/")
def index():
    """Main dashboard page"""
    # Render main dashboard
    # Display project status
    # Show system metrics

@app.route("/api/settings", methods=["GET", "POST"])
def settings_api():
    """Settings management API"""
    # Load/save application settings
    # Configuration management

@app.route("/api/create-project", methods=["POST"])
def create_project():
    """Project creation API"""
    # Create new projects
    # Template-based project setup

@app.route("/api/chat", methods=["POST"])
def chat_api():
    """AI chat integration API"""
    # AI chat functionality
    # GPT-OSS integration
```

---

## 🤖 **AI Integration APIs**

### **Multi-Provider AI System (`integrations/multi_provider_ai.py`)**

#### **Core Class**
```python
class MultiProviderAI:
    """Multi-provider AI integration system"""
    
    def __init__(self):
        """Initialize multi-provider AI system"""
        # Load provider configurations
        # Setup fallback chains
        # Initialize health monitoring
    
    async def generate_response(
        self,
        prompt: str,
        task_type: str = "general",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate AI response with provider selection"""
        # Select optimal provider
        # Generate response
        # Handle errors and fallbacks
    
    def generate_response_sync(
        self,
        prompt: str,
        task_type: str = "general",
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Synchronous wrapper for generate_response"""
        # Run async method in event loop
        # Return synchronous result
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all AI providers"""
        # Check provider availability
        # Return configuration status
        # Monitor health metrics
```

#### **Supported Providers**
```python
PROVIDERS = {
    "openai": {
        "models": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
        "base_url": "https://api.openai.com/v1",
        "cost_per_1k_tokens": 0.12
    },
    "anthropic": {
        "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        "base_url": "https://api.anthropic.com",
        "cost_per_1k_tokens": 0.15
    },
    "google": {
        "models": ["gemini-pro", "gemini-pro-vision"],
        "base_url": "https://generativelanguage.googleapis.com",
        "cost_per_1k_tokens": 0.10
    },
    "cohere": {
        "models": ["command", "command-light", "command-nightly"],
        "base_url": "https://api.cohere.ai",
        "cost_per_1k_tokens": 0.08
    },
    "mistral": {
        "models": ["mistral-large", "mistral-medium", "mistral-small"],
        "base_url": "https://api.mistral.ai",
        "cost_per_1k_tokens": 0.14
    },
    "perplexity": {
        "models": ["llama-3.1-8b-instruct", "llama-3.1-70b-instruct"],
        "base_url": "https://api.perplexity.ai",
        "cost_per_1k_tokens": 0.06
    },
    "gpt_oss": {
        "models": ["gpt-oss:20b", "gpt-oss:7b", "mistral:7b"],
        "base_url": "http://localhost:11434",
        "cost_per_1k_tokens": 0.00
    }
}
```

### **Local AI Integration (`integrations/gpt_oss.py`)**

#### **Core Class**
```python
class GPTOSSClient:
    """Local AI client using GPT-OSS via Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gpt-oss:20b"):
        """Initialize GPT-OSS client"""
        # Setup Ollama connection
        # Configure model parameters
        # Initialize caching
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using local AI model"""
        # Send prompt to Ollama
        # Process response
        # Handle errors and caching
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get caching statistics"""
        # Return cache hit rates
        # Performance metrics
        # Storage statistics
```

---

## 📋 **Project Management APIs**

### **Project Templates**
```python
PROJECT_TEMPLATES = {
    "Web Application": {
        "description": "Full-stack web application with modern UI",
        "estimated_duration": "8-12 weeks",
        "team_size": "3-5 developers",
        "complexity": "Medium",
        "tech_stack": ["React", "Node.js", "PostgreSQL"],
        "estimated_budget": 15000
    },
    "Mobile App": {
        "description": "Cross-platform mobile application",
        "estimated_duration": "12-16 weeks",
        "team_size": "4-6 developers",
        "complexity": "High",
        "tech_stack": ["React Native", "Firebase", "Redux"],
        "estimated_budget": 25000
    },
    "API Development": {
        "description": "RESTful API with documentation",
        "estimated_duration": "4-6 weeks",
        "team_size": "2-3 developers",
        "complexity": "Medium",
        "tech_stack": ["FastAPI", "PostgreSQL", "Docker"],
        "estimated_budget": 8000
    },
    "Data Analytics": {
        "description": "Data processing and visualization platform",
        "estimated_duration": "6-10 weeks",
        "team_size": "3-4 developers",
        "complexity": "High",
        "tech_stack": ["Python", "Pandas", "Plotly", "PostgreSQL"],
        "estimated_budget": 18000
    },
    "E-commerce Platform": {
        "description": "Complete online shopping solution",
        "estimated_duration": "10-14 weeks",
        "team_size": "5-7 developers",
        "complexity": "High",
        "tech_stack": ["React", "Node.js", "Stripe", "MongoDB"],
        "estimated_budget": 30000
    }
}
```

### **Project Data Structure**
```python
PROJECT_SCHEMA = {
    "id": "string",  # Unique project identifier
    "name": "string",  # Project name
    "description": "string",  # Project description
    "template": "string",  # Project template used
    "progress": "integer",  # Progress percentage (0-100)
    "team": ["string"],  # Team member names
    "budget": "integer",  # Total budget in dollars
    "spent": "integer",  # Amount spent in dollars
    "deadline": "string",  # Deadline date (YYYY-MM-DD)
    "status": "string",  # Planning, Active, Testing, Completed, On Hold
    "priority": "string",  # Low, Medium, High, Critical
    "risk_level": "string",  # Low, Medium, High, Critical
    "risk_factors": ["string"],  # Risk factor descriptions
    "milestones": ["string"],  # Key milestone descriptions
    "tasks": ["object"],  # Task objects with status and assignee
    "created_date": "string",  # Creation date (YYYY-MM-DD)
    "notes": ["string"]  # Project notes and comments
}
```

---

## 👥 **User Management APIs**

### **SSO Integration**
```python
SSO_PROVIDERS = {
    "azure_ad": {
        "name": "Azure Active Directory",
        "config_fields": ["tenant_id", "client_id", "client_secret", "domain"],
        "auth_url": "https://login.microsoftonline.com",
        "api_version": "v2.0"
    },
    "aws_iam": {
        "name": "AWS IAM",
        "config_fields": ["access_key", "secret_key", "role_arn"],
        "auth_url": "https://sts.amazonaws.com",
        "api_version": "2011-06-15"
    },
    "google_workspace": {
        "name": "Google Workspace",
        "config_fields": ["client_id", "client_secret", "domain"],
        "auth_url": "https://accounts.google.com",
        "api_version": "v1"
    },
    "okta": {
        "name": "Okta",
        "config_fields": ["domain", "client_id", "client_secret"],
        "auth_url": "https://{domain}.okta.com",
        "api_version": "v1"
    },
    "onelogin": {
        "name": "OneLogin",
        "config_fields": ["client_id", "client_secret", "subdomain"],
        "auth_url": "https://{subdomain}.onelogin.com",
        "api_version": "v1"
    },
    "auth0": {
        "name": "Auth0",
        "config_fields": ["domain", "client_id", "client_secret"],
        "auth_url": "https://{domain}.auth0.com",
        "api_version": "v2"
    }
}
```

### **User Data Structure**
```python
USER_SCHEMA = {
    "id": "string",  # Unique user identifier
    "name": "string",  # Full name
    "email": "string",  # Email address
    "role": "string",  # Developer, Project Manager, DevOps, Stakeholder, Admin
    "sso_provider": "string",  # SSO provider name
    "status": "string",  # Active, Inactive, Suspended
    "groups": ["string"],  # Group memberships
    "permissions": ["string"],  # User permissions
    "last_login": "string",  # Last login timestamp
    "created_date": "string",  # Account creation date
    "preferences": "object"  # User preferences and settings
}
```

---

## 📊 **Analytics APIs**

### **Business Intelligence Metrics**
```python
BI_METRICS = {
    "project_metrics": {
        "total_projects": "integer",
        "active_projects": "integer",
        "completed_projects": "integer",
        "average_progress": "float",
        "budget_utilization": "float"
    },
    "ai_performance": {
        "response_time": "float",
        "success_rate": "float",
        "cost_per_request": "float",
        "cache_hit_rate": "float",
        "provider_usage": "object"
    },
    "user_activity": {
        "active_users": "integer",
        "feature_usage": "object",
        "session_duration": "float",
        "engagement_metrics": "object"
    },
    "system_health": {
        "cpu_usage": "float",
        "memory_usage": "float",
        "disk_usage": "float",
        "network_usage": "float",
        "service_status": "object"
    }
}
```

### **ROI Analysis**
```python
ROI_METRICS = {
    "investment": {
        "total_investment": "float",
        "monthly_investment": "float",
        "investment_breakdown": "object"
    },
    "returns": {
        "cost_savings": "float",
        "revenue_generated": "float",
        "efficiency_gains": "float"
    },
    "analysis": {
        "roi_percentage": "float",
        "payback_period": "string",
        "net_benefit": "float",
        "risk_assessment": "object"
    }
}
```

---

## 🔒 **Security APIs**

### **Security Scanning**
```python
SECURITY_SCAN_RESULTS = {
    "overall_score": "integer",  # Security score (0-100)
    "status": "string",  # Pass, Warning, Fail
    "issues_found": "integer",  # Number of security issues
    "vulnerabilities": ["object"],  # Vulnerability details
    "recommendations": ["string"],  # Security recommendations
    "metrics": {
        "critical_issues": "integer",
        "high_issues": "integer",
        "medium_issues": "integer",
        "low_issues": "integer"
    }
}
```

### **Compliance Tracking**
```python
COMPLIANCE_FRAMEWORKS = {
    "soc2": {
        "name": "SOC 2",
        "status": "string",  # Compliant, Pending, Non-Compliant
        "last_audit": "string",  # Last audit date
        "next_audit": "string",  # Next audit date
        "controls": "object"  # Control compliance status
    },
    "gdpr": {
        "name": "GDPR",
        "status": "string",
        "last_audit": "string",
        "next_audit": "string",
        "data_processing": "object"
    },
    "hipaa": {
        "name": "HIPAA",
        "status": "string",
        "last_audit": "string",
        "next_audit": "string",
        "privacy_controls": "object"
    },
    "iso27001": {
        "name": "ISO 27001",
        "status": "string",
        "last_audit": "string",
        "next_audit": "string",
        "security_controls": "object"
    }
}
```

---

## 🚀 **CLI Interface**

### **Command Structure**
```bash
python cli.py --mode <mode> [options]
```

### **Available Modes**
```python
CLI_MODES = {
    "compose": {
        "description": "Generate applications from ideas",
        "options": ["--idea", "--template", "--provider", "--verbose"],
        "example": "python cli.py --mode compose --idea 'AI task manager'"
    },
    "journal": {
        "description": "Analyze codebases and generate insights",
        "options": ["--path", "--output", "--format"],
        "example": "python cli.py --mode journal --path ./my-project"
    },
    "blueprint": {
        "description": "Create project blueprints and architecture",
        "options": ["--idea", "--complexity", "--output"],
        "example": "python cli.py --mode blueprint --idea 'E-commerce platform'"
    },
    "score": {
        "description": "Score applications against industry standards",
        "options": ["--path", "--template", "--output"],
        "example": "python cli.py --mode score --path ./my-app"
    },
    "plugin": {
        "description": "Manage and execute plugins",
        "options": ["--name", "--action", "--config"],
        "example": "python cli.py --mode plugin --name security-scanner"
    }
}
```

---

## 🔧 **Configuration APIs**

### **Application Configuration**
```python
APP_CONFIG = {
    "environment": "string",  # Development, Staging, Production
    "log_level": "string",  # DEBUG, INFO, WARNING, ERROR
    "api_keys_path": "string",  # Path to API keys file
    "cache_dir": "string",  # Cache directory path
    "max_file_size": "integer",  # Maximum file upload size
    "session_timeout": "integer",  # Session timeout in minutes
    "theme": "string",  # Light, Dark, Custom
    "language": "string",  # en, es, fr, de, etc.
    "auto_save": "boolean",  # Auto-save enabled
    "notifications": "boolean"  # Notifications enabled
}
```

### **API Keys Configuration**
```python
API_KEYS_CONFIG = {
    "openai": {
        "api_key": "string",
        "org_id": "string",
        "enabled": "boolean",
        "models": ["string"],
        "base_url": "string"
    },
    "anthropic": {
        "api_key": "string",
        "enabled": "boolean",
        "models": ["string"],
        "base_url": "string"
    },
    "google": {
        "api_key": "string",
        "enabled": "boolean",
        "models": ["string"],
        "base_url": "string"
    },
    "gpt_oss": {
        "url": "string",
        "model": "string",
        "enabled": "boolean",
        "models": ["string"],
        "base_url": "string"
    },
    "settings": {
        "default_provider": "string",
        "fallback_chain": ["string"],
        "timeout": "integer",
        "max_retries": "integer",
        "cost_optimization": "boolean",
        "performance_tracking": "boolean"
    }
}
```

---

## 📊 **Session State Management**

### **Streamlit Session State**
```python
SESSION_STATE_KEYS = {
    # User and authentication
    "user_role": "string",  # Current user role
    "current_user": "object",  # Current user data
    "team_members": ["object"],  # Team member data
    "users": ["object"],  # All users data
    "groups": ["object"],  # All groups data
    
    # Project management
    "projects": ["object"],  # All projects data
    "project_templates": "object",  # Project templates
    "show_new_project_form": "boolean",  # New project form visibility
    "editing_project": "string",  # Project being edited
    "viewing_project": "string",  # Project being viewed
    
    # AI and chat
    "chat_history": ["object"],  # Chat message history
    "global_chat_history": ["object"],  # Global chat history
    "ai_lab_data": "object",  # AI lab test data
    
    # Business intelligence
    "business_metrics": "object",  # Business metrics data
    "analytics_data": "object",  # Analytics data
    
    # UI state
    "current_page": "string",  # Current page/dashboard
    "show_project_report": "boolean",  # Project report visibility
    "show_team_management": "boolean",  # Team management visibility
    "show_budget_review": "boolean"  # Budget review visibility
}
```

---

## 🔌 **External Integrations**

### **Git Integration**
```python
GIT_INTEGRATION = {
    "repository": {
        "url": "string",  # Repository URL
        "branch": "string",  # Current branch
        "status": "string"  # Repository status
    },
    "commits": {
        "last_commit": "string",  # Last commit hash
        "commit_message": "string",  # Last commit message
        "commit_date": "string"  # Last commit date
    },
    "branches": ["string"],  # Available branches
    "tags": ["string"]  # Available tags
}
```

### **Deployment Integration**
```python
DEPLOYMENT_CONFIG = {
    "platform": "string",  # Vercel, Netlify, Heroku, AWS, etc.
    "environment": "string",  # Production, Staging, Development
    "url": "string",  # Deployment URL
    "status": "string",  # Deployment status
    "last_deploy": "string",  # Last deployment date
    "build_time": "string"  # Build duration
}
```

---

## 📈 **Performance Monitoring**

### **System Metrics**
```python
SYSTEM_METRICS = {
    "cpu": {
        "usage_percent": "float",
        "load_average": "float",
        "temperature": "float"
    },
    "memory": {
        "total": "integer",
        "used": "integer",
        "available": "integer",
        "usage_percent": "float"
    },
    "disk": {
        "total": "integer",
        "used": "integer",
        "free": "integer",
        "usage_percent": "float"
    },
    "network": {
        "bytes_sent": "integer",
        "bytes_recv": "integer",
        "packets_sent": "integer",
        "packets_recv": "integer"
    }
}
```

### **Application Metrics**
```python
APP_METRICS = {
    "response_time": "float",  # Average response time
    "requests_per_second": "float",  # Request rate
    "error_rate": "float",  # Error percentage
    "active_sessions": "integer",  # Active user sessions
    "memory_usage": "float",  # Application memory usage
    "uptime": "string"  # Application uptime
}
```

---

## 🚨 **Error Handling**

### **Error Types**
```python
ERROR_TYPES = {
    "ImportError": "Module import failures",
    "ConnectionError": "Network connection issues",
    "AuthenticationError": "Authentication failures",
    "PermissionError": "Permission and access issues",
    "ValidationError": "Data validation failures",
    "TimeoutError": "Request timeout issues",
    "ResourceError": "Resource exhaustion issues"
}
```

### **Error Response Format**
```python
ERROR_RESPONSE = {
    "error": "string",  # Error message
    "type": "string",  # Error type
    "code": "integer",  # Error code
    "details": "object",  # Error details
    "suggestions": ["string"],  # Suggested solutions
    "timestamp": "string"  # Error timestamp
}
```

---

## 📚 **Development APIs**

### **Plugin System**
```python
PLUGIN_INTERFACE = {
    "name": "string",  # Plugin name
    "version": "string",  # Plugin version
    "description": "string",  # Plugin description
    "author": "string",  # Plugin author
    "dependencies": ["string"],  # Required dependencies
    "entry_point": "string",  # Main function name
    "config_schema": "object"  # Configuration schema
}
```

### **Extension Points**
```python
EXTENSION_POINTS = {
    "ai_providers": "Custom AI provider integration",
    "project_templates": "Custom project templates",
    "security_scanners": "Custom security scanning",
    "deployment_targets": "Custom deployment platforms",
    "analytics_providers": "Custom analytics integration"
}
```

---

**AutoDevCore API Reference - Comprehensive technical documentation for the production-ready development platform.**
