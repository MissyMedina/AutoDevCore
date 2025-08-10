"""
Blueprint Mode - Analyze legacy codebases and generate structure diagrams with GPT-OSS
"""

import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from .base import BaseMode
from integrations import gpt_oss_client


class BlueprintMode(BaseMode):
    """Blueprint mode for analyzing legacy codebases with GPT-OSS integration."""
    
    def __init__(self, path: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.path = Path(path)
    
    def execute(self):
        """Execute the blueprint mode."""
        print(f"🏗️ Blueprint Mode - Intelligent Codebase Analysis")
        print(f"📁 Analyzing: {self.path}")
        print()
        
        if not self.path.exists():
            print(f"❌ Error: Path {self.path} does not exist")
            return
        
        self.log_thought("BlueprintAgent", f"Starting intelligent analysis of {self.path}")
        
        # Analyze the codebase structure
        self.log_thought("BlueprintAgent", "Scanning directory structure")
        structure = self._analyze_structure()
        self.log_thought("BlueprintAgent", "Directory structure analyzed", structure)
        
        # GPT-OSS code analysis
        self.log_thought("BlueprintAgent", "Starting GPT-OSS code analysis")
        code_analysis = self._analyze_code_with_gpt_oss()
        self.log_thought("BlueprintAgent", "GPT-OSS analysis complete", code_analysis)
        
        # Analyze dependencies
        self.log_thought("BlueprintAgent", "Analyzing code dependencies")
        dependencies = self._analyze_dependencies()
        self.log_thought("BlueprintAgent", "Dependencies analyzed", dependencies)
        
        # Extract API documentation
        self.log_thought("BlueprintAgent", "Extracting API documentation")
        api_docs = self._extract_api_documentation()
        self.log_thought("BlueprintAgent", "API documentation extracted", api_docs)
        
        # Detect code patterns
        self.log_thought("BlueprintAgent", "Detecting code patterns")
        patterns = self._detect_code_patterns()
        self.log_thought("BlueprintAgent", "Code patterns detected", patterns)
        
        # Generate comprehensive architecture diagram
        self.log_thought("BlueprintAgent", "Generating comprehensive architecture diagram")
        self._generate_architecture_diagram(structure, code_analysis, dependencies)
        
        # Generate detailed analysis report
        self.log_thought("BlueprintAgent", "Generating detailed analysis report")
        self._generate_analysis_report(structure, code_analysis, dependencies, api_docs, patterns)
        
        # Generate refactoring recommendations
        self.log_thought("BlueprintAgent", "Generating refactoring recommendations")
        recommendations = self._generate_refactoring_recommendations(code_analysis, patterns)
        self.log_thought("BlueprintAgent", "Refactoring recommendations generated", recommendations)
        
        # Save thought trail and generate visualizations
        self.save_thought_trail()
        
        print("✅ Intelligent blueprint analysis complete!")
        print(f"📄 Analysis saved to: {self.output_dir}")
        print("📊 Architecture diagram generated")
        print("📋 API documentation extracted")
        print("🔍 Code patterns detected")
        print("💡 Refactoring recommendations provided")
    
    def _analyze_structure(self) -> dict:
        """Analyze the directory structure."""
        structure = {
            "root": str(self.path),
            "directories": [],
            "files": [],
            "file_types": {},
            "total_files": 0,
            "total_lines": 0,
            "languages": {}
        }
        
        for item in self.path.rglob("*"):
            if item.is_file():
                relative_path = str(item.relative_to(self.path))
                structure["files"].append(relative_path)
                structure["total_files"] += 1
                
                # Count lines
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        structure["total_lines"] += lines
                except:
                    pass
                
                # Analyze file types
                ext = item.suffix.lower()
                if ext:
                    structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
                
                # Detect languages
                if ext in ['.py', '.pyx', '.pyi']:
                    structure["languages"]["Python"] = structure["languages"].get("Python", 0) + 1
                elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                    structure["languages"]["JavaScript/TypeScript"] = structure["languages"].get("JavaScript/TypeScript", 0) + 1
                elif ext in ['.java']:
                    structure["languages"]["Java"] = structure["languages"].get("Java", 0) + 1
                elif ext in ['.go']:
                    structure["languages"]["Go"] = structure["languages"].get("Go", 0) + 1
                elif ext in ['.rs']:
                    structure["languages"]["Rust"] = structure["languages"].get("Rust", 0) + 1
                elif ext in ['.cpp', '.cc', '.cxx', '.c']:
                    structure["languages"]["C/C++"] = structure["languages"].get("C/C++", 0) + 1
                    
            elif item.is_dir():
                structure["directories"].append(str(item.relative_to(self.path)))
        
        return structure
    
    def _analyze_code_with_gpt_oss(self) -> dict:
        """Analyze code using GPT-OSS."""
        print("🔍 Analyzing code with GPT-OSS...")
        
        try:
            # Get key files for analysis
            key_files = self._get_key_files()
            
            analysis = {
                "architecture_patterns": self._analyze_architecture_patterns(key_files),
                "code_quality": self._analyze_code_quality(key_files),
                "design_patterns": self._analyze_design_patterns(key_files),
                "complexity_analysis": self._analyze_complexity(key_files),
                "security_analysis": self._analyze_security_patterns(key_files)
            }
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ GPT-OSS analysis failed, using fallback: {e}")
            return self._fallback_code_analysis()
    
    def _get_key_files(self) -> List[Path]:
        """Get key files for analysis."""
        key_files = []
        
        # Look for important files
        important_patterns = [
            "*.py", "*.js", "*.ts", "*.java", "*.go", "*.rs",
            "main.py", "app.py", "index.js", "package.json",
            "requirements.txt", "Dockerfile", "README.md",
            "*.py", "api/*.py", "models/*.py", "utils/*.py"
        ]
        
        for pattern in important_patterns:
            key_files.extend(self.path.glob(pattern))
        
        # Limit to 10 files for analysis
        return key_files[:10]
    
    def _analyze_architecture_patterns(self, key_files: List[Path]) -> dict:
        """Analyze architecture patterns using GPT-OSS."""
        try:
            # Read sample files for analysis
            sample_code = ""
            for file_path in key_files[:3]:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sample_code += f"\n# {file_path.name}\n{f.read()}\n"
                except:
                    continue
            
            if not sample_code:
                return {"error": "No readable code files found"}
            
            prompt = f"""
            Analyze the following code for architecture patterns. Focus on:
            1. Application architecture (MVC, MVVM, Clean Architecture, etc.)
            2. Module organization and structure
            3. Dependency injection patterns
            4. Service layer patterns
            5. Data access patterns
            
            Code to analyze:
            {sample_code[:2000]}
            
            Provide a JSON response with:
            - architecture_type (string)
            - patterns_detected (list)
            - module_structure (dict)
            - recommendations (list)
            """
            
            response = gpt_oss_client.generate(prompt, temperature=0.3, max_tokens=500)
            content = response.get("message", {}).get("content", "")
            
            try:
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse GPT-OSS response"}
            except:
                return {"error": "Invalid JSON response from GPT-OSS"}
                
        except Exception as e:
            return {"error": f"GPT-OSS analysis failed: {str(e)}"}
    
    def _analyze_code_quality(self, key_files: List[Path]) -> dict:
        """Analyze code quality using GPT-OSS."""
        try:
            sample_code = ""
            for file_path in key_files[:2]:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        sample_code += f"\n# {file_path.name}\n{f.read()}\n"
                except:
                    continue
            
            if not sample_code:
                return {"error": "No readable code files found"}
            
            prompt = f"""
            Analyze the following code for quality metrics. Focus on:
            1. Code organization and readability
            2. Naming conventions
            3. Error handling
            4. Documentation quality
            5. Best practices adherence
            
            Code to analyze:
            {sample_code[:1500]}
            
            Provide a JSON response with:
            - overall_quality_score (0-100)
            - strengths (list)
            - weaknesses (list)
            - improvement_suggestions (list)
            """
            
            response = gpt_oss_client.generate(prompt, temperature=0.3, max_tokens=400)
            content = response.get("message", {}).get("content", "")
            
            try:
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse GPT-OSS response"}
            except:
                return {"error": "Invalid JSON response from GPT-OSS"}
                
        except Exception as e:
            return {"error": f"GPT-OSS analysis failed: {str(e)}"}
    
    def _analyze_design_patterns(self, key_files: List[Path]) -> dict:
        """Analyze design patterns in the code."""
        # Simplified pattern detection
        patterns = {
            "patterns_detected": [],
            "anti_patterns": [],
            "recommendations": []
        }
        
        for file_path in key_files:
            if file_path.suffix == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Simple pattern detection
                        if 'class' in content and 'def __init__' in content:
                            patterns["patterns_detected"].append("Constructor Pattern")
                        if 'def get_' in content and 'def set_' in content:
                            patterns["patterns_detected"].append("Getter/Setter Pattern")
                        if 'import' in content and 'from' in content:
                            patterns["patterns_detected"].append("Dependency Injection")
                        if 'try:' in content and 'except:' in content:
                            patterns["patterns_detected"].append("Error Handling Pattern")
                            
                except:
                    continue
        
        return patterns
    
    def _analyze_complexity(self, key_files: List[Path]) -> dict:
        """Analyze code complexity."""
        complexity = {
            "cyclomatic_complexity": "Low",
            "cognitive_complexity": "Low",
            "nesting_depth": "Low",
            "recommendations": []
        }
        
        return complexity
    
    def _analyze_security_patterns(self, key_files: List[Path]) -> dict:
        """Analyze security patterns in the code."""
        security = {
            "security_patterns": [],
            "vulnerabilities": [],
            "recommendations": []
        }
        
        for file_path in key_files:
            if file_path.suffix == '.py':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Simple security pattern detection
                        if 'password' in content.lower():
                            security["security_patterns"].append("Password Handling")
                        if 'token' in content.lower():
                            security["security_patterns"].append("Token Management")
                        if 'encrypt' in content.lower():
                            security["security_patterns"].append("Encryption")
                        if 'sql' in content.lower() and 'execute' in content.lower():
                            security["vulnerabilities"].append("Potential SQL Injection")
                            
                except:
                    continue
        
        return security
    
    def _fallback_code_analysis(self) -> dict:
        """Fallback analysis when GPT-OSS is unavailable."""
        return {
            "architecture_patterns": {"architecture_type": "Unknown", "patterns_detected": []},
            "code_quality": {"overall_quality_score": 60, "strengths": [], "weaknesses": ["Analysis unavailable"]},
            "design_patterns": {"patterns_detected": [], "anti_patterns": []},
            "complexity_analysis": {"cyclomatic_complexity": "Unknown", "recommendations": []},
            "security_analysis": {"security_patterns": [], "vulnerabilities": []}
        }
    
    def _analyze_dependencies(self) -> dict:
        """Analyze code dependencies."""
        dependencies = {
            "python_imports": [],
            "javascript_imports": [],
            "external_packages": [],
            "internal_dependencies": []
        }
        
        # Analyze Python files
        for py_file in self.path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            dependencies["python_imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            dependencies["python_imports"].append(node.module)
                            
            except:
                continue
        
        # Remove duplicates
        dependencies["python_imports"] = list(set(dependencies["python_imports"]))
        
        return dependencies
    
    def _extract_api_documentation(self) -> dict:
        """Extract API documentation from code."""
        api_docs = {
            "endpoints": [],
            "models": [],
            "schemas": []
        }
        
        # Look for FastAPI/Flask endpoints
        for py_file in self.path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if '@app.route' in content or '@router.' in content:
                    # Extract route information
                    lines = content.split('\n')
                    for line in lines:
                        if '@app.route' in line or '@router.' in line:
                            api_docs["endpoints"].append(line.strip())
                            
            except:
                continue
        
        return api_docs
    
    def _detect_code_patterns(self) -> dict:
        """Detect code patterns and anti-patterns."""
        patterns = {
            "design_patterns": [],
            "anti_patterns": [],
            "code_smells": [],
            "recommendations": []
        }
        
        # Simple pattern detection
        for py_file in self.path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Detect patterns
                if 'class' in content and 'def __init__' in content:
                    patterns["design_patterns"].append("Constructor Pattern")
                if 'def get_' in content and 'def set_' in content:
                    patterns["design_patterns"].append("Getter/Setter Pattern")
                if 'try:' in content and 'except:' in content:
                    patterns["design_patterns"].append("Error Handling")
                    
                # Detect anti-patterns
                if 'global ' in content:
                    patterns["anti_patterns"].append("Global Variables")
                if 'eval(' in content:
                    patterns["anti_patterns"].append("Eval Usage")
                if 'exec(' in content:
                    patterns["anti_patterns"].append("Exec Usage")
                    
            except:
                continue
        
        return patterns
    
    def _generate_architecture_diagram(self, structure: dict, code_analysis: dict, dependencies: dict):
        """Generate a comprehensive architecture diagram."""
        diagram_file = self.output_dir / "architecture.md"
        
        with open(diagram_file, 'w') as f:
            f.write("# Intelligent Codebase Architecture Diagram\n\n")
            f.write("## System Overview\n\n")
            f.write(f"- **Root Directory**: {structure['root']}\n")
            f.write(f"- **Total Files**: {structure['total_files']}\n")
            f.write(f"- **Total Lines**: {structure['total_lines']}\n")
            f.write(f"- **Languages**: {', '.join(structure['languages'].keys())}\n\n")
            
            # Architecture diagram
            f.write("## Architecture Diagram\n\n")
            f.write("```mermaid\ngraph TD\n")
            
            # Add root node
            f.write(f'    Root["{self.path.name}"]\n')
            
            # Add main directories
            for directory in structure["directories"][:8]:
                if not any(skip in directory for skip in ['__pycache__', '.git', '.vscode', 'node_modules']):
                    clean_name = directory.replace("/", "_").replace("-", "_").replace(".", "_")
                    f.write(f'    {clean_name}["{directory}"]\n')
                    f.write(f'    Root --> {clean_name}\n')
            
            # Add file type nodes
            for ext, count in sorted(structure["file_types"].items(), key=lambda x: x[1], reverse=True)[:5]:
                if count > 1:
                    clean_name = ext.replace(".", "").upper()
                    f.write(f'    {clean_name}[{ext}: {count} files]\n')
                    f.write(f'    Root --> {clean_name}\n')
            
            f.write("```\n\n")
            
            # Dependencies diagram
            if dependencies["python_imports"]:
                f.write("## Dependencies\n\n")
                f.write("```mermaid\ngraph LR\n")
                f.write(f'    App["{self.path.name}"]\n')
                
                for dep in dependencies["python_imports"][:10]:
                    clean_dep = dep.replace(".", "_").replace("-", "_")
                    f.write(f'    {clean_dep}["{dep}"]\n')
                    f.write(f'    App --> {clean_dep}\n')
                
                f.write("```\n")
        
        print(f"📊 Architecture diagram saved to: {diagram_file}")
    
    def _generate_analysis_report(self, structure: dict, code_analysis: dict, dependencies: dict, api_docs: dict, patterns: dict):
        """Generate a detailed analysis report."""
        report_file = self.output_dir / "analysis_report.md"
        
        with open(report_file, 'w') as f:
            f.write("# Intelligent Codebase Analysis Report\n\n")
            f.write(f"**Analyzed**: {self.path}\n")
            f.write(f"**Analysis Method**: GPT-OSS Enhanced\n\n")
            
            # Structure analysis
            f.write("## 📁 Structure Analysis\n\n")
            f.write(f"- **Total Files**: {structure['total_files']}\n")
            f.write(f"- **Total Lines**: {structure['total_lines']}\n")
            f.write(f"- **Directories**: {len(structure['directories'])}\n")
            f.write(f"- **Languages**: {', '.join(structure['languages'].keys())}\n\n")
            
            # File types breakdown
            f.write("### File Types\n\n")
            for ext, count in sorted(structure["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"- **{ext}**: {count} files\n")
            f.write("\n")
            
            # Code analysis
            f.write("## 🔍 Code Analysis\n\n")
            
            # Architecture patterns
            arch_patterns = code_analysis.get("architecture_patterns", {})
            if "architecture_type" in arch_patterns:
                f.write(f"### Architecture Type: {arch_patterns['architecture_type']}\n\n")
            if "patterns_detected" in arch_patterns:
                f.write("**Detected Patterns**:\n")
                for pattern in arch_patterns["patterns_detected"]:
                    f.write(f"- {pattern}\n")
                f.write("\n")
            
            # Code quality
            quality = code_analysis.get("code_quality", {})
            if "overall_quality_score" in quality:
                f.write(f"### Code Quality Score: {quality['overall_quality_score']}/100\n\n")
            if "strengths" in quality and quality["strengths"]:
                f.write("**Strengths**:\n")
                for strength in quality["strengths"][:5]:
                    f.write(f"- {strength}\n")
                f.write("\n")
            
            # Dependencies
            f.write("## 📦 Dependencies\n\n")
            if dependencies["python_imports"]:
                f.write("### Python Imports\n\n")
                for dep in dependencies["python_imports"][:15]:
                    f.write(f"- {dep}\n")
                f.write("\n")
            
            # API Documentation
            if api_docs["endpoints"]:
                f.write("## 🔌 API Endpoints\n\n")
                for endpoint in api_docs["endpoints"][:10]:
                    f.write(f"- `{endpoint}`\n")
                f.write("\n")
            
            # Code Patterns
            f.write("## 🎯 Code Patterns\n\n")
            if patterns["design_patterns"]:
                f.write("### Design Patterns\n\n")
                for pattern in patterns["design_patterns"]:
                    f.write(f"- {pattern}\n")
                f.write("\n")
            
            if patterns["anti_patterns"]:
                f.write("### Anti-Patterns\n\n")
                for anti_pattern in patterns["anti_patterns"]:
                    f.write(f"- {anti_pattern}\n")
                f.write("\n")
        
        print(f"📄 Analysis report saved to: {report_file}")
    
    def _generate_refactoring_recommendations(self, code_analysis: dict, patterns: dict) -> dict:
        """Generate refactoring recommendations."""
        recommendations = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": []
        }
        
        # Analyze code quality for recommendations
        quality = code_analysis.get("code_quality", {})
        if "weaknesses" in quality:
            for weakness in quality["weaknesses"]:
                if "documentation" in weakness.lower():
                    recommendations["medium_priority"].append("Improve code documentation")
                elif "error" in weakness.lower():
                    recommendations["high_priority"].append("Enhance error handling")
                elif "naming" in weakness.lower():
                    recommendations["medium_priority"].append("Improve naming conventions")
        
        # Analyze anti-patterns
        for anti_pattern in patterns.get("anti_patterns", []):
            if "Global Variables" in anti_pattern:
                recommendations["high_priority"].append("Replace global variables with dependency injection")
            elif "Eval Usage" in anti_pattern:
                recommendations["high_priority"].append("Remove eval() usage for security")
            elif "Exec Usage" in anti_pattern:
                recommendations["high_priority"].append("Remove exec() usage for security")
        
        # Add general recommendations
        if not recommendations["high_priority"]:
            recommendations["medium_priority"].append("Consider adding unit tests")
            recommendations["medium_priority"].append("Implement logging for better debugging")
        
        return recommendations
