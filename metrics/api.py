#!/usr/bin/env python3
"""
Metrics API - Easy access to monitoring and performance functionality
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .performance import PerformanceMonitor
from .monitoring_dashboard import MonitoringDashboard, MetricsCollector
from .config import get_config, get_thresholds
from .storage import get_storage


class MetricsAPI:
    """High-level API for metrics and monitoring functionality."""

    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.dashboard = MonitoringDashboard()
        self.collector = MetricsCollector()
        self.config = get_config()
        self.is_monitoring = False

    def start_monitoring(self) -> Dict[str, Any]:
        """Start comprehensive monitoring."""
        try:
            self.monitor.start_monitoring()
            self.dashboard.start()
            self.is_monitoring = True

            return {
                "success": True,
                "message": "Monitoring started successfully",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and save metrics."""
        try:
            self.monitor.stop_monitoring()
            self.dashboard.stop()
            self.is_monitoring = False

            return {
                "success": True,
                "message": "Monitoring stopped successfully",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory.percent,
                    "memory_available": memory.available,
                    "memory_total": memory.total,
                    "disk_usage": disk.percent,
                    "disk_free": disk.free,
                    "disk_total": disk.total,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance monitoring summary."""
        try:
            if not self.is_monitoring:
                return {
                    "success": False,
                    "error": "Monitoring not started",
                    "timestamp": datetime.now().isoformat(),
                }

            summary = self.monitor.get_summary()
            return {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "summary": summary,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def record_metric(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Record a custom metric."""
        try:
            storage = get_storage()
            success = storage.store_metric(name, value, labels)
            return {
                "success": success,
                "message": (
                    f"Metric '{name}' recorded successfully"
                    if success
                    else "Failed to record metric"
                ),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_metrics_history(self, metric_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get historical metrics data."""
        try:
            storage = get_storage()
            history = storage.get_metrics(metric_name, hours)
            return {
                "success": True,
                "metric_name": metric_name,
                "hours": hours,
                "data_points": len(history),
                "history": history,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def check_alerts(self) -> Dict[str, Any]:
        """Check for triggered alerts."""
        try:
            storage = get_storage()
            alerts = storage.get_alerts(hours=24)
            return {
                "success": True,
                "alerts_count": len(alerts),
                "alerts": alerts,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            storage = get_storage()
            health_status = storage.get_health_status(hours=24)
            return {
                "success": True,
                "health_status": health_status,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def export_metrics(self, format: str = "json", hours: int = 24) -> Dict[str, Any]:
        """Export metrics data."""
        try:
            storage = get_storage()
            data = storage.export_data(format, hours)
            return {
                "success": "error" not in data,
                "format": format,
                "hours": hours,
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }


# Global metrics API instance
metrics_api = MetricsAPI()


def get_metrics_api() -> MetricsAPI:
    """Get the global metrics API instance."""
    return metrics_api


def start_monitoring() -> Dict[str, Any]:
    """Start monitoring using the global API."""
    return metrics_api.start_monitoring()


def get_system_metrics() -> Dict[str, Any]:
    """Get system metrics using the global API."""
    return metrics_api.get_system_metrics()


def record_metric(
    name: str, value: float, labels: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Record a metric using the global API."""
    return metrics_api.record_metric(name, value, labels)
