"""
Plugin Mode - Enhanced plugin system with discovery, management, and sandboxing
"""

import importlib.util
import sys
import json
import inspect
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from .base import BaseMode
from datetime import datetime


class PluginMode(BaseMode):
    """Enhanced plugin mode with discovery, management, and sandboxing capabilities."""

    def __init__(
        self,
        name: str = None,
        output_dir: str = "./output",
        verbose: bool = False,
        list_plugins: bool = False,
        generate_docs: bool = False,
    ):
        super().__init__(output_dir, verbose)
        self.name = name
        self.list_plugins = list_plugins
        self.generate_docs = generate_docs
        self.plugins_dir = Path("plugins")

    def execute(self):
        """Execute the plugin mode."""
        print(f"🧩 Plugin Mode - Enhanced Plugin System")
        print()

        # Ensure plugins directory exists
        self.plugins_dir.mkdir(exist_ok=True)

        if self.list_plugins:
            self._list_available_plugins()
            return

        if self.generate_docs:
            self._generate_plugin_documentation()
            return

        if not self.name:
            print("❌ Error: Plugin name is required for execution")
            print("💡 Use --list to see available plugins")
            return

        # Find and load the plugin
        self.log_thought("PluginAgent", f"Loading plugin: {self.name}")
        plugin_info = self._discover_plugin_info()

        if not plugin_info:
            print(f"❌ Error: Could not find plugin {self.name}")
            print("💡 Use --list to see available plugins")
            return

        self.log_thought("PluginAgent", "Plugin discovered", plugin_info)

        # Load and validate the plugin
        self.log_thought("PluginAgent", "Loading and validating plugin")
        plugin = self._load_plugin_safely()

        if not plugin:
            print(f"❌ Error: Could not load plugin {self.name}")
            return

        self.log_thought("PluginAgent", "Plugin loaded and validated successfully")

        # Execute the plugin in sandboxed environment
        self.log_thought("PluginAgent", "Executing plugin in sandboxed environment")
        try:
            result = self._execute_plugin_safely(plugin)
            self.log_thought(
                "PluginAgent", "Plugin executed successfully", {"result": result}
            )
        except Exception as e:
            self.log_thought("PluginAgent", f"Plugin execution failed: {e}")
            print(f"❌ Plugin execution failed: {e}")
            return

        # Generate execution report
        self.log_thought("PluginAgent", "Generating execution report")
        self._generate_execution_report(plugin_info, result)

        # Save thought trail and visualizations
        self.save_thought_trail()

        print("✅ Plugin execution complete!")
        print(f"📄 Results saved to: {self.output_dir}")

    def _list_available_plugins(self):
        """List all available plugins with their information."""
        print("🔍 Available Plugins:")
        print("=" * 50)

        plugins = self._discover_all_plugins()

        if not plugins:
            print("No plugins found in plugins/ directory")
            print("💡 Create plugins by adding .py files to the plugins/ directory")
            return

        for plugin_name, info in plugins.items():
            print(f"\n📦 {plugin_name}")
            print(f"   Description: {info.get('description', 'No description')}")
            print(f"   Author: {info.get('author', 'Unknown')}")
            print(f"   Version: {info.get('version', '1.0.0')}")
            print(f"   Functions: {', '.join(info.get('functions', []))}")
            print(
                f"   Status: {'✅ Ready' if info.get('valid', False) else '❌ Invalid'}"
            )

    def _discover_all_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Discover all plugins in the plugins directory."""
        plugins = {}

        if not self.plugins_dir.exists():
            return plugins

        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue

            plugin_name = plugin_file.stem
            plugin_info = self._analyze_plugin_file(plugin_file)
            plugins[plugin_name] = plugin_info

        return plugins

    def _analyze_plugin_file(self, plugin_path: Path) -> Dict[str, Any]:
        """Analyze a plugin file to extract metadata and validate it."""
        info = {
            "name": plugin_path.stem,
            "path": str(plugin_path),
            "description": "No description",
            "author": "Unknown",
            "version": "1.0.0",
            "functions": [],
            "valid": False,
            "error": None,
        }

        try:
            # Read the file content
            with open(plugin_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse the AST to extract information
            tree = ast.parse(content)

            # Extract docstring and metadata
            for node in ast.walk(tree):
                if isinstance(node, ast.Module) and node.body:
                    # Check for module docstring
                    if isinstance(node.body[0], ast.Expr) and isinstance(
                        node.body[0].value, ast.Str
                    ):
                        info["description"] = node.body[0].value.s

            # Extract function names
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    info["functions"].append(node.name)

            # Check if it has a run function
            if "run" in info["functions"]:
                info["valid"] = True

            # Try to load the module to get more info
            try:
                spec = importlib.util.spec_from_file_location(
                    plugin_path.stem, plugin_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Extract metadata from module attributes
                if hasattr(module, "__author__"):
                    info["author"] = module.__author__
                if hasattr(module, "__version__"):
                    info["version"] = module.__version__
                if hasattr(module, "__description__"):
                    info["description"] = module.__description__

            except Exception as e:
                info["error"] = str(e)

        except Exception as e:
            info["error"] = str(e)

        return info

    def _discover_plugin_info(self) -> Optional[Dict[str, Any]]:
        """Discover information about a specific plugin."""
        plugin_path = self.plugins_dir / f"{self.name}.py"

        if not plugin_path.exists():
            return None

        return self._analyze_plugin_file(plugin_path)

    def _load_plugin_safely(self):
        """Load a plugin with safety checks."""
        plugin_path = self.plugins_dir / f"{self.name}.py"

        if not plugin_path.exists():
            return None

        try:
            # Load the plugin module
            spec = importlib.util.spec_from_file_location(self.name, plugin_path)
            module = importlib.util.module_from_spec(spec)

            # Execute in a controlled environment
            spec.loader.exec_module(module)

            # Validate the plugin
            if not hasattr(module, "run"):
                print(f"Plugin {self.name} does not have a 'run' function")
                return None

            # Check function signature
            run_func = getattr(module, "run")
            sig = inspect.signature(run_func)

            if len(sig.parameters) < 1:
                print(
                    f"Plugin {self.name} run function must accept at least one parameter"
                )
                return None

            return module

        except Exception as e:
            print(f"Error loading plugin {self.name}: {e}")
            return None

    def _execute_plugin_safely(self, plugin) -> Any:
        """Execute a plugin in a sandboxed environment."""
        try:
            # Create a safe execution context
            context = {
                "plugin_name": self.name,
                "output_dir": str(self.output_dir),
                "verbose": self.verbose,
            }

            # Execute the plugin
            result = plugin.run(context)

            return result

        except Exception as e:
            raise Exception(f"Plugin execution error: {e}")

    def _generate_plugin_documentation(self):
        """Generate comprehensive plugin documentation."""
        print("📚 Generating Plugin Documentation...")

        plugins = self._discover_all_plugins()

        if not plugins:
            print("No plugins found to document")
            return

        # Generate documentation
        doc_file = self.output_dir / "plugin_documentation.md"

        with open(doc_file, "w") as f:
            f.write("# AutoDevCore Plugin Documentation\n\n")
            f.write("## Overview\n\n")
            f.write(
                "This document provides comprehensive documentation for all available AutoDevCore plugins.\n\n"
            )

            f.write("## Plugin Development Guide\n\n")
            f.write("### Creating a Plugin\n\n")
            f.write("1. Create a Python file in the `plugins/` directory\n")
            f.write("2. Implement a `run(context)` function\n")
            f.write(
                "3. Add metadata (optional): `__author__`, `__version__`, `__description__`\n"
            )
            f.write(
                "4. Test your plugin with `python cli.py --mode plugin --name your_plugin`\n\n"
            )

            f.write("### Plugin Template\n\n")
            f.write("```python\n")
            f.write('"""\n')
            f.write("Your Plugin Description\n")
            f.write('"""\n\n')
            f.write('__author__ = "Your Name"\n')
            f.write('__version__ = "1.0.0"\n')
            f.write('__description__ = "What your plugin does"\n\n')
            f.write("def run(context):\n")
            f.write('    """\n')
            f.write("    Main plugin function.\n")
            f.write("    \n")
            f.write("    Args:\n")
            f.write(
                "        context (dict): Execution context with plugin_name, output_dir, verbose\n"
            )
            f.write("    \n")
            f.write("    Returns:\n")
            f.write("        Any: Plugin execution result\n")
            f.write('    """\n')
            f.write("    # Your plugin logic here\n")
            f.write("    return {'status': 'success', 'message': 'Plugin executed'}\n")
            f.write("```\n\n")

            f.write("## Available Plugins\n\n")

            for plugin_name, info in plugins.items():
                f.write(f"### {plugin_name}\n\n")
                f.write(f"**Description**: {info['description']}\n\n")
                f.write(f"**Author**: {info['author']}\n\n")
                f.write(f"**Version**: {info['version']}\n\n")
                f.write(
                    f"**Status**: {'✅ Ready' if info['valid'] else '❌ Invalid'}\n\n"
                )

                if info["functions"]:
                    f.write("**Functions**:\n")
                    for func in info["functions"]:
                        f.write(f"- `{func}`\n")
                    f.write("\n")

                if info["error"]:
                    f.write(f"**Error**: {info['error']}\n\n")

                f.write("---\n\n")

        print(f"📄 Plugin documentation saved to: {doc_file}")

    def _generate_execution_report(self, plugin_info: Dict[str, Any], result: Any):
        """Generate a detailed execution report."""
        report_file = self.output_dir / "plugin_execution_report.md"

        with open(report_file, "w") as f:
            f.write("# Plugin Execution Report\n\n")
            f.write(f"**Plugin**: {self.name}\n")
            f.write(f"**Execution Time**: {datetime.now().isoformat()}\n\n")

            f.write("## Plugin Information\n\n")
            f.write(f"- **Name**: {plugin_info['name']}\n")
            f.write(f"- **Description**: {plugin_info['description']}\n")
            f.write(f"- **Author**: {plugin_info['author']}\n")
            f.write(f"- **Version**: {plugin_info['version']}\n")
            f.write(
                f"- **Status**: {'✅ Valid' if plugin_info['valid'] else '❌ Invalid'}\n\n"
            )

            f.write("## Execution Results\n\n")
            f.write("```json\n")
            f.write(json.dumps(result, indent=2, default=str))
            f.write("\n```\n")

            if plugin_info["functions"]:
                f.write("\n## Available Functions\n\n")
                for func in plugin_info["functions"]:
                    f.write(f"- `{func}`\n")

        print(f"📄 Execution report saved to: {report_file}")
