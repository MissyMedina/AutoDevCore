#!/usr/bin/env python3
"""
Enterprise-Grade Monitoring Dashboard - Real-time metrics, alerting, and analytics
"""

import json
import time
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import psutil
import logging
from collections import defaultdict, deque
import sqlite3
import hashlib
import sys


@dataclass
class MetricPoint:
    """Individual metric data point."""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Alert configuration and state."""

    name: str
    condition: str
    threshold: float
    severity: str  # info, warning, error, critical
    message: str
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0


@dataclass
class HealthCheck:
    """Health check configuration."""

    name: str
    check_function: Callable
    interval: int  # seconds
    timeout: int = 30
    enabled: bool = True
    last_check: Optional[datetime] = None
    last_status: str = "unknown"
    last_error: Optional[str] = None


class MetricsCollector:
    """Collect and store system metrics."""

    def __init__(self, retention_days: int = 30):
        self.retention_days = retention_days
        self.metrics = defaultdict(
            lambda: deque(maxlen=10000)
        )  # Keep last 10k points per metric
        self.db_path = Path("logs/metrics.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for metrics storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                value REAL NOT NULL,
                labels TEXT,
                metadata TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_metrics_name_time 
            ON metrics(metric_name, timestamp)
        """
        )

        conn.commit()
        conn.close()

    def record_metric(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] = None,
        metadata: Dict[str, Any] = None,
    ):
        """Record a metric value."""
        timestamp = datetime.now()
        labels = labels or {}
        metadata = metadata or {}

        # Store in memory
        metric_point = MetricPoint(
            timestamp=timestamp, value=value, labels=labels, metadata=metadata
        )
        self.metrics[name].append(metric_point)

        # Store in database
        self._store_metric_db(name, timestamp, value, labels, metadata)

    def _store_metric_db(
        self,
        name: str,
        timestamp: datetime,
        value: float,
        labels: Dict[str, str],
        metadata: Dict[str, Any],
    ):
        """Store metric in SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO metrics (metric_name, timestamp, value, labels, metadata)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    name,
                    timestamp.isoformat(),
                    value,
                    json.dumps(labels),
                    json.dumps(metadata),
                ),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to store metric in database: {e}")

    def get_metric(self, name: str, duration: timedelta = None) -> List[MetricPoint]:
        """Get metric data for a specific time range."""
        if duration is None:
            duration = timedelta(hours=1)

        cutoff_time = datetime.now() - duration

        # Get from memory first
        memory_data = [
            point for point in self.metrics[name] if point.timestamp >= cutoff_time
        ]

        # Get from database for longer ranges
        if duration > timedelta(hours=1):
            db_data = self._get_metric_db(name, cutoff_time)
            memory_data.extend(db_data)

        return sorted(memory_data, key=lambda x: x.timestamp)

    def _get_metric_db(self, name: str, cutoff_time: datetime) -> List[MetricPoint]:
        """Get metric data from database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT timestamp, value, labels, metadata
                FROM metrics
                WHERE metric_name = ? AND timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 1000
            """,
                (name, cutoff_time.isoformat()),
            )

            results = cursor.fetchall()
            conn.close()

            return [
                MetricPoint(
                    timestamp=datetime.fromisoformat(row[0]),
                    value=row[1],
                    labels=json.loads(row[2]) if row[2] else {},
                    metadata=json.loads(row[3]) if row[3] else {},
                )
                for row in results
            ]
        except Exception as e:
            logging.error(f"Failed to retrieve metric from database: {e}")
            return []

    def cleanup_old_metrics(self):
        """Clean up metrics older than retention period."""
        cutoff_time = datetime.now() - timedelta(days=self.retention_days)

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM metrics
                WHERE timestamp < ?
            """,
                (cutoff_time.isoformat(),),
            )

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            logging.info(f"Cleaned up {deleted_count} old metric records")
        except Exception as e:
            logging.error(f"Failed to cleanup old metrics: {e}")


class AlertManager:
    """Manage alerts and notifications."""

    def __init__(self):
        self.alerts = {}
        self.alert_handlers = []
        self.triggered_alerts = {}

    def add_alert(self, alert: Alert):
        """Add a new alert."""
        self.alerts[alert.name] = alert

    def add_alert_handler(self, handler: Callable[[Alert, Dict[str, Any]], None]):
        """Add an alert handler function."""
        self.alert_handlers.append(handler)

    def check_alerts(self, metrics_collector: MetricsCollector):
        """Check all alerts against current metrics."""
        for alert_name, alert in self.alerts.items():
            if not alert.enabled:
                continue

            try:
                # Parse condition (simple format: metric_name > threshold)
                parts = alert.condition.split()
                if len(parts) != 3:
                    continue

                metric_name, operator, threshold_str = parts
                threshold = float(threshold_str)

                # Get latest metric value
                metric_data = metrics_collector.get_metric(
                    metric_name, timedelta(minutes=5)
                )
                if not metric_data:
                    continue

                latest_value = metric_data[-1].value

                # Check condition
                triggered = False
                if operator == ">":
                    triggered = latest_value > threshold
                elif operator == "<":
                    triggered = latest_value < threshold
                elif operator == ">=":
                    triggered = latest_value >= threshold
                elif operator == "<=":
                    triggered = latest_value <= threshold
                elif operator == "==":
                    triggered = latest_value == threshold

                if triggered:
                    self._trigger_alert(
                        alert,
                        {
                            "metric_name": metric_name,
                            "current_value": latest_value,
                            "threshold": threshold,
                            "operator": operator,
                        },
                    )
                else:
                    # Reset alert if condition is no longer met
                    if alert_name in self.triggered_alerts:
                        del self.triggered_alerts[alert_name]
                        alert.last_triggered = None
                        alert.trigger_count = 0

            except Exception as e:
                logging.error(f"Error checking alert {alert_name}: {e}")

    def _trigger_alert(self, alert: Alert, context: Dict[str, Any]):
        """Trigger an alert."""
        now = datetime.now()

        # Check if alert was recently triggered (avoid spam)
        if alert.last_triggered and now - alert.last_triggered < timedelta(minutes=5):
            return

        alert.last_triggered = now
        alert.trigger_count += 1
        self.triggered_alerts[alert.name] = {
            "alert": alert,
            "context": context,
            "triggered_at": now,
        }

        # Call alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert, context)
            except Exception as e:
                logging.error(f"Error in alert handler: {e}")

        logging.warning(f"Alert triggered: {alert.name} - {alert.message}")


class HealthChecker:
    """Perform health checks on system components."""

    def __init__(self):
        self.health_checks = {}
        self.check_thread = None
        self.running = False

    def add_health_check(self, health_check: HealthCheck):
        """Add a health check."""
        self.health_checks[health_check.name] = health_check

    def start_monitoring(self):
        """Start health check monitoring."""
        if self.running:
            return

        self.running = True
        self.check_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.check_thread.start()

    def stop_monitoring(self):
        """Stop health check monitoring."""
        self.running = False
        if self.check_thread:
            self.check_thread.join()

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            for health_check in self.health_checks.values():
                if not health_check.enabled:
                    continue

                # Check if it's time to run this health check
                if (
                    health_check.last_check is None
                    or datetime.now() - health_check.last_check
                    >= timedelta(seconds=health_check.interval)
                ):

                    self._run_health_check(health_check)

            time.sleep(1)  # Check every second

    def _run_health_check(self, health_check: HealthCheck):
        """Run a single health check."""
        try:
            # Run health check with timeout
            result = asyncio.run(
                asyncio.wait_for(
                    asyncio.create_task(health_check.check_function()),
                    timeout=health_check.timeout,
                )
            )

            health_check.last_status = "healthy"
            health_check.last_error = None

        except asyncio.TimeoutError:
            health_check.last_status = "timeout"
            health_check.last_error = "Health check timed out"
        except Exception as e:
            health_check.last_status = "error"
            health_check.last_error = str(e)

        health_check.last_check = datetime.now()


class MonitoringDashboard:
    """Main monitoring dashboard class."""

    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.health_checker = HealthChecker()
        self.collection_thread = None
        self.running = False

        # Initialize default metrics collection
        self._setup_default_metrics()
        self._setup_default_alerts()
        self._setup_default_health_checks()

    def _setup_default_metrics(self):
        """Setup default system metrics collection."""

        def collect_system_metrics():
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics_collector.record_metric(
                "system.cpu.usage", cpu_percent, labels={"type": "overall"}
            )

            # Memory usage
            memory = psutil.virtual_memory()
            self.metrics_collector.record_metric(
                "system.memory.usage", memory.percent, labels={"type": "overall"}
            )
            self.metrics_collector.record_metric(
                "system.memory.available",
                memory.available / (1024**3),  # GB
                labels={"type": "available"},
            )

            # Disk usage
            disk = psutil.disk_usage("/")
            self.metrics_collector.record_metric(
                "system.disk.usage",
                (disk.used / disk.total) * 100,
                labels={"type": "overall"},
            )

            # Network I/O
            net_io = psutil.net_io_counters()
            self.metrics_collector.record_metric(
                "system.network.bytes_sent", net_io.bytes_sent, labels={"type": "sent"}
            )
            self.metrics_collector.record_metric(
                "system.network.bytes_recv",
                net_io.bytes_recv,
                labels={"type": "received"},
            )

        self.default_metrics_collector = collect_system_metrics

    def _setup_default_alerts(self):
        """Setup default alerts."""
        default_alerts = [
            Alert(
                name="high_cpu_usage",
                condition="system.cpu.usage > 80",
                threshold=80.0,
                severity="warning",
                message="CPU usage is above 80%",
            ),
            Alert(
                name="high_memory_usage",
                condition="system.memory.usage > 85",
                threshold=85.0,
                severity="warning",
                message="Memory usage is above 85%",
            ),
            Alert(
                name="low_disk_space",
                condition="system.disk.usage > 90",
                threshold=90.0,
                severity="critical",
                message="Disk usage is above 90%",
            ),
            Alert(
                name="critical_cpu_usage",
                condition="system.cpu.usage > 95",
                threshold=95.0,
                severity="critical",
                message="CPU usage is critically high (>95%)",
            ),
        ]

        for alert in default_alerts:
            self.alert_manager.add_alert(alert)

    def _setup_default_health_checks(self):
        """Setup default health checks."""

        async def check_ai_models():
            # Check if AI models are available
            from plugins.multi_model_ai import multi_model_ai

            report = multi_model_ai.get_performance_report()
            available_models = report["available_models"]
            total_models = report["total_models"]

            if available_models == 0:
                raise Exception("No AI models available")
            elif available_models < total_models:
                raise Exception(
                    f"Only {available_models}/{total_models} models available"
                )

            return "healthy"

        async def check_plugin_system():
            # Check if plugin system is working
            from plugins.plugin_manager import PluginManager

            manager = PluginManager()
            plugins = manager.discover_plugins()

            if len(plugins) == 0:
                raise Exception("No plugins discovered")

            return "healthy"

        health_checks = [
            HealthCheck(
                name="ai_models",
                check_function=check_ai_models,
                interval=60,  # Check every minute
                timeout=30,
            ),
            HealthCheck(
                name="plugin_system",
                check_function=check_plugin_system,
                interval=300,  # Check every 5 minutes
                timeout=30,
            ),
        ]

        for health_check in health_checks:
            self.health_checker.add_health_check(health_check)

    def start(self):
        """Start the monitoring dashboard."""
        if self.running:
            return

        self.running = True

        # Start health checker
        self.health_checker.start_monitoring()

        # Start metrics collection thread
        self.collection_thread = threading.Thread(
            target=self._collection_loop, daemon=True
        )
        self.collection_thread.start()

        # Start alert checking thread
        alert_thread = threading.Thread(target=self._alert_loop, daemon=True)
        alert_thread.start()

        logging.info("Monitoring dashboard started")

    def stop(self):
        """Stop the monitoring dashboard."""
        self.running = False

        if self.collection_thread:
            self.collection_thread.join()

        self.health_checker.stop_monitoring()

        logging.info("Monitoring dashboard stopped")

    def _collection_loop(self):
        """Metrics collection loop."""
        while self.running:
            try:
                # Collect default system metrics
                self.default_metrics_collector()

                # Wait before next collection
                time.sleep(30)  # Collect every 30 seconds

            except Exception as e:
                logging.error(f"Error in metrics collection: {e}")
                time.sleep(60)  # Wait longer on error

    def _alert_loop(self):
        """Alert checking loop."""
        while self.running:
            try:
                self.alert_manager.check_alerts(self.metrics_collector)
                time.sleep(10)  # Check alerts every 10 seconds
            except Exception as e:
                logging.error(f"Error in alert checking: {e}")
                time.sleep(30)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        # Get current metrics
        current_metrics = {}
        for metric_name in [
            "system.cpu.usage",
            "system.memory.usage",
            "system.disk.usage",
        ]:
            data = self.metrics_collector.get_metric(metric_name, timedelta(minutes=5))
            if data:
                current_metrics[metric_name] = {
                    "current": data[-1].value,
                    "history": [
                        {"timestamp": point.timestamp.isoformat(), "value": point.value}
                        for point in data[-20:]  # Last 20 points
                    ],
                }

        # Get health check status
        health_status = {}
        for name, health_check in self.health_checker.health_checks.items():
            health_status[name] = {
                "status": health_check.last_status,
                "last_check": (
                    health_check.last_check.isoformat()
                    if health_check.last_check
                    else None
                ),
                "error": health_check.last_error,
            }

            # Get active alerts
        active_alerts = []
        try:
            for alert_name, alert_data in self.alert_manager.triggered_alerts.items():
                active_alerts.append(
                    {
                        "name": alert_name,
                        "severity": alert_data["alert"].severity,
                        "message": alert_data["alert"].message,
                        "triggered_at": alert_data["triggered_at"].isoformat(),
                        "context": alert_data["context"],
                    }
                )
        except (AttributeError, KeyError, TypeError) as e:
            # If alert_manager or triggered_alerts is not properly initialized
            active_alerts = []

        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": current_metrics,
            "health_status": health_status,
            "active_alerts": active_alerts,
            "system_info": {
                "uptime": time.time(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
            },
        }

    def generate_report(self) -> str:
        """Generate a comprehensive monitoring report."""
        dashboard_data = self.get_dashboard_data()

        report = f"""
# AutoDevCore Monitoring Report
Generated: {dashboard_data['timestamp']}

## System Health Overview

### Current Metrics
"""

        for metric_name, data in dashboard_data["metrics"].items():
            report += f"- **{metric_name}**: {data['current']:.2f}\n"

        report += "\n### Health Checks\n"
        for name, status in dashboard_data["health_status"].items():
            status_emoji = (
                "✅"
                if status["status"] == "healthy"
                else "⚠️" if status["status"] == "timeout" else "❌"
            )
            report += f"- {status_emoji} **{name}**: {status['status']}\n"

        if dashboard_data["active_alerts"]:
            report += "\n### Active Alerts\n"
            for alert in dashboard_data["active_alerts"]:
                severity_emoji = (
                    "🔴"
                    if alert["severity"] == "critical"
                    else "🟡" if alert["severity"] == "warning" else "🔵"
                )
                report += (
                    f"- {severity_emoji} **{alert['name']}**: {alert['message']}\n"
                )

        return report


# Global monitoring dashboard instance
monitoring_dashboard = MonitoringDashboard()


def run(context=None):
    """Plugin entry point for testing the monitoring dashboard."""
    # Start monitoring
    monitoring_dashboard.start()

    # Wait a bit for data collection
    time.sleep(5)

    # Get dashboard data
    dashboard_data = monitoring_dashboard.get_dashboard_data()

    # Generate report
    report = monitoring_dashboard.generate_report()

    # Stop monitoring
    monitoring_dashboard.stop()

    return {
        "status": "success",
        "message": "Monitoring dashboard test completed",
        "data": {
            "dashboard_data": dashboard_data,
            "report": report,
            "metrics_count": len(dashboard_data.get("metrics", {})),
            "health_checks_count": len(dashboard_data.get("health_status", {})),
            "active_alerts_count": len(dashboard_data.get("active_alerts", [])),
        },
    }
