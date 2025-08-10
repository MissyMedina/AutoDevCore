#!/usr/bin/env python3
"""
AutoDevCore CLI - Modular AI agents that build smarter, score deeper.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from splash import show_splash
from modes.compose import ComposeMode
from modes.journal import JournalMode
from modes.blueprint import BlueprintMode
from modes.score import ScoreMode
from modes.plugin import PluginMode


def main():
    """Main CLI entry point for AutoDevCore."""
    
    # Show splash screen
    show_splash()
    
    parser = argparse.ArgumentParser(
        description="AutoDevCore - Modular AI agents that build smarter, score deeper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./autodevcore --mode compose --idea "restaurant inventory manager"
  ./autodevcore --mode journal
  ./autodevcore --mode blueprint --path ./legacy_codebase
  ./autodevcore --mode score --app-dir ./myapp --template profiles/fintech.yaml
  ./autodevcore --mode plugin --name ascii_weather
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["compose", "journal", "blueprint", "score", "plugin"],
        required=True,
        help="Operation mode"
    )
    
    parser.add_argument(
        "--idea",
        type=str,
        help="App idea description (for compose mode)"
    )
    
    parser.add_argument(
        "--path",
        type=str,
        help="Path to codebase (for blueprint mode)"
    )
    
    parser.add_argument(
        "--template",
        type=str,
        help="Scoring template profile (for score mode)"
    )
    
    parser.add_argument(
        "--app-dir",
        type=str,
        help="App directory to score (for score mode)"
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help="Plugin name (for plugin mode)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory for generated files"
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize the appropriate mode
    if args.mode == "compose":
        if not args.idea:
            print("Error: --idea is required for compose mode")
            sys.exit(1)
        mode = ComposeMode(args.idea, args.output_dir, args.verbose)
        
    elif args.mode == "journal":
        mode = JournalMode(args.output_dir, args.verbose)
        
    elif args.mode == "blueprint":
        if not args.path:
            print("Error: --path is required for blueprint mode")
            sys.exit(1)
        mode = BlueprintMode(args.path, args.output_dir, args.verbose)
        
    elif args.mode == "score":
        if not args.template:
            print("Error: --template is required for score mode")
            sys.exit(1)
        if not args.app_dir:
            print("Error: --app-dir is required for score mode")
            sys.exit(1)
        mode = ScoreMode(args.app_dir, args.template, args.output_dir, args.verbose)
        
    elif args.mode == "plugin":
        if not args.name:
            print("Error: --name is required for plugin mode")
            sys.exit(1)
        mode = PluginMode(args.name, args.output_dir, args.verbose)
    
    # Execute the mode
    try:
        mode.execute()
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
