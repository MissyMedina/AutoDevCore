#!/usr/bin/env python3
"""
Test Complexity Improvements - Verify that complexity optimizations work correctly
"""

import unittest
from datetime import datetime
from typing import Any, Dict, List

from utils.complexity_optimizer import (
    ComplexityOptimizer,
    ErrorHandler,
    ModelConfig,
    ModelSelector,
    Priority,
    TaskType,
)

from utils.interface_abstraction import (
    ComponentBase,
    DependencyInjector,
    EventManager,
    MessageQueue,
    ServiceLocator,
)

from utils.type_enhancer import (
    LogLevel,
    Result,
    Status,
    TypeSafeCache,
    TypeSafeLogger,
    TypeSafeValidator,
    ValidationResult,
)

class TestComplexityOptimizer(unittest.TestCase):
    """Test complexity optimization utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = ComplexityOptimizer()
        self.model_selector = ModelSelector()
        self.error_handler = ErrorHandler()

    def test_extract_conditional_logic(self):
        """Test conditional logic extraction."""

        def true_action():
            return "success"

        def false_action():
            return "failure"

        # Test with condition True
        result = self.optimizer.extract_conditional_logic(
            condition=True, true_action=true_action, false_action=false_action
        )
        self.assertEqual(result, "success")

        # Test with condition False
        result = self.optimizer.extract_conditional_logic(
            condition=False, true_action=true_action, false_action=false_action
        )
        self.assertEqual(result, "failure")

    def test_strategy_pattern(self):
        """Test strategy pattern creation."""
        conditions = [
            {
                "predicate": lambda x: x < 10,
                "action": lambda x: f"small_{x}",
                "default_action": lambda x: "unknown",
            },
            {
                "predicate": lambda x: x >= 10 and x < 100,
                "action": lambda x: f"medium_{x}",
                "default_action": lambda x: "unknown",
            },
            {
                "predicate": lambda x: x >= 100,
                "action": lambda x: f"large_{x}",
                "default_action": lambda x: "unknown",
            },
        ]

        strategy = self.optimizer.create_strategy_pattern(conditions)

        self.assertEqual(strategy(5), "small_5")
        self.assertEqual(strategy(50), "medium_50")
        self.assertEqual(strategy(500), "large_500")

    def test_model_selector(self):
        """Test model selection logic."""
        # Test normal priority
        config = self.model_selector.select_model(
            TaskType.CODE_GENERATION, Priority.NORMAL
        )
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.model, "claude-3")

        # Test high priority
        config = self.model_selector.select_model(TaskType.APP_PLANNING, Priority.HIGH)
        self.assertEqual(config.provider, "openai")
        self.assertEqual(config.max_tokens, 4000)  # Doubled for high priority

        # Test low priority
        config = self.model_selector.select_model(TaskType.CODE_ANALYSIS, Priority.LOW)
        self.assertEqual(config.provider, "gpt-oss")
        self.assertEqual(config.max_tokens, 500)  # Halved for low priority

    def test_error_handler(self):
        """Test error handling."""
        # Test AI error handling
        error = Exception("timeout error")
        result = self.error_handler.handle_ai_error(error, "gpt-oss")

        self.assertFalse(result["success"])
        self.assertEqual(result["type"], "exception")
        self.assertEqual(result["fallback_provider"], "gpt-oss")

        # Test validation error handling
        result = self.error_handler.handle_validation_error("username", 123, "string")
        self.assertFalse(result["success"])
        self.assertEqual(result["field"], "username")
        self.assertEqual(result["expected_type"], "string")

class TestInterfaceAbstraction(unittest.TestCase):
    """Test interface abstraction utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.service_locator = ServiceLocator()
        self.event_manager = EventManager()
        self.dependency_injector = DependencyInjector()
        self.message_queue = MessageQueue()

    def test_service_locator(self):
        """Test service locator pattern."""
        test_service = {"name": "test", "data": "value"}
        self.service_locator.register("test_service", test_service)

        self.assertTrue(self.service_locator.has("test_service"))
        retrieved_service = self.service_locator.get("test_service")
        self.assertEqual(retrieved_service, test_service)

        with self.assertRaises(KeyError):
            self.service_locator.get("nonexistent_service")

    def test_event_manager(self):
        """Test event manager."""
        events_received = []

        def event_handler(data):
            events_received.append(data)

        self.event_manager.subscribe("test_event", event_handler)
        self.event_manager.publish("test_event", "test_data")

        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0], "test_data")

    def test_dependency_injector(self):
        """Test dependency injector."""
        test_dependency = {"key": "value"}
        self.dependency_injector.register("test_dep", test_dependency)

        class TestClass:
            def __init__(self):
                self.test_dep = None

        test_obj = TestClass()
        self.dependency_injector.inject(test_obj, test_dep=test_dependency)

        self.assertEqual(test_obj.test_dep, test_dependency)

    def test_message_queue(self):
        """Test message queue."""
        messages_received = []

        def message_handler(message):
            messages_received.append(message)

        self.message_queue.subscribe("test_queue", message_handler)
        self.message_queue.publish("test_queue", "test_message")

        self.assertEqual(len(messages_received), 1)
        self.assertEqual(messages_received[0], "test_message")

        messages = self.message_queue.get_messages("test_queue")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], "test_message")

class TestTypeEnhancer(unittest.TestCase):
    """Test type enhancement utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = TypeSafeCache()
        self.logger = TypeSafeLogger("TestLogger")
        self.validator = TypeSafeValidator()

    def test_type_safe_cache(self):
        """Test type-safe cache."""
        # Test basic operations
        self.cache.set("test_key", "test_value", 3600)
        value = self.cache.get("test_key")
        self.assertEqual(value, "test_value")

        # Test TTL
        self.cache.set("expire_key", "expire_value", 1)

        import time

        time.sleep(1.1)  # Wait for expiration
        expired_value = self.cache.get("expire_key")
        self.assertIsNone(expired_value)

        # Test deletion
        self.assertTrue(self.cache.delete("test_key"))
        self.assertFalse(self.cache.delete("nonexistent_key"))

        # Test stats
        stats = self.cache.get_stats()
        self.assertIn("total_entries", stats)
        self.assertIn("active_entries", stats)

    def test_type_safe_logger(self):
        """Test type-safe logger."""
        self.logger.info("Test message", {"key": "value"})
        self.logger.error("Error message")

        logs = self.logger.get_logs()
        self.assertEqual(len(logs), 2)

        info_logs = self.logger.get_logs(LogLevel.INFO)
        self.assertEqual(len(info_logs), 1)
        self.assertEqual(info_logs[0]["message"], "Test message")

        error_logs = self.logger.get_logs(LogLevel.ERROR)
        self.assertEqual(len(error_logs), 1)
        self.assertEqual(error_logs[0]["message"], "Error message")

    def test_type_safe_validator(self):
        """Test type-safe validator."""
        # Test string validation
        result = self.validator.validate_string("test", min_length=3, max_length=10)
        self.assertTrue(result.is_valid)

        result = self.validator.validate_string("ab", min_length=3)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)

        # Test integer validation
        result = self.validator.validate_integer(5, min_value=0, max_value=10)
        self.assertTrue(result.is_valid)

        result = self.validator.validate_integer(15, max_value=10)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)

        # Test list validation
        result = self.validator.validate_list([1, 2, 3], min_length=2, max_length=5)
        self.assertTrue(result.is_valid)

        result = self.validator.validate_list([1], min_length=2)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)

class TestComponentBase(unittest.TestCase):
    """Test component base class."""

    def setUp(self):
        """Set up test fixtures."""
        self.component = ComponentBase()

    def test_event_publishing(self):
        """Test event publishing."""
        events_received = []

        def event_handler(data):
            events_received.append(data)

        self.component.subscribe_event("test_event", event_handler)
        self.component.publish_event("test_event", "test_data")

        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0], "test_data")

    def test_message_sending(self):
        """Test message sending."""
        messages_received = []

        def message_handler(message):
            messages_received.append(message)

        self.component.subscribe_queue("test_queue", message_handler)
        self.component.send_message("test_queue", "test_message")

        self.assertEqual(len(messages_received), 1)
        self.assertEqual(messages_received[0], "test_message")

if __name__ == "__main__":
    unittest.main()
