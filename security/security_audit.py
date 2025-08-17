#!/usr/bin/env python3
"""
AutoDevCore Security Audit Tool
Comprehensive security assessment and hardening
"""

import ast
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class SecurityAuditor:
    """Comprehensive security auditor for AutoDevCore."""

    def __init__(self):
        self.audit_results = {
            "overall_score": 0,
            "critical_issues": [],
            "high_issues": [],
            "medium_issues": [],
            "low_issues": [],
            "recommendations": [],
            "compliance": {},
        }

    def run_full_audit(self) -> Dict[str, Any]:
        """Run comprehensive security audit."""
        print("🔒 AutoDevCore Security Audit")
        print("=" * 50)

        # 1. Code Security Analysis
        self.audit_code_security()

        # 2. Dependency Security
        self.audit_dependencies()

        # 3. Configuration Security
        self.audit_configuration()

        # 4. Authentication & Authorization
        self.audit_auth_security()

        # 5. Data Security
        self.audit_data_security()

        # 6. Network Security
        self.audit_network_security()

        # 7. OWASP Compliance
        self.audit_owasp_compliance()

        # 8. Generate Security Report
        self.generate_security_report()

        return self.audit_results

    def audit_code_security(self):
        """Audit code for security vulnerabilities."""
        print("🔍 Auditing Code Security...")

        # Check for common security issues
        security_patterns = {
            "sql_injection": [
                r"execute\s*\(\s*[\"'].*\+.*[\"']",
                r"cursor\.execute\s*\(\s*[\"'].*\+.*[\"']",
            ],
            "command_injection": [
                r"subprocess\.call\s*\(\s*[\"'].*\+.*[\"']",
                r"os\.system\s*\(\s*[\"'].*\+.*[\"']",
            ],
            "path_traversal": [
                r"open\s*\(\s*[\"'].*\+.*[\"']",
                r"Path\s*\(\s*[\"'].*\+.*[\"']",
            ],
            "hardcoded_secrets": [
                r"password\s*=\s*[\"'][^\"']+[\"']",
                r"secret\s*=\s*[\"'][^\"']+[\"']",
                r"api_key\s*=\s*[\"'][^\"']+[\"']",
            ],
        }

        issues_found = []

        for file_path in Path(".").rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, "r") as f:
                    content = f.read()

                for vuln_type, patterns in security_patterns.items():
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues_found.append(
                                {
                                    "type": vuln_type,
                                    "file": str(file_path),
                                    "severity": (
                                        "high"
                                        if vuln_type
                                        in ["sql_injection", "command_injection"]
                                        else "medium"
                                    ),
                                    "description": f"Potential {vuln_type} vulnerability found",
                                }
                            )
            except Exception as e:
                print(f"Warning: Could not audit {file_path}: {e}")

        # Add findings to results
        for issue in issues_found:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            else:
                self.audit_results["medium_issues"].append(issue)

        print(f"✅ Code security audit complete: {len(issues_found)} issues found")

    def audit_dependencies(self):
        """Audit dependencies for vulnerabilities."""
        print("📦 Auditing Dependencies...")

        try:
            # Run safety check
            result = subprocess.run(
                ["safety", "check", "--json"], capture_output=True, text=True
            )

            if result.returncode == 0:
                vulnerabilities = json.loads(result.stdout)

                for vuln in vulnerabilities:
                    issue = {
                        "type": "dependency_vulnerability",
                        "package": vuln.get("package", "unknown"),
                        "severity": vuln.get("severity", "medium"),
                        "description": vuln.get("description", "Vulnerability found"),
                        "cve": vuln.get("cve", "N/A"),
                    }

                    if issue["severity"] == "high":
                        self.audit_results["high_issues"].append(issue)
                    else:
                        self.audit_results["medium_issues"].append(issue)

                print(
                    f"✅ Dependency audit complete: {len(vulnerabilities)} vulnerabilities found"
                )
            else:
                print("⚠️ Safety check not available, skipping dependency audit")

        except Exception as e:
            print(f"⚠️ Dependency audit failed: {e}")

    def audit_configuration(self):
        """Audit configuration security."""
        print("⚙️ Auditing Configuration Security...")

        config_issues = []

        # Check for environment file
        if Path(".env").exists():
            config_issues.append(
                {
                    "type": "environment_file",
                    "severity": "medium",
                    "description": ".env file found - ensure it's not committed to version control",
                }
            )

        # Check for hardcoded secrets in config files
        config_files = [".env.example", "config.py", "settings.py"]
        for config_file in config_files:
            if Path(config_file).exists():
                with open(config_file, "r") as f:
                    content = f.read()
                    if re.search(r"password\s*=\s*[\"'][^\"']+[\"']", content):
                        config_issues.append(
                            {
                                "type": "hardcoded_secret",
                                "file": config_file,
                                "severity": "high",
                                "description": "Hardcoded password found in configuration",
                            }
                        )

        # Check Docker security
        if Path("Dockerfile").exists():
            with open("Dockerfile", "r") as f:
                content = f.read()
                if "USER root" in content and "USER autodev" not in content:
                    config_issues.append(
                        {
                            "type": "docker_security",
                            "severity": "medium",
                            "description": "Docker container runs as root - consider using non-root user",
                        }
                    )

        # Add findings
        for issue in config_issues:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            else:
                self.audit_results["medium_issues"].append(issue)

        print(f"✅ Configuration audit complete: {len(config_issues)} issues found")

    def audit_auth_security(self):
        """Audit authentication and authorization security."""
        print("🔐 Auditing Authentication Security...")

        auth_issues = []

        # Check for JWT implementation
        jwt_files = list(Path(".").rglob("*jwt*")) + list(Path(".").rglob("*auth*"))
        if not jwt_files:
            auth_issues.append(
                {
                    "type": "authentication",
                    "severity": "high",
                    "description": "No authentication system found - implement JWT or OAuth",
                }
            )

        # Check for password hashing
        password_files = list(Path(".").rglob("*password*"))
        hashing_found = False
        for file_path in password_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    if "bcrypt" in content or "hashlib" in content:
                        hashing_found = True
                        break
            except:
                continue

        if not hashing_found:
            auth_issues.append(
                {
                    "type": "password_security",
                    "severity": "high",
                    "description": "No password hashing found - implement bcrypt or similar",
                }
            )

        # Check for role-based access control
        rbac_files = list(Path(".").rglob("*role*")) + list(
            Path(".").rglob("*permission*")
        )
        if not rbac_files:
            auth_issues.append(
                {
                    "type": "authorization",
                    "severity": "medium",
                    "description": "No role-based access control found - implement RBAC",
                }
            )

        # Add findings
        for issue in auth_issues:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            else:
                self.audit_results["medium_issues"].append(issue)

        print(f"✅ Authentication audit complete: {len(auth_issues)} issues found")

    def audit_data_security(self):
        """Audit data security and privacy."""
        print("💾 Auditing Data Security...")

        data_issues = []

        # Check for data encryption
        encryption_files = list(Path(".").rglob("*encrypt*")) + list(
            Path(".").rglob("*crypto*")
        )
        if not encryption_files:
            data_issues.append(
                {
                    "type": "data_encryption",
                    "severity": "medium",
                    "description": "No data encryption found - implement encryption for sensitive data",
                }
            )

        # Check for secure data storage
        if Path("data").exists():
            data_files = list(Path("data").rglob("*.json"))
            for data_file in data_files:
                try:
                    with open(data_file, "r") as f:
                        content = f.read()
                        if "password" in content.lower() or "secret" in content.lower():
                            data_issues.append(
                                {
                                    "type": "sensitive_data",
                                    "file": str(data_file),
                                    "severity": "high",
                                    "description": "Sensitive data found in plain text file",
                                }
                            )
                except:
                    continue

        # Check for data validation
        validation_files = list(Path(".").rglob("*validate*")) + list(
            Path(".").rglob("*pydantic*")
        )
        if not validation_files:
            data_issues.append(
                {
                    "type": "data_validation",
                    "severity": "medium",
                    "description": "No data validation found - implement input validation",
                }
            )

        # Add findings
        for issue in data_issues:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            else:
                self.audit_results["medium_issues"].append(issue)

        print(f"✅ Data security audit complete: {len(data_issues)} issues found")

    def audit_network_security(self):
        """Audit network security."""
        print("🌐 Auditing Network Security...")

        network_issues = []

        # Check for HTTPS configuration
        if Path("docker-compose.yml").exists():
            with open("docker-compose.yml", "r") as f:
                content = f.read()
                if "443" in content and "ssl" in content:
                    network_issues.append(
                        {
                            "type": "ssl_configuration",
                            "severity": "low",
                            "description": "SSL/TLS configuration found - good practice",
                        }
                    )
                else:
                    network_issues.append(
                        {
                            "type": "ssl_missing",
                            "severity": "medium",
                            "description": "No SSL/TLS configuration found - implement HTTPS",
                        }
                    )

        # Check for CORS configuration
        cors_files = list(Path(".").rglob("*cors*"))
        if not cors_files:
            network_issues.append(
                {
                    "type": "cors_configuration",
                    "severity": "medium",
                    "description": "No CORS configuration found - implement proper CORS settings",
                }
            )

        # Check for rate limiting
        rate_limit_files = list(Path(".").rglob("*rate*")) + list(
            Path(".").rglob("*throttle*")
        )
        if not rate_limit_files:
            network_issues.append(
                {
                    "type": "rate_limiting",
                    "severity": "medium",
                    "description": "No rate limiting found - implement rate limiting for API endpoints",
                }
            )

        # Add findings
        for issue in network_issues:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            elif issue["severity"] == "medium":
                self.audit_results["medium_issues"].append(issue)
            else:
                self.audit_results["low_issues"].append(issue)

        print(f"✅ Network security audit complete: {len(network_issues)} issues found")

    def audit_owasp_compliance(self):
        """Audit OWASP Top 10 compliance."""
        print("🛡️ Auditing OWASP Compliance...")

        owasp_issues = []

        # OWASP Top 10 checks
        owasp_checks = {
            "A01:2021 - Broken Access Control": self.check_access_control(),
            "A02:2021 - Cryptographic Failures": self.check_cryptography(),
            "A03:2021 - Injection": self.check_injection_vulnerabilities(),
            "A04:2021 - Insecure Design": self.check_design_security(),
            "A05:2021 - Security Misconfiguration": self.check_configuration(),
            "A06:2021 - Vulnerable Components": self.check_vulnerable_components(),
            "A07:2021 - Authentication Failures": self.check_authentication(),
            "A08:2021 - Software and Data Integrity Failures": self.check_data_integrity(),
            "A09:2021 - Security Logging Failures": self.check_logging(),
            "A10:2021 - Server-Side Request Forgery": self.check_ssrf(),
        }

        for owasp_item, issues in owasp_checks.items():
            for issue in issues:
                issue["owasp_category"] = owasp_item
                owasp_issues.append(issue)

        # Add findings
        for issue in owasp_issues:
            if issue["severity"] == "high":
                self.audit_results["high_issues"].append(issue)
            elif issue["severity"] == "medium":
                self.audit_results["medium_issues"].append(issue)
            else:
                self.audit_results["low_issues"].append(issue)

        print(f"✅ OWASP compliance audit complete: {len(owasp_issues)} issues found")

    def check_access_control(self) -> List[Dict[str, Any]]:
        """Check for broken access control."""
        issues = []

        # Check for proper authorization checks
        auth_files = list(Path(".").rglob("*auth*")) + list(
            Path(".").rglob("*permission*")
        )
        if not auth_files:
            issues.append(
                {
                    "type": "access_control",
                    "severity": "high",
                    "description": "No access control implementation found",
                }
            )

        return issues

    def check_cryptography(self) -> List[Dict[str, Any]]:
        """Check for cryptographic failures."""
        issues = []

        # Check for weak crypto
        crypto_files = list(Path(".").rglob("*crypto*")) + list(
            Path(".").rglob("*hash*")
        )
        for file_path in crypto_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    if "md5" in content or "sha1" in content:
                        issues.append(
                            {
                                "type": "weak_crypto",
                                "file": str(file_path),
                                "severity": "high",
                                "description": "Weak cryptographic algorithm found (MD5/SHA1)",
                            }
                        )
            except:
                continue

        return issues

    def check_injection_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Check for injection vulnerabilities."""
        issues = []

        # Check for SQL injection
        sql_patterns = [
            r"execute\s*\(\s*[\"'].*\+.*[\"']",
            r"cursor\.execute\s*\(\s*[\"'].*\+.*[\"']",
        ]

        for file_path in Path(".").rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    for pattern in sql_patterns:
                        if re.search(pattern, content):
                            issues.append(
                                {
                                    "type": "sql_injection",
                                    "file": str(file_path),
                                    "severity": "high",
                                    "description": "Potential SQL injection vulnerability",
                                }
                            )
            except:
                continue

        return issues

    def check_design_security(self) -> List[Dict[str, Any]]:
        """Check for insecure design."""
        issues = []

        # Check for proper input validation
        validation_files = list(Path(".").rglob("*validate*")) + list(
            Path(".").rglob("*pydantic*")
        )
        if not validation_files:
            issues.append(
                {
                    "type": "input_validation",
                    "severity": "medium",
                    "description": "No input validation found - implement proper validation",
                }
            )

        return issues

    def check_configuration(self) -> List[Dict[str, Any]]:
        """Check for security misconfiguration."""
        issues = []

        # Check for debug mode in production
        if Path(".env").exists():
            with open(".env", "r") as f:
                content = f.read()
                if "DEBUG=true" in content:
                    issues.append(
                        {
                            "type": "debug_mode",
                            "severity": "medium",
                            "description": "Debug mode enabled - disable in production",
                        }
                    )

        return issues

    def check_vulnerable_components(self) -> List[Dict[str, Any]]:
        """Check for vulnerable components."""
        issues = []

        # This is handled by dependency audit
        return issues

    def check_authentication(self) -> List[Dict[str, Any]]:
        """Check for authentication failures."""
        issues = []

        # Check for proper session management
        session_files = list(Path(".").rglob("*session*"))
        if not session_files:
            issues.append(
                {
                    "type": "session_management",
                    "severity": "medium",
                    "description": "No session management found - implement secure sessions",
                }
            )

        return issues

    def check_data_integrity(self) -> List[Dict[str, Any]]:
        """Check for data integrity failures."""
        issues = []

        # Check for data validation
        validation_files = list(Path(".").rglob("*validate*"))
        if not validation_files:
            issues.append(
                {
                    "type": "data_validation",
                    "severity": "medium",
                    "description": "No data validation found - implement input validation",
                }
            )

        return issues

    def check_logging(self) -> List[Dict[str, Any]]:
        """Check for security logging failures."""
        issues = []

        # Check for security logging
        logging_files = list(Path(".").rglob("*log*"))
        security_logging = False

        for file_path in logging_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    if "security" in content.lower() or "audit" in content.lower():
                        security_logging = True
                        break
            except:
                continue

        if not security_logging:
            issues.append(
                {
                    "type": "security_logging",
                    "severity": "medium",
                    "description": "No security logging found - implement audit logging",
                }
            )

        return issues

    def check_ssrf(self) -> List[Dict[str, Any]]:
        """Check for SSRF vulnerabilities."""
        issues = []

        # Check for URL validation
        url_patterns = [
            r"requests\.get\s*\(\s*[\"'].*\+.*[\"']",
            r"urllib\.request\.urlopen\s*\(\s*[\"'].*\+.*[\"']",
        ]

        for file_path in Path(".").rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    for pattern in url_patterns:
                        if re.search(pattern, content):
                            issues.append(
                                {
                                    "type": "ssrf",
                                    "file": str(file_path),
                                    "severity": "high",
                                    "description": "Potential SSRF vulnerability",
                                }
                            )
            except:
                continue

        return issues

    def generate_security_report(self):
        """Generate comprehensive security report."""
        print("📊 Generating Security Report...")

        # Calculate overall score
        total_issues = (
            len(self.audit_results["critical_issues"]) * 4
            + len(self.audit_results["high_issues"]) * 3
            + len(self.audit_results["medium_issues"]) * 2
            + len(self.audit_results["low_issues"]) * 1
        )

        max_score = 100
        self.audit_results["overall_score"] = max(0, max_score - total_issues)

        # Generate recommendations
        self.generate_recommendations()

        # Save report
        with open("security_audit_report.json", "w") as f:
            json.dump(self.audit_results, f, indent=2, default=str)

        print(f"✅ Security report generated: security_audit_report.json")
        print(f"📈 Overall Security Score: {self.audit_results['overall_score']}/100")

    def generate_recommendations(self):
        """Generate security recommendations."""
        recommendations = []

        # Critical recommendations
        if self.audit_results["critical_issues"]:
            recommendations.append(
                {
                    "priority": "critical",
                    "action": "Fix all critical security issues immediately",
                    "impact": "High risk of security breach",
                }
            )

        # High priority recommendations
        if self.audit_results["high_issues"]:
            recommendations.append(
                {
                    "priority": "high",
                    "action": "Implement authentication and authorization system",
                    "impact": "Prevent unauthorized access",
                }
            )

            recommendations.append(
                {
                    "priority": "high",
                    "action": "Add input validation and sanitization",
                    "impact": "Prevent injection attacks",
                }
            )

        # Medium priority recommendations
        if self.audit_results["medium_issues"]:
            recommendations.append(
                {
                    "priority": "medium",
                    "action": "Implement SSL/TLS encryption",
                    "impact": "Secure data transmission",
                }
            )

            recommendations.append(
                {
                    "priority": "medium",
                    "action": "Add rate limiting and CORS configuration",
                    "impact": "Prevent abuse and improve security",
                }
            )

        # General recommendations
        recommendations.extend(
            [
                {
                    "priority": "medium",
                    "action": "Implement comprehensive logging and monitoring",
                    "impact": "Detect and respond to security incidents",
                },
                {
                    "priority": "medium",
                    "action": "Regular security updates and dependency scanning",
                    "impact": "Keep dependencies secure",
                },
                {
                    "priority": "low",
                    "action": "Implement security headers and CSP",
                    "impact": "Additional security layers",
                },
            ]
        )

        self.audit_results["recommendations"] = recommendations

def main():
    """Run security audit."""
    auditor = SecurityAuditor()
    results = auditor.run_full_audit()

    print("\n" + "=" * 50)
    print("🔒 SECURITY AUDIT SUMMARY")
    print("=" * 50)
    print(f"Overall Score: {results['overall_score']}/100")
    print(f"Critical Issues: {len(results['critical_issues'])}")
    print(f"High Issues: {len(results['high_issues'])}")
    print(f"Medium Issues: {len(results['medium_issues'])}")
    print(f"Low Issues: {len(results['low_issues'])}")
    print("=" * 50)

    if results["overall_score"] >= 80:
        print("✅ Security Status: GOOD")
    elif results["overall_score"] >= 60:
        print("⚠️ Security Status: NEEDS IMPROVEMENT")
    else:
        print("❌ Security Status: CRITICAL - IMMEDIATE ACTION REQUIRED")

    return results

if __name__ == "__main__":
    main()
