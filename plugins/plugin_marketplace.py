#!/usr/bin/env python3
"""
Plugin Marketplace - Enhanced plugin ecosystem for AutoDevCore
"""

import json
import requests
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PluginMarketplace:
    """Plugin marketplace for discovering, installing, and managing plugins."""
    
    def __init__(self, marketplace_url: str = "https://api.github.com/repos/MissyMedina/AutoDevCore-Plugins/contents"):
        self.marketplace_url = marketplace_url
        self.plugins_dir = Path("plugins")
        self.registry_file = Path("plugins/plugin_registry.json")
        self.plugins_dir.mkdir(exist_ok=True)
        self._load_registry()
    
    def _load_registry(self):
        """Load the local plugin registry."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    self.registry = json.load(f)
            except:
                self.registry = {"plugins": {}, "last_updated": None}
        else:
            self.registry = {"plugins": {}, "last_updated": None}
    
    def _save_registry(self):
        """Save the local plugin registry."""
        self.registry["last_updated"] = datetime.now().isoformat()
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def discover_plugins(self, category: str = None, search_term: str = None) -> List[Dict[str, Any]]:
        """Discover available plugins from the marketplace."""
        try:
            # For now, return local plugins. In the future, this would fetch from remote marketplace
            plugins = []
            
            for plugin_file in self.plugins_dir.glob("*.py"):
                if plugin_file.name == "__init__.py":
                    continue
                
                plugin_info = self._analyze_plugin_file(plugin_file)
                if plugin_info:
                    # Apply filters
                    if category and category.lower() not in plugin_info.get("categories", []):
                        continue
                    if search_term and search_term.lower() not in plugin_info.get("name", "").lower():
                        continue
                    
                    plugins.append(plugin_info)
            
            return plugins
            
        except Exception as e:
            print(f"Error discovering plugins: {e}")
            return []
    
    def _analyze_plugin_file(self, plugin_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a plugin file to extract metadata."""
        try:
            with open(plugin_path, 'r') as f:
                content = f.read()
            
            # Extract plugin metadata from docstring or comments
            plugin_info = {
                "name": plugin_path.stem,
                "file_path": str(plugin_path),
                "size_bytes": plugin_path.stat().st_size,
                "last_modified": datetime.fromtimestamp(plugin_path.stat().st_mtime).isoformat(),
                "categories": self._extract_categories(content),
                "description": self._extract_description(content),
                "version": self._extract_version(content),
                "author": self._extract_author(content),
                "dependencies": self._extract_dependencies(content),
                "status": "installed"
            }
            
            return plugin_info
            
        except Exception as e:
            print(f"Error analyzing plugin {plugin_path}: {e}")
            return None
    
    def _extract_categories(self, content: str) -> List[str]:
        """Extract categories from plugin content."""
        categories = []
        lines = content.split('\n')
        
        for line in lines:
            if 'category' in line.lower() or 'categories' in line.lower():
                # Look for category information in comments or docstrings
                if '#' in line or '"""' in line or "'''" in line:
                    # Extract categories from the line
                    if 'security' in line.lower():
                        categories.append('Security')
                    if 'utility' in line.lower():
                        categories.append('Utility')
                    if 'analysis' in line.lower():
                        categories.append('Analysis')
                    if 'generation' in line.lower():
                        categories.append('Generation')
        
        return categories if categories else ['Utility']
    
    def _extract_description(self, content: str) -> str:
        """Extract description from plugin content."""
        lines = content.split('\n')
        
        for line in lines:
            if 'description' in line.lower() and ('#' in line or '"""' in line):
                # Extract description from comment or docstring
                if '#' in line:
                    return line.split('#')[1].strip()
                elif '"""' in line:
                    return line.split('"""')[1].strip()
        
        return "No description available"
    
    def _extract_version(self, content: str) -> str:
        """Extract version from plugin content."""
        lines = content.split('\n')
        
        for line in lines:
            if 'version' in line.lower() and ('#' in line or '=' in line):
                if '=' in line:
                    return line.split('=')[1].strip().strip('"\'')
        
        return "1.0.0"
    
    def _extract_author(self, content: str) -> str:
        """Extract author from plugin content."""
        lines = content.split('\n')
        
        for line in lines:
            if 'author' in line.lower() and ('#' in line or '=' in line):
                if '=' in line:
                    return line.split('=')[1].strip().strip('"\'')
        
        return "Unknown"
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from plugin content."""
        dependencies = []
        lines = content.split('\n')
        
        for line in lines:
            if 'import' in line or 'from' in line:
                # Extract import statements
                if 'import ' in line:
                    module = line.split('import ')[1].split()[0]
                    dependencies.append(module)
                elif 'from ' in line and ' import ' in line:
                    module = line.split('from ')[1].split(' import ')[0]
                    dependencies.append(module)
        
        return list(set(dependencies))
    
    def install_plugin(self, plugin_name: str) -> bool:
        """Install a plugin from the marketplace."""
        try:
            # For now, just validate that the plugin exists locally
            plugin_path = self.plugins_dir / f"{plugin_name}.py"
            
            if not plugin_path.exists():
                print(f"❌ Plugin {plugin_name} not found")
                return False
            
            # Add to registry
            plugin_info = self._analyze_plugin_file(plugin_path)
            if plugin_info:
                self.registry["plugins"][plugin_name] = plugin_info
                self._save_registry()
                print(f"✅ Plugin {plugin_name} installed successfully")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error installing plugin {plugin_name}: {e}")
            return False
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin."""
        try:
            plugin_path = self.plugins_dir / f"{plugin_name}.py"
            
            if plugin_path.exists():
                # Remove from registry
                if plugin_name in self.registry["plugins"]:
                    del self.registry["plugins"][plugin_name]
                    self._save_registry()
                
                print(f"✅ Plugin {plugin_name} uninstalled successfully")
                return True
            
            print(f"❌ Plugin {plugin_name} not found")
            return False
            
        except Exception as e:
            print(f"Error uninstalling plugin {plugin_name}: {e}")
            return False
    
    def list_installed_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins."""
        return list(self.registry["plugins"].values())
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin."""
        return self.registry["plugins"].get(plugin_name)
    
    def update_plugin(self, plugin_name: str) -> bool:
        """Update a plugin to the latest version."""
        try:
            # For now, just re-analyze the plugin file
            plugin_path = self.plugins_dir / f"{plugin_name}.py"
            
            if plugin_path.exists():
                plugin_info = self._analyze_plugin_file(plugin_path)
                if plugin_info:
                    self.registry["plugins"][plugin_name] = plugin_info
                    self._save_registry()
                    print(f"✅ Plugin {plugin_name} updated successfully")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error updating plugin {plugin_name}: {e}")
            return False
    
    def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """Search for plugins by name, description, or category."""
        plugins = self.discover_plugins()
        results = []
        
        query_lower = query.lower()
        
        for plugin in plugins:
            if (query_lower in plugin.get("name", "").lower() or
                query_lower in plugin.get("description", "").lower() or
                any(query_lower in cat.lower() for cat in plugin.get("categories", []))):
                results.append(plugin)
        
        return results
    
    def get_plugin_categories(self) -> List[str]:
        """Get all available plugin categories."""
        plugins = self.discover_plugins()
        categories = set()
        
        for plugin in plugins:
            categories.update(plugin.get("categories", []))
        
        return sorted(list(categories))


def run(context=None):
    """Plugin marketplace entry point."""
    marketplace = PluginMarketplace()
    
    # Discover available plugins
    plugins = marketplace.discover_plugins()
    
    return {
        "status": "success",
        "message": f"Plugin marketplace initialized with {len(plugins)} plugins",
        "data": {
            "total_plugins": len(plugins),
            "categories": marketplace.get_plugin_categories(),
            "plugins": plugins[:5],  # Return first 5 plugins
            "timestamp": datetime.now().isoformat()
        }
    }
