#!/usr/bin/env python3
"""
Metrics Configuration - Monitoring settings and alert thresholds
"""

from typing import Dict, Any

# Default monitoring configuration
DEFAULT_METRICS_CONFIG = {
    "retention_days": 30,
    "collection_interval": 60,  # seconds
    "max_metrics_per_type": 10000,
    "database_path": "logs/metrics.db",
    "log_level": "INFO",
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "cpu_usage": {"warning": 70.0, "critical": 90.0},
    "memory_usage": {"warning": 80.0, "critical": 95.0},
    "disk_usage": {"warning": 85.0, "critical": 95.0},
    "response_time": {"warning": 2.0, "critical": 5.0},  # seconds
    "error_rate": {"warning": 5.0, "critical": 10.0},  # percentage
}

# Alert configurations
DEFAULT_ALERTS = [
    {
        "name": "High CPU Usage",
        "condition": "cpu_usage > 90",
        "threshold": 90.0,
        "severity": "critical",
        "message": "CPU usage is critically high",
    },
    {
        "name": "High Memory Usage",
        "condition": "memory_usage > 95",
        "threshold": 95.0,
        "severity": "critical",
        "message": "Memory usage is critically high",
    },
    {
        "name": "Slow Response Time",
        "condition": "response_time > 5",
        "threshold": 5.0,
        "severity": "warning",
        "message": "Response time is slow",
    },
    {
        "name": "High Error Rate",
        "condition": "error_rate > 10",
        "threshold": 10.0,
        "severity": "critical",
        "message": "Error rate is critically high",
    },
]

# Health check configurations
HEALTH_CHECKS = {
    "database": {"interval": 300, "timeout": 30, "enabled": True},  # 5 minutes
    "api_endpoints": {"interval": 60, "timeout": 10, "enabled": True},  # 1 minute
    "file_system": {"interval": 600, "timeout": 30, "enabled": True},  # 10 minutes
}

# Metrics collection settings
METRICS_COLLECTION = {
    "system_metrics": {"enabled": True, "interval": 60, "retention": 30},
    "application_metrics": {"enabled": True, "interval": 30, "retention": 30},
    "business_metrics": {"enabled": True, "interval": 300, "retention": 90},
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    "refresh_interval": 30,  # seconds
    "max_data_points": 1000,
    "theme": "dark",
    "auto_refresh": True,
    "export_formats": ["json", "csv", "pdf"],
}

def get_config() -> Dict[str, Any]:
    """Get the complete metrics configuration."""
    return {
        "default": DEFAULT_METRICS_CONFIG,
        "thresholds": PERFORMANCE_THRESHOLDS,
        "alerts": DEFAULT_ALERTS,
        "health_checks": HEALTH_CHECKS,
        "collection": METRICS_COLLECTION,
        "dashboard": DASHBOARD_CONFIG,
    }

def get_thresholds() -> Dict[str, Any]:
    """Get performance thresholds."""
    return PERFORMANCE_THRESHOLDS

def get_alerts() -> list:
    """Get default alert configurations."""
    return DEFAULT_ALERTS

def get_health_checks() -> Dict[str, Any]:
    """Get health check configurations."""
    return HEALTH_CHECKS
