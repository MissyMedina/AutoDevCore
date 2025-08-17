#!/usr/bin/env python3
"""
Metrics Storage - Unified data storage management for metrics
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import psutil


class MetricsStorage:
    """Unified storage manager for all metrics data."""

    def __init__(self, base_path: str = "logs/metrics"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Database for structured metrics
        self.db_path = self.base_path / "metrics.db"
        self._init_database()

        # JSON files for different metric types
        self.performance_file = self.base_path / "performance.json"
        self.system_file = self.base_path / "system.json"
        self.alerts_file = self.base_path / "alerts.json"
        self.health_file = self.base_path / "health.json"

        # Initialize files if they don't exist
        self._init_files()

    def _init_database(self):
        """Initialize SQLite database for metrics storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main metrics table
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

        # Performance operations table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS performance_ops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_name TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration REAL,
                status TEXT,
                metadata TEXT
            )
        """
        )

        # Alerts table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_name TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                resolved BOOLEAN DEFAULT FALSE,
                resolved_at DATETIME
            )
        """
        )

        # Health checks table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS health_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_name TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                details TEXT,
                error_message TEXT
            )
        """
        )

        # Create indexes for better performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_metrics_name_time ON metrics(metric_name, timestamp)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_health_timestamp ON health_checks(timestamp)"
        )

        conn.commit()
        conn.close()

    def _init_files(self):
        """Initialize JSON files with default structure."""
        files_to_init = {
            self.performance_file: {"operations": {}, "system_stats": []},
            self.system_file: {"cpu_usage": [], "memory_usage": [], "disk_usage": []},
            self.alerts_file: {"alerts": [], "config": {}},
            self.health_file: {"checks": [], "overall_status": "unknown"},
        }

        for file_path, default_data in files_to_init.items():
            if not file_path.exists():
                with open(file_path, "w") as f:
                    json.dump(default_data, f, indent=2, default=str)

    def store_metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store a metric in the database."""
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
                    datetime.now().isoformat(),
                    value,
                    json.dumps(labels or {}),
                    json.dumps(metadata or {}),
                ),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing metric: {e}")
            return False

    def store_performance_operation(
        self,
        operation_name: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        duration: Optional[float] = None,
        status: str = "running",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Store performance operation data."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO performance_ops (operation_name, start_time, end_time, duration, status, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    operation_name,
                    start_time.isoformat(),
                    end_time.isoformat() if end_time else None,
                    duration,
                    status,
                    json.dumps(metadata or {}),
                ),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing performance operation: {e}")
            return False

    def store_alert(self, alert_name: str, severity: str, message: str) -> bool:
        """Store an alert."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO alerts (alert_name, severity, message, timestamp)
                VALUES (?, ?, ?, ?)
            """,
                (alert_name, severity, message, datetime.now().isoformat()),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing alert: {e}")
            return False

    def store_health_check(
        self,
        check_name: str,
        status: str,
        details: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> bool:
        """Store a health check result."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO health_checks (check_name, status, timestamp, details, error_message)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    check_name,
                    status,
                    datetime.now().isoformat(),
                    details,
                    error_message,
                ),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing health check: {e}")
            return False

    def get_metrics(
        self, metric_name: Optional[str] = None, hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Get metrics from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if metric_name:
                cursor.execute(
                    """
                    SELECT metric_name, timestamp, value, labels, metadata
                    FROM metrics
                    WHERE metric_name = ? AND timestamp >= datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                """.format(
                        hours
                    ),
                    (metric_name,),
                )
            else:
                cursor.execute(
                    """
                    SELECT metric_name, timestamp, value, labels, metadata
                    FROM metrics
                    WHERE timestamp >= datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                """.format(
                        hours
                    )
                )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "metric_name": row[0],
                        "timestamp": row[1],
                        "value": row[2],
                        "labels": json.loads(row[3]) if row[3] else {},
                        "metadata": json.loads(row[4]) if row[4] else {},
                    }
                )

            conn.close()
            return results
        except Exception as e:
            print(f"Error getting metrics: {e}")
            return []

    def get_alerts(
        self, hours: int = 24, severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get alerts from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if severity:
                cursor.execute(
                    """
                    SELECT alert_name, severity, message, timestamp, resolved
                    FROM alerts
                    WHERE severity = ? AND timestamp >= datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                """.format(
                        hours
                    ),
                    (severity,),
                )
            else:
                cursor.execute(
                    """
                    SELECT alert_name, severity, message, timestamp, resolved
                    FROM alerts
                    WHERE timestamp >= datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                """.format(
                        hours
                    )
                )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "alert_name": row[0],
                        "severity": row[1],
                        "message": row[2],
                        "timestamp": row[3],
                        "resolved": bool(row[4]),
                    }
                )

            conn.close()
            return results
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []

    def get_health_status(self, hours: int = 24) -> Dict[str, Any]:
        """Get health check status."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT check_name, status, timestamp, details
                FROM health_checks
                WHERE timestamp >= datetime('now', '-{} hours')
                ORDER BY timestamp DESC
            """.format(
                    hours
                )
            )

            checks = {}
            for row in cursor.fetchall():
                check_name = row[0]
                if check_name not in checks:
                    checks[check_name] = {
                        "latest_status": row[1],
                        "latest_timestamp": row[2],
                        "details": row[3],
                        "history": [],
                    }
                checks[check_name]["history"].append(
                    {"status": row[1], "timestamp": row[2], "details": row[3]}
                )

            conn.close()

            # Determine overall status
            overall_status = "healthy"
            for check_data in checks.values():
                if check_data["latest_status"] == "error":
                    overall_status = "error"
                    break
                elif check_data["latest_status"] == "warning":
                    overall_status = "warning"

            return {
                "overall_status": overall_status,
                "checks": checks,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error getting health status: {e}")
            return {
                "overall_status": "unknown",
                "checks": {},
                "timestamp": datetime.now().isoformat(),
            }

    def cleanup_old_data(self, days: int = 30) -> bool:
        """Clean up old metrics data."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Delete old metrics
            cursor.execute(
                "DELETE FROM metrics WHERE timestamp < datetime('now', '-{} days')".format(
                    days
                )
            )

            # Delete old performance operations
            cursor.execute(
                "DELETE FROM performance_ops WHERE start_time < datetime('now', '-{} days')".format(
                    days
                )
            )

            # Delete old alerts (keep unresolved ones)
            cursor.execute(
                "DELETE FROM alerts WHERE resolved = 1 AND timestamp < datetime('now', '-{} days')".format(
                    days
                )
            )

            # Delete old health checks
            cursor.execute(
                "DELETE FROM health_checks WHERE timestamp < datetime('now', '-{} days')".format(
                    days
                )
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error cleaning up old data: {e}")
            return False

    def export_data(self, format: str = "json", hours: int = 24) -> Dict[str, Any]:
        """Export metrics data."""
        try:
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "time_range_hours": hours,
                "metrics": self.get_metrics(hours=hours),
                "alerts": self.get_alerts(hours=hours),
                "health_status": self.get_health_status(hours=hours),
            }

            if format == "json":
                return data
            elif format == "csv":
                # Convert to CSV format (simplified)
                return {
                    "csv_data": "timestamp,metric_name,value\n"
                    + "\n".join(
                        [
                            f"{m['timestamp']},{m['metric_name']},{m['value']}"
                            for m in data["metrics"]
                        ]
                    )
                }
            else:
                return {"error": f"Unsupported format: {format}"}
        except Exception as e:
            return {"error": str(e)}


# Global storage instance
metrics_storage = MetricsStorage()


def get_storage() -> MetricsStorage:
    """Get the global metrics storage instance."""
    return metrics_storage
