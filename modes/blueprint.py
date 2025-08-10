"""
Blueprint Mode - Analyze legacy codebases and generate structure diagrams
"""

from pathlib import Path
from .base import BaseMode


class BlueprintMode(BaseMode):
    """Blueprint mode for analyzing legacy codebases."""
    
    def __init__(self, path: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.path = Path(path)
    
    def execute(self):
        """Execute the blueprint mode."""
        print(f"🏗️ Blueprint Mode - Legacy Codebase Analysis")
        print(f"📁 Analyzing: {self.path}")
        print()
        
        if not self.path.exists():
            print(f"❌ Error: Path {self.path} does not exist")
            return
        
        self.log_thought("BlueprintAgent", f"Starting analysis of {self.path}")
        self.log_thought("BlueprintAgent", "Scanning directory structure")
        
        # Analyze the codebase structure
        structure = self._analyze_structure()
        self.log_thought("BlueprintAgent", "Directory structure analyzed", structure)
        
        # Generate architecture diagram
        self.log_thought("BlueprintAgent", "Generating architecture diagram")
        self._generate_architecture_diagram(structure)
        
        # Generate dependency graph
        self.log_thought("BlueprintAgent", "Analyzing dependencies")
        dependencies = self._analyze_dependencies()
        self.log_thought("BlueprintAgent", "Dependencies analyzed", dependencies)
        
        # Save thought trail
        self.save_thought_trail()
        self.generate_mermaid_diagram()
        
        print("✅ Blueprint analysis complete!")
        print(f"📄 Analysis saved to: {self.output_dir}")
        print("📊 Architecture diagram generated")
    
    def _analyze_structure(self) -> dict:
        """Analyze the directory structure."""
        structure = {
            "root": str(self.path),
            "directories": [],
            "files": [],
            "file_types": {}
        }
        
        for item in self.path.rglob("*"):
            if item.is_file():
                structure["files"].append(str(item.relative_to(self.path)))
                ext = item.suffix.lower()
                if ext:
                    structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
            elif item.is_dir():
                structure["directories"].append(str(item.relative_to(self.path)))
        
        return structure
    
    def _analyze_dependencies(self) -> dict:
        """Analyze code dependencies."""
        # This is a simplified analysis
        # In production, this would use AST parsing to find imports
        dependencies = {
            "python_imports": [],
            "javascript_imports": [],
            "external_packages": []
        }
        
        return dependencies
    
    def _generate_architecture_diagram(self, structure: dict):
        """Generate an architecture diagram."""
        diagram_file = self.output_dir / "architecture.md"
        
        with open(diagram_file, 'w') as f:
            f.write("# Codebase Architecture Diagram\n\n")
            f.write("```mermaid\ngraph TD\n")
            
            # Add root node
            f.write(f'    Root["{self.path.name}"]\n')
            
            # Add directories
            for directory in structure["directories"][:10]:  # Limit to first 10
                f.write(f'    {directory.replace("/", "_").replace("-", "_")}["{directory}"]\n')
                f.write(f'    Root --> {directory.replace("/", "_").replace("-", "_")}\n')
            
            f.write("```\n")
        
        print(f"📊 Architecture diagram saved to: {diagram_file}")
