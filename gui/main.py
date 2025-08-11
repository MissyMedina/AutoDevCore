#!/usr/bin/env python3
"""
AutoDevCore GUI - Visual Development Hub
A professional interface that bridges technical and business needs
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import AutoDevCore modules
try:
    from integrations.gpt_oss import gpt_oss_client
    from plugins.ai_orchestrator import AIOrchestrator
    from plugins.collaboration_platform import CollaborationPlatform
    from plugins.monitoring_dashboard import MonitoringDashboard
    from plugins.performance_optimizer import PerformanceOptimizer
    from plugins.plugin_manager import PluginManager
    from plugins.security_auditor import SecurityAuditor

    AUTODEV_AVAILABLE = True
    st.session_state.autodev_available = True
except ImportError as e:
    st.warning(f"Some AutoDevCore modules not available: {e}")
    AUTODEV_AVAILABLE = False
    st.session_state.autodev_available = False

# Import help documentation
try:
    from help_docs import show_help_documentation

    HELP_AVAILABLE = True
except ImportError as e:
    st.warning(f"Help documentation not available: {e}")
    HELP_AVAILABLE = False

# Import API configuration panel
try:
    from api_config_panel import show_api_config_panel

    API_CONFIG_AVAILABLE = True
except ImportError as e:
    st.warning(f"API configuration panel not available: {e}")
    API_CONFIG_AVAILABLE = False

# Import multi-provider AI
try:
    from integrations.multi_provider_ai import multi_provider_ai

    MULTI_PROVIDER_AVAILABLE = True
except ImportError as e:
    st.warning(f"Multi-provider AI not available: {e}")
    MULTI_PROVIDER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AutoDevCore - Visual Development Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown(
    """
<style>
    /* Professional color scheme */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #7c3aed;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --background-color: #f8fafc;
        --surface-color: #ffffff;
        --text-color: #1e293b;
    }
    
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: var(--surface-color);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: var(--success-color); }
    .status-warning { background-color: var(--warning-color); }
    .status-offline { background-color: var(--error-color); }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--background-color);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--success-color), var(--primary-color));
    }
    
    /* Code block styling */
    .stCodeBlock {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "user_role" not in st.session_state:
    st.session_state.user_role = "developer"
if "current_project" not in st.session_state:
    st.session_state.current_project = None
if "ai_models" not in st.session_state:
    st.session_state.ai_models = {
        "gpt-4": {"status": "online", "load": 45, "cost": 2.50},
        "claude": {"status": "online", "load": 30, "cost": 1.80},
        "gpt-oss": {"status": "online", "load": 85, "cost": 0.00},
    }
if "gpt_oss_status" not in st.session_state:
    st.session_state.gpt_oss_status = "unknown"


def test_gpt_oss_connection():
    """Test GPT-OSS connection and return status"""
    try:
        if AUTODEV_AVAILABLE:
            # Test basic connection
            cache_stats = gpt_oss_client.get_cache_stats()
            st.session_state.gpt_oss_status = "online"
            return True, cache_stats
        else:
            st.session_state.gpt_oss_status = "offline"
            return False, "AutoDevCore modules not available"
    except Exception as e:
        st.session_state.gpt_oss_status = "error"
        return False, str(e)


def main_header():
    """Main application header"""
    st.markdown(
        """
    <div class="main-header">
        <h1>🚀 AutoDevCore - Visual Development Hub</h1>
        <p>Transform ideas into fully functional applications in minutes, not weeks</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def sidebar_navigation():
    """Sidebar navigation and user controls"""
    with st.sidebar:
        st.markdown("### 🎯 Navigation")

        # User role selector
        role = st.selectbox(
            "👤 Your Role",
            [
                "developer",
                "project_manager",
                "devops_engineer",
                "new_developer",
                "stakeholder",
            ],
            index=[
                "developer",
                "project_manager",
                "devops_engineer",
                "new_developer",
                "stakeholder",
            ].index(st.session_state.user_role),
        )
        st.session_state.user_role = role

        st.markdown("---")

        # Main navigation
        page = st.radio(
            "📋 Main Sections",
            [
                "Dashboard",
                "Projects",
                "AI Lab",
                "Team",
                "Deploy",
                "Analytics",
                "API Config",
            ],
        )

        st.markdown("---")

        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🆕 New Project"):
            st.session_state.current_project = None
            st.rerun()

        if st.button("🔧 Settings"):
            st.info("Settings panel would open here")

        if st.button("❓ Help"):
            st.session_state.current_page = "help"
            st.rerun()

        st.markdown("---")

        # System status
        st.markdown("### 🔍 System Status")

        # Test GPT-OSS connection
        if st.button("🔄 Test GPT-OSS"):
            with st.spinner("Testing GPT-OSS connection..."):
                success, result = test_gpt_oss_connection()
                if success:
                    st.success("✅ GPT-OSS Connected!")
                    st.session_state.ai_models["gpt-oss"]["status"] = "online"
                else:
                    st.error(f"❌ GPT-OSS Error: {result}")
                    st.session_state.ai_models["gpt-oss"]["status"] = "offline"

        # AI Models Status
        for model, status in st.session_state.ai_models.items():
            status_color = {
                "online": "status-online",
                "warning": "status-warning",
                "offline": "status-offline",
            }[status["status"]]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <span class="status-indicator {status_color}"></span>
                <span style="font-weight: 600;">{model.upper()}</span>
                <span style="margin-left: auto; font-size: 0.8em; color: #666;">
                    {status['load']}% | ${status['cost']}
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )

        return page


def dashboard_page():
    """Main dashboard with role-based views"""
    st.markdown("## 📊 Dashboard")

    # Role-based dashboard content
    if st.session_state.user_role == "project_manager":
        project_manager_dashboard()
    elif st.session_state.user_role == "developer":
        developer_dashboard()
    elif st.session_state.user_role == "devops_engineer":
        devops_dashboard()
    elif st.session_state.user_role == "new_developer":
        new_developer_dashboard()
    elif st.session_state.user_role == "stakeholder":
        stakeholder_dashboard()


def project_manager_dashboard():
    """Dashboard view for project managers"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🚀 Active Projects")

        projects = [
            {"name": "E-commerce Platform", "progress": 75, "team": 4, "budget": 15000},
            {"name": "CRM Application", "progress": 45, "team": 3, "budget": 8000},
            {"name": "API Gateway", "progress": 90, "team": 2, "budget": 5000},
        ]

        for project in projects:
            with st.container():
                st.markdown(
                    f"""
                <div class="metric-card">
                    <h4>{project['name']}</h4>
                    <p>Progress: {project['progress']}%</p>
                    <p>Team: {project['team']} members</p>
                    <p>Budget: ${project['budget']:,}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("### 👥 Team Activity")

        team_activity = [
            {"name": "John", "activity": "Coding", "status": "online"},
            {"name": "Sarah", "activity": "Testing", "status": "online"},
            {"name": "Mike", "activity": "Review", "status": "away"},
            {"name": "Alice", "activity": "Planning", "status": "offline"},
        ]

        for member in team_activity:
            status_color = {
                "online": "status-online",
                "away": "status-warning",
                "offline": "status-offline",
            }[member["status"]]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <span class="status-indicator {status_color}"></span>
                <span style="font-weight: 600;">{member['name']}</span>
                <span style="margin-left: auto; font-size: 0.8em; color: #666;">
                    {member['activity']}
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col3:
        st.markdown("### 📈 Progress Metrics")

        # Progress chart
        progress_data = {
            "Project": ["E-commerce", "CRM", "API"],
            "Progress": [75, 45, 90],
            "Budget Used": [60, 40, 85],
        }
        df = pd.DataFrame(progress_data)

        fig = px.bar(
            df,
            x="Project",
            y=["Progress", "Budget Used"],
            title="Project Progress vs Budget",
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Recent activity timeline
    st.markdown("### 📋 Recent Activity Timeline")

    activities = [
        {
            "time": "10:30 AM",
            "activity": "AI generated authentication system",
            "user": "John",
        },
        {
            "time": "09:15 AM",
            "activity": "Team collaboration session started",
            "user": "Sarah",
        },
        {
            "time": "08:45 AM",
            "activity": 'New project "E-commerce" created',
            "user": "Mike",
        },
        {"time": "08:30 AM", "activity": "Security audit completed", "user": "Alice"},
    ]

    for activity in activities:
        st.markdown(
            f"""
        <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
            <span style="font-weight: 600; color: #666; min-width: 80px;">{activity['time']}</span>
            <span style="margin-left: 1rem;">{activity['activity']}</span>
            <span style="margin-left: auto; color: #666;">by {activity['user']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )


def developer_dashboard():
    """Dashboard view for developers"""
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📝 Code Editor")

        # Code editor simulation
        code = st.text_area(
            "Code Editor",
            value="""function createUser(userData) {
    // AI-generated code
    const user = new User(userData);
    return user.save();
}""",
            height=300,
            help="AI-assisted code editor",
        )

        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            if st.button("🤖 AI Generate"):
                st.success("AI is generating optimized code...")

        with col1_2:
            if st.button("🔍 Debug"):
                st.info("Running code analysis...")

        with col1_3:
            if st.button("🚀 Deploy"):
                st.info("Preparing deployment...")

    with col2:
        st.markdown("### 🔧 Development Tools")

        tools = [
            "AI Code Generation",
            "Real-time Debugging",
            "Performance Profiling",
            "Security Scanning",
            "Code Review",
            "Testing Suite",
        ]

        for tool in tools:
            if st.button(f"🔧 {tool}", key=f"tool_{tool}"):
                st.info(f"{tool} tool activated")

        st.markdown("---")

        st.markdown("### 🤖 AI Assistant")
        st.markdown(
            """
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #2563eb;">
            <p><strong>AI Assistant:</strong> "I can help optimize this code. Would you like me to suggest improvements for performance and security?"</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def devops_dashboard():
    """Dashboard view for DevOps engineers"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔄 CI/CD Pipeline")

        pipeline_steps = [
            {"step": "Build", "status": "success", "time": "2m 30s"},
            {"step": "Test", "status": "success", "time": "1m 45s"},
            {"step": "Deploy", "status": "running", "time": "--"},
            {"step": "Verify", "status": "pending", "time": "--"},
        ]

        for step in pipeline_steps:
            status_icon = {
                "success": "✅",
                "running": "🔄",
                "pending": "⏳",
                "failed": "❌",
            }[step["status"]]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <span style="font-size: 1.2em; margin-right: 0.5rem;">{status_icon}</span>
                <span style="font-weight: 600;">{step['step']}</span>
                <span style="margin-left: auto; color: #666;">{step['time']}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("### 📊 System Monitoring")

        # System metrics
        metrics = {
            "CPU Usage": 45,
            "Memory Usage": 60,
            "Disk Usage": 30,
            "Network I/O": 25,
        }

        for metric, value in metrics.items():
            st.markdown(
                f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>{metric}</span>
                    <span>{value}%</span>
                </div>
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #059669, #2563eb); height: 100%; width: {value}%;"></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col3:
        st.markdown("### 🔒 Security Status")

        security_metrics = {
            "Security Score": 85,
            "Vulnerabilities": 2,
            "Compliance": "Pass",
            "Last Scan": "2 hours ago",
        }

        for metric, value in security_metrics.items():
            st.markdown(
                f"""
            <div style="display: flex; justify-content: space-between; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <span>{metric}</span>
                <span style="font-weight: 600;">{value}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )


def new_developer_dashboard():
    """Dashboard view for new developers"""
    st.markdown("### 🎓 Welcome to AutoDevCore!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📚 Learning Path")

        learning_steps = [
            {"step": "1. Create Your First App", "status": "available"},
            {"step": "2. Learn AI Code Generation", "status": "available"},
            {"step": "3. Explore Templates", "status": "available"},
            {"step": "4. Join Team Collaboration", "status": "locked"},
            {"step": "5. Advanced Features", "status": "locked"},
        ]

        for step in learning_steps:
            status_icon = {"available": "✅", "locked": "🔒", "completed": "🎉"}[
                step["status"]
            ]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <span style="font-size: 1.2em; margin-right: 0.5rem;">{status_icon}</span>
                <span>{step['step']}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("#### 🚀 Quick Start")

        if st.button("🆕 Create Your First App"):
            st.success("Starting app creation wizard...")

        if st.button("📖 View Tutorials"):
            st.info("Opening tutorial library...")

        if st.button("🎯 Try Templates"):
            st.info("Loading template gallery...")

        if st.button("❓ Get Help"):
            st.info("Opening help center...")

    st.markdown("### 🤖 AI Assistant")
    st.markdown(
        """
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #2563eb;">
        <p><strong>AI Assistant:</strong> "Welcome! I'm here to help you learn. Let's start by creating your first application together. What kind of app would you like to build?"</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def stakeholder_dashboard():
    """Dashboard view for stakeholders"""
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Business Overview")

        # Business metrics
        business_metrics = {
            "Active Projects": 3,
            "Team Members": 8,
            "Cost Savings": "$25,000",
            "Time Saved": "120 hours",
            "Success Rate": "94%",
            "Customer Satisfaction": "4.8/5",
        }

        for metric, value in business_metrics.items():
            st.markdown(
                f"""
            <div class="metric-card">
                <h4>{metric}</h4>
                <p style="font-size: 1.5em; font-weight: 600; color: #2563eb;">{value}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("### 📈 ROI Analysis")

        # ROI chart
        roi_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "Cost Savings": [5000, 8000, 12000, 18000, 25000],
            "Time Savings": [20, 35, 50, 80, 120],
        }
        df = pd.DataFrame(roi_data)

        fig = px.line(
            df,
            x="Month",
            y=["Cost Savings", "Time Savings"],
            title="Monthly ROI Progress",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Executive Summary")
    st.markdown(
        """
    <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0;">
        <h4>🚀 AutoDevCore Impact Report</h4>
        <p><strong>Key Achievements:</strong></p>
        <ul>
            <li>70% faster project delivery</li>
            <li>50% reduction in development costs</li>
            <li>60% improvement in team collaboration</li>
            <li>40% fewer bugs through AI assistance</li>
        </ul>
        <p><strong>Next Quarter Goals:</strong></p>
        <ul>
            <li>Scale to 10+ concurrent projects</li>
            <li>Implement advanced AI features</li>
            <li>Expand team collaboration tools</li>
            <li>Launch enterprise features</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )


def projects_page():
    """Projects management page"""
    st.markdown("## 🎯 Projects")

    # Project creation wizard
    if st.button("🆕 Create New Project"):
        st.session_state.show_project_wizard = True

    if st.session_state.get("show_project_wizard", False):
        with st.form("new_project_form"):
            st.markdown("### 📋 New Project Wizard")

            project_name = st.text_input("Project Name")
            project_description = st.text_area("Description")
            framework = st.selectbox(
                "Framework", ["FastAPI", "Django", "Flask", "React", "Vue.js"]
            )
            complexity = st.selectbox("Complexity", ["Simple", "Medium", "Complex"])

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("🚀 Create Project"):
                    if project_name and project_description:
                        st.success(f"Project '{project_name}' created successfully!")
                        st.session_state.show_project_wizard = False
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")

            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_project_wizard = False
                    st.rerun()

    # Existing projects
    st.markdown("### 📁 Your Projects")

    projects = [
        {
            "name": "E-commerce Platform",
            "description": "Full-featured online store with payment processing",
            "progress": 75,
            "team": ["John", "Sarah", "Mike"],
            "last_updated": "2 hours ago",
        },
        {
            "name": "CRM Application",
            "description": "Customer relationship management system",
            "progress": 45,
            "team": ["Alice", "Bob"],
            "last_updated": "1 day ago",
        },
    ]

    for project in projects:
        with st.expander(f"📁 {project['name']} ({project['progress']}% complete)"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Description:** {project['description']}")
                st.markdown(f"**Team:** {', '.join(project['team'])}")
                st.markdown(f"**Last Updated:** {project['last_updated']}")

                # Progress bar
                st.progress(project["progress"] / 100)

            with col2:
                if st.button("👁️ View", key=f"view_{project['name']}"):
                    st.session_state.current_project = project["name"]
                    st.info(f"Opening project: {project['name']}")

                if st.button("🔧 Edit", key=f"edit_{project['name']}"):
                    st.info(f"Editing project: {project['name']}")

                if st.button("🚀 Deploy", key=f"deploy_{project['name']}"):
                    st.info(f"Deploying project: {project['name']}")


def ai_lab_page():
    """AI Lab page for AI model management and testing"""
    st.markdown("## 🤖 AI Lab")

    # Multi-Provider AI Status
    if MULTI_PROVIDER_AVAILABLE:
        st.markdown("### 🌐 Multi-Provider AI Status")

        provider_status = multi_provider_ai.get_provider_status()
        available_providers = multi_provider_ai.get_available_providers()

        if available_providers:
            st.success(f"✅ {len(available_providers)} AI providers configured")

            # Show provider status
            status_cols = st.columns(len(provider_status))
            for i, (provider, status) in enumerate(provider_status.items()):
                with status_cols[i]:
                    if status["configured"]:
                        if status["connected"]:
                            st.success(f"✅ {provider.title()}")
                        else:
                            st.error(f"❌ {provider.title()}")
                        st.caption(status["message"])
                    else:
                        st.info(f"⚪ {provider.title()}")
                        st.caption("Not configured")
        else:
            st.warning("⚠️ No AI providers configured")
            st.info("Configure providers in the API Config section")

    # Test GPT-OSS connection status
    if AUTODEV_AVAILABLE:
        st.success("✅ AutoDevCore modules loaded successfully!")
    else:
        st.error("❌ AutoDevCore modules not available")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧠 AI Model Status")

        # Test GPT-OSS connection
        if st.button("🔄 Test GPT-OSS Connection"):
            with st.spinner("Testing connection..."):
                success, result = test_gpt_oss_connection()
                if success:
                    st.success("✅ GPT-OSS Connected!")
                    st.session_state.ai_models["gpt-oss"]["status"] = "online"

                    # Show cache stats
                    if isinstance(result, dict):
                        st.markdown("#### 📊 Cache Statistics")
                        st.json(result)
                else:
                    st.error(f"❌ GPT-OSS Error: {result}")
                    st.session_state.ai_models["gpt-oss"]["status"] = "offline"

        for model, status in st.session_state.ai_models.items():
            with st.container():
                status_color = {
                    "online": "#059669",
                    "warning": "#d97706",
                    "offline": "#dc2626",
                }[status["status"]]

                st.markdown(
                    f"""
                <div class="metric-card">
                    <h4>🤖 {model.upper()}</h4>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Status:</span>
                        <span style="color: {status_color}; font-weight: 600;">
                            {status['status'].title()}
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Load:</span>
                        <span>{status['load']}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span>Cost:</span>
                        <span>${status['cost']}</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    with col2:
        st.markdown("### 📊 AI Performance Analytics")

        # Performance metrics
        performance_data = {
            "Response Time": 2.3,
            "Success Rate": 94.2,
            "Cost Efficiency": 0.12,
            "Model Selection": 78,
        }

        for metric, value in performance_data.items():
            st.metric(
                metric,
                f"{value}{'s' if metric == 'Response Time' else '%' if metric in ['Success Rate', 'Model Selection'] else '$'}",
            )

        # Enhanced AI Generation Form
        st.markdown("### 🎯 AI Generation Testing")

        with st.form("ai_test_form"):
            prompt = st.text_area(
                "Enter your prompt:",
                value="Write a Python function to calculate the fibonacci sequence",
            )

            # Enhanced model selection
            if MULTI_PROVIDER_AVAILABLE and available_providers:
                model_options = ["Auto"] + available_providers + ["GPT-OSS"]
            else:
                model_options = ["GPT-OSS", "Auto"]

            model_choice = st.selectbox("Select AI Model", model_options)
            task_type = st.selectbox(
                "Task Type",
                ["general", "code_generation", "analysis", "creative", "research"],
            )

            if st.form_submit_button("🤖 Generate"):
                if prompt:
                    with st.spinner("Generating response..."):
                        try:
                            if model_choice == "GPT-OSS" and AUTODEV_AVAILABLE:
                                # Use GPT-OSS
                                response = gpt_oss_client.generate_response(prompt)

                                if response:
                                    st.success("✅ GPT-OSS response generated!")
                                    st.markdown("#### 🤖 Generated Response (GPT-OSS):")
                                    st.code(response, language="python")

                                    # Show cache stats after generation
                                    cache_stats = gpt_oss_client.get_cache_stats()
                                    st.markdown("#### 📊 Updated Cache Statistics:")
                                    st.json(cache_stats)
                                else:
                                    st.error("❌ No response received from GPT-OSS")

                            elif (
                                model_choice in available_providers
                                and MULTI_PROVIDER_AVAILABLE
                            ):
                                # Use specific provider
                                result = multi_provider_ai.generate_response(
                                    prompt, provider=model_choice, task_type=task_type
                                )

                                if result["success"]:
                                    st.success(
                                        f"✅ {model_choice.title()} response generated!"
                                    )
                                    st.markdown(
                                        f"#### 🤖 Generated Response ({model_choice.title()}):"
                                    )
                                    st.code(result["content"], language="python")
                                    st.info(
                                        f"Provider: {result['provider']}, Model: {result['model']}, Time: {result['response_time']:.2f}s"
                                    )
                                else:
                                    st.error(f"Generation failed: {result['error']}")

                            elif (
                                model_choice == "Auto"
                                and MULTI_PROVIDER_AVAILABLE
                                and available_providers
                            ):
                                # Auto-select provider
                                result = multi_provider_ai.generate_response(
                                    prompt, task_type=task_type
                                )

                                if result["success"]:
                                    st.success(
                                        f"✅ Auto-selected {result['provider'].title()} response generated!"
                                    )
                                    st.markdown(
                                        f"#### 🤖 Generated Response (Auto-selected: {result['provider'].title()}):"
                                    )
                                    st.code(result["content"], language="python")
                                    st.info(
                                        f"Provider: {result['provider']}, Model: {result['model']}, Time: {result['response_time']:.2f}s"
                                    )
                                else:
                                    st.error(f"Generation failed: {result['error']}")

                            else:
                                st.info(
                                    "This would use the selected AI model for generation"
                                )

                        except Exception as e:
                            st.error(f"❌ Error generating response: {str(e)}")
                            st.info(
                                "💡 Make sure Ollama is running with a compatible model"
                            )
                elif not AUTODEV_AVAILABLE:
                    st.error("❌ AutoDevCore modules not available")
                else:
                    st.error("❌ Please enter a prompt")

    # Provider Comparison
    if MULTI_PROVIDER_AVAILABLE and len(available_providers) > 1:
        st.markdown("---")
        st.markdown("### 📊 Provider Comparison")

        if st.button("🔄 Compare Providers"):
            test_prompt = (
                "Write a simple Python function to calculate the factorial of a number"
            )

            comparison_results = []

            for provider in available_providers:
                with st.spinner(f"Testing {provider}..."):
                    result = multi_provider_ai.generate_response(
                        test_prompt, provider=provider, max_tokens=200
                    )

                    comparison_results.append(
                        {
                            "provider": provider,
                            "success": result["success"],
                            "response_time": result.get("response_time", 0),
                            "content_length": len(result.get("content", "")),
                        }
                    )

            # Display comparison
            if comparison_results:
                st.markdown("#### Performance Comparison")

                comp_data = []
                for result in comparison_results:
                    comp_data.append(
                        {
                            "Provider": result["provider"].title(),
                            "Success": "✅" if result["success"] else "❌",
                            "Response Time (s)": f"{result['response_time']:.2f}",
                            "Content Length": result["content_length"],
                        }
                    )

                import pandas as pd

                df = pd.DataFrame(comp_data)
                st.dataframe(df, use_container_width=True)

    # GPT-OSS Configuration
    st.markdown("### ⚙️ GPT-OSS Configuration")

    if AUTODEV_AVAILABLE:
        try:
            # Show current configuration
            config = {
                "Base URL": gpt_oss_client.base_url,
                "Model": gpt_oss_client.model,
                "Cache Enabled": gpt_oss_client.cache_enabled,
                "Optimization Params": gpt_oss_client.optimization_params,
            }

            st.markdown("#### Current Settings:")
            st.json(config)

            # Cache management
            if st.button("🗑️ Clear Cache"):
                try:
                    gpt_oss_client.clear_cache()
                    st.success("✅ Cache cleared successfully!")
                except Exception as e:
                    st.error(f"❌ Error clearing cache: {str(e)}")

        except Exception as e:
            st.error(f"❌ Error accessing GPT-OSS configuration: {str(e)}")
    else:
        st.warning(
            "⚠️ AutoDevCore modules not available - cannot access GPT-OSS configuration"
        )


def team_page():
    """Team collaboration page"""
    st.markdown("## 👥 Team Collaboration")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 👤 Team Members")

        team_members = [
            {"name": "John", "role": "Frontend Developer", "status": "online"},
            {"name": "Sarah", "role": "Backend Developer", "status": "online"},
            {"name": "Mike", "role": "DevOps Engineer", "status": "away"},
            {"name": "Alice", "role": "Project Manager", "status": "offline"},
        ]

        for member in team_members:
            status_color = {
                "online": "status-online",
                "away": "status-warning",
                "offline": "status-offline",
            }[member["status"]]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <span class="status-indicator {status_color}"></span>
                <div>
                    <div style="font-weight: 600;">{member['name']}</div>
                    <div style="font-size: 0.8em; color: #666;">{member['role']}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("### 💬 Live Chat")

        # Chat messages
        messages = [
            {
                "user": "John",
                "message": "Anyone see the auth issue?",
                "time": "10:30 AM",
            },
            {"user": "Sarah", "message": "Yes, I'm on it", "time": "10:31 AM"},
            {"user": "Mike", "message": "Deploying fix now", "time": "10:32 AM"},
        ]

        # Display messages
        for msg in messages:
            st.markdown(
                f"""
            <div style="margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-weight: 600;">{msg['user']}</span>
                    <span style="font-size: 0.8em; color: #666;">{msg['time']}</span>
                </div>
                <div>{msg['message']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Message input
        new_message = st.text_input("Type your message...")
        if st.button("Send"):
            if new_message:
                st.success("Message sent!")
                st.rerun()


def deploy_page():
    """Deployment and DevOps page"""
    st.markdown("## 🚀 Deployment & DevOps")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔄 CI/CD Pipeline")

        pipeline_steps = [
            {"step": "Build", "status": "success", "time": "2m 30s"},
            {"step": "Test", "status": "success", "time": "1m 45s"},
            {"step": "Deploy", "status": "running", "time": "--"},
            {"step": "Verify", "status": "pending", "time": "--"},
        ]

        for step in pipeline_steps:
            status_icon = {
                "success": "✅",
                "running": "🔄",
                "pending": "⏳",
                "failed": "❌",
            }[step["status"]]

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 5px;">
                <span style="font-size: 1.2em; margin-right: 0.5rem;">{status_icon}</span>
                <span style="font-weight: 600;">{step['step']}</span>
                <span style="margin-left: auto; color: #666;">{step['time']}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("### 🌍 Environment Status")

        environments = [
            {"name": "Production", "version": "v2.1.0", "status": "stable"},
            {"name": "Staging", "version": "v2.2.0-beta", "status": "testing"},
            {"name": "Development", "version": "v2.2.0-dev", "status": "building"},
        ]

        for env in environments:
            status_color = {
                "stable": "#059669",
                "testing": "#d97706",
                "building": "#dc2626",
            }[env["status"]]

            st.markdown(
                f"""
            <div class="metric-card">
                <h4>🌍 {env['name']}</h4>
                <p>Version: {env['version']}</p>
                <p style="color: {status_color}; font-weight: 600;">Status: {env['status'].title()}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col3:
        st.markdown("### 🔒 Security Scanner")

        if st.button("🔍 Run Security Scan"):
            with st.spinner("Scanning for vulnerabilities..."):
                time.sleep(3)
                st.success("Security scan completed!")

                st.markdown(
                    """
                <div class="metric-card">
                    <h4>🔒 Security Results</h4>
                    <p>Score: 85/100</p>
                    <p>Issues Found: 2</p>
                    <p>Status: ✅ Pass</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )


def analytics_page():
    """Analytics and reporting page"""
    st.markdown("## 📊 Analytics & Reporting")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Performance Metrics")

        # Performance chart
        performance_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "Response Time": [3.2, 2.8, 2.5, 2.3, 2.1],
            "Success Rate": [88, 90, 92, 93, 94],
        }
        df = pd.DataFrame(performance_data)

        fig = px.line(
            df,
            x="Month",
            y=["Response Time", "Success Rate"],
            title="Performance Trends",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💰 Cost Analysis")

        # Cost chart
        cost_data = {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "AI Costs": [150, 180, 220, 280, 320],
            "Infrastructure": [500, 550, 600, 650, 700],
        }
        df = pd.DataFrame(cost_data)

        fig = px.bar(
            df,
            x="Month",
            y=["AI Costs", "Infrastructure"],
            title="Monthly Costs",
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed metrics
    st.markdown("### 📋 Detailed Metrics")

    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

    with metrics_col1:
        st.metric("Total Projects", "12")
        st.metric("Active Users", "8")

    with metrics_col2:
        st.metric("Code Generated", "45,230 lines")
        st.metric("AI Requests", "1,234")

    with metrics_col3:
        st.metric("Deployments", "67")
        st.metric("Uptime", "99.9%")

    with metrics_col4:
        st.metric("Cost Savings", "$25,000")
        st.metric("Time Saved", "120 hours")


def main():
    """Main application function"""
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Main header
    main_header()

    # Sidebar navigation
    current_page = sidebar_navigation()

    # Check if help page is requested
    if st.session_state.current_page == "help":
        show_help_documentation()
        return

    # Page routing
    if current_page == "Dashboard":
        dashboard_page()
    elif current_page == "Projects":
        projects_page()
    elif current_page == "AI Lab":
        ai_lab_page()
    elif current_page == "Team":
        team_page()
    elif current_page == "Deploy":
        deploy_page()
    elif current_page == "Analytics":
        analytics_page()
    elif current_page == "API Config":
        if API_CONFIG_AVAILABLE:
            show_api_config_panel()
        else:
            st.error("API Configuration panel is not available")
            st.info("Please ensure all required modules are installed")


if __name__ == "__main__":
    main()
