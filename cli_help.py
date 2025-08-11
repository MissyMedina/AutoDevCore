#!/usr/bin/env python3
"""
AutoDevCore CLI Help Documentation
Standalone help system for command-line users
"""

import sys
import os
from pathlib import Path

def print_section(title, content):
    """Print a formatted section"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(content)

def show_cli_help():
    """Display comprehensive CLI help documentation"""
    
    print("🚀 AutoDevCore CLI Help Documentation")
    print("=" * 60)
    print("Comprehensive guide for command-line usage")
    
    # Basic Commands
    basic_commands = """
🚀 Basic Commands

Starting AutoDevCore:
  python main.py                    # Start the main application
  python main.py --config config.yaml  # Start with specific configuration
  python main.py --debug            # Start in debug mode

GPT-OSS Integration:
  python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.get_cache_stats())"
  python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.test_connection())"
  python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.generate_response('Write a Python function'))"
"""
    print_section("🚀 Basic Commands", basic_commands)
    
    # Project Management
    project_commands = """
🎯 Project Management Commands

Creating Projects:
  python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('MyApp', 'A simple web application')"
  python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('MyApp', 'FastAPI web app', framework='fastapi')"
  python -c "from agents.security_generator import SecurityGeneratorAgent; sec = SecurityGeneratorAgent(); sec.generate_security_features('MyApp')"

Managing Projects:
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_projects())"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.get_project_status('MyApp'))"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.delete_project('MyApp')"
"""
    print_section("🎯 Project Management", project_commands)
    
    # AI Operations
    ai_commands = """
🤖 AI Operations Commands

Multi-Model AI:
  python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.generate_response('Create a REST API'))"
  python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.generate_app_plan('E-commerce platform'))"
  python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.analyze_code('path/to/code.py'))"

Performance Monitoring:
  python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.get_dashboard_data())"
  python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.run_health_checks())"
  python -c "from utils.performance_monitor import performance_monitor; print(performance_monitor.get_performance_report())"
"""
    print_section("🤖 AI Operations", ai_commands)
    
    # Plugin Management
    plugin_commands = """
🔧 Plugin Management Commands

Plugin Operations:
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_plugins())"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.install_plugin('plugin_name')"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.uninstall_plugin('plugin_name')"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.search_plugins('ai'))"

Plugin Development:
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.validate_plugin('path/to/plugin.py'))"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.test_plugin('plugin_name'))"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.generate_report())"
"""
    print_section("🔧 Plugin Management", plugin_commands)
    
    # Collaboration
    collaboration_commands = """
👥 Collaboration Commands

Team Management:
  python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); tm.create_team('MyTeam', 'Team description')"
  python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); tm.add_member('MyTeam', 'user@email.com', 'editor')"
  python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); print(tm.get_team_members('MyTeam'))"
  python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); print(tm.has_permission('MyTeam', 'user@email.com', 'edit_project'))"

Collaboration Platform:
  python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); cp.start()"
  python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.create_collaborative_project('MyProject', 'Project description', 'owner@email.com'))"
  python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.invite_to_project('MyProject', 'user@email.com', 'editor'))"
  python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); print(cp.get_project_status('MyProject'))"
"""
    print_section("👥 Collaboration", collaboration_commands)
    
    # Deployment
    deployment_commands = """
🚀 Deployment Commands

CI/CD Pipeline:
  python -c "from plugins.security_auditor import SecurityAuditor; sa = SecurityAuditor(); print(sa.run_full_audit())"
  python -c "from tests.load_test import run_comprehensive_load_test; print(run_comprehensive_load_test())"
  python -c "import subprocess; subprocess.run(['docker', 'build', '-t', 'autodevcore', '.'])"
  python -c "import subprocess; subprocess.run(['docker-compose', 'up', '-d'])"

Performance Optimization:
  python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); print(po.optimize_all())"
  python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); po.clear_cache()"
  python -c "from plugins.performance_integration import PerformanceIntegration; pi = PerformanceIntegration(); print(pi.get_performance_score())"
"""
    print_section("🚀 Deployment", deployment_commands)
    
    # Testing
    testing_commands = """
🔧 Testing Commands

Test Suites:
  python tests/end_to_end_test.py
  python -m pytest tests/ -v
  python -m pytest tests/ --cov=plugins --cov=integrations --cov=agents --cov=utils
  python -m pytest tests/test_collaboration_final.py -v

Load Testing:
  python -c "from tests.load_test import run_comprehensive_load_test; print(run_comprehensive_load_test())"
  python -c "from tests.load_test import run_load_test_scenario; print(run_load_test_scenario('ai_generation', 100))"
  python -c "from tests.load_test import generate_load_test_report; print(generate_load_test_report())"
"""
    print_section("🔧 Testing", testing_commands)
    
    # Utilities
    utility_commands = """
🛠️ Utility Commands

System Information:
  python --version
  pip list
  python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
  python -c "import psutil; print(f'Disk: {psutil.disk_usage(\"/\").percent}%')"

Configuration:
  python -c "import os; print([k for k in os.environ.keys() if 'AUTO' in k.upper()])"
  python -c "from config.settings import validate_config; print(validate_config())"
  python -c "from config.settings import export_config; export_config('config_backup.yaml')"
"""
    print_section("🛠️ Utilities", utility_commands)
    
    # Emergency Commands
    emergency_commands = """
🚨 Emergency Commands

Recovery Operations:
  pkill -f "python.*main.py"
  pkill -f "streamlit"
  pkill -f "ollama"
  python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); po.clear_all_caches()"
  python -c "from config.settings import reset_config; reset_config()"
  python -c "from utils.backup import backup_all_data; backup_all_data('backup_$(date +%Y%m%d_%H%M%S).tar.gz')"
"""
    print_section("🚨 Emergency Commands", emergency_commands)
    
    # Pro Tips
    pro_tips = """
💡 Pro Tips

Command Aliases (add to ~/.bashrc or ~/.zshrc):
  alias autodev="python main.py"
  alias autodev-gui="python run_gui.py"
  alias autodev-test="python -m pytest tests/ -v"
  alias autodev-cache="python -c \"from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.get_cache_stats())\""
  alias autodev-health="python -c \"from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.run_health_checks())\""

Environment Variables:
  export AUTODEV_DEBUG=true
  export AUTODEV_CONFIG_PATH=/path/to/config
  export AUTODEV_LOG_LEVEL=DEBUG
  export AUTODEV_CACHE_DIR=/path/to/cache

Exit Codes:
  0: Success
  1: General error
  2: Configuration error
  3: Network error
  4: Permission error
  5: Resource error
"""
    print_section("💡 Pro Tips", pro_tips)
    
    print(f"\n{'='*60}")
    print("📚 For more detailed help, visit the GUI help documentation")
    print("🌐 Run: python run_gui.py and click the Help button")
    print(f"{'='*60}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['--help', '-h', 'help']:
            show_cli_help()
        elif command == 'basic':
            print_section("🚀 Basic Commands", """
Starting AutoDevCore:
  python main.py
  python main.py --debug

GPT-OSS Integration:
  python -c "from integrations.gpt_oss import gpt_oss_client; print(gpt_oss_client.get_cache_stats())"
            """)
        elif command == 'projects':
            print_section("🎯 Project Management", """
Creating Projects:
  python -c "from agents.code_generator import CodeGeneratorAgent; gen = CodeGeneratorAgent(); gen.generate_codebase('MyApp', 'A simple web application')"

Managing Projects:
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_projects())"
            """)
        elif command == 'ai':
            print_section("🤖 AI Operations", """
Multi-Model AI:
  python -c "from plugins.ai_orchestrator import AIOrchestrator; ai = AIOrchestrator(); print(ai.generate_response('Create a REST API'))"

Performance Monitoring:
  python -c "from plugins.monitoring_dashboard import MonitoringDashboard; md = MonitoringDashboard(); print(md.get_dashboard_data())"
            """)
        elif command == 'plugins':
            print_section("🔧 Plugin Management", """
Plugin Operations:
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); print(pm.list_plugins())"
  python -c "from plugins.plugin_manager import PluginManager; pm = PluginManager(); pm.install_plugin('plugin_name')"
            """)
        elif command == 'collaboration':
            print_section("👥 Collaboration", """
Team Management:
  python -c "from plugins.team_manager import TeamManager; tm = TeamManager(); tm.create_team('MyTeam', 'Team description')"

Collaboration Platform:
  python -c "from plugins.collaboration_platform import CollaborationPlatform; cp = CollaborationPlatform(); cp.start()"
            """)
        elif command == 'deploy':
            print_section("🚀 Deployment", """
CI/CD Pipeline:
  python -c "from plugins.security_auditor import SecurityAuditor; sa = SecurityAuditor(); print(sa.run_full_audit())"

Performance Optimization:
  python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); print(po.optimize_all())"
            """)
        elif command == 'testing':
            print_section("🔧 Testing", """
Test Suites:
  python tests/end_to_end_test.py
  python -m pytest tests/ -v

Load Testing:
  python -c "from tests.load_test import run_comprehensive_load_test; print(run_comprehensive_load_test())"
            """)
        elif command == 'utilities':
            print_section("🛠️ Utilities", """
System Information:
  python --version
  pip list
  python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
            """)
        elif command == 'emergency':
            print_section("🚨 Emergency Commands", """
Recovery Operations:
  pkill -f "python.*main.py"
  pkill -f "streamlit"
  pkill -f "ollama"
  python -c "from plugins.performance_optimizer import PerformanceOptimizer; po = PerformanceOptimizer(); po.clear_all_caches()"
            """)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: basic, projects, ai, plugins, collaboration, deploy, testing, utilities, emergency")
            print("Use --help for full documentation")
    else:
        show_cli_help()

if __name__ == "__main__":
    main()
