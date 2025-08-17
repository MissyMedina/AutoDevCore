#!/usr/bin/env python3
"""
Simple AutoDevCore GUI Launcher
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Launch the GUI with the correct Python environment"""
    print("🚀 Launching AutoDevCore GUI with Python 3.12...")

    # Get the project root
    project_root = Path(__file__).parent

    # Check if virtual environment exists
    venv_path = project_root / "gui_env"
    if not venv_path.exists():
        print("❌ Virtual environment not found. Creating...")
        subprocess.run([sys.executable, "-m", "venv", "gui_env"], check=True)
        print("✅ Virtual environment created")

    # Activate virtual environment and run GUI
    if os.name == "nt":  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"

    print(f"🐍 Using Python: {python_exe}")
    print("🌐 Starting Streamlit server...")
    print("📱 The GUI will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Run streamlit with the virtual environment Python
        subprocess.run(
            [
                str(python_exe),
                "-m",
                "streamlit",
                "run",
                "test_gui.py",
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
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
