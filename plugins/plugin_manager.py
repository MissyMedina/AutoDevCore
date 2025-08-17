#!/usr/bin/env python3
"""
Plugin Manager - Advanced plugin management with validation and testing
"""

import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

class PluginValidator:
    """Validate plugins for security and functionality."""

    def __init__(self):
        self.forbidden_modules = {
            "os",
            "subprocess",
            "sys",
            "eval",
            "exec",
            "globals",
            "locals",
            "open",
            "file",
            "input",
            "raw_input",
            "__import__",
        }

        self.required_functions = ["run"]
        self.max_file_size = 1024 * 1024  # 1MB
        self.max_complexity = 10

    def validate_plugin(self, plugin_path: Path) -> Tuple[bool, List[str]]:
        """Validate a plugin file."""
        errors = []

        # Check file size
        if plugin_path.stat().st_size > self.max_file_size:
            errors.append(f"Plugin file too large: {plugin_path.stat().st_size} bytes")

        # Read and parse the file
        try:
            with open(plugin_path, "r") as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Check for forbidden imports
            import_errors = self._check_imports(tree)
            errors.extend(import_errors)

            # Check for required functions
            function_errors = self._check_functions(tree)
            errors.extend(function_errors)

            # Check complexity
            complexity_errors = self._check_complexity(tree)
            errors.extend(complexity_errors)

            # Check for dangerous operations
            security_errors = self._check_security(tree)
            errors.extend(security_errors)

        except Exception as e:
            errors.append(f"Failed to parse plugin: {e}")

        return len(errors) == 0, errors

    def _check_imports(self, tree: ast.AST) -> List[str]:
        """Check for forbidden imports."""
        errors = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.forbidden_modules:
                        errors.append(f"Forbidden import: {alias.name}")

            elif isinstance(node, ast.ImportFrom):
                if node.module in self.forbidden_modules:
                    errors.append(f"Forbidden import: {node.module}")

        return errors

    def _check_functions(self, tree: ast.AST) -> List[str]:
        """Check for required functions."""
        errors = []
        found_functions = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                found_functions.add(node.name)

        for required_func in self.required_functions:
            if required_func not in found_functions:
                errors.append(f"Missing required function: {required_func}")

        return errors

    def _check_complexity(self, tree: ast.AST) -> List[str]:
        """Check code complexity."""
        errors = []
        complexity = 0

        for node in ast.walk(tree):
            if isinstance(
                node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)
            ):
                complexity += 1

        if complexity > self.max_complexity:
            errors.append(
                f"Code too complex: {complexity} control structures (max: {self.max_complexity})"
            )

        return errors

    def _check_security(self, tree: ast.AST) -> List[str]:
        """Check for security issues."""
        errors = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.forbidden_modules:
                        errors.append(f"Dangerous function call: {node.func.id}")
                elif isinstance(node.func, ast.Attribute):
                    if node.func.attr in ["eval", "exec", "compile"]:
                        errors.append(f"Dangerous function call: {node.func.attr}")

        return errors

class PluginTester:
    """Test plugins for functionality."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def test_plugin(self, plugin_path: Path) -> Tuple[bool, Dict[str, Any]]:
        """Test a plugin for basic functionality."""
        try:
            # Load the plugin
            spec = importlib.util.spec_from_file_location(plugin_path.stem, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Test the run function
            if hasattr(module, "run"):
                start_time = datetime.now()

                try:
                    result = module.run()
                    end_time = datetime.now()

                    test_result = {
                        "success": True,
                        "execution_time": (end_time - start_time).total_seconds(),
                        "result_type": type(result).__name__,
                        "result_keys": (
                            list(result.keys()) if isinstance(result, dict) else None
                        ),
                        "error": None,
                    }

                    return True, test_result

                except Exception as e:
                    test_result = {
                        "success": False,
                        "execution_time": 0,
                        "result_type": None,
                        "result_keys": None,
                        "error": str(e),
                    }

                    return False, test_result
            else:
                return False, {"error": "No run function found"}

        except Exception as e:
            return False, {"error": f"Failed to load plugin: {e}"}

class DependencyManager:
    """Manage plugin dependencies."""

    def __init__(self):
        self.dependency_cache = {}

    def check_dependencies(self, plugin_path: Path) -> Dict[str, Any]:
        """Check if plugin dependencies are available."""
        try:
            with open(plugin_path, "r") as f:
                content = f.read()

            dependencies = self._extract_dependencies(content)
            status = {}

            for dep in dependencies:
                try:
                    importlib.import_module(dep)
                    status[dep] = {"available": True, "version": self._get_version(dep)}
                except ImportError:
                    status[dep] = {"available": False, "version": None}

            return status

        except Exception as e:
            return {"error": str(e)}

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from plugin content."""
        dependencies = []
        lines = content.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("import "):
                module = line.split("import ")[1].split()[0]
                dependencies.append(module)
            elif line.startswith("from ") and " import " in line:
                module = line.split("from ")[1].split(" import ")[0]
                dependencies.append(module)

        return list(set(dependencies))

    def _get_version(self, module_name: str) -> Optional[str]:
        """Get version of an installed module."""
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "__version__"):
                return module.__version__
            return "unknown"
        except:
            return None

    def install_dependency(self, dependency: str) -> bool:
        """Install a dependency using pip."""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
            return True
        except subprocess.CalledProcessError:
            return False

class PluginManager:
    """Advanced plugin manager with validation, testing, and dependency management."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)

        self.validator = PluginValidator()
        self.tester = PluginTester()
        self.dependency_manager = DependencyManager()

        self.plugin_registry = {}
        self.load_registry()

    def load_registry(self):
        """Load plugin registry from file."""
        registry_file = self.plugins_dir / "plugin_registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, "r") as f:
                    self.plugin_registry = json.load(f)
            except:
                self.plugin_registry = {}

    def save_registry(self):
        """Save plugin registry to file."""
        registry_file = self.plugins_dir / "plugin_registry.json"
        with open(registry_file, "w") as f:
            json.dump(self.plugin_registry, f, indent=2)

    def discover_plugins(self) -> List[Dict[str, Any]]:
        """Discover and analyze all plugins."""
        plugins = []

        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name == "__init__.py":
                continue

            plugin_info = self.analyze_plugin(plugin_file)
            if plugin_info:
                plugins.append(plugin_info)

        return plugins

    def analyze_plugin(self, plugin_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a plugin file comprehensively."""
        try:
            # Basic file info
            stat = plugin_path.stat()
            file_hash = self._calculate_file_hash(plugin_path)

            plugin_info = {
                "name": plugin_path.stem,
                "file_path": str(plugin_path),
                "size_bytes": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_hash": file_hash,
                "status": "unknown",
            }

            # Validate plugin
            is_valid, validation_errors = self.validator.validate_plugin(plugin_path)
            plugin_info["validation"] = {
                "is_valid": is_valid,
                "errors": validation_errors,
            }

            # Test plugin
            test_passed, test_result = self.tester.test_plugin(plugin_path)
            plugin_info["testing"] = test_result

            # Check dependencies
            dependencies = self.dependency_manager.check_dependencies(plugin_path)
            plugin_info["dependencies"] = dependencies

            # Determine overall status
            if is_valid and test_passed:
                plugin_info["status"] = "ready"
            elif is_valid:
                plugin_info["status"] = "test_failed"
            else:
                plugin_info["status"] = "invalid"

            # Extract metadata
            metadata = self._extract_metadata(plugin_path)
            plugin_info.update(metadata)

            return plugin_info

        except Exception as e:
            print(f"Error analyzing plugin {plugin_path}: {e}")
            return None

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _extract_metadata(self, plugin_path: Path) -> Dict[str, Any]:
        """Extract metadata from plugin file."""
        try:
            with open(plugin_path, "r") as f:
                content = f.read()

            metadata = {
                "description": "No description available",
                "version": "1.0.0",
                "author": "Unknown",
                "categories": ["Utility"],
                "tags": [],
            }

            lines = content.split("\n")
            for line in lines:
                line = line.strip()

                # Extract description
                if "description" in line.lower() and ("#" in line or '"""' in line):
                    if "#" in line:
                        metadata["description"] = line.split("#")[1].strip()
                    elif '"""' in line:
                        metadata["description"] = line.split('"""')[1].strip()

                # Extract version
                if "version" in line.lower() and "=" in line:
                    metadata["version"] = line.split("=")[1].strip().strip("\"'")

                # Extract author
                if "author" in line.lower() and "=" in line:
                    metadata["author"] = line.split("=")[1].strip().strip("\"'")

                # Extract categories
                if "category" in line.lower() or "categories" in line.lower():
                    if "security" in line.lower():
                        metadata["categories"].append("Security")
                    if "analysis" in line.lower():
                        metadata["categories"].append("Analysis")
                    if "generation" in line.lower():
                        metadata["categories"].append("Generation")

            return metadata

        except Exception as e:
            print(f"Error extracting metadata from {plugin_path}: {e}")
            return {
                "description": "No description available",
                "version": "1.0.0",
                "author": "Unknown",
                "categories": ["Utility"],
                "tags": [],
            }

    def install_plugin(self, plugin_name: str) -> bool:
        """Install a plugin (add to registry)."""
        plugin_path = self.plugins_dir / f"{plugin_name}.py"

        if not plugin_path.exists():
            print(f"❌ Plugin {plugin_name} not found")
            return False

        plugin_info = self.analyze_plugin(plugin_path)
        if plugin_info and plugin_info["status"] == "ready":
            self.plugin_registry[plugin_name] = plugin_info
            self.save_registry()
            print(f"✅ Plugin {plugin_name} installed successfully")
            return True
        else:
            print(f"❌ Plugin {plugin_name} failed validation or testing")
            return False

    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin (remove from registry)."""
        if plugin_name in self.plugin_registry:
            del self.plugin_registry[plugin_name]
            self.save_registry()
            print(f"✅ Plugin {plugin_name} uninstalled successfully")
            return True
        else:
            print(f"❌ Plugin {plugin_name} not found in registry")
            return False

    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin."""
        return self.plugin_registry.get(plugin_name)

    def list_plugins(self, status_filter: str = None) -> List[Dict[str, Any]]:
        """List plugins with optional status filtering."""
        plugins = list(self.plugin_registry.values())

        if status_filter:
            plugins = [p for p in plugins if p.get("status") == status_filter]

        return plugins

    def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """Search plugins by name, description, or category."""
        plugins = list(self.plugin_registry.values())
        results = []

        query_lower = query.lower()

        for plugin in plugins:
            if (
                query_lower in plugin.get("name", "").lower()
                or query_lower in plugin.get("description", "").lower()
                or any(
                    query_lower in cat.lower() for cat in plugin.get("categories", [])
                )
            ):
                results.append(plugin)

        return results

    def update_plugin(self, plugin_name: str) -> bool:
        """Update plugin information."""
        plugin_path = self.plugins_dir / f"{plugin_name}.py"

        if plugin_path.exists():
            plugin_info = self.analyze_plugin(plugin_path)
            if plugin_info:
                self.plugin_registry[plugin_name] = plugin_info
                self.save_registry()
                print(f"✅ Plugin {plugin_name} updated successfully")
                return True

        return False

    def get_plugin_categories(self) -> List[str]:
        """Get all available plugin categories."""
        categories = set()

        for plugin in self.plugin_registry.values():
            categories.update(plugin.get("categories", []))

        return sorted(list(categories))

    def generate_report(self) -> str:
        """Generate a comprehensive plugin report."""
        plugins = list(self.plugin_registry.values())

        report = f"""
# AutoDevCore Plugin Report
Generated: {datetime.now().isoformat()}

## Summary
- **Total Plugins**: {len(plugins)}
- **Ready**: {len([p for p in plugins if p.get('status') == 'ready'])}
- **Test Failed**: {len([p for p in plugins if p.get('status') == 'test_failed'])}
- **Invalid**: {len([p for p in plugins if p.get('status') == 'invalid'])}

## Categories
"""

        categories = self.get_plugin_categories()
        for category in categories:
            category_plugins = [
                p for p in plugins if category in p.get("categories", [])
            ]
            report += f"- **{category}**: {len(category_plugins)} plugins\n"

        report += "\n## Plugin Details\n"

        for plugin in plugins:
            status_emoji = (
                "✅"
                if plugin.get("status") == "ready"
                else "⚠️" if plugin.get("status") == "test_failed" else "❌"
            )
            report += f"""
### {status_emoji} {plugin.get('name')}
- **Status**: {plugin.get('status')}
- **Version**: {plugin.get('version')}
- **Author**: {plugin.get('author')}
- **Description**: {plugin.get('description')}
- **Categories**: {', '.join(plugin.get('categories', []))}
- **Size**: {plugin.get('size_bytes')} bytes
- **Last Modified**: {plugin.get('last_modified')}
"""

        return report

def run(context=None):
    """Plugin manager entry point."""
    manager = PluginManager()

    # Discover and analyze all plugins
    plugins = manager.discover_plugins()

    return {
        "status": "success",
        "message": f"Plugin manager initialized with {len(plugins)} plugins",
        "data": {
            "total_plugins": len(plugins),
            "ready_plugins": len([p for p in plugins if p.get("status") == "ready"]),
            "categories": manager.get_plugin_categories(),
            "plugins": plugins[:5],  # Return first 5 plugins
            "timestamp": datetime.now().isoformat(),
        },
    }
