"""
Plugin Mode - Execute custom plugins
"""

import importlib.util
import sys
from pathlib import Path
from .base import BaseMode


class PluginMode(BaseMode):
    """Plugin mode for executing custom plugins."""
    
    def __init__(self, name: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.name = name
    
    def execute(self):
        """Execute the plugin mode."""
        print(f"🧩 Plugin Mode - Custom Plugin Execution")
        print(f"🔌 Plugin: {self.name}")
        print()
        
        # Find and load the plugin
        self.log_thought("PluginAgent", f"Loading plugin: {self.name}")
        plugin = self._load_plugin()
        
        if not plugin:
            print(f"❌ Error: Could not load plugin {self.name}")
            return
        
        self.log_thought("PluginAgent", "Plugin loaded successfully")
        
        # Execute the plugin
        self.log_thought("PluginAgent", "Executing plugin")
        try:
            result = plugin.run("AutoDevCore plugin execution")
            self.log_thought("PluginAgent", "Plugin executed successfully", {"result": result})
        except Exception as e:
            self.log_thought("PluginAgent", f"Plugin execution failed: {e}")
            print(f"❌ Plugin execution failed: {e}")
            return
        
        # Save thought trail
        self.save_thought_trail()
        self.generate_mermaid_diagram()
        
        print("✅ Plugin execution complete!")
        print(f"📄 Results saved to: {self.output_dir}")
    
    def _load_plugin(self):
        """Load a plugin from the plugins directory."""
        # Try to find the plugin file
        plugin_path = Path("plugins") / f"{self.name}.py"
        
        if not plugin_path.exists():
            print(f"Plugin not found: {plugin_path}")
            return None
        
        try:
            # Load the plugin module
            spec = importlib.util.spec_from_file_location(self.name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if the plugin has a run function
            if hasattr(module, 'run'):
                return module
            else:
                print(f"Plugin {self.name} does not have a 'run' function")
                return None
                
        except Exception as e:
            print(f"Error loading plugin {self.name}: {e}")
            return None
