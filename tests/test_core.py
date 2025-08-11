"""
Core unit tests for AutoDevCore.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from integrations.gpt_oss import GPTOSSClient

# Import the modules to test
from modes.base import BaseMode
from modes.compose import ComposeMode
from modes.score import ScoreMode
from utils.performance import PerformanceMonitor, PerformanceOptimizer


class TestBaseMode:
    """Test the base mode functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

        # Create a concrete test class since BaseMode is abstract
        class TestMode(BaseMode):
            def execute(self):
                pass

        self.base_mode = TestMode(self.temp_dir, verbose=True)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_log_thought(self):
        """Test thought logging functionality."""
        self.base_mode.log_thought("TestAgent", "Test thought")

        assert len(self.base_mode.thought_trail) == 1
        thought = self.base_mode.thought_trail[0]
        assert thought["agent"] == "TestAgent"
        assert thought["thought"] == "Test thought"
        assert "timestamp" in thought

    def test_log_thought_with_data(self):
        """Test thought logging with data."""
        test_data = {"key": "value", "number": 42}
        self.base_mode.log_thought("TestAgent", "Test thought", test_data)

        thought = self.base_mode.thought_trail[0]
        assert thought["data"] == test_data

    def test_save_thought_trail(self):
        """Test saving thought trail to file."""
        self.base_mode.log_thought("TestAgent", "Test thought")
        self.base_mode.save_thought_trail()

        trail_file = Path(self.temp_dir) / "thought_trail.json"
        assert trail_file.exists()

    def test_generate_mermaid_diagram(self):
        """Test Mermaid diagram generation."""
        self.base_mode.log_thought("Agent1", "First thought")
        self.base_mode.log_thought("Agent2", "Second thought")
        self.base_mode.generate_mermaid_diagram()

        mermaid_file = Path(self.temp_dir) / "thought_trail.md"
        assert mermaid_file.exists()

        content = mermaid_file.read_text()
        assert "graph TD" in content
        assert "Agent1" in content
        assert "Agent2" in content


class TestComposeMode:
    """Test the compose mode functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.compose_mode = ComposeMode("test app idea", self.temp_dir, verbose=True)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("modes.compose.ComposerAgent")
    @patch("modes.compose.PRDWriterAgent")
    @patch("modes.compose.CodeGeneratorAgent")
    @patch("modes.compose.READMEWriterAgent")
    def test_execute_success(self, mock_readme, mock_code, mock_prd, mock_composer):
        """Test successful compose execution."""
        # Mock the agents
        mock_composer.return_value.create_app_plan.return_value = {
            "app_name": "TestApp",
            "features": ["feature1", "feature2"],
            "tech_stack": {"backend": "Python/FastAPI"},
        }

        mock_prd.return_value.generate_prd.return_value = "Test PRD content"
        mock_code.return_value.generate_codebase.return_value = {
            "main.py": "print('hello')"
        }
        mock_readme.return_value.generate_readme.return_value = "Test README content"

        # Mock the compose mode to use our mocked agents
        with patch.object(
            self.compose_mode, "composer", mock_composer.return_value
        ), patch.object(
            self.compose_mode, "prd_writer", mock_prd.return_value
        ), patch.object(
            self.compose_mode, "code_generator", mock_code.return_value
        ), patch.object(
            self.compose_mode, "readme_writer", mock_readme.return_value
        ):

            # Execute the mode
            self.compose_mode.execute()

            # Verify agents were called
            mock_composer.return_value.create_app_plan.assert_called_once()
            mock_prd.return_value.generate_prd.assert_called_once()
            mock_code.return_value.generate_codebase.assert_called_once()
            mock_readme.return_value.generate_readme.assert_called_once()


class TestScoreMode:
    """Test the score mode functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.app_dir = tempfile.mkdtemp()

        # Create a test app structure
        (Path(self.app_dir) / "main.py").write_text("print('hello')")
        (Path(self.app_dir) / "requirements.txt").write_text("fastapi==0.104.1")

        self.score_mode = ScoreMode(
            self.app_dir, "profiles/fintech.yaml", self.temp_dir, verbose=True
        )

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        shutil.rmtree(self.app_dir, ignore_errors=True)

    def test_load_template(self):
        """Test template loading."""
        # Create a test template
        template_content = """
        categories:
          Security:
            - name: "Authentication"
              type: "boolean"
              max_score: 10
        """
        template_file = Path(self.temp_dir) / "test_template.yaml"
        template_file.write_text(template_content)

        # Mock the template path
        with patch.object(self.score_mode, "template", str(template_file)):
            template = self.score_mode._load_template()
            assert "Security" in template["categories"]

    def test_evaluate_app(self):
        """Test app evaluation."""
        template = {
            "categories": {
                "Security": [
                    {"name": "Authentication", "type": "boolean", "max_score": 10}
                ]
            }
        }

        result = self.score_mode._evaluate_app_intelligent(template, {})
        assert "overall_score" in result
        assert "categories" in result


class TestGPTOSSClient:
    """Test the GPT-OSS client functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.client = GPTOSSClient()

    def test_cache_key_generation(self):
        """Test cache key generation."""
        prompt = "test prompt"
        cache_key1 = self.client._get_cache_key(prompt)
        cache_key2 = self.client._get_cache_key(prompt)

        assert cache_key1 == cache_key2
        assert len(cache_key1) == 32  # MD5 hash length

    def test_cache_key_uniqueness(self):
        """Test cache key uniqueness for different prompts."""
        prompt1 = "test prompt 1"
        prompt2 = "test prompt 2"

        cache_key1 = self.client._get_cache_key(prompt1)
        cache_key2 = self.client._get_cache_key(prompt2)

        assert cache_key1 != cache_key2

    @patch("requests.Session.post")
    def test_make_request_success(self, mock_post):
        """Test successful request."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": "test response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.client._make_request("test prompt")

        assert result["response"] == "test response"
        mock_post.assert_called_once()

    @patch("requests.Session.post")
    def test_make_request_timeout(self, mock_post):
        """Test request timeout handling."""
        # Clear cache first to ensure we don't get cached response
        self.client.clear_cache()

        mock_post.side_effect = requests.exceptions.Timeout()

        result = self.client._make_request("test prompt")

        assert "timeout" in result["response"].lower()
        assert result["done"] is True

    def test_generate_with_error(self):
        """Test generate method with error handling."""
        with patch.object(
            self.client, "_make_request", side_effect=Exception("test error")
        ):
            result = self.client.generate("test prompt")

            assert "Error" in result["response"]
            assert result["done"] is True


class TestPerformanceMonitor:
    """Test the performance monitor functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.monitor = PerformanceMonitor()
        self.monitor.metrics_file = Path(self.temp_dir) / "test_metrics.json"

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_start_monitoring(self):
        """Test starting performance monitoring."""
        self.monitor.start_monitoring()

        assert self.monitor.monitoring is True
        assert "start_time" in self.monitor.metrics
        assert "operations" in self.monitor.metrics

    def test_operation_timing(self):
        """Test operation timing functionality."""
        self.monitor.start_monitoring()
        self.monitor.start_operation("test_op")

        # Simulate some work
        import time

        time.sleep(0.1)

        self.monitor.end_operation("test_op")

        assert "test_op" in self.monitor.metrics["operations"]
        op_metrics = self.monitor.metrics["operations"]["test_op"]
        assert op_metrics["count"] == 1
        assert op_metrics["total_time"] > 0

    def test_system_stats_recording(self):
        """Test system statistics recording."""
        self.monitor.start_monitoring()
        self.monitor.record_system_stats()

        assert len(self.monitor.metrics["cpu_usage"]) == 1
        assert len(self.monitor.metrics["memory_usage"]) == 1
        assert len(self.monitor.metrics["system_stats"]) == 1

    def test_get_summary(self):
        """Test performance summary generation."""
        self.monitor.start_monitoring()
        self.monitor.start_operation("test_op")
        self.monitor.end_operation("test_op")
        self.monitor.stop_monitoring()

        summary = self.monitor.get_summary()

        assert summary["total_operations"] == 1
        assert summary["slowest_operation"] == "test_op"
        assert summary["fastest_operation"] == "test_op"


class TestPerformanceOptimizer:
    """Test the performance optimizer functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.optimizer = PerformanceOptimizer()

    def test_get_optimization_recommendations(self):
        """Test optimization recommendations."""
        recommendations = self.optimizer.get_optimization_recommendations()

        assert "immediate" in recommendations
        assert "short_term" in recommendations
        assert "long_term" in recommendations

        assert len(recommendations["immediate"]) > 0
        assert len(recommendations["short_term"]) > 0
        assert len(recommendations["long_term"]) > 0

    def test_analyze_performance_no_file(self):
        """Test performance analysis with no metrics file."""
        suggestions = self.optimizer.analyze_performance(Path("nonexistent.json"))

        assert len(suggestions) == 1
        assert "Error" in suggestions[0]


# Integration tests
class TestIntegration:
    """Integration tests for AutoDevCore."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_compose_workflow(self):
        """Test the complete compose workflow."""
        # This would test the full integration of all components
        # For now, we'll just verify the basic structure
        compose_mode = ComposeMode("test app", self.temp_dir, verbose=True)

        assert compose_mode.idea == "test app"
        assert compose_mode.output_dir == Path(self.temp_dir)
        assert compose_mode.verbose is True

    def test_full_score_workflow(self):
        """Test the complete score workflow."""
        app_dir = tempfile.mkdtemp()
        (Path(app_dir) / "main.py").write_text("print('hello')")

        score_mode = ScoreMode(
            app_dir, "profiles/fintech.yaml", self.temp_dir, verbose=True
        )

        assert score_mode.app_dir == Path(app_dir)
        assert score_mode.template == "profiles/fintech.yaml"

        shutil.rmtree(app_dir, ignore_errors=True)


# Performance tests
class TestPerformance:
    """Performance tests for AutoDevCore."""

    def test_cache_performance(self):
        """Test cache performance."""
        client = GPTOSSClient()

        # Test cache key generation performance
        import time

        start_time = time.time()

        for i in range(1000):
            client._get_cache_key(f"prompt {i}")

        end_time = time.time()
        duration = end_time - start_time

        # Should be very fast (less than 1 second for 1000 operations)
        assert duration < 1.0

    def test_thought_logging_performance(self):
        """Test thought logging performance."""
        temp_dir = tempfile.mkdtemp()

        # Create a concrete test class since BaseMode is abstract
        class TestMode(BaseMode):
            def execute(self):
                pass

        base_mode = TestMode(temp_dir, verbose=False)

        import time

        start_time = time.time()

        for i in range(1000):
            base_mode.log_thought("TestAgent", f"Thought {i}")

        end_time = time.time()
        duration = end_time - start_time

        # Should be very fast (less than 1 second for 1000 operations)
        assert duration < 1.0

        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
