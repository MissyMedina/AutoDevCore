"""
Security Scanner Plugin - Scan code for security vulnerabilities
"""

__author__ = "AutoDevCore Team"
__version__ = "1.0.0"
__description__ = (
    "Scans code for common security vulnerabilities and provides remediation advice"
)

import re
import ast
from pathlib import Path
from typing import Dict, List, Any


def run(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scan code for security vulnerabilities.

    Args:
        context (dict): Execution context with plugin_name, output_dir, verbose

    Returns:
        dict: Security scan results with vulnerabilities and recommendations
    """
    output_dir = Path(context.get("output_dir", "./output"))
    verbose = context.get("verbose", False)

    # Find Python files in the current directory
    python_files = list(Path(".").rglob("*.py"))

    security_results = {
        "files_scanned": len(python_files),
        "vulnerabilities": {"critical": [], "high": [], "medium": [], "low": []},
        "security_score": 100,
        "recommendations": [],
    }

    # Security patterns to check
    security_patterns = {
        "critical": [
            (r"eval\s*\(", "Code execution vulnerability - eval() usage"),
            (r"exec\s*\(", "Code execution vulnerability - exec() usage"),
            (r"__import__\s*\(", "Dynamic import vulnerability"),
            (r"pickle\.loads\s*\(", "Unsafe deserialization - pickle usage"),
        ],
        "high": [
            (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password detected"),
            (r"secret\s*=\s*['\"][^'\"]+['\"]", "Hardcoded secret detected"),
            (r"api_key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key detected"),
            (
                r"\.execute\s*\(\s*[^)]*\+",
                "Potential SQL injection - string concatenation",
            ),
        ],
        "medium": [
            (r"input\s*\(", "User input handling - validate and sanitize"),
            (r"raw_input\s*\(", "User input handling - validate and sanitize"),
            (r"subprocess\.call\s*\(", "Command execution - validate input"),
            (r"os\.system\s*\(", "Command execution - validate input"),
        ],
        "low": [
            (r"print\s*\(\s*[^)]*password", "Potential password logging"),
            (r"logging\..*password", "Potential password logging"),
            (r"debug\s*\(\s*[^)]*secret", "Potential secret logging"),
        ],
    }

    for file_path in python_files:
        if "plugins" in str(file_path) or "__pycache__" in str(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for patterns
            for severity, patterns in security_patterns.items():
                for pattern, description in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[: match.start()].count("\n") + 1
                        line_content = content.split("\n")[line_num - 1].strip()

                        vulnerability = {
                            "file": str(file_path),
                            "line": line_num,
                            "description": description,
                            "code": line_content,
                            "pattern": pattern,
                        }

                        security_results["vulnerabilities"][severity].append(
                            vulnerability
                        )

            # AST-based analysis
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Check for dangerous function calls
                        if isinstance(node.func, ast.Name):
                            func_name = node.func.id
                            if func_name in ["eval", "exec", "input"]:
                                line_num = node.lineno
                                line_content = content.split("\n")[line_num - 1].strip()

                                vulnerability = {
                                    "file": str(file_path),
                                    "line": line_num,
                                    "description": f"Dangerous function call: {func_name}()",
                                    "code": line_content,
                                    "pattern": f"{func_name}()",
                                }

                                if func_name in ["eval", "exec"]:
                                    security_results["vulnerabilities"][
                                        "critical"
                                    ].append(vulnerability)
                                else:
                                    security_results["vulnerabilities"][
                                        "medium"
                                    ].append(vulnerability)

            except SyntaxError:
                if verbose:
                    print(f"Syntax error in {file_path}")

        except Exception as e:
            if verbose:
                print(f"Error scanning {file_path}: {e}")

    # Calculate security score
    score_deductions = {"critical": 20, "high": 10, "medium": 5, "low": 2}

    for severity, vulnerabilities in security_results["vulnerabilities"].items():
        deduction = len(vulnerabilities) * score_deductions[severity]
        security_results["security_score"] -= deduction

    security_results["security_score"] = max(security_results["security_score"], 0)

    # Generate recommendations
    if security_results["vulnerabilities"]["critical"]:
        security_results["recommendations"].append(
            "🚨 CRITICAL: Remove all eval() and exec() usage immediately"
        )

    if security_results["vulnerabilities"]["high"]:
        security_results["recommendations"].append(
            "🔴 HIGH: Move hardcoded secrets to environment variables"
        )

    if security_results["vulnerabilities"]["medium"]:
        security_results["recommendations"].append(
            "🟡 MEDIUM: Implement proper input validation and sanitization"
        )

    if security_results["vulnerabilities"]["low"]:
        security_results["recommendations"].append(
            "🟢 LOW: Review logging practices to avoid exposing sensitive data"
        )

    # Save detailed report
    report_file = output_dir / "security_scan_report.md"
    with open(report_file, "w") as f:
        f.write("# Security Scan Report\n\n")
        f.write(f"**Files Scanned**: {security_results['files_scanned']}\n")
        f.write(f"**Security Score**: {security_results['security_score']}/100\n\n")

        for severity in ["critical", "high", "medium", "low"]:
            vulns = security_results["vulnerabilities"][severity]
            if vulns:
                f.write(f"## {severity.upper()} Vulnerabilities ({len(vulns)})\n\n")
                for vuln in vulns:
                    f.write(f"### {vuln['file']}:{vuln['line']}\n")
                    f.write(f"**Issue**: {vuln['description']}\n\n")
                    f.write(f"**Code**: `{vuln['code']}`\n\n")
                    f.write("---\n\n")

        f.write("## Recommendations\n\n")
        for rec in security_results["recommendations"]:
            f.write(f"- {rec}\n")

    return {
        "status": "success",
        "message": "Security scan completed successfully",
        "results": security_results,
        "report_file": str(report_file),
    }
