#!/usr/bin/env python3
"""
Interface Abstraction - Reduce module coupling and improve interconnectedness
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class AIProvider(Protocol):
    """Protocol for AI providers to reduce coupling."""

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from AI provider."""
        ...

    def get_status(self) -> Dict[str, Any]:
        """Get provider status."""
        ...


class CacheProvider(Protocol):
    """Protocol for cache providers."""

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        ...

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache."""
        ...


class DatabaseProvider(Protocol):
    """Protocol for database providers."""

    def connect(self) -> bool:
        """Connect to database."""
        ...

    def query(self, sql: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute database query."""
        ...


class EventBus(Protocol):
    """Protocol for event bus to decouple components."""

    def publish(self, event: str, data: Any) -> None:
        """Publish event."""
        ...

    def subscribe(self, event: str, handler: callable) -> None:
        """Subscribe to event."""
        ...


class ConfigProvider(Protocol):
    """Protocol for configuration providers."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        ...


@dataclass
class ServiceConfig:
    """Configuration for service dependencies."""

    ai_provider: AIProvider
    cache_provider: CacheProvider
    database_provider: DatabaseProvider
    event_bus: EventBus
    config_provider: ConfigProvider


class ServiceLocator:
    """Service locator pattern to reduce direct dependencies."""

    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Register a service."""
        self._services[name] = service

    def get(self, name: str) -> Any:
        """Get a service by name."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' not found")
        return self._services[name]

    def has(self, name: str) -> bool:
        """Check if service exists."""
        return name in self._services


class EventManager:
    """Event manager to decouple components."""

    def __init__(self):
        self._handlers: Dict[str, List[callable]] = {}

    def publish(self, event: str, data: Any = None) -> None:
        """Publish an event."""
        if event in self._handlers:
            for handler in self._handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error in event handler for {event}: {e}")

    def subscribe(self, event: str, handler: callable) -> None:
        """Subscribe to an event."""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def unsubscribe(self, event: str, handler: callable) -> None:
        """Unsubscribe from an event."""
        if event in self._handlers and handler in self._handlers[event]:
            self._handlers[event].remove(handler)


class DependencyInjector:
    """Dependency injector to manage component dependencies."""

    def __init__(self):
        self._dependencies: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}

    def register(self, name: str, dependency: Any) -> None:
        """Register a dependency."""
        self._dependencies[name] = dependency

    def register_factory(self, name: str, factory: callable) -> None:
        """Register a dependency factory."""
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        """Get a dependency by name."""
        if name in self._dependencies:
            return self._dependencies[name]
        elif name in self._factories:
            return self._factories[name]()
        else:
            raise KeyError(f"Dependency '{name}' not found")

    def inject(self, target: Any, **kwargs) -> None:
        """Inject dependencies into target object."""
        for name, value in kwargs.items():
            if hasattr(target, name):
                setattr(target, name, value)


class MessageQueue:
    """Simple message queue to decouple components."""

    def __init__(self):
        self._queues: Dict[str, List[Any]] = {}
        self._subscribers: Dict[str, List[callable]] = {}

    def publish(self, queue: str, message: Any) -> None:
        """Publish message to queue."""
        if queue not in self._queues:
            self._queues[queue] = []
        self._queues[queue].append(message)

        # Notify subscribers
        if queue in self._subscribers:
            for subscriber in self._subscribers[queue]:
                try:
                    subscriber(message)
                except Exception as e:
                    print(f"Error in queue subscriber for {queue}: {e}")

    def subscribe(self, queue: str, handler: callable) -> None:
        """Subscribe to queue."""
        if queue not in self._subscribers:
            self._subscribers[queue] = []
        self._subscribers[queue].append(handler)

    def get_messages(self, queue: str) -> List[Any]:
        """Get all messages from queue."""
        return self._queues.get(queue, [])


class InterfaceRegistry:
    """Registry for interface implementations."""

    def __init__(self):
        self._interfaces: Dict[str, Any] = {}

    def register_interface(self, name: str, interface: Any) -> None:
        """Register an interface."""
        self._interfaces[name] = interface

    def get_interface(self, name: str) -> Any:
        """Get interface by name."""
        if name not in self._interfaces:
            raise KeyError(f"Interface '{name}' not found")
        return self._interfaces[name]

    def list_interfaces(self) -> List[str]:
        """List all registered interfaces."""
        return list(self._interfaces.keys())


# Global instances for dependency injection
service_locator = ServiceLocator()
event_manager = EventManager()
dependency_injector = DependencyInjector()
message_queue = MessageQueue()
interface_registry = InterfaceRegistry()


class ComponentBase:
    """Base class for components to use dependency injection."""

    def __init__(self):
        self.event_manager = event_manager
        self.message_queue = message_queue

    def publish_event(self, event: str, data: Any = None) -> None:
        """Publish an event."""
        self.event_manager.publish(event, data)

    def subscribe_event(self, event: str, handler: callable) -> None:
        """Subscribe to an event."""
        self.event_manager.subscribe(event, handler)

    def send_message(self, queue: str, message: Any) -> None:
        """Send message to queue."""
        self.message_queue.publish(queue, message)

    def subscribe_queue(self, queue: str, handler: callable) -> None:
        """Subscribe to queue."""
        self.message_queue.subscribe(queue, handler)
