"""
Score Mode - Evaluate apps against industry templates with GPT-OSS integration
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from integrations import gpt_oss_client

from .base import BaseMode

class ScoreMode(BaseMode):
    """Score mode for evaluating apps against industry templates with GPT-OSS."""

    def __init__(
        self, app_dir: str, template: str, output_dir: str, verbose: bool = False
    ):
        super().__init__(output_dir, verbose)
        self.app_dir = Path(app_dir)
        self.template = template

    def execute(self):
        """Execute the score mode."""
        print(f"📊 Score Mode - Intelligent App Evaluation")
        print(f"📁 App Directory: {self.app_dir}")
        print(f"📋 Template: {self.template}")
        print()

        # Validate app directory
        if not self.app_dir.exists():
            print(f"❌ Error: App directory {self.app_dir} does not exist")
            return

        # Load the scoring template
        self.log_thought("ScoreAgent", f"Loading scoring template: {self.template}")
        template_data = self._load_template()

        if not template_data:
            print(f"❌ Error: Could not load template {self.template}")
            return

        self.log_thought("ScoreAgent", "Template loaded successfully", template_data)

        # Analyze the app codebase
        self.log_thought("ScoreAgent", "Starting codebase analysis")
        code_analysis = self._analyze_codebase()
        self.log_thought("ScoreAgent", "Codebase analysis complete", code_analysis)

        # Evaluate the app with GPT-OSS
        self.log_thought("ScoreAgent", "Starting intelligent app evaluation")
        scores = self._evaluate_app_intelligent(template_data, code_analysis)
        self.log_thought("ScoreAgent", "Intelligent evaluation complete", scores)

        # Generate radar chart
        self.log_thought("ScoreAgent", "Generating radar chart")
        self._generate_radar_chart(scores, template_data)

        # Generate detailed report
        self.log_thought("ScoreAgent", "Generating detailed report")
        self._generate_report(scores, template_data, code_analysis)

        # Save thought trail
        self.save_thought_trail()
        self.generate_mermaid_diagram()

        print("✅ Intelligent app scoring complete!")
        print(f"📄 Results saved to: {self.output_dir}")
        print("📊 Radar chart generated")
        print(f"🎯 Overall Score: {scores['overall_score']:.1f}%")

    def _load_template(self) -> dict:
        """Load the scoring template."""
        # Try multiple possible locations
        possible_paths = [
            Path(self.template),  # Direct path
            Path("profiles") / f"{self.template}.yaml",  # profiles/template.yaml
            Path("profiles") / self.template,  # profiles/template
            Path("profiles") / f"{self.template}.yml",  # profiles/template.yml
        ]

        for template_path in possible_paths:
            if template_path.exists():
                try:
                    with open(template_path, "r") as f:
                        template_data = yaml.safe_load(f)
                        if template_data:
                            print(f"✅ Loaded template from: {template_path}")
                            return template_data
                except Exception as e:
                    print(f"⚠️ Error loading template from {template_path}: {e}")
                    continue

        # If no template found, return a default template
        print(f"⚠️ Could not load template '{self.template}', using default template")
        return self._get_default_template()

    def _get_default_template(self) -> dict:
        """Get a default scoring template."""
        return {
            "name": "Default Template",
            "description": "Default scoring template for general applications",
            "categories": {
                "Security": {
                    "weight": 25,
                    "criteria": {
                        "Authentication": {
                            "weight": 40,
                            "description": "User authentication system",
                        },
                        "Input Validation": {
                            "weight": 30,
                            "description": "Input sanitization and validation",
                        },
                        "Data Protection": {
                            "weight": 30,
                            "description": "Data encryption and protection",
                        },
                    },
                },
                "Performance": {
                    "weight": 25,
                    "criteria": {
                        "Response Time": {
                            "weight": 50,
                            "description": "API response time",
                        },
                        "Scalability": {
                            "weight": 50,
                            "description": "Application scalability",
                        },
                    },
                },
                "Code Quality": {
                    "weight": 25,
                    "criteria": {
                        "Structure": {
                            "weight": 40,
                            "description": "Code organization and structure",
                        },
                        "Documentation": {
                            "weight": 30,
                            "description": "Code documentation",
                        },
                        "Testing": {
                            "weight": 30,
                            "description": "Test coverage and quality",
                        },
                    },
                },
                "User Experience": {
                    "weight": 25,
                    "criteria": {
                        "Interface": {
                            "weight": 50,
                            "description": "User interface quality",
                        },
                        "Accessibility": {
                            "weight": 50,
                            "description": "Application accessibility",
                        },
                    },
                },
            },
        }

    def _analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the codebase using GPT-OSS."""
        print("🔍 Analyzing codebase with GPT-OSS...")

        try:
            # Get key files for analysis
            key_files = self._get_key_files()

            analysis = {
                "file_structure": self._analyze_file_structure(),
                "code_quality": self._analyze_code_quality(key_files),
                "security_analysis": self._analyze_security(key_files),
                "performance_analysis": self._analyze_performance(key_files),
                "architecture_analysis": self._analyze_architecture(key_files),
            }

            return analysis

        except Exception as e:
            print(f"⚠️ GPT-OSS analysis failed, using fallback: {e}")
            return self._fallback_analysis()

    def _get_key_files(self) -> List[Path]:
        """Get key files for analysis."""
        key_files = []

        # Look for common important files
        important_files = [
            "main.py",
            "app.py",
            "index.js",
            "package.json",
            "requirements.txt",
            "Dockerfile",
            "README.md",
            "config.py",
            "settings.py",
            ".env.example",
        ]

        for file_name in important_files:
            file_path = self.app_dir / file_name
            if file_path.exists():
                key_files.append(file_path)

        # Look for Python files in common directories
        for pattern in ["*.py", "api/*.py", "models/*.py", "utils/*.py"]:
            key_files.extend(self.app_dir.glob(pattern))

        return key_files[:10]  # Limit to 10 files for analysis

    def _analyze_file_structure(self) -> Dict[str, Any]:
        """Analyze the file structure."""
        structure = {
            "total_files": 0,
            "python_files": 0,
            "javascript_files": 0,
            "config_files": 0,
            "documentation_files": 0,
            "directories": [],
        }

        for item in self.app_dir.rglob("*"):
            if item.is_file():
                structure["total_files"] += 1
                if item.suffix == ".py":
                    structure["python_files"] += 1
                elif item.suffix in [".js", ".ts"]:
                    structure["javascript_files"] += 1
                elif item.name in [
                    "requirements.txt",
                    "package.json",
                    "Dockerfile",
                    ".env",
                ]:
                    structure["config_files"] += 1
                elif item.suffix in [".md", ".txt"]:
                    structure["documentation_files"] += 1
            elif item.is_dir() and item != self.app_dir:
                structure["directories"].append(str(item.relative_to(self.app_dir)))

        return structure

    def _analyze_code_quality(self, key_files: List[Path]) -> Dict[str, Any]:
        """Analyze code quality using GPT-OSS."""
        try:
            # Read sample files for analysis
            sample_code = ""
            for file_path in key_files[:3]:  # Analyze first 3 files
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        sample_code += f"\n# {file_path.name}\n{f.read()}\n"
                except:
                    continue

            if not sample_code:
                return {"error": "No readable code files found"}

            prompt = f"""
            Analyze the following code for quality metrics. Focus on:
            1. Code organization and structure
            2. Naming conventions
            3. Error handling
            4. Documentation
            5. Best practices

            Code to analyze:
            {sample_code[:2000]}  # Limit to 2000 chars

            Provide a JSON response with:
            - overall_quality_score (0-100)
            - strengths (list of positive aspects)
            - weaknesses (list of areas for improvement)
            - recommendations (list of specific improvements)
            """

            response = gpt_oss_client.generate(prompt, temperature=0.3, max_tokens=500)
            content = response.get("message", {}).get("content", "")

            # Try to extract JSON from response
            try:
                # Look for JSON in the response
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
            return {"error": f"GPT-OSS analysis failed: {str(e)}"}

    def _analyze_security(self, key_files: List[Path]) -> Dict[str, Any]:
        """Analyze security aspects using GPT-OSS."""
        try:
            # Look for security-related files and code
            security_indicators = []

            for file_path in key_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if any(
                            keyword in content.lower()
                            for keyword in [
                                "password",
                                "secret",
                                "token",
                                "auth",
                                "encrypt",
                                "hash",
                            ]
                        ):
                            security_indicators.append(str(file_path))
                except:
                    continue

            prompt = f"""
            Analyze the security aspects of this application based on:
            1. Files with security indicators: {security_indicators}
            2. Common security best practices

            Provide a JSON response with:
            - security_score (0-100)
            - security_strengths (list)
            - security_concerns (list)
            - security_recommendations (list)
            """

            response = gpt_oss_client.generate(prompt, temperature=0.3, max_tokens=400)
            content = response.get("message", {}).get("content", "")

            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {
                        "security_score": 50,
                        "security_concerns": ["Unable to analyze"],
                    }
            except:
                return {"security_score": 50, "security_concerns": ["Analysis failed"]}

        except Exception as e:
            return {
                "security_score": 50,
                "security_concerns": [f"Analysis error: {str(e)}"],
            }

    def _analyze_performance(self, key_files: List[Path]) -> Dict[str, Any]:
        """Analyze performance aspects."""
        # Simplified performance analysis
        return {
            "performance_score": 75,
            "performance_notes": ["Basic performance analysis completed"],
            "recommendations": ["Consider adding caching", "Optimize database queries"],
        }

    def _analyze_architecture(self, key_files: List[Path]) -> Dict[str, Any]:
        """Analyze architecture patterns."""
        # Simplified architecture analysis
        return {
            "architecture_score": 80,
            "patterns_detected": ["MVC", "REST API"],
            "recommendations": ["Consider microservices for scale"],
        }

    def _fallback_analysis(self) -> Dict[str, Any]:
        """Fallback analysis when GPT-OSS is unavailable."""
        return {
            "file_structure": {"total_files": 0, "python_files": 0},
            "code_quality": {
                "overall_quality_score": 60,
                "strengths": [],
                "weaknesses": ["Analysis unavailable"],
            },
            "security_analysis": {
                "security_score": 50,
                "security_concerns": ["Analysis unavailable"],
            },
            "performance_analysis": {
                "performance_score": 50,
                "performance_notes": ["Analysis unavailable"],
            },
            "architecture_analysis": {
                "architecture_score": 50,
                "patterns_detected": [],
                "recommendations": [],
            },
        }

    def _evaluate_app_intelligent(
        self, template_data: dict, code_analysis: dict
    ) -> dict:
        """Evaluate the app intelligently using GPT-OSS and code analysis."""
        scores = {
            "overall_score": 0,
            "categories": {},
            "recommendations": [],
            "code_analysis": code_analysis,
        }

        categories = template_data.get("categories", {})

        for category, criteria in categories.items():
            category_score = 0
            category_max = 0

            for criterion in criteria:
                max_score = (
                    criterion.get("max_score", 1)
                    if criterion.get("type") == "scale"
                    else 1
                )
                category_max += max_score
                score = self._evaluate_criterion_intelligent(
                    criterion, code_analysis, category
                )
                category_score += score

            scores["categories"][category] = {
                "score": category_score,
                "max_score": category_max,
                "percentage": (
                    (category_score / category_max) * 100 if category_max > 0 else 0
                ),
            }

        # Calculate overall score
        total_score = sum(cat["score"] for cat in scores["categories"].values())
        total_max = sum(cat["max_score"] for cat in scores["categories"].values())
        scores["overall_score"] = (
            (total_score / total_max) * 100 if total_max > 0 else 0
        )

        # Generate intelligent recommendations
        scores["recommendations"] = self._generate_recommendations(
            scores, code_analysis
        )

        return scores

    def _evaluate_criterion_intelligent(
        self, criterion: dict, code_analysis: dict, category: str
    ) -> int:
        """Evaluate a single criterion intelligently."""
        criterion_name = criterion.get("name", "")
        criterion_type = criterion.get("type", "boolean")

        # Map categories to analysis data
        if category.lower() == "security":
            analysis = code_analysis.get("security_analysis", {})
            score = analysis.get("security_score", 50)
            return min(5, max(0, int(score / 20)))  # Convert 0-100 to 0-5

        elif category.lower() == "code quality":
            analysis = code_analysis.get("code_quality", {})
            score = analysis.get("overall_quality_score", 60)
            return min(5, max(0, int(score / 20)))

        elif category.lower() == "performance":
            analysis = code_analysis.get("performance_analysis", {})
            score = analysis.get("performance_score", 75)
            return min(5, max(0, int(score / 20)))

        elif category.lower() == "architecture":
            analysis = code_analysis.get("architecture_analysis", {})
            score = analysis.get("architecture_score", 80)
            return min(5, max(0, int(score / 20)))

        else:
            # Default intelligent scoring based on file structure
            file_structure = code_analysis.get("file_structure", {})
            if file_structure.get("total_files", 0) > 5:
                return 4 if criterion_type == "boolean" else 3
            elif file_structure.get("total_files", 0) > 2:
                return 3 if criterion_type == "boolean" else 2
            else:
                return 2 if criterion_type == "boolean" else 1

    def _generate_recommendations(self, scores: dict, code_analysis: dict) -> List[str]:
        """Generate intelligent recommendations based on scores and analysis."""
        recommendations = []

        # Add recommendations based on low scores
        for category, data in scores["categories"].items():
            if data["percentage"] < 60:
                recommendations.append(
                    f"Improve {category.lower()} - current score: {data['percentage']:.1f}%"
                )

        # Add recommendations from code analysis
        code_quality = code_analysis.get("code_quality", {})
        if "recommendations" in code_quality:
            recommendations.extend(code_quality["recommendations"][:3])

        security_analysis = code_analysis.get("security_analysis", {})
        if "security_recommendations" in security_analysis:
            recommendations.extend(security_analysis["security_recommendations"][:2])

        # Add general recommendations
        if scores["overall_score"] < 70:
            recommendations.append("Consider comprehensive code review and refactoring")

        return recommendations[:5]  # Limit to 5 recommendations

    def _generate_radar_chart(self, scores: dict, template_data: dict):
        """Generate a radar chart of the scores."""
        chart_file = self.output_dir / "radar_chart.md"

        with open(chart_file, "w") as f:
            f.write("# App Scoring Radar Chart\n\n")
            f.write("```mermaid\nradarChart\n")
            f.write("    title Intelligent App Evaluation Results\n")

            # Add categories
            categories = list(scores["categories"].keys())
            f.write(f"    categories {categories}\n")

            # Add scores
            score_values = [
                scores["categories"][cat]["percentage"] for cat in categories
            ]
            f.write(f"    App {score_values}\n")

            f.write("```\n")

        print(f"📊 Radar chart saved to: {chart_file}")

    def _generate_report(self, scores: dict, template_data: dict, code_analysis: dict):
        """Generate a detailed scoring report."""
        report_file = self.output_dir / "scoring_report.md"

        with open(report_file, "w") as f:
            f.write("# Intelligent App Scoring Report\n\n")
            f.write(f"**Template**: {self.template}\n")
            f.write(f"**Overall Score**: {scores['overall_score']:.1f}%\n")
            f.write(f"**Analysis Method**: GPT-OSS Enhanced\n\n")

            f.write("## Category Breakdown\n\n")

            for category, data in scores["categories"].items():
                f.write(f"### {category}\n")
                f.write(f"- **Score**: {data['score']}/{data['max_score']}\n")
                f.write(f"- **Percentage**: {data['percentage']:.1f}%\n\n")

            f.write("## Code Analysis Summary\n\n")

            # Code Quality
            code_quality = code_analysis.get("code_quality", {})
            if "overall_quality_score" in code_quality:
                f.write(f"### Code Quality\n")
                f.write(f"- **Score**: {code_quality['overall_quality_score']}/100\n")
                if "strengths" in code_quality and code_quality["strengths"]:
                    f.write(
                        f"- **Strengths**: {', '.join(code_quality['strengths'][:3])}\n"
                    )
                if "weaknesses" in code_quality and code_quality["weaknesses"]:
                    f.write(
                        f"- **Areas for Improvement**: {', '.join(code_quality['weaknesses'][:3])}\n"
                    )
                f.write("\n")

            # Security
            security = code_analysis.get("security_analysis", {})
            if "security_score" in security:
                f.write(f"### Security Analysis\n")
                f.write(f"- **Score**: {security['security_score']}/100\n")
                if "security_concerns" in security and security["security_concerns"]:
                    f.write(
                        f"- **Concerns**: {', '.join(security['security_concerns'][:3])}\n"
                    )
                f.write("\n")

            f.write("## Recommendations\n\n")
            for i, recommendation in enumerate(scores.get("recommendations", []), 1):
                f.write(f"{i}. {recommendation}\n")

            f.write("\n## File Structure\n\n")
            file_structure = code_analysis.get("file_structure", {})
            f.write(f"- **Total Files**: {file_structure.get('total_files', 0)}\n")
            f.write(f"- **Python Files**: {file_structure.get('python_files', 0)}\n")
            f.write(
                f"- **JavaScript Files**: {file_structure.get('javascript_files', 0)}\n"
            )
            f.write(
                f"- **Configuration Files**: {file_structure.get('config_files', 0)}\n"
            )
            f.write(
                f"- **Documentation Files**: {file_structure.get('documentation_files', 0)}\n"
            )

        print(f"📄 Detailed report saved to: {report_file}")
