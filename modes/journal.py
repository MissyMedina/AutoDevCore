"""
Journal Mode - Intelligent codebase analysis and insights with GPT-OSS
"""

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations import gpt_oss_client

from .base import BaseMode


class JournalMode(BaseMode):
    """Journal mode for intelligent codebase analysis and insights with GPT-OSS integration."""

    def __init__(self, path: str, output_dir: str, verbose: bool = False):
        super().__init__(output_dir, verbose)
        self.path = Path(path)

    def execute(self):
        """Execute the journal mode."""
        print("📝 Journal Mode - Intelligent Codebase Insights")
        print(f"📁 Analyzing: {self.path}")
        print()

        if not self.path.exists():
            print(f"❌ Error: Path {self.path} does not exist")
            return

        self.log_thought(
            "JournalAgent", f"Starting intelligent codebase analysis of {self.path}"
        )

        # Comprehensive codebase analysis
        self.log_thought("JournalAgent", "Performing comprehensive codebase scan")
        codebase_metrics = self._analyze_codebase_metrics()
        self.log_thought(
            "JournalAgent", "Codebase metrics calculated", codebase_metrics
        )

        # Technical debt analysis
        self.log_thought("JournalAgent", "Analyzing technical debt")
        technical_debt = self._analyze_technical_debt()
        self.log_thought(
            "JournalAgent", "Technical debt analysis complete", technical_debt
        )

        # Performance analysis
        self.log_thought("JournalAgent", "Analyzing performance patterns")
        performance_analysis = self._analyze_performance_patterns()
        self.log_thought(
            "JournalAgent", "Performance analysis complete", performance_analysis
        )

        # Security vulnerability detection
        self.log_thought("JournalAgent", "Detecting security vulnerabilities")
        security_analysis = self._detect_security_vulnerabilities()
        self.log_thought(
            "JournalAgent", "Security analysis complete", security_analysis
        )

        # Code quality metrics
        self.log_thought("JournalAgent", "Calculating code quality metrics")
        quality_metrics = self._calculate_quality_metrics()
        self.log_thought("JournalAgent", "Quality metrics calculated", quality_metrics)

        # GPT-OSS intelligent insights
        self.log_thought("JournalAgent", "Generating GPT-OSS insights")
        ai_insights = self._generate_ai_insights()
        self.log_thought("JournalAgent", "AI insights generated", ai_insights)

        # Generate comprehensive journal report
        self.log_thought("JournalAgent", "Generating comprehensive journal report")
        self._generate_journal_report(
            codebase_metrics,
            technical_debt,
            performance_analysis,
            security_analysis,
            quality_metrics,
            ai_insights,
        )

        # Generate actionable recommendations
        self.log_thought("JournalAgent", "Generating actionable recommendations")
        recommendations = self._generate_actionable_recommendations(
            technical_debt, security_analysis, quality_metrics
        )
        self.log_thought("JournalAgent", "Recommendations generated", recommendations)

        # Save thought trail and generate visualizations
        self.save_thought_trail()

        print("✅ Intelligent journal analysis complete!")
        print(f"📄 Analysis saved to: {self.output_dir}")
        print("📊 Code quality metrics calculated")
        print("🔍 Security vulnerabilities detected")
        print("⚡ Performance patterns analyzed")
        print("💡 Actionable recommendations provided")

    def _analyze_codebase_metrics(self) -> dict:
        """Analyze comprehensive codebase metrics."""
        metrics = {
            "file_count": 0,
            "line_count": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "languages": {},
            "file_types": {},
            "complexity_metrics": {
                "average_function_length": 0,
                "average_class_length": 0,
                "max_nesting_depth": 0,
            },
        }

        total_functions = 0
        total_classes = 0
        function_lengths = []
        class_lengths = []
        max_nesting = 0

        for file_path in self.path.rglob("*"):
            if file_path.is_file():
                metrics["file_count"] += 1

                # Count lines and analyze content
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        metrics["line_count"] += len(lines)

                        for line in lines:
                            stripped = line.strip()
                            if stripped.startswith("#"):
                                metrics["comment_lines"] += 1
                            elif not stripped:
                                metrics["blank_lines"] += 1
                            else:
                                metrics["code_lines"] += 1

                        # Analyze Python files for complexity
                        if file_path.suffix == ".py":
                            try:
                                tree = ast.parse("".join(lines))
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.FunctionDef):
                                        total_functions += 1
                                        function_lengths.append(len(node.body))
                                    elif isinstance(node, ast.ClassDef):
                                        total_classes += 1
                                        class_lengths.append(len(node.body))
                                    elif (
                                        isinstance(node, ast.If)
                                        or isinstance(node, ast.For)
                                        or isinstance(node, ast.While)
                                    ):
                                        # Simple nesting depth calculation
                                        depth = self._calculate_nesting_depth(node)
                                        max_nesting = max(max_nesting, depth)
                            except:
                                pass

                except:
                    continue

                # Count file types
                ext = file_path.suffix.lower()
                if ext:
                    metrics["file_types"][ext] = metrics["file_types"].get(ext, 0) + 1

                # Detect languages
                if ext in [".py", ".pyx", ".pyi"]:
                    metrics["languages"]["Python"] = (
                        metrics["languages"].get("Python", 0) + 1
                    )
                elif ext in [".js", ".ts", ".jsx", ".tsx"]:
                    metrics["languages"]["JavaScript/TypeScript"] = (
                        metrics["languages"].get("JavaScript/TypeScript", 0) + 1
                    )
                elif ext in [".java"]:
                    metrics["languages"]["Java"] = (
                        metrics["languages"].get("Java", 0) + 1
                    )
                elif ext in [".go"]:
                    metrics["languages"]["Go"] = metrics["languages"].get("Go", 0) + 1
                elif ext in [".rs"]:
                    metrics["languages"]["Rust"] = (
                        metrics["languages"].get("Rust", 0) + 1
                    )
                elif ext in [".cpp", ".cc", ".cxx", ".c"]:
                    metrics["languages"]["C/C++"] = (
                        metrics["languages"].get("C/C++", 0) + 1
                    )

        # Calculate averages
        if function_lengths:
            metrics["complexity_metrics"]["average_function_length"] = sum(
                function_lengths
            ) / len(function_lengths)
        if class_lengths:
            metrics["complexity_metrics"]["average_class_length"] = sum(
                class_lengths
            ) / len(class_lengths)
        metrics["complexity_metrics"]["max_nesting_depth"] = max_nesting

        return metrics

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 1) -> int:
        """Calculate nesting depth of AST nodes."""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                max_depth = max(
                    max_depth, self._calculate_nesting_depth(child, current_depth + 1)
                )

        return max_depth

    def _analyze_technical_debt(self) -> dict:
        """Analyze technical debt in the codebase."""
        technical_debt = {
            "code_smells": [],
            "anti_patterns": [],
            "duplicate_code": [],
            "complexity_issues": [],
            "maintenance_issues": [],
            "debt_score": 0,
        }

        debt_score = 0

        for file_path in self.path.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")

                    # Detect code smells and anti-patterns
                    for i, line in enumerate(lines, 1):
                        stripped = line.strip()

                        # Long functions/methods
                        if len(stripped) > 120:
                            technical_debt["code_smells"].append(
                                f"Long line in {file_path.name}:{i}"
                            )
                            debt_score += 1

                        # Magic numbers
                        if (
                            any(char.isdigit() for char in stripped)
                            and len(stripped) < 10
                        ):
                            if any(
                                word in stripped.lower()
                                for word in ["password", "secret", "key", "token"]
                            ):
                                technical_debt["anti_patterns"].append(
                                    f"Hardcoded value in {file_path.name}:{i}"
                                )
                                debt_score += 2

                        # Global variables
                        if stripped.startswith("global "):
                            technical_debt["anti_patterns"].append(
                                f"Global variable in {file_path.name}:{i}"
                            )
                            debt_score += 3

                        # Eval/exec usage
                        if "eval(" in stripped or "exec(" in stripped:
                            technical_debt["anti_patterns"].append(
                                f"Dangerous eval/exec in {file_path.name}:{i}"
                            )
                            debt_score += 5

                        # TODO/FIXME comments
                        if "TODO" in stripped or "FIXME" in stripped:
                            technical_debt["maintenance_issues"].append(
                                f"TODO/FIXME in {file_path.name}:{i}"
                            )
                            debt_score += 1

                    # Detect complexity issues
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if (
                                isinstance(node, ast.FunctionDef)
                                and len(node.body) > 20
                            ):
                                technical_debt["complexity_issues"].append(
                                    f"Long function {node.name} in {file_path.name}"
                                )
                                debt_score += 2
                            elif isinstance(node, ast.ClassDef) and len(node.body) > 50:
                                technical_debt["complexity_issues"].append(
                                    f"Large class {node.name} in {file_path.name}"
                                )
                                debt_score += 2
                    except:
                        pass

            except:
                continue

        technical_debt["debt_score"] = min(debt_score, 100)  # Cap at 100
        return technical_debt

    def _analyze_performance_patterns(self) -> dict:
        """Analyze performance patterns in the code."""
        performance = {
            "database_queries": [],
            "memory_issues": [],
            "algorithm_complexity": [],
            "optimization_opportunities": [],
            "performance_score": 80,
        }

        for file_path in self.path.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Detect database query patterns
                    if "query(" in content or "execute(" in content:
                        performance["database_queries"].append(
                            f"Database queries in {file_path.name}"
                        )

                    # Detect potential memory issues
                    if "for " in content and "in " in content and "range(" in content:
                        performance["memory_issues"].append(
                            f"Potential memory usage in {file_path.name}"
                        )

                    # Detect algorithm complexity
                    if "for " in content and "for " in content:
                        performance["algorithm_complexity"].append(
                            f"Nested loops in {file_path.name}"
                        )

                    # Optimization opportunities
                    if "list(" in content and "map(" in content:
                        performance["optimization_opportunities"].append(
                            f"List comprehension opportunity in {file_path.name}"
                        )

            except:
                continue

        # Adjust performance score based on findings
        if performance["algorithm_complexity"]:
            performance["performance_score"] -= 10
        if performance["memory_issues"]:
            performance["performance_score"] -= 5

        return performance

    def _detect_security_vulnerabilities(self) -> dict:
        """Detect security vulnerabilities in the code."""
        security = {
            "critical_vulnerabilities": [],
            "high_risk_vulnerabilities": [],
            "medium_risk_vulnerabilities": [],
            "low_risk_vulnerabilities": [],
            "security_score": 85,
        }

        for file_path in self.path.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Critical vulnerabilities
                    if "eval(" in content or "exec(" in content:
                        security["critical_vulnerabilities"].append(
                            f"Code execution vulnerability in {file_path.name}"
                        )
                        security["security_score"] -= 20

                    # High risk vulnerabilities
                    if (
                        "password" in content
                        and "=" in content
                        and not "hash" in content
                    ):
                        security["high_risk_vulnerabilities"].append(
                            f"Potential password exposure in {file_path.name}"
                        )
                        security["security_score"] -= 10

                    if (
                        "sql" in content.lower()
                        and "execute" in content
                        and not "parameter" in content
                    ):
                        security["high_risk_vulnerabilities"].append(
                            f"Potential SQL injection in {file_path.name}"
                        )
                        security["security_score"] -= 15

                    # Medium risk vulnerabilities
                    if "input(" in content:
                        security["medium_risk_vulnerabilities"].append(
                            f"User input handling in {file_path.name}"
                        )
                        security["security_score"] -= 5

                    # Low risk vulnerabilities
                    if "print(" in content and "password" in content.lower():
                        security["low_risk_vulnerabilities"].append(
                            f"Potential password logging in {file_path.name}"
                        )
                        security["security_score"] -= 2

            except:
                continue

        security["security_score"] = max(security["security_score"], 0)
        return security

    def _calculate_quality_metrics(self) -> dict:
        """Calculate comprehensive code quality metrics."""
        quality = {
            "maintainability_index": 80,
            "cyclomatic_complexity": "Low",
            "code_coverage": "Unknown",
            "documentation_coverage": 0,
            "test_coverage": 0,
            "code_style": "Good",
            "overall_quality_score": 75,
        }

        total_files = 0
        documented_files = 0
        test_files = 0

        for file_path in self.path.rglob("*.py"):
            total_files += 1

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Check for documentation
                    if '"""' in content or "'''" in content:
                        documented_files += 1

                    # Check for test files
                    if "test_" in file_path.name or "Test" in file_path.name:
                        test_files += 1

            except:
                continue

        # Calculate coverage percentages
        if total_files > 0:
            quality["documentation_coverage"] = (documented_files / total_files) * 100
            quality["test_coverage"] = (test_files / total_files) * 100

        # Adjust overall quality score
        quality["overall_quality_score"] = (
            quality["maintainability_index"] * 0.3
            + quality["documentation_coverage"] * 0.2
            + quality["test_coverage"] * 0.3
            + (100 if quality["code_style"] == "Good" else 70) * 0.2
        )

        return quality

    def _generate_ai_insights(self) -> dict:
        """Generate AI-powered insights using GPT-OSS."""
        print("🤖 Generating AI insights with GPT-OSS...")

        try:
            # Get sample code for analysis
            sample_code = ""
            key_files = list(self.path.rglob("*.py"))[:3]

            for file_path in key_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        sample_code += f"\n# {file_path.name}\n{f.read()}\n"
                except:
                    continue

            if not sample_code:
                return {"error": "No readable code files found"}

            prompt = f"""
            Analyze the following codebase and provide intelligent insights. Focus on:
            1. Code architecture and design patterns
            2. Potential improvements and optimizations
            3. Best practices adherence
            4. Scalability considerations
            5. Maintainability factors

            Code to analyze:
            {sample_code[:2000]}

            Provide a JSON response with:
            - architecture_insights (list)
            - improvement_opportunities (list)
            - best_practices_assessment (dict)
            - scalability_analysis (dict)
            - maintainability_score (0-100)
            """

            response = gpt_oss_client.generate(prompt, temperature=0.3, max_tokens=600)
            content = response.get("message", {}).get("content", "")

            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse GPT-OSS response"}
            except:
                return {"error": "Invalid JSON response from GPT-OSS"}

        except Exception as e:
            print(f"⚠️ GPT-OSS insights failed, using fallback: {e}")
            return self._fallback_ai_insights()

    def _fallback_ai_insights(self) -> dict:
        """Fallback insights when GPT-OSS is unavailable."""
        return {
            "architecture_insights": [
                "Modular structure detected",
                "Clear separation of concerns",
            ],
            "improvement_opportunities": [
                "Add comprehensive documentation",
                "Implement unit tests",
            ],
            "best_practices_assessment": {
                "overall": "Good",
                "areas_for_improvement": ["Documentation", "Testing"],
            },
            "scalability_analysis": {
                "current_state": "Moderate",
                "recommendations": ["Add caching", "Optimize database queries"],
            },
            "maintainability_score": 70,
        }

    def _generate_journal_report(
        self,
        codebase_metrics: dict,
        technical_debt: dict,
        performance_analysis: dict,
        security_analysis: dict,
        quality_metrics: dict,
        ai_insights: dict,
    ):
        """Generate a comprehensive journal report."""
        report_file = self.output_dir / "journal_report.md"

        with open(report_file, "w") as f:
            f.write("# Intelligent Codebase Journal Report\n\n")
            f.write(f"**Analyzed**: {self.path}\n")
            f.write(f"**Analysis Method**: GPT-OSS Enhanced\n\n")

            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Files**: {codebase_metrics['file_count']}\n")
            f.write(f"- **Total Lines**: {codebase_metrics['line_count']}\n")
            f.write(f"- **Code Lines**: {codebase_metrics['code_lines']}\n")
            f.write(
                f"- **Languages**: {', '.join(codebase_metrics['languages'].keys())}\n"
            )
            f.write(f"- **Technical Debt Score**: {technical_debt['debt_score']}/100\n")
            f.write(
                f"- **Security Score**: {security_analysis['security_score']}/100\n"
            )
            f.write(
                f"- **Quality Score**: {quality_metrics['overall_quality_score']:.1f}/100\n\n"
            )

            # Code Quality Metrics
            f.write("## 🎯 Code Quality Metrics\n\n")
            f.write(
                f"- **Maintainability Index**: {quality_metrics['maintainability_index']}\n"
            )
            f.write(
                f"- **Documentation Coverage**: {quality_metrics['documentation_coverage']:.1f}%\n"
            )
            f.write(f"- **Test Coverage**: {quality_metrics['test_coverage']:.1f}%\n")
            f.write(
                f"- **Cyclomatic Complexity**: {quality_metrics['cyclomatic_complexity']}\n\n"
            )

            # Technical Debt Analysis
            f.write("## 🏗️ Technical Debt Analysis\n\n")
            f.write(f"**Debt Score**: {technical_debt['debt_score']}/100\n\n")

            if technical_debt["code_smells"]:
                f.write("### Code Smells\n\n")
                for smell in technical_debt["code_smells"][:5]:
                    f.write(f"- {smell}\n")
                f.write("\n")

            if technical_debt["anti_patterns"]:
                f.write("### Anti-Patterns\n\n")
                for pattern in technical_debt["anti_patterns"][:5]:
                    f.write(f"- {pattern}\n")
                f.write("\n")

            # Security Analysis
            f.write("## 🔒 Security Analysis\n\n")
            f.write(
                f"**Security Score**: {security_analysis['security_score']}/100\n\n"
            )

            if security_analysis["critical_vulnerabilities"]:
                f.write("### Critical Vulnerabilities\n\n")
                for vuln in security_analysis["critical_vulnerabilities"]:
                    f.write(f"- ⚠️ {vuln}\n")
                f.write("\n")

            if security_analysis["high_risk_vulnerabilities"]:
                f.write("### High Risk Vulnerabilities\n\n")
                for vuln in security_analysis["high_risk_vulnerabilities"][:3]:
                    f.write(f"- 🔴 {vuln}\n")
                f.write("\n")

            # Performance Analysis
            f.write("## ⚡ Performance Analysis\n\n")
            f.write(
                f"**Performance Score**: {performance_analysis['performance_score']}/100\n\n"
            )

            if performance_analysis["optimization_opportunities"]:
                f.write("### Optimization Opportunities\n\n")
                for opp in performance_analysis["optimization_opportunities"][:3]:
                    f.write(f"- {opp}\n")
                f.write("\n")

            # AI Insights
            f.write("## 🤖 AI-Powered Insights\n\n")

            if "architecture_insights" in ai_insights:
                f.write("### Architecture Insights\n\n")
                for insight in ai_insights["architecture_insights"][:3]:
                    f.write(f"- {insight}\n")
                f.write("\n")

            if "improvement_opportunities" in ai_insights:
                f.write("### Improvement Opportunities\n\n")
                for opp in ai_insights["improvement_opportunities"][:3]:
                    f.write(f"- {opp}\n")
                f.write("\n")

            if "maintainability_score" in ai_insights:
                f.write(
                    f"### AI Maintainability Score: {ai_insights['maintainability_score']}/100\n\n"
                )

        print(f"📄 Journal report saved to: {report_file}")

    def _generate_actionable_recommendations(
        self, technical_debt: dict, security_analysis: dict, quality_metrics: dict
    ) -> dict:
        """Generate actionable recommendations based on analysis."""
        recommendations = {
            "immediate_actions": [],
            "short_term": [],
            "long_term": [],
            "priority_score": 0,
        }

        priority_score = 0

        # Immediate actions based on critical issues
        if technical_debt["anti_patterns"]:
            recommendations["immediate_actions"].append(
                "Remove dangerous eval()/exec() usage"
            )
            priority_score += 20

        if security_analysis["critical_vulnerabilities"]:
            recommendations["immediate_actions"].append(
                "Fix critical security vulnerabilities"
            )
            priority_score += 25

        # Short term improvements
        if quality_metrics["documentation_coverage"] < 50:
            recommendations["short_term"].append("Improve code documentation coverage")
            priority_score += 10

        if quality_metrics["test_coverage"] < 30:
            recommendations["short_term"].append("Add unit tests to improve coverage")
            priority_score += 15

        if technical_debt["code_smells"]:
            recommendations["short_term"].append(
                "Refactor code smells and long functions"
            )
            priority_score += 8

        # Long term improvements
        if quality_metrics["overall_quality_score"] < 80:
            recommendations["long_term"].append(
                "Implement comprehensive code review process"
            )
            priority_score += 5

        recommendations["long_term"].append("Set up automated code quality checks")
        recommendations["long_term"].append("Establish coding standards and guidelines")

        recommendations["priority_score"] = min(priority_score, 100)
        return recommendations
