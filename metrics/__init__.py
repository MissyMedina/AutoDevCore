#!/usr/bin/env python3
"""
Metrics Package - Comprehensive monitoring, performance tracking, and analytics
"""

from .performance import PerformanceMonitor, PerformanceOptimizer
from .performance_monitor import PerformanceMonitor as LegacyPerformanceMonitor
from .monitoring_dashboard import (
    MetricsCollector,
    MonitoringDashboard,
    Alert,
    HealthCheck,
    MetricPoint,
)

from .performance_optimizer import PerformanceOptimizer as PluginPerformanceOptimizer
from .api import (
    MetricsAPI,
    get_metrics_api,
    start_monitoring,
    get_system_metrics,
    record_metric,
)

from .storage import MetricsStorage, get_storage

# from .performance_integration import PerformanceIntegration  # Temporarily disabled due to import issues

__all__ = [
    # Core performance monitoring
    "PerformanceMonitor",
    "PerformanceOptimizer",
    "LegacyPerformanceMonitor",
    # Monitoring dashboard
    "MetricsCollector",
    "MonitoringDashboard",
    "Alert",
    "HealthCheck",
    "MetricPoint",
    # Performance optimization
    "PluginPerformanceOptimizer",
    # 'PerformanceIntegration',  # Temporarily disabled
    # API
    "MetricsAPI",
    "get_metrics_api",
    "start_monitoring",
    "get_system_metrics",
    "record_metric",
    # Storage
    "MetricsStorage",
    "get_storage",
]

# Version info
__version__ = "1.0.0"
__author__ = "AutoDevCore Team"
__description__ = (
    "Enterprise-grade monitoring and performance analytics for AutoDevCore"
)


# Legacy functions (kept for backward compatibility)
def get_default_dashboard():
    """Get the default monitoring dashboard instance."""

    from .monitoring_dashboard import MonitoringDashboard

    return MonitoringDashboard()


def get_performance_monitor():
    """Get the default performance monitor instance."""

    from .performance import PerformanceMonitor

    return PerformanceMonitor()


def start_monitoring_legacy():
    """Start comprehensive monitoring across all systems (legacy)."""
    dashboard = get_default_dashboard()
    monitor = get_performance_monitor()

    # Start monitoring
    monitor.start_monitoring()
    dashboard.start()

    return dashboard, monitor
