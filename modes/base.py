"""
Base Mode Class for AutoDevCore
"""

import json
import os
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod


class BaseMode(ABC):
    """Base class for all AutoDevCore modes."""
    
    def __init__(self, output_dir: str, verbose: bool = False):
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.log_file = self.output_dir / "autodevcore.log"
        self.thought_trail = []
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def log_thought(self, agent: str, thought: str, data: dict = None):
        """Log a thought from an agent."""
        thought_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "thought": thought,
            "data": data or {}
        }
        
        self.thought_trail.append(thought_entry)
        
        if self.verbose:
            print(f"[{agent}] {thought}")
            if data:
                print(f"  Data: {json.dumps(data, indent=2)}")
    
    def save_thought_trail(self):
        """Save the thought trail to JSON file."""
        trail_file = self.output_dir / "thought_trail.json"
        with open(trail_file, 'w') as f:
            json.dump(self.thought_trail, f, indent=2)
        
        print(f"💭 Thought trail saved to: {trail_file}")
    
    def generate_mermaid_diagram(self):
        """Generate a Mermaid diagram from the thought trail."""
        if not self.thought_trail:
            return
        
        mermaid_content = "graph TD\n"
        
        for i, thought in enumerate(self.thought_trail):
            node_id = f"A{i}"
            agent = thought["agent"]
            thought_text = thought["thought"][:50] + "..." if len(thought["thought"]) > 50 else thought["thought"]
            
            mermaid_content += f'    {node_id}["{agent}: {thought_text}"]\n'
            
            if i > 0:
                mermaid_content += f'    A{i-1} --> {node_id}\n'
        
        mermaid_file = self.output_dir / "thought_trail.md"
        with open(mermaid_file, 'w') as f:
            f.write("# AutoDevCore Thought Trail\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_content)
            f.write("```\n")
        
        print(f"📊 Mermaid diagram saved to: {mermaid_file}")
    
    @abstractmethod
    def execute(self):
        """Execute the mode's main functionality."""
        pass
