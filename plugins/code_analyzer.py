"""
Code Analyzer Plugin - Analyze code complexity and quality metrics
"""

__author__ = "AutoDevCore Team"
__version__ = "1.0.0"
__description__ = (
    "Analyzes code complexity, quality metrics, and provides recommendations"
)

import ast
import os
from pathlib import Path
from typing import Any, Dict, List

def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze code complexity and quality metrics.

    Args:
        context (dict): Execution context with plugin_name, output_dir, verbose

    Returns:
        dict: Analysis results with metrics and recommendations
    """
    output_dir = Path(context.get("output_dir", "./output"))
    verbose = context.get("verbose", False)

    # Find Python files in the current directory
    python_files = list(Path(".").rglob("*.py"))

    analysis_results = {
        "files_analyzed": len(python_files),
        "total_lines": 0,
        "functions": [],
        "classes": [],
        "complexity_metrics": {
            "high_complexity_functions": [],
            "long_functions": [],
            "deep_nesting": [],
        },
        "quality_issues": [],
        "recommendations": [],
    }

    for file_path in python_files:
        if "plugins" in str(file_path) or "__pycache__" in str(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                analysis_results["total_lines"] += len(lines)

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_info = {
                        "name": node.name,
                        "file": str(file_path),
                        "line": node.lineno,
                        "length": len(node.body),
                        "complexity": calculate_complexity(node),
                    }
                    analysis_results["functions"].append(function_info)

                    # Check for issues
                    if function_info["complexity"] > 10:
                        analysis_results["complexity_metrics"][
                            "high_complexity_functions"
                        ].append(function_info)

                    if function_info["length"] > 20:
                        analysis_results["complexity_metrics"]["long_functions"].append(
                            function_info
                        )

                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "file": str(file_path),
                        "line": node.lineno,
                        "methods": len(
                            [n for n in node.body if isinstance(n, ast.FunctionDef)]
                        ),
                    }
                    analysis_results["classes"].append(class_info)

        except Exception as e:
            if verbose:
                print(f"Error analyzing {file_path}: {e}")

    # Generate recommendations
    if analysis_results["complexity_metrics"]["high_complexity_functions"]:
        analysis_results["recommendations"].append(
            "Consider refactoring high complexity functions into smaller, more focused functions"
        )

    if analysis_results["complexity_metrics"]["long_functions"]:
        analysis_results["recommendations"].append(
            "Break down long functions into smaller, more manageable pieces"
        )

    if analysis_results["total_lines"] > 1000:
        analysis_results["recommendations"].append(
            "Consider splitting large files into smaller modules"
        )

    # Save detailed report
    report_file = output_dir / "code_analysis_report.md"
    with open(report_file, "w") as f:
        f.write("# Code Analysis Report\n\n")
        f.write(f"**Files Analyzed**: {analysis_results['files_analyzed']}\n")
        f.write(f"**Total Lines**: {analysis_results['total_lines']}\n")
        f.write(f"**Functions**: {len(analysis_results['functions'])}\n")
        f.write(f"**Classes**: {len(analysis_results['classes'])}\n\n")

        f.write("## Quality Issues\n\n")
        for issue in analysis_results["quality_issues"]:
            f.write(f"- {issue}\n")

        f.write("\n## Recommendations\n\n")
        for rec in analysis_results["recommendations"]:
            f.write(f"- {rec}\n")

    return {
        "status": "success",
        "message": "Code analysis completed successfully",
        "results": analysis_results,
        "report_file": str(report_file),
    }

def calculate_complexity(node: ast.AST) -> int:
    """Calculate cyclomatic complexity of an AST node."""
    complexity = 1  # Base complexity

    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif isinstance(child, ast.ExceptHandler):
            complexity += 1
        elif isinstance(child, ast.With):
            complexity += 1
        elif isinstance(child, ast.AsyncWith):
            complexity += 1

    return complexity
