#!/usr/bin/env python3
"""
AutoDevCore GUI Help Documentation System
Comprehensive help and user guides for all features
"""

import json
from pathlib import Path

import streamlit as st


class HelpDocumentation:
    """Comprehensive help documentation system for AutoDevCore GUI"""

    def __init__(self):
        self.help_sections = {
            "getting_started": {
                "title": "🚀 Getting Started",
                "icon": "🚀",
                "content": self._get_getting_started_content(),
            },
            "dashboard": {
                "title": "📊 Dashboard Guide",
                "icon": "📊",
                "content": self._get_dashboard_content(),
            },
            "projects": {
                "title": "🎯 Project Management",
                "icon": "🎯",
                "content": self._get_projects_content(),
            },
            "ai_lab": {
                "title": "🤖 AI Lab & GPT-OSS",
                "icon": "🤖",
                "content": self._get_ai_lab_content(),
            },
            "team": {
                "title": "👥 Team Collaboration",
                "icon": "👥",
                "content": self._get_team_content(),
            },
            "deploy": {
                "title": "🚀 Deployment & DevOps",
                "icon": "🚀",
                "content": self._get_deploy_content(),
            },
            "analytics": {
                "title": "📈 Analytics & Reporting",
                "icon": "📈",
                "content": self._get_analytics_content(),
            },
            "cli_guide": {
                "title": "💻 CLI Command Guide",
                "icon": "💻",
                "content": self._get_cli_guide_content(),
            },
            "troubleshooting": {
                "title": "🔧 Troubleshooting",
                "icon": "🔧",
                "content": self._get_troubleshooting_content(),
            },
            "faq": {
                "title": "❓ Frequently Asked Questions",
                "icon": "❓",
                "content": self._get_faq_content(),
            },
        }

    def _get_getting_started_content(self):
        return """
        # 🚀 Welcome to AutoDevCore - Visual Development Hub
        
        AutoDevCore is a professional AI-powered development platform that transforms ideas into fully functional applications in minutes, not weeks.
        
        ## 🎯 What You Can Do
        
        - **Generate complete applications** from simple descriptions
        - **Collaborate in real-time** with your team
        - **Monitor performance** and system health
        - **Deploy applications** with enterprise-grade tools
        - **Track progress** and business metrics
        
        ## 👤 Choose Your Role
        
        The interface adapts to your role:
        
        - **Developer**: AI-assisted coding, debugging, and deployment tools
        - **Project Manager**: High-level project tracking and team management
        - **DevOps Engineer**: Deployment pipelines and system monitoring
        - **New Developer**: Guided tutorials and learning paths
        - **Stakeholder**: Business metrics and ROI analysis
        
        ## 🎨 Interface Overview
        
        ### Sidebar Navigation
        - **Role Selector**: Choose your role to customize the interface
        - **Main Sections**: Navigate between different areas
        - **Quick Actions**: Common tasks and shortcuts
        - **System Status**: Monitor AI models and system health
        
        ### Main Content Area
        - **Dashboard**: Role-based overview and metrics
        - **Projects**: Create and manage applications
        - **AI Lab**: Test and configure AI models
        - **Team**: Collaborate with your team
        - **Deploy**: Manage deployments and infrastructure
        - **Analytics**: View performance and business metrics
        
        ## 🚀 Quick Start Steps
        
        1. **Select your role** from the sidebar
        2. **Test GPT-OSS connection** in the sidebar
        3. **Create your first project** using the Projects section
        4. **Try AI generation** in the AI Lab
        5. **Explore all features** to discover capabilities
        
        ## 💡 Pro Tips
        
        - Use the **Test GPT-OSS** button to verify your AI setup
        - Switch between roles to see different perspectives
        - Check the **System Status** for real-time health monitoring
        - Use **Quick Actions** for common tasks
        """

    def _get_dashboard_content(self):
        return """
        # 📊 Dashboard Guide
        
        The Dashboard provides a role-based overview of your development environment and projects.
        
        ## 🎯 Role-Based Views
        
        ### Developer Dashboard
        - **Code Editor**: AI-assisted development environment
        - **Development Tools**: Debugging, testing, and profiling
        - **AI Assistant**: Context-aware help and suggestions
        
        ### Project Manager Dashboard
        - **Active Projects**: Progress tracking and team allocation
        - **Team Activity**: Real-time updates on team members
        - **Progress Metrics**: Visual charts and timelines
        - **Recent Activity**: Timeline of recent actions
        
        ### DevOps Engineer Dashboard
        - **CI/CD Pipeline**: Visual workflow status
        - **System Monitoring**: Real-time health metrics
        - **Security Status**: Vulnerability scanning results
        
        ### New Developer Dashboard
        - **Learning Path**: Step-by-step tutorials
        - **Quick Start**: Guided project creation
        - **AI Assistant**: Helpful guidance and tips
        
        ### Stakeholder Dashboard
        - **Business Overview**: High-level metrics and KPIs
        - **ROI Analysis**: Cost savings and time efficiency
        - **Executive Summary**: Impact reports and achievements
        
        ## 📈 Understanding Metrics
        
        ### Performance Metrics
        - **Response Time**: AI model response speed
        - **Success Rate**: Percentage of successful operations
        - **Cost Efficiency**: Cost per request
        - **Model Selection**: Optimal model usage percentage
        
        ### Project Metrics
        - **Progress**: Completion percentage
        - **Team Size**: Number of team members
        - **Budget**: Project cost tracking
        - **Timeline**: Estimated completion time
        
        ## 🔄 Real-Time Updates
        
        The dashboard updates in real-time to show:
        - Team member activity and status
        - Project progress changes
        - System health metrics
        - Recent activities and events
        
        ## 🎨 Customization
        
        - Switch between roles to see different views
        - Use the sidebar to access different sections
        - Monitor system status for health indicators
        """

    def _get_projects_content(self):
        return """
        # 🎯 Project Management Guide
        
        The Projects section helps you create, manage, and track your applications.
        
        ## 🆕 Creating New Projects
        
        ### Project Creation Wizard
        1. Click **"🆕 Create New Project"**
        2. Fill in project details:
           - **Project Name**: Choose a descriptive name
           - **Description**: Explain what the project does
           - **Framework**: Select your preferred technology
           - **Complexity**: Choose Simple, Medium, or Complex
        3. Click **"🚀 Create Project"**
        
        ### Supported Frameworks
        - **FastAPI**: Modern Python web framework
        - **Django**: Full-featured Python framework
        - **Flask**: Lightweight Python framework
        - **React**: Modern JavaScript frontend
        - **Vue.js**: Progressive JavaScript framework
        
        ### Complexity Levels
        - **Simple**: Basic applications with minimal features
        - **Medium**: Standard applications with common features
        - **Complex**: Advanced applications with sophisticated features
        
        ## 📁 Managing Existing Projects
        
        ### Project Overview
        Each project shows:
        - **Progress**: Completion percentage with visual bar
        - **Team**: List of team members
        - **Last Updated**: Recent activity timestamp
        - **Description**: Project details and purpose
        
        ### Project Actions
        - **👁️ View**: Open project details
        - **🔧 Edit**: Modify project settings
        - **🚀 Deploy**: Deploy to production
        
        ## 📊 Project Tracking
        
        ### Progress Monitoring
        - Visual progress bars
        - Completion percentages
        - Time estimates
        - Budget tracking
        
        ### Team Management
        - Team member assignments
        - Role definitions
        - Activity tracking
        - Collaboration tools
        
        ## 🔄 Project Lifecycle
        
        ### Development Phase
        1. **Planning**: Define requirements and scope
        2. **Design**: Create architecture and UI/UX
        3. **Development**: Build features and functionality
        4. **Testing**: Quality assurance and bug fixes
        5. **Deployment**: Release to production
        
        ### Best Practices
        - Use descriptive project names
        - Provide detailed descriptions
        - Choose appropriate complexity levels
        - Assign team members early
        - Monitor progress regularly
        """

    def _get_ai_lab_content(self):
        return """
        # 🤖 AI Lab & GPT-OSS Guide
        
        The AI Lab is where you interact with AI models, test generation, and monitor performance.
        
        ## 🧠 AI Model Status
        
        ### Available Models
        - **GPT-4**: OpenAI's advanced language model
        - **Claude**: Anthropic's conversational AI
        - **GPT-OSS**: Local/offline AI via Ollama
        
        ### Model Information
        Each model shows:
        - **Status**: Online, Warning, or Offline
        - **Load**: Current usage percentage
        - **Cost**: Cost per request
        
        ## 🔄 Testing Connections
        
        ### GPT-OSS Connection Test
        1. Click **"🔄 Test GPT-OSS Connection"**
        2. Wait for connection verification
        3. View cache statistics if successful
        4. Check error messages if failed
        
        ### Connection Requirements
        - **Ollama**: Must be running locally
        - **Compatible Model**: Llama, Mistral, or similar
        - **Network Access**: For remote models
        - **API Keys**: For OpenAI/Anthropic models
        
        ## 🎯 AI Generation Testing
        
        ### Using the Generation Form
        1. **Enter your prompt**: Describe what you want to generate
        2. **Select model**: Choose GPT-OSS, Auto, GPT-4, or Claude
        3. **Click Generate**: Wait for AI response
        4. **Review results**: Check generated code/content
        
        ### Prompt Examples
        ```
        Write a Python function to calculate fibonacci numbers
        Create a simple web API endpoint
        Generate a React component for a todo list
        Write a database schema for user management
        Create a Docker configuration for a web app
        ```
        
        ### Understanding Responses
        - **Code Generation**: Syntax-highlighted code
        - **Cache Statistics**: Performance metrics
        - **Error Handling**: Clear error messages
        - **Fallback Responses**: When models are unavailable
        
        ## ⚙️ Configuration Management
        
        ### Current Settings
        View your current configuration:
        - **Base URL**: API endpoint for GPT-OSS
        - **Model**: Selected AI model
        - **Cache Enabled**: Caching status
        - **Optimization Params**: Performance settings
        
        ### Cache Management
        - **View Statistics**: Hit rates and performance
        - **Clear Cache**: Remove cached responses
        - **Monitor Usage**: Track cache efficiency
        
        ## 📊 Performance Analytics
        
        ### Key Metrics
        - **Response Time**: Average generation time
        - **Success Rate**: Percentage of successful requests
        - **Cost Efficiency**: Cost per request
        - **Model Selection**: Optimal model usage
        
        ### Optimization Tips
        - Use specific, clear prompts
        - Test different models for different tasks
        - Monitor cache performance
        - Clear cache when needed
        """

    def _get_team_content(self):
        return """
        # 👥 Team Collaboration Guide
        
        The Team section enables real-time collaboration and communication.
        
        ## 👤 Team Members
        
        ### Member Status
        - **🟢 Online**: Active and available
        - **🟡 Away**: Temporarily unavailable
        - **🔴 Offline**: Not currently active
        
        ### Member Information
        Each team member shows:
        - **Name**: Team member's name
        - **Role**: Job title and responsibilities
        - **Status**: Current availability
        - **Activity**: What they're currently working on
        
        ## 💬 Live Chat
        
        ### Using the Chat
        1. **View Messages**: See conversation history
        2. **Type Message**: Enter your text in the input field
        3. **Send**: Click send or press Enter
        4. **Real-time Updates**: Messages appear instantly
        
        ### Chat Features
        - **Real-time Messaging**: Instant communication
        - **Message History**: View previous conversations
        - **User Identification**: See who sent each message
        - **Timestamp**: When messages were sent
        
        ### Best Practices
        - Be clear and concise
        - Use appropriate tone
        - Reference specific projects or tasks
        - Respond promptly to team members
        
        ## 🤝 Collaboration Features
        
        ### Shared Workspaces
        - **Project Access**: Team members can view projects
        - **Real-time Editing**: Simultaneous collaboration
        - **Version Control**: Track changes and updates
        - **File Sharing**: Share resources and documents
        
        ### Team Coordination
        - **Task Assignment**: Assign work to team members
        - **Progress Tracking**: Monitor individual contributions
        - **Deadline Management**: Track project timelines
        - **Resource Allocation**: Manage team workload
        
        ## 📋 Team Management
        
        ### Adding Team Members
        1. **Invite Users**: Send invitations via email
        2. **Assign Roles**: Define responsibilities
        3. **Set Permissions**: Control access levels
        4. **Onboard**: Provide training and resources
        
        ### Role Management
        - **Owner**: Full system access
        - **Admin**: Project management access
        - **Editor**: Code editing capabilities
        - **Viewer**: Read-only access
        - **Guest**: Limited access
        
        ## 🔒 Security & Privacy
        
        ### Data Protection
        - **Encrypted Communication**: Secure messaging
        - **Access Control**: Role-based permissions
        - **Audit Logs**: Track team activities
        - **Privacy Settings**: Control data sharing
        
        ### Best Practices
        - Use strong passwords
        - Regularly update permissions
        - Monitor team activities
        - Follow security guidelines
        """

    def _get_deploy_content(self):
        return """
        # 🚀 Deployment & DevOps Guide
        
        The Deploy section provides tools for managing deployments and infrastructure.
        
        ## 🔄 CI/CD Pipeline
        
        ### Pipeline Stages
        1. **Build**: Compile and package application
        2. **Test**: Run automated tests
        3. **Deploy**: Deploy to target environment
        4. **Verify**: Confirm successful deployment
        
        ### Status Indicators
        - **✅ Success**: Stage completed successfully
        - **🔄 Running**: Stage currently in progress
        - **⏳ Pending**: Stage waiting to start
        - **❌ Failed**: Stage encountered errors
        
        ### Pipeline Monitoring
        - **Real-time Updates**: Live status tracking
        - **Execution Times**: Performance metrics
        - **Error Logs**: Detailed failure information
        - **Rollback Options**: Quick recovery tools
        
        ## 🌍 Environment Management
        
        ### Environment Types
        - **Development**: Local development environment
        - **Staging**: Pre-production testing
        - **Production**: Live application environment
        
        ### Environment Status
        Each environment shows:
        - **Version**: Current deployment version
        - **Status**: Stable, Testing, or Building
        - **Health**: System performance metrics
        - **Uptime**: Availability statistics
        
        ### Environment Actions
        - **Deploy**: Push new version
        - **Rollback**: Revert to previous version
        - **Scale**: Adjust resource allocation
        - **Monitor**: View performance metrics
        
        ## 📊 System Monitoring
        
        ### Key Metrics
        - **CPU Usage**: Processor utilization
        - **Memory Usage**: RAM consumption
        - **Disk Usage**: Storage utilization
        - **Network I/O**: Network traffic
        
        ### Performance Monitoring
        - **Real-time Graphs**: Live metric visualization
        - **Alert Thresholds**: Automatic notifications
        - **Historical Data**: Trend analysis
        - **Capacity Planning**: Resource forecasting
        
        ## 🔒 Security Scanner
        
        ### Security Features
        - **Vulnerability Scanning**: Detect security issues
        - **Compliance Checking**: Verify standards compliance
        - **Dependency Analysis**: Check for known vulnerabilities
        - **Configuration Auditing**: Review security settings
        
        ### Security Metrics
        - **Security Score**: Overall security rating
        - **Issues Found**: Number of vulnerabilities
        - **Compliance Status**: Standards compliance
        - **Last Scan**: Most recent security check
        
        ### Running Security Scans
        1. Click **"🔍 Run Security Scan"**
        2. Wait for scan completion
        3. Review results and recommendations
        4. Address any identified issues
        
        ## 🛠️ DevOps Tools
        
        ### Infrastructure Management
        - **Container Orchestration**: Docker and Kubernetes
        - **Cloud Integration**: AWS, Azure, GCP
        - **Configuration Management**: Infrastructure as Code
        - **Monitoring Stack**: Prometheus, Grafana
        
        ### Automation Features
        - **Auto-scaling**: Dynamic resource allocation
        - **Auto-healing**: Automatic recovery
        - **Blue-green Deployments**: Zero-downtime updates
        - **Canary Releases**: Gradual rollout
        
        ## 📈 Deployment Analytics
        
        ### Deployment Metrics
        - **Success Rate**: Percentage of successful deployments
        - **Deployment Time**: Average deployment duration
        - **Rollback Rate**: Frequency of rollbacks
        - **Uptime**: System availability percentage
        
        ### Best Practices
        - Test thoroughly in staging
        - Use automated deployment pipelines
        - Monitor deployments closely
        - Have rollback plans ready
        """

    def _get_analytics_content(self):
        return """
        # 📈 Analytics & Reporting Guide
        
        The Analytics section provides comprehensive insights into your development operations.
        
        ## 📊 Performance Metrics
        
        ### Response Time Trends
        - **Historical Data**: Track performance over time
        - **Trend Analysis**: Identify patterns and improvements
        - **Benchmarking**: Compare against targets
        - **Optimization Opportunities**: Find areas for improvement
        
        ### Success Rate Analysis
        - **Overall Success**: Percentage of successful operations
        - **Category Breakdown**: Success by feature type
        - **Error Analysis**: Common failure patterns
        - **Improvement Tracking**: Monitor progress over time
        
        ## 💰 Cost Analysis
        
        ### AI Costs
        - **Model Usage**: Cost by AI model
        - **Request Volume**: Number of AI requests
        - **Cost Efficiency**: Cost per request
        - **Budget Tracking**: Monitor spending against limits
        
        ### Infrastructure Costs
        - **Compute Resources**: CPU and memory costs
        - **Storage**: Data storage expenses
        - **Network**: Bandwidth and transfer costs
        - **Services**: Third-party service costs
        
        ### Cost Optimization
        - **Resource Utilization**: Optimize resource usage
        - **Model Selection**: Choose cost-effective AI models
        - **Caching Strategies**: Reduce redundant requests
        - **Scaling Policies**: Right-size infrastructure
        
        ## 📋 Detailed Metrics
        
        ### Project Metrics
        - **Total Projects**: Number of active projects
        - **Active Users**: Team member engagement
        - **Code Generated**: Lines of code produced
        - **AI Requests**: Number of AI interactions
        
        ### Operational Metrics
        - **Deployments**: Number of successful deployments
        - **Uptime**: System availability percentage
        - **Cost Savings**: Money saved through automation
        - **Time Saved**: Hours saved through efficiency
        
        ## 📈 Business Intelligence
        
        ### ROI Analysis
        - **Investment Tracking**: Development costs
        - **Benefit Measurement**: Time and cost savings
        - **ROI Calculation**: Return on investment
        - **Trend Analysis**: ROI over time
        
        ### Productivity Metrics
        - **Development Speed**: Time to market
        - **Team Efficiency**: Output per team member
        - **Quality Metrics**: Bug rates and fixes
        - **Innovation Index**: New feature development
        
        ## 🎯 Custom Reports
        
        ### Report Types
        - **Executive Summary**: High-level business metrics
        - **Technical Deep Dive**: Detailed technical analysis
        - **Team Performance**: Individual and team metrics
        - **Project Status**: Current project health
        
        ### Report Features
        - **Interactive Charts**: Click to drill down
        - **Export Options**: PDF, CSV, Excel formats
        - **Scheduled Reports**: Automatic report generation
        - **Custom Dashboards**: Personalized views
        
        ## 📊 Data Visualization
        
        ### Chart Types
        - **Line Charts**: Trend analysis over time
        - **Bar Charts**: Comparison between categories
        - **Pie Charts**: Proportional breakdowns
        - **Heat Maps**: Multi-dimensional data visualization
        
        ### Interactive Features
        - **Zoom and Pan**: Detailed data exploration
        - **Filtering**: Focus on specific data subsets
        - **Drill-down**: Navigate from summary to detail
        - **Real-time Updates**: Live data refresh
        
        ## 🔍 Data Analysis
        
        ### Statistical Analysis
        - **Trend Identification**: Pattern recognition
        - **Anomaly Detection**: Unusual data points
        - **Correlation Analysis**: Relationship identification
        - **Forecasting**: Future prediction models
        
        ### Insights Generation
        - **Automated Insights**: AI-powered analysis
        - **Recommendation Engine**: Actionable suggestions
        - **Alert System**: Important metric notifications
        - **Benchmarking**: Industry comparison
        
        ## 📈 Best Practices
        
        ### Data Management
        - **Data Quality**: Ensure accurate metrics
        - **Regular Monitoring**: Consistent tracking
        - **Historical Preservation**: Maintain data history
        - **Privacy Compliance**: Protect sensitive data
        
        ### Analysis Techniques
        - **Baseline Establishment**: Set performance benchmarks
        - **Goal Setting**: Define improvement targets
        - **Regular Reviews**: Periodic analysis sessions
        - **Action Planning**: Implement improvements
        """

    def _get_troubleshooting_content(self):
        return """
        # 🔧 Troubleshooting Guide
        
        Common issues and solutions for AutoDevCore GUI.
        
        ## 🚨 Common Issues
        
        ### GUI Won't Start
        **Problem**: Streamlit server fails to start
        
        **Solutions**:
        1. **Check Python Version**: Ensure Python 3.12+ is installed
        2. **Verify Dependencies**: Install missing modules
        3. **Check Port Availability**: Ensure port 8501 is free
        4. **Restart Terminal**: Clear any hanging processes
        
        **Commands**:
        ```bash
        # Check Python version
        python --version
        
        # Install dependencies
        pip install -r gui/requirements.txt
        
        # Check port usage
        lsof -i :8501
        
        # Kill hanging processes
        pkill -f streamlit
        ```
        
        ### Module Import Errors
        **Problem**: "No module named 'module_name'" errors
        
        **Solutions**:
        1. **Install Missing Modules**: Use pip to install
        2. **Check Virtual Environment**: Ensure correct environment
        3. **Verify Path**: Check Python path configuration
        4. **Restart GUI**: Reload after installing modules
        
        **Common Modules**:
        ```bash
        pip install aiohttp websockets psutil redis
        ```
        
        ### GPT-OSS Connection Issues
        **Problem**: Cannot connect to GPT-OSS/Ollama
        
        **Solutions**:
        1. **Start Ollama**: Ensure Ollama is running
        2. **Check Model**: Verify compatible model is installed
        3. **Test Connection**: Use Ollama CLI to test
        4. **Check Network**: Verify local network access
        
        **Commands**:
        ```bash
        # Start Ollama
        ollama serve
        
        # List models
        ollama list
        
        # Test model
        ollama run llama2 "Hello, world!"
        ```
        
        ### Performance Issues
        **Problem**: GUI is slow or unresponsive
        
        **Solutions**:
        1. **Check System Resources**: Monitor CPU and memory
        2. **Clear Cache**: Remove cached data
        3. **Restart Services**: Reload GUI and backend
        4. **Optimize Settings**: Adjust performance parameters
        
        **Commands**:
        ```bash
        # Check system resources
        top
        htop
        
        # Clear cache
        rm -rf ~/.cache/streamlit
        ```
        
        ## 🔍 Diagnostic Tools
        
        ### System Health Check
        ```bash
        # Check Python environment
        python -c "import sys; print(sys.version)"
        
        # Check installed packages
        pip list
        
        # Check system resources
        ps aux | grep python
        ```
        
        ### Network Diagnostics
        ```bash
        # Test local connectivity
        curl -I http://localhost:8501
        
        # Check Ollama connection
        curl http://localhost:11434/api/tags
        
        # Test external APIs
        curl -I https://api.openai.com/v1/models
        ```
        
        ### Log Analysis
        ```bash
        # View Streamlit logs
        tail -f ~/.streamlit/logs/streamlit.log
        
        # Check system logs
        dmesg | tail -20
        
        # Monitor real-time logs
        journalctl -f
        ```
        
        ## 🛠️ Advanced Troubleshooting
        
        ### Debug Mode
        Enable debug logging for detailed information:
        
        ```bash
        # Run with debug logging
        streamlit run gui/main.py --logger.level=debug
        
        # Check debug output
        tail -f ~/.streamlit/logs/streamlit.log
        ```
        
        ### Environment Isolation
        Create a clean environment for testing:
        
        ```bash
        # Create new virtual environment
        python -m venv test_env
        
        # Activate environment
        source test_env/bin/activate  # Linux/Mac
        test_env\\Scripts\\activate   # Windows
        
        # Install minimal dependencies
        pip install streamlit plotly pandas
        ```
        
        ### Configuration Reset
        Reset GUI configuration to defaults:
        
        ```bash
        # Remove configuration files
        rm -rf ~/.streamlit/
        
        # Clear cache
        rm -rf ~/.cache/streamlit/
        
        # Restart GUI
        streamlit run gui/main.py
        ```
        
        ## 📞 Getting Help
        
        ### Self-Service Resources
        - **Documentation**: Check this help system
        - **Logs**: Review error logs for details
        - **Community**: Search for similar issues
        - **Tutorials**: Follow step-by-step guides
        
        ### Support Channels
        - **GitHub Issues**: Report bugs and request features
        - **Discord Community**: Get help from other users
        - **Email Support**: Contact the development team
        - **Documentation**: Comprehensive guides and tutorials
        
        ### Information to Provide
        When seeking help, include:
        - **Error Messages**: Exact error text
        - **System Information**: OS, Python version, etc.
        - **Steps to Reproduce**: How to trigger the issue
        - **Logs**: Relevant log files
        - **Screenshots**: Visual evidence of the problem
        
        ## 🔄 Recovery Procedures
        
        ### Complete Reset
        If all else fails, perform a complete reset:
        
        ```bash
        # Stop all services
        pkill -f streamlit
        pkill -f ollama
        
        # Remove all data
        rm -rf gui_env/
        rm -rf ~/.streamlit/
        rm -rf ~/.cache/streamlit/
        
        # Reinstall from scratch
        python -m venv gui_env
        source gui_env/bin/activate
        pip install -r gui/requirements.txt
        ```
        
        ### Backup and Restore
        Always backup important data:
        
        ```bash
        # Backup configuration
        cp -r ~/.streamlit/ ~/.streamlit_backup/
        
        # Backup projects
        cp -r projects/ projects_backup/
        
        # Restore if needed
        cp -r ~/.streamlit_backup/ ~/.streamlit/
        ```
        """

    def _get_faq_content(self):
        return """
        # ❓ Frequently Asked Questions
        
        Common questions and answers about AutoDevCore GUI.
        
        ## 🤖 AI & GPT-OSS Questions
        
        **Q: What is GPT-OSS?**
        A: GPT-OSS is a local AI model that runs through Ollama, providing offline AI capabilities without requiring external API keys or internet connectivity.
        
        **Q: How do I set up GPT-OSS?**
        A: Install Ollama, download a compatible model (like llama2), and start the Ollama service. The GUI will automatically detect and connect to it.
        
        **Q: Which AI models are supported?**
        A: The GUI supports GPT-4 (OpenAI), Claude (Anthropic), and GPT-OSS (local via Ollama). You can also use the "Auto" option for intelligent model selection.
        
        **Q: Why is my AI generation slow?**
        A: Local models like GPT-OSS can be slower than cloud models. Try using smaller models, optimizing your prompts, or using cloud models for faster responses.
        
        **Q: How much does AI generation cost?**
        A: GPT-OSS is free (local), while GPT-4 and Claude have per-request costs. The GUI shows real-time cost tracking for all models.
        
        ## 🎯 Project Management Questions
        
        **Q: How do I create a new project?**
        A: Go to the Projects section, click "Create New Project", fill in the details (name, description, framework, complexity), and click "Create Project".
        
        **Q: What frameworks are supported?**
        A: The GUI supports FastAPI, Django, Flask, React, and Vue.js. More frameworks can be added through the plugin system.
        
        **Q: How do I track project progress?**
        A: Each project shows a progress bar, completion percentage, team assignments, and last update time. The dashboard provides an overview of all projects.
        
        **Q: Can I collaborate with my team?**
        A: Yes! Use the Team section for real-time chat, member status tracking, and shared project access. Team members can work on projects simultaneously.
        
        **Q: How do I deploy my project?**
        A: Use the Deploy section to manage CI/CD pipelines, environment deployments, and infrastructure monitoring. The GUI provides visual deployment tools.
        
        ## 🖥️ Technical Questions
        
        **Q: What are the system requirements?**
        A: Python 3.12+, 4GB RAM minimum, 2GB disk space. For AI features, you'll need additional RAM for local models (8GB+ recommended).
        
        **Q: How do I install missing modules?**
        A: The GUI will show warnings for missing modules. Install them using pip: `pip install module_name`. Common modules include aiohttp, websockets, psutil, and redis.
        
        **Q: Can I run the GUI on a server?**
        A: Yes! The GUI can be deployed on servers, cloud platforms, or Docker containers. Use `--server.address 0.0.0.0` for network access.
        
        **Q: How do I customize the interface?**
        A: Modify the CSS in `gui/main.py` for styling changes, or edit the Python code to add new features. The GUI is built with Streamlit for easy customization.
        
        **Q: Is the GUI secure?**
        A: The GUI includes security features like input validation, secure communication, and role-based access control. Always follow security best practices for production use.
        
        ## 👥 Team & Collaboration Questions
        
        **Q: How many team members can I have?**
        A: There's no hard limit, but performance may vary with large teams. The GUI is designed to handle teams of 10-50 members efficiently.
        
        **Q: Can I control who sees what?**
        A: Yes! Use role-based access control. Assign roles like Owner, Admin, Editor, Viewer, or Guest to control what each team member can access.
        
        **Q: How do I invite team members?**
        A: Use the Team section to send invitations via email. Team members will receive a link to join the project with appropriate permissions.
        
        **Q: Is the chat secure?**
        A: Chat messages are encrypted and stored securely. Only team members with appropriate permissions can access the conversation history.
        
        **Q: Can I export team data?**
        A: Yes! Use the Analytics section to export team performance reports, project data, and collaboration metrics in various formats.
        
        ## 📊 Analytics & Performance Questions
        
        **Q: What metrics are tracked?**
        A: The GUI tracks AI performance, project progress, team activity, system health, cost analysis, and business metrics like ROI and time savings.
        
        **Q: How accurate are the analytics?**
        A: Analytics are based on real-time data from your usage. The more you use the system, the more accurate and comprehensive the analytics become.
        
        **Q: Can I create custom reports?**
        A: Yes! Use the Analytics section to create custom dashboards, filter data, and generate reports for specific time periods or projects.
        
        **Q: How do I optimize performance?**
        A: Use the Performance section to monitor system resources, optimize AI model selection, implement caching strategies, and scale infrastructure as needed.
        
        **Q: What's the cost savings calculation based on?**
        A: Cost savings are calculated by comparing traditional development time and costs with AI-assisted development, including time saved and efficiency improvements.
        
        ## 🔧 Troubleshooting Questions
        
        **Q: The GUI won't start, what should I do?**
        A: Check Python version (3.12+), install missing dependencies, ensure port 8501 is free, and restart the terminal. See the Troubleshooting section for detailed steps.
        
        **Q: GPT-OSS connection fails, how do I fix it?**
        A: Ensure Ollama is running (`ollama serve`), check if a compatible model is installed (`ollama list`), and verify the model works (`ollama run model_name "test"`).
        
        **Q: I'm getting module errors, what's wrong?**
        A: Install missing modules using pip. Common missing modules include aiohttp, websockets, psutil, and redis. The GUI will show warnings for missing dependencies.
        
        **Q: The GUI is slow, how can I improve performance?**
        A: Check system resources, clear cache, restart services, optimize AI model selection, and consider upgrading hardware if needed.
        
        **Q: How do I reset the GUI to defaults?**
        A: Remove configuration files (`rm -rf ~/.streamlit/`), clear cache (`rm -rf ~/.cache/streamlit/`), and restart the GUI. See the Troubleshooting section for complete reset procedures.
        
        ## 🚀 Advanced Questions
        
        **Q: Can I integrate with external tools?**
        A: Yes! The GUI supports integrations with GitHub, GitLab, CI/CD platforms, cloud providers, and monitoring tools through the plugin system.
        
        **Q: How do I add custom features?**
        A: Modify the Python code in `gui/main.py` or create custom plugins. The GUI is built with Streamlit and can be extended with additional components.
        
        **Q: Can I deploy the GUI in production?**
        A: Yes! Use Docker containers, cloud platforms, or traditional servers. Follow security best practices and use proper authentication for production deployments.
        
        **Q: How do I backup my data?**
        A: Backup configuration files, project data, and user settings. The GUI provides export options for analytics and project information.
        
        **Q: Is there an API for the GUI?**
        A: The GUI is built on top of AutoDevCore's backend APIs. You can access the same functionality programmatically through the AutoDevCore Python modules.
        
        ## 📞 Support Questions
        
        **Q: Where can I get help?**
        A: Check this help system, review documentation, join the Discord community, or contact the development team through GitHub issues.
        
        **Q: How do I report a bug?**
        A: Use GitHub issues to report bugs. Include error messages, system information, steps to reproduce, and relevant logs or screenshots.
        
        **Q: Can I request new features?**
        A: Yes! Use GitHub issues to request new features. Provide detailed descriptions of what you need and how it would benefit your workflow.
        
        **Q: Is there training available?**
        A: Check the documentation for tutorials and guides. The GUI includes built-in help and learning paths for new users.
        
        **Q: How do I stay updated?**
        A: Follow the project on GitHub, join the Discord community, and check for regular updates and new features.
        """

    def _get_cli_guide_content(self):
        return """
        # 💻 AutoDevCore CLI Command Guide
        
        AutoDevCore provides a powerful command-line interface for developers who prefer terminal-based workflows.
        
        ## 🚀 Basic Commands
        
        ### Starting AutoDevCore
        ```bash
        # Start the main application
        python main.py
        
        # Start with specific configuration
        python main.py --config config.yaml
        
        # Start in debug mode
        python main.py --debug
        ```
        
        ### GPT-OSS Integration
        ```bash
        # Check GPT-OSS cache statistics
        python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.get_cache_stats())"
        
        # Test GPT-OSS connection
        python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.test_connection())"
        
        # Generate response via CLI
        python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.generate_response('Write a Python function'))"
        ```
        
        ## 🎯 Project Management Commands
        
        ### Creating Projects
        ```bash
        # Generate a new application
        python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('MyApp', 'A simple web application')"
        
        # Generate with specific framework
        python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('MyApp', 'FastAPI web app', framework='fastapi')"
        
        # Generate security features
        python -c "from agents.security_generator import SecurityGeneratorAgent; sec = SecurityGeneratorAgent(); sec.generate_security_features('MyApp')"
        ```
        
        ### Managing Projects
        ```bash
        # List all projects
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_projects())"
        
        # Get project status
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.get_project_status('MyApp'))"
        
        # Delete project
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.delete_project('MyApp')"
        ```
        
        ## 🤖 AI Operations Commands
        
        ### Multi-Model AI
        ```bash
        # Use AI Orchestrator
        python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.generate_response('Create a REST API'))"
        
        # Generate app plan
        python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.generate_app_plan('E-commerce platform'))"
        
        # Analyze code
        python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.analyze_code('path/to/code.py'))"
        ```
        
        ### Performance Monitoring
        ```bash
        # Check system performance
        python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.get_dashboard_data())"
        
        # Run health checks
        python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.run_health_checks())"
        
        # Get performance metrics
        python -c "from utils.performance_monitor import performance_monitor; print(performance_monitor.get_performance_report())"
        ```
        
        ## 🔧 Plugin Management Commands
        
        ### Plugin Operations
        ```bash
        # List installed plugins
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_plugins())"
        
        # Install plugin
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.install_plugin('plugin_name')"
        
        # Uninstall plugin
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.uninstall_plugin('plugin_name')"
        
        # Search plugins
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.search_plugins('ai'))"
        ```
        
        ### Plugin Development
        ```bash
        # Validate plugin
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.validate_plugin('path/to/plugin.py'))"
        
        # Test plugin
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.test_plugin('plugin_name'))"
        
        # Generate plugin report
        python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.generate_report())"
        ```
        
        ## 👥 Collaboration Commands
        
        ### Team Management
        ```bash
        # Create team
        python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); tm.create_team('MyTeam', 'Team description')"
        
        # Add team member
        python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); tm.add_member('MyTeam', 'user@email.com', 'editor')"
        
        # List team members
        python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); print(tm.get_team_members('MyTeam'))"
        
        # Check permissions
        python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); print(tm.has_permission('MyTeam', 'user@email.com', 'edit_project'))"
        ```
        
        ### Collaboration Platform
        ```bash
        # Start collaboration platform
        python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); cp.start()"
        
        # Create collaborative project
        python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.create_collaborative_project('MyProject', 'Project description', 'owner@email.com'))"
        
        # Invite to project
        python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.invite_to_project('MyProject', 'user@email.com', 'editor'))"
        
        # Get project status
        python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.get_project_status('MyProject'))"
        ```
        
        ## 🚀 Deployment Commands
        
        ### CI/CD Pipeline
        ```bash
        # Run security audit
        python -c "from plugins.security_auditor import SecurityAuditor; sa = SecurityAuditor(); print(sa.run_full_audit())"
        
        # Run performance tests
        python -c "from tests.load_test import run_comprehensive_load_test; print(run_comprehensive_load_test())"
        
        # Build Docker image
        python -c "import subprocess; subprocess.run(['docker', 'build', '-t', 'autodevcore', '.'])"
        
        # Deploy with Docker Compose
        python -c "import subprocess; subprocess.run(['docker-compose', 'up', '-d'])"
        ```
        
        ### Performance Optimization
        ```bash
        # Run performance optimizer
        python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); print(po.optimize_all())"
        
        # Clear cache
        python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); po.clear_cache()"
        
        # Monitor performance
        python -c "from plugins.performance_integration import PerformanceIntegration; pi = PerformanceIntegration(); print(pi.get_performance_score())"
        ```
        
        ## 📊 Analytics Commands
        
        ### Data Analysis
        ```bash
        # Get analytics data
        python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.get_analytics_data())"
        
        # Export metrics
        python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); md.export_metrics('metrics.csv')"
        
        # Generate report
        python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); md.generate_report('report.pdf')"
        ```
        
        ## 🔧 Testing Commands
        
        ### Test Suites
        ```bash
        # Run end-to-end tests
        python tests/end_to_end_test.py
        
        # Run unit tests
        python -m pytest tests/ -v
        
        # Run with coverage
        python -m pytest tests/ --cov=plugins --cov=integrations --cov=agents --cov=utils
        
        # Run specific test
        python -m pytest tests/test_collaboration_final.py -v
        ```
        
        ### Load Testing
        ```bash
        # Run load test
        python -c "from tests.load_test import run_comprehensive_load_test; print(run_comprehensive_load_test())"
        
        # Run specific scenario
        python -c "from tests.load_test import run_load_test_scenario; print(run_load_test_scenario('ai_generation', 100))"
        
        # Generate load test report
        python -c "from tests.load_test import generate_load_test_report; print(generate_load_test_report())"
        ```
        
        ## 🛠️ Utility Commands
        
        ### System Information
        ```bash
        # Check Python version
        python --version
        
        # Check installed packages
        pip list
        
        # Check system resources
        python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
        
        # Check disk usage
        python -c "import psutil; print(f'Disk: {psutil.disk_usage(\"/\").percent}%')"
        ```
        
        ### Configuration
        ```bash
        # Check environment variables
        python -c "import os; print([k for k in os.environ.keys() if 'AUTO' in k.upper()])"
        
        # Validate configuration
        python -c "from config.settings import validate_config; print(validate_config())"
        
        # Export configuration
        python -c "from config.settings import export_config; export_config('config_backup.yaml')"
        ```
        
        ## 📚 Documentation Commands
        
        ### Generate Documentation
        ```bash
        # Generate API documentation
        python -c "from docs.generator import generate_api_docs; generate_api_docs()"
        
        # Generate user guide
        python -c "from docs.generator import generate_user_guide; generate_user_guide()"
        
        # Generate changelog
        python -c "from docs.generator import generate_changelog; generate_changelog()"
        ```
        
        ## 🚨 Emergency Commands
        
        ### Recovery Operations
        ```bash
        # Kill all AutoDevCore processes
        pkill -f "python.*main.py"
        pkill -f "streamlit"
        pkill -f "ollama"
        
        # Clear all caches
        python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); po.clear_all_caches()"
        
        # Reset configuration
        python -c "from config.settings import reset_config; reset_config()"
        
        # Backup data
        python -c "from utils.backup import backup_all_data; backup_all_data('backup_$(date +%Y%m%d_%H%M%S).tar.gz')"
        ```
        
        ## 💡 Pro Tips
        
        ### Command Aliases
        Create useful aliases in your shell configuration:
        ```bash
        # Add to ~/.bashrc or ~/.zshrc
        alias autodev="python main.py"
        alias autodev-gui="python run_gui.py"
        alias autodev-test="python -m pytest tests/ -v"
        alias autodev-cache="python -c \"from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.get_cache_stats())\""
        alias autodev-health="python -c \"from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.run_health_checks())\""
        ```
        
        ### Scripts
        Create reusable scripts for common operations:
        ```bash
        # Create script: autodev-generate.sh
        #!/bin/bash
        python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('$1', '$2')"
        
        # Create script: autodev-deploy.sh
        #!/bin/bash
        python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); cp.deploy_project('$1')"
        ```
        
        ### Automation
        Use cron jobs for automated tasks:
        ```bash
        # Daily health check
        0 9 * * * python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); md.run_health_checks()"
        
        # Weekly backup
        0 2 * * 0 python -c "from utils.backup import backup_all_data; backup_all_data('weekly_backup_$(date +%Y%m%d).tar.gz')"
        ```
        
        ## 📖 Command Reference
        
        ### Quick Reference
        | Command | Description | Example |
        |---------|-------------|---------|
        | `python main.py` | Start AutoDevCore | `python main.py --debug` |
        | `python -c "..."` | Execute Python code | `python -c "print('Hello')"` |
        | `python -m pytest` | Run tests | `python -m pytest tests/ -v` |
        | `pip install` | Install packages | `pip install -r requirements.txt` |
        
        ### Environment Variables
        ```bash
        export AUTODEV_DEBUG=true
        export AUTODEV_CONFIG_PATH=/path/to/config
        export AUTODEV_LOG_LEVEL=DEBUG
        export AUTODEV_CACHE_DIR=/path/to/cache
        ```
        
        ### Exit Codes
        - `0`: Success
        - `1`: General error
        - `2`: Configuration error
        - `3`: Network error
        - `4`: Permission error
        - `5`: Resource error
        """

    def show_help_page(self):
        """Display the main help page with navigation"""
        st.markdown("## 📚 AutoDevCore Help & Documentation")

        # Help navigation
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🚀 Getting Started")
            if st.button("🚀 Getting Started Guide"):
                st.session_state.help_section = "getting_started"
                st.rerun()

        with col2:
            st.markdown("### 🎯 Core Features")
            if st.button("📊 Dashboard Guide"):
                st.session_state.help_section = "dashboard"
                st.rerun()
            if st.button("🎯 Project Management"):
                st.session_state.help_section = "projects"
                st.rerun()
            if st.button("🤖 AI Lab Guide"):
                st.session_state.help_section = "ai_lab"
                st.rerun()

        with col3:
            st.markdown("### 🔧 Support")
            if st.button("🔧 Troubleshooting"):
                st.session_state.help_section = "troubleshooting"
                st.rerun()
            if st.button("❓ FAQ"):
                st.session_state.help_section = "faq"
                st.rerun()

        # Additional sections
        st.markdown("### 👥 Collaboration & Deployment")
        col4, col5, col6 = st.columns(3)

        with col4:
            if st.button("👥 Team Collaboration"):
                st.session_state.help_section = "team"
                st.rerun()

        with col5:
            if st.button("🚀 Deployment Guide"):
                st.session_state.help_section = "deploy"
                st.rerun()

        with col6:
            if st.button("📈 Analytics Guide"):
                st.session_state.help_section = "analytics"
                st.rerun()

        # CLI Guide section
        st.markdown("### 💻 Command Line Interface")
        if st.button("💻 CLI Command Guide"):
            st.session_state.help_section = "cli_guide"
            st.rerun()

        # Show selected section content
        if hasattr(st.session_state, "help_section") and st.session_state.help_section:
            section = self.help_sections.get(st.session_state.help_section)
            if section:
                st.markdown(f"## {section['icon']} {section['title']}")
                st.markdown(section["content"])

                # Back to help menu button
                if st.button("← Back to Help Menu"):
                    st.session_state.help_section = None
                    st.rerun()
        else:
            # Default help overview
            st.markdown(
                """
            ### Welcome to AutoDevCore Help!
            
            This comprehensive help system will guide you through all aspects of AutoDevCore GUI and CLI.
            
            **Quick Start:**
            1. Read the **Getting Started Guide** to understand the basics
            2. Explore **Core Features** to learn about specific functionality
            3. Check the **CLI Command Guide** for terminal-based workflows
            4. Review **Troubleshooting** if you encounter issues
            5. Check **FAQ** for common questions
            
            **Need Help?**
            - Use the navigation buttons above to explore different sections
            - Each section contains detailed information and step-by-step guides
            - Look for the **Back to Help Menu** button to return here
            
            **Pro Tips:**
            - Bookmark this page for quick reference
            - Use the search function in your browser to find specific topics
            - Check the troubleshooting section before contacting support
            - Use CLI commands for automation and scripting
            """
            )


def show_help_documentation():
    """Main function to display help documentation"""
    help_docs = HelpDocumentation()
    help_docs.show_help_page()
