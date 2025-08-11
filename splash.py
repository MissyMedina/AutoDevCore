"""
Splash screen and help display for AutoDevCore.
"""

from datetime import datetime

def show_splash():
    """Display the AutoDevCore splash banner."""
    splash = """
    ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                                          ║
    ║      .o.                       .             oooooooooo.                           .oooooo.             ║
    ║     .888.                    .o8             `888'   `Y8b                         d8P'  `Y8b            ║
    ║    .8"888.     oooo  oooo  .o888oo  .ooooo.   888      888  .ooooo.  oooo    ooo 888           .ooooo. ║
    ║   .8' `888.    `888  `888    888   d88' `88b  888      888 d88' `88b  `88.  .8'  888          d88' `88b║
    ║  .88ooo8888.    888   888    888   888   888  888      888 888ooo888   `88..8'   888          888   888║
    ║ .8'     `888.   888   888    888 . 888   888  888     d88' 888    .o    `888'    `88b    ooo  888   888║
    ║o88o     o8888o  `V88V"V8P'   "888" `Y8bod8P' o888bood8P'   `Y8bod8P'     `8'      `Y8bood8P'  `Y8bod8P'║
    ║                                                                                                          ║
    ║                    Modular AI agents that build smarter, score deeper                                    ║
    ║                                                                                                          ║
    ║                              The core of intelligent development                                         ║
    ║                                                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(splash)
    print(f"🚀 AutoDevCore v1.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

def show_help():
    """Display help information."""
    help_text = """
    🎯 AutoDevCore - The core of intelligent development
    
    USAGE:
        python cli.py --mode <mode> [options]
    
    MODES:
        compose    - Generate complete applications from ideas
        journal    - Analyze codebases and generate insights
        blueprint  - Create architecture diagrams from code
        score      - Evaluate applications against templates
        plugin     - Execute custom plugins
    
    EXAMPLES:
        python cli.py --mode compose --idea "task management app" --output-dir ./myapp
        python cli.py --mode score --app-dir ./myapp --template fintech
        python cli.py --mode plugin --name ascii_weather
    
    OPTIONS:
        --verbose     - Enable verbose output
        --help        - Show this help message
    
    FEATURES:
        🤖 GPT-OSS Integration - Local AI-powered reasoning
        🧠 Agent Thought Trails - Track AI reasoning steps
        📊 App Personality Scoring - Industry-specific evaluation
        🔌 Plugin System - Extensible functionality
        📈 Architecture Diagrams - Visual code analysis
    """
    print(help_text)
