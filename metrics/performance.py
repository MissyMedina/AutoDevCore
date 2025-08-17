"""
Performance monitoring and optimization utilities for AutoDevCore.
"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil

class PerformanceMonitor:
    """Monitor and track performance metrics."""

    def __init__(self):
        self.metrics = {}
        self.start_times = {}
        self.monitoring = False
        self.metrics_file = Path("logs/performance_metrics.json")
        self.metrics_file.parent.mkdir(exist_ok=True)

    def start_monitoring(self):
        """Start performance monitoring."""
        self.monitoring = True
        self.metrics = {
            "start_time": datetime.now().isoformat(),
            "operations": {},
            "system_stats": [],
            "memory_usage": [],
            "cpu_usage": [],
        }

    def stop_monitoring(self):
        """Stop performance monitoring and save metrics."""
        self.monitoring = False
        self.metrics["end_time"] = datetime.now().isoformat()
        self._save_metrics()

    def start_operation(self, operation_name: str):
        """Start timing an operation."""
        if not self.monitoring:
            return

        self.start_times[operation_name] = time.time()

        if operation_name not in self.metrics["operations"]:
            self.metrics["operations"][operation_name] = {
                "count": 0,
                "total_time": 0,
                "min_time": float("inf"),
                "max_time": 0,
                "avg_time": 0,
            }

    def end_operation(self, operation_name: str):
        """End timing an operation."""
        if not self.monitoring or operation_name not in self.start_times:
            return

        duration = time.time() - self.start_times[operation_name]
        del self.start_times[operation_name]

        op_metrics = self.metrics["operations"][operation_name]
        op_metrics["count"] += 1
        op_metrics["total_time"] += duration
        op_metrics["min_time"] = min(op_metrics["min_time"], duration)
        op_metrics["max_time"] = max(op_metrics["max_time"], duration)
        op_metrics["avg_time"] = op_metrics["total_time"] / op_metrics["count"]

    def record_system_stats(self):
        """Record current system statistics."""
        if not self.monitoring:
            return

        timestamp = datetime.now().isoformat()

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics["cpu_usage"].append(
            {"timestamp": timestamp, "cpu_percent": cpu_percent}
        )

        # Memory usage
        memory = psutil.virtual_memory()
        self.metrics["memory_usage"].append(
            {
                "timestamp": timestamp,
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
            }
        )

        # System stats
        disk = psutil.disk_usage("/")
        self.metrics["system_stats"].append(
            {
                "timestamp": timestamp,
                "disk_total": disk.total,
                "disk_used": disk.used,
                "disk_free": disk.free,
                "disk_percent": (disk.used / disk.total) * 100,
            }
        )

    def _save_metrics(self):
        """Save metrics to file."""
        try:
            with open(self.metrics_file, "w") as f:
                json.dump(self.metrics, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving performance metrics: {e}")

    def get_summary(self) -> Dict[str, Any]:
        """Get a performance summary."""
        if not self.metrics:
            return {"error": "No metrics available"}

        summary = {
            "monitoring_duration": 0,
            "total_operations": 0,
            "slowest_operation": None,
            "fastest_operation": None,
            "average_cpu_usage": 0,
            "average_memory_usage": 0,
        }

        # Calculate monitoring duration
        if "start_time" in self.metrics and "end_time" in self.metrics:
            start = datetime.fromisoformat(self.metrics["start_time"])
            end = datetime.fromisoformat(self.metrics["end_time"])
            summary["monitoring_duration"] = (end - start).total_seconds()

        # Analyze operations
        if self.metrics["operations"]:
            operations = self.metrics["operations"]
            summary["total_operations"] = sum(op["count"] for op in operations.values())

            # Find slowest and fastest operations
            slowest_time = 0
            fastest_time = float("inf")

            for op_name, op_metrics in operations.items():
                if op_metrics["max_time"] > slowest_time:
                    slowest_time = op_metrics["max_time"]
                    summary["slowest_operation"] = op_name

                if op_metrics["min_time"] < fastest_time:
                    fastest_time = op_metrics["min_time"]
                    summary["fastest_operation"] = op_name

        # Calculate average system usage
        if self.metrics["cpu_usage"]:
            cpu_values = [stat["cpu_percent"] for stat in self.metrics["cpu_usage"]]
            summary["average_cpu_usage"] = sum(cpu_values) / len(cpu_values)

        if self.metrics["memory_usage"]:
            memory_values = [stat["percent"] for stat in self.metrics["memory_usage"]]
            summary["average_memory_usage"] = sum(memory_values) / len(memory_values)

        return summary

class PerformanceOptimizer:
    """Optimize performance based on monitoring data."""

    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.optimization_suggestions = []

    def analyze_performance(self, metrics_file: Path) -> List[str]:
        """Analyze performance metrics and provide optimization suggestions."""
        suggestions = []

        try:
            with open(metrics_file, "r") as f:
                metrics = json.load(f)

            # Analyze operation times
            for op_name, op_metrics in metrics.get("operations", {}).items():
                avg_time = op_metrics.get("avg_time", 0)
                max_time = op_metrics.get("max_time", 0)

                if avg_time > 10:  # More than 10 seconds average
                    suggestions.append(
                        f"⚠️ {op_name} is slow (avg: {avg_time:.2f}s) - consider optimization"
                    )

                if max_time > 60:  # More than 60 seconds max
                    suggestions.append(
                        f"🚨 {op_name} has very slow operations (max: {max_time:.2f}s) - investigate bottlenecks"
                    )

            # Analyze system usage
            cpu_usage = metrics.get("cpu_usage", [])
            if cpu_usage:
                avg_cpu = sum(stat["cpu_percent"] for stat in cpu_usage) / len(
                    cpu_usage
                )
                if avg_cpu > 80:
                    suggestions.append(
                        f"🔥 High CPU usage detected (avg: {avg_cpu:.1f}%) - consider reducing load"
                    )

            memory_usage = metrics.get("memory_usage", [])
            if memory_usage:
                avg_memory = sum(stat["percent"] for stat in memory_usage) / len(
                    memory_usage
                )
                if avg_memory > 85:
                    suggestions.append(
                        f"💾 High memory usage detected (avg: {avg_memory:.1f}%) - consider memory optimization"
                    )

            # Check for potential bottlenecks
            if not suggestions:
                suggestions.append(
                    "✅ Performance looks good! No major issues detected."
                )

        except Exception as e:
            suggestions.append(f"❌ Error analyzing performance: {e}")

        return suggestions

    def get_optimization_recommendations(self) -> Dict[str, List[str]]:
        """Get specific optimization recommendations."""
        recommendations = {"immediate": [], "short_term": [], "long_term": []}

        # Immediate optimizations
        recommendations["immediate"].extend(
            [
                "Enable caching for GPT-OSS requests",
                "Reduce context window size for faster inference",
                "Use quantized models when available",
                "Implement request batching",
            ]
        )

        # Short term optimizations
        recommendations["short_term"].extend(
            [
                "Implement parallel processing for independent operations",
                "Add connection pooling for database operations",
                "Optimize file I/O operations",
                "Implement lazy loading for large datasets",
            ]
        )

        # Long term optimizations
        recommendations["long_term"].extend(
            [
                "Consider using smaller, faster models",
                "Implement distributed processing",
                "Add GPU acceleration support",
                "Optimize memory usage patterns",
            ]
        )

        return recommendations

# Global performance monitor instance
performance_monitor = PerformanceMonitor()
performance_optimizer = PerformanceOptimizer()

def monitor_operation(operation_name: str):
    """Decorator to monitor operation performance."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            performance_monitor.start_operation(operation_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                performance_monitor.end_operation(operation_name)

        return wrapper

    return decorator

def get_performance_report() -> Dict[str, Any]:
    """Get a comprehensive performance report."""
    summary = performance_monitor.get_summary()
    recommendations = performance_optimizer.get_optimization_recommendations()

    return {
        "summary": summary,
        "recommendations": recommendations,
        "cache_stats": performance_monitor.metrics.get("cache_stats", {}),
        "timestamp": datetime.now().isoformat(),
    }
