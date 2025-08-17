"""
AutoDevCore End-to-End Test Suite
Comprehensive testing of all features from basic functionality to advanced capabilities
"""

import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
import pytest

# Test environment setup/teardown fixtures
@pytest.fixture(scope="session", name="environment")
def setup_environment():
    """Set up test environment for all tests"""
    # Create temporary directory for tests
    temp_dir = tempfile.mkdtemp(prefix="autodevcore_test_")
    test_app_dir = os.path.join(temp_dir, "test_app")

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Set up project paths
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))

    yield {
        "temp_dir": temp_dir,
        "test_app_dir": test_app_dir,
        "project_root": project_root,
    }

    # Cleanup after all tests are done
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        print("Warning: Failed to clean up test environment")

@pytest.fixture(scope="function", name="output_dir")
def setup_output_dir():
    """Create a clean output directory for each test"""
    output_dir = os.path.join("output", f"test_{time.time()}")
    os.makedirs(output_dir, exist_ok=True)
    yield output_dir
    try:
        shutil.rmtree(output_dir)
    except Exception:
        print("Warning: Failed to clean up test output directory")

# Pytest test functions
# Minimal pytest-compatible smoke test
def test_end_to_end_smoke(environment):
    """Minimal smoke test to ensure the test environment is set up."""
    assert environment["temp_dir"] is not None
    assert environment["test_app_dir"] is not None
    assert environment["project_root"] is not None

def test_ai_model_integration(environment):
    """Test AI model integration and basic operations"""
    try:

        from plugins.ai_orchestrator import AIOrchestrator
        from plugins.multi_model_ai import MultiModelAI

        # Initialize AI components
        multi_model = MultiModelAI()
        orchestrator = AIOrchestrator()

        # Test that the orchestrator can be initialized and has the method
        assert hasattr(
            orchestrator, "generate_response"
        ), "AI orchestrator missing generate_response method"

        # Test AI models can be used
        response = orchestrator.generate_response("Test prompt", task_type="test")
        assert response is not None, "AI model returned no response"

        # Test multi-model AI
        multi_model_result = multi_model.process("Test prompt", model="test")
        assert multi_model_result is not None, "Multi-model AI returned no result"

    except ImportError as e:
        pytest.skip(f"AI model integration test skipped: {e}")
    except Exception as e:
        pytest.fail(f"AI model integration test failed: {e}")

def test_plugin_system(environment):
    """Test plugin system functionality"""
    try:

        from plugins.plugin_manager import PluginManager

        # Initialize plugin manager
        pm = PluginManager()

        # Test plugin listing
        plugins = pm.list_plugins()
        assert plugins is not None, "Plugin listing returned None"

        # Test plugin search
        results = pm.search_plugins("collaboration")
        assert results is not None, "Plugin search returned None"

        # Test plugin validation if available
        if hasattr(pm, "validate_plugin"):
            result = pm.validate_plugin("test_plugin")
            assert result is not None, "Plugin validation failed"

    except ImportError as e:
        pytest.skip(f"Plugin system test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Plugin system test failed: {e}")

def test_collaboration_platform(environment):
    """Test collaboration platform functionality"""
    try:

        from plugins.collaboration_platform import CollaborationPlatform

        # Initialize collaboration platform
        cp = CollaborationPlatform()

        # Test core functionality
        assert hasattr(
            cp, "create_collaborative_project"
        ), "Collaboration platform missing create_collaborative_project method"

        # Test project creation
        if hasattr(cp, "create_collaborative_project"):
            project = cp.create_collaborative_project(
                project_name="test_project",
                description="Test project for integration tests",
                owner_id="test_user",
                owner_email="test@example.com",
            )
            assert project is not None, "Failed to create collaborative project"

    except ImportError as e:
        pytest.skip(f"Collaboration platform test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Collaboration platform test failed: {e}")

def test_performance_optimization(environment, output_dir):
    """Test performance optimization system"""
    try:

        from plugins.performance_optimizer import PerformanceOptimizer

        # Initialize optimizer
        optimizer = PerformanceOptimizer()

        # Test performance optimization
        results = optimizer.run_full_optimization()
        assert results is not None, "Performance optimization returned no results"
        assert isinstance(
            results, dict
        ), "Performance optimization results not in expected format"

        # Test performance report
        report = optimizer.get_performance_report()
        assert report is not None, "Performance report generation failed"

        # Validate improvement metrics if available
        if "overall_improvement" in results:
            assert isinstance(
                results["overall_improvement"], (int, float)
            ), "Invalid improvement metric type"

    except ImportError as e:
        pytest.skip(f"Performance optimization test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Performance optimization test failed: {e}")

def test_security_auditing(environment):
    """Test security auditing system"""
    try:

        from plugins.security_auditor import SecurityAuditor

        # Initialize security auditor
        auditor = SecurityAuditor()

        # Test security audit
        results = auditor.run_full_audit()
        assert results is not None, "Security audit returned no results"
        assert hasattr(
            results, "overall_score"
        ), "Security audit results missing overall score"

        # Test score is within valid range
        assert (
            0 <= results.overall_score <= 100
        ), f"Invalid security score: {results.overall_score}"

    except ImportError as e:
        pytest.skip(f"Security auditing test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Security auditing test failed: {e}")

def test_monitoring_dashboard(environment):
    """Test monitoring dashboard functionality"""
    try:

        from plugins.monitoring_dashboard import MonitoringDashboard

        # Initialize dashboard
        dashboard = MonitoringDashboard()

        # Test dashboard data collection
        data = dashboard.get_dashboard_data()
        assert data is not None, "Dashboard returned no data"
        assert isinstance(data, dict), "Dashboard data not in expected format"

        # Test required metrics are present
        assert "metrics" in data, "Dashboard data missing metrics"
        assert data["metrics"], "Dashboard has no metrics"

    except ImportError as e:
        pytest.skip(f"Monitoring dashboard test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Monitoring dashboard test failed: {e}")

def test_code_generation(environment):
    """Test code generation functionality"""
    try:

        from agents.code_generator import CodeGeneratorAgent

        # Initialize code generator
        code_gen = CodeGeneratorAgent()

        # Test code generation capabilities
        assert hasattr(
            code_gen, "generate_codebase"
        ), "Code generator missing generate_codebase method"

        # If we can generate code, test basic generation
        if hasattr(code_gen, "generate_codebase"):
            result = code_gen.generate_codebase(
                app_plan={
                    "name": "Simple task manager",
                    "description": "Basic task management application",
                    "type": "web",
                    "framework": "fastapi",
                    "complexity": "simple",
                },
                app_dir=environment["test_app_dir"],
            )
            assert result is not None, "Code generation returned no result"

    except ImportError as e:
        pytest.skip(f"Code generation test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Code generation test failed: {e}")

def test_security_generation(environment):
    """Test security feature generation"""
    try:

        from agents.security_generator import SecurityGeneratorAgent

        # Initialize security generator
        security_gen = SecurityGeneratorAgent()

        # Test security generation capabilities
        assert hasattr(
            security_gen, "generate_security_features"
        ), "Security generator missing generate_security_features method"

        # If we can generate security features, test basic generation
        if hasattr(security_gen, "generate_security_features"):
            result = security_gen.generate_security_features(
                app_plan={"name": "test_app", "type": "web", "security_level": "high"}
            )
            assert result is not None, "Security feature generation returned no result"

    except ImportError as e:
        pytest.skip(f"Security generation test skipped: {e}")
    except Exception as e:
        pytest.fail(f"Security generation test failed: {e}")

def test_system_health():
    """Test system health functionality"""
    try:

        import psutil

        # Check system memory
        memory = psutil.virtual_memory()
        assert memory.percent < 95, f"High memory usage: {memory.percent}%"

        # Check CPU usage
        cpu = psutil.cpu_percent(interval=1)
        assert cpu < 95, f"High CPU usage: {cpu}%"

        # Check SQLite (always available)
        import sqlite3

        conn = sqlite3.connect(":memory:")
        conn.close()

        # Check Redis if available
        try:

            import redis

            r = redis.Redis(host="localhost", port=6379, db=0)
            r.ping()
        except (ImportError, redis.ConnectionError):
            pytest.skip("Redis not available")

    except Exception as e:
        pytest.fail(f"System health check failed: {e}")

def test_documentation():
    """Test documentation files"""
    required_docs = [
        "docs/USER_GUIDE.md",
        "docs/API_REFERENCE.md",
        "HACKATHON_SUBMISSION_FINAL.md",
        "README.md",
        "CHANGELOG.md",
        "requirements.txt",
    ]

    missing_docs = [doc for doc in required_docs if not os.path.exists(doc)]

    if missing_docs:
        pytest.fail(f"Missing documentation files: {missing_docs}")

@pytest.mark.integration
def test_configuration():
    """Test configuration and environment setup"""
    # Check Python version
    python_version = sys.version_info
    assert (
        python_version.major >= 3 and python_version.minor >= 11
    ), f"Python version {python_version.major}.{python_version.minor} < 3.11"

    # Check required directories
    required_dirs = [
        "plugins",
        "agents",
        "integrations",
        "tests",
        "docs",
        "output",
    ]

    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    assert not missing_dirs, f"Missing directories: {missing_dirs}"

    # Check environment files
    assert os.path.exists(".env") or os.path.exists(
        ".env.example"
    ), "Missing environment configuration (.env or .env.example)"

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
