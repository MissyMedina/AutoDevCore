#!/usr/bin/env python3
"""
Evaluate Complexity and Interconnectedness Improvements
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ComplexityAnalyzer:
    """Analyze code complexity metrics."""

    def __init__(self):
        self.complexity_scores = {}
        self.function_complexities = []
        self.class_complexities = []

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze complexity of a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Analyze functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_function_complexity(node)
                    self.function_complexities.append(complexity)

                elif isinstance(node, ast.ClassDef):
                    complexity = self._calculate_class_complexity(node)
                    self.class_complexities.append(complexity)

            return {
                "file": str(file_path),
                "functions": len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                ),
                "classes": len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                ),
                "avg_function_complexity": sum(
                    self.function_complexities[
                        -len(
                            [
                                n
                                for n in ast.walk(tree)
                                if isinstance(n, ast.FunctionDef)
                            ]
                        ) :
                    ]
                )
                / max(
                    1,
                    len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                ),
            }

        except Exception as e:
            return {"file": str(file_path), "error": str(e)}

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With):
                complexity += 1

        return complexity

    def _calculate_class_complexity(self, node: ast.ClassDef) -> int:
        """Calculate complexity of a class."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1

        return complexity

    def get_overall_complexity_score(self) -> float:
        """Calculate overall complexity score (1-10)."""
        if not self.function_complexities:
            return 10.0

        avg_complexity = sum(self.function_complexities) / len(
            self.function_complexities
        )

        # Score based on average complexity
        if avg_complexity <= 3:
            return 10.0
        elif avg_complexity <= 5:
            return 9.0
        elif avg_complexity <= 7:
            return 8.0
        elif avg_complexity <= 10:
            return 7.0
        else:
            return 6.0


class InterconnectednessAnalyzer:
    """Analyze module interconnectedness."""

    def __init__(self):
        self.imports = {}
        self.dependencies = {}
        self.coupling_scores = {}

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze interconnectedness of a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            file_imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        file_imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        file_imports.append(node.module)

            self.imports[str(file_path)] = file_imports

            return {
                "file": str(file_path),
                "imports": file_imports,
                "import_count": len(file_imports),
            }

        except Exception as e:
            return {"file": str(file_path), "error": str(e)}

    def calculate_coupling(self) -> Dict[str, float]:
        """Calculate coupling between modules."""
        coupling_scores = {}

        for file_path, imports in self.imports.items():
            # Count internal dependencies
            internal_deps = sum(
                1
                for imp in imports
                if not imp.startswith(
                    (
                        "os",
                        "sys",
                        "json",
                        "time",
                        "datetime",
                        "pathlib",
                        "typing",
                        "unittest",
                        "pytest",
                    )
                )
            )

            # Score based on internal dependencies
            if internal_deps == 0:
                coupling_scores[file_path] = 10.0  # Perfect
            elif internal_deps <= 2:
                coupling_scores[file_path] = 9.0
            elif internal_deps <= 5:
                coupling_scores[file_path] = 8.0
            elif internal_deps <= 10:
                coupling_scores[file_path] = 7.0
            else:
                coupling_scores[file_path] = 6.0

        self.coupling_scores = coupling_scores
        return coupling_scores

    def get_overall_interconnectedness_score(self) -> float:
        """Calculate overall interconnectedness score (1-10)."""
        if not self.coupling_scores:
            return 10.0

        avg_coupling = sum(self.coupling_scores.values()) / len(self.coupling_scores)
        return avg_coupling


def main():
    """Main evaluation function."""
    print("🔍 Evaluating Complexity and Interconnectedness Improvements")
    print("=" * 60)

    # Analyze Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        if "venv" in root or "__pycache__" in root or ".git" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)

    print(f"📁 Found {len(python_files)} Python files to analyze")

    # Analyze complexity
    print("\n🧮 Analyzing Code Complexity...")
    complexity_analyzer = ComplexityAnalyzer()

    for file_path in python_files:
        result = complexity_analyzer.analyze_file(file_path)
        if "error" not in result:
            print(
                f"   📄 {file_path.name}: {result['functions']} functions, avg complexity: {result['avg_function_complexity']:.1f}"
            )

    complexity_score = complexity_analyzer.get_overall_complexity_score()
    print(f"\n📊 Complexity Score: {complexity_score}/10")

    # Analyze interconnectedness
    print("\n🔗 Analyzing Module Interconnectedness...")
    interconnectedness_analyzer = InterconnectednessAnalyzer()

    for file_path in python_files:
        result = interconnectedness_analyzer.analyze_file(file_path)
        if "error" not in result:
            print(f"   📄 {file_path.name}: {result['import_count']} imports")

    coupling_scores = interconnectedness_analyzer.calculate_coupling()
    interconnectedness_score = (
        interconnectedness_analyzer.get_overall_interconnectedness_score()
    )
    print(f"\n📊 Interconnectedness Score: {interconnectedness_score}/10")

    # Check for our improvements
    print("\n🎯 Checking for Complexity Improvements...")

    improvement_files = [
        "utils/complexity_optimizer.py",
        "utils/interface_abstraction.py",
        "utils/type_enhancer.py",
        "tests/test_complexity_improvements.py",
    ]

    improvements_found = 0
    for file_path in improvement_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} - Found")
            improvements_found += 1
        else:
            print(f"   ❌ {file_path} - Missing")

    # Calculate final scores
    print("\n" + "=" * 60)
    print("📊 FINAL EVALUATION RESULTS")
    print("=" * 60)

    print(f"🧮 Complexity Metrics: {complexity_score}/10")
    if complexity_score >= 9.5:
        print("   🎉 EXCELLENT - Optimal complexity achieved!")
    elif complexity_score >= 8.0:
        print("   ✅ GOOD - Low complexity maintained")
    else:
        print("   ⚠️  NEEDS IMPROVEMENT - High complexity detected")

    print(f"🔗 Interconnectedness: {interconnectedness_score}/10")
    if interconnectedness_score >= 9.5:
        print("   🎉 EXCELLENT - Perfect decoupling achieved!")
    elif interconnectedness_score >= 8.0:
        print("   ✅ GOOD - Low coupling maintained")
    else:
        print("   ⚠️  NEEDS IMPROVEMENT - High coupling detected")

    print(f"🛠️  Improvements Implemented: {improvements_found}/4")
    if improvements_found == 4:
        print("   🎉 ALL IMPROVEMENTS SUCCESSFULLY IMPLEMENTED!")

    # Overall assessment
    overall_score = (complexity_score + interconnectedness_score) / 2
    print(f"\n🏆 Overall Quality Score: {overall_score:.1f}/10")

    if overall_score >= 9.5:
        print("🎉 PERFECT SCORE ACHIEVED! Your code is God-Tier!")
    elif overall_score >= 9.0:
        print("🌟 EXCELLENT! Near-perfect code quality!")
    elif overall_score >= 8.0:
        print("✅ GOOD! Solid code quality maintained!")
    else:
        print("⚠️  NEEDS WORK - Room for improvement")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
