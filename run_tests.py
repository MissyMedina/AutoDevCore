#!/usr/bin/env python3
"""
Test runner for AutoDevCore.
"""

import sys
import subprocess
import os
from pathlib import Path
import json
from datetime import datetime


def run_tests():
    """Run all tests and generate reports."""
    print("🧪 Running AutoDevCore Test Suite")
    print("=" * 50)
    
    # Create test output directory
    test_output_dir = Path("test_output")
    test_output_dir.mkdir(exist_ok=True)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=.",
        "--cov-report=html:test_output/coverage_html",
        "--cov-report=json:test_output/coverage.json",
        "--cov-report=term-missing",
        "--junitxml=test_output/test_results.xml",
        "--html=test_output/test_report.html",
        "--self-contained-html"
    ]
    
    try:
        print("Running tests...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Save test output
        with open(test_output_dir / "test_output.txt", "w") as f:
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\n\nSTDERR:\n")
            f.write(result.stderr)
        
        # Parse results
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
        
        print(f"\nTest output saved to: {test_output_dir}")
        
        # Generate test summary
        generate_test_summary(result, test_output_dir)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def generate_test_summary(result, output_dir):
    """Generate a test summary report."""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "success": result.returncode == 0,
        "stdout_lines": len(result.stdout.split('\n')),
        "stderr_lines": len(result.stderr.split('\n')),
        "exit_code": result.returncode
    }
    
    # Try to extract test statistics from output
    lines = result.stdout.split('\n')
    for line in lines:
        if "passed" in line and "failed" in line:
            summary["test_stats"] = line.strip()
            break
    
    # Save summary
    with open(output_dir / "test_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"📊 Test summary saved to: {output_dir / 'test_summary.json'}")


def run_performance_tests():
    """Run performance tests."""
    print("\n⚡ Running Performance Tests")
    print("=" * 30)
    
    try:
        # Import and run performance tests
        from tests.test_core import TestPerformance
        
        test_perf = TestPerformance()
        
        print("Testing cache performance...")
        test_perf.test_cache_performance()
        print("✅ Cache performance test passed")
        
        print("Testing thought logging performance...")
        test_perf.test_thought_logging_performance()
        print("✅ Thought logging performance test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("\n🔗 Running Integration Tests")
    print("=" * 30)
    
    try:
        # Import and run integration tests
        from tests.test_core import TestIntegration
        
        test_integration = TestIntegration()
        
        print("Testing compose workflow...")
        test_integration.test_full_compose_workflow()
        print("✅ Compose workflow test passed")
        
        print("Testing score workflow...")
        test_integration.test_full_score_workflow()
        print("✅ Score workflow test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False


def check_code_quality():
    """Check code quality with linting tools."""
    print("\n🔍 Running Code Quality Checks")
    print("=" * 35)
    
    quality_checks = []
    
    # Run flake8
    try:
        print("Running flake8...")
        result = subprocess.run([sys.executable, "-m", "flake8", "."], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ flake8 passed")
            quality_checks.append(("flake8", True, ""))
        else:
            print("❌ flake8 found issues")
            quality_checks.append(("flake8", False, result.stdout))
    except Exception as e:
        print(f"❌ flake8 error: {e}")
        quality_checks.append(("flake8", False, str(e)))
    
    # Run black check
    try:
        print("Running black check...")
        result = subprocess.run([sys.executable, "-m", "black", "--check", "."], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ black formatting check passed")
            quality_checks.append(("black", True, ""))
        else:
            print("❌ black formatting issues found")
            quality_checks.append(("black", False, result.stdout))
    except Exception as e:
        print(f"❌ black error: {e}")
        quality_checks.append(("black", False, str(e)))
    
    # Save quality report
    quality_report = {
        "timestamp": datetime.now().isoformat(),
        "checks": [
            {
                "tool": tool,
                "passed": passed,
                "output": output
            }
            for tool, passed, output in quality_checks
        ]
    }
    
    with open("test_output/quality_report.json", "w") as f:
        json.dump(quality_report, f, indent=2)
    
    print(f"📊 Quality report saved to: test_output/quality_report.json")
    
    return all(passed for _, passed, _ in quality_checks)


def main():
    """Main test runner function."""
    print("🚀 AutoDevCore Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run unit tests
    if not run_tests():
        all_passed = False
    
    # Run performance tests
    if not run_performance_tests():
        all_passed = False
    
    # Run integration tests
    if not run_integration_tests():
        all_passed = False
    
    # Run code quality checks
    if not check_code_quality():
        all_passed = False
    
    # Final summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests and checks passed!")
        print("✅ AutoDevCore is ready for production!")
    else:
        print("⚠️ Some tests or checks failed!")
        print("🔧 Please review the test output and fix issues.")
    
    print(f"\n📁 All test results saved to: test_output/")
    print("📊 Coverage report: test_output/coverage_html/index.html")
    print("📋 Test report: test_output/test_report.html")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
