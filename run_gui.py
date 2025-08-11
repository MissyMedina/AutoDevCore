#!/usr/bin/env python3
"""
AutoDevCore GUI Launcher
Launches the Streamlit-based Visual Development Hub
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Launch the AutoDevCore GUI"""
    print("🚀 Launching AutoDevCore Visual Development Hub...")

    # Get the project root
    project_root = Path(__file__).parent
    gui_path = project_root / "gui" / "main.py"

    # Check if GUI file exists
    if not gui_path.exists():
        print(f"❌ GUI file not found at: {gui_path}")
        print("Please ensure the GUI is properly installed.")
        return 1

    # Check if streamlit is installed
    try:
        import streamlit

        print(f"✅ Streamlit {streamlit.__version__} found")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "gui/requirements.txt"],
                check=True,
            )
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return 1

    # Launch the GUI
    print("🌐 Starting AutoDevCore GUI...")
    print("📱 The GUI will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Change to project root and run streamlit
        os.chdir(project_root)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(gui_path),
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
                "--browser.gatherUsageStats",
                "false",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 AutoDevCore GUI stopped")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
