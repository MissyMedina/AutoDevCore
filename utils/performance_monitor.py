#!/usr/bin/env python3
"""
Performance Monitor - Track and analyze AutoDevCore performance metrics
"""

import time
import json
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque


class PerformanceMonitor:
    """Monitor and track performance metrics for AutoDevCore."""
    
    def __init__(self, metrics_dir: str = "logs/metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance tracking
        self.operation_times = defaultdict(list)
        self.memory_usage = deque(maxlen=1000)
        self.cpu_usage = deque(maxlen=1000)
        self.error_counts = defaultdict(int)
        self.success_counts = defaultdict(int)
        
        # Real-time monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Load historical data
        self._load_historical_metrics()
    
    def start_operation(self, operation_name: str) -> str:
        """Start timing an operation and return operation ID."""
        operation_id = f"{operation_name}_{int(time.time() * 1000)}"
        self.operation_times[operation_name].append({
            "id": operation_id,
            "start_time": time.time(),
            "status": "running"
        })
        return operation_id
    
    def end_operation(self, operation_name: str, operation_id: str, success: bool = True):
        """End timing an operation."""
        end_time = time.time()
        
        # Find the operation
        for op in self.operation_times[operation_name]:
            if op["id"] == operation_id:
                op["end_time"] = end_time
                op["duration"] = end_time - op["start_time"]
                op["status"] = "completed" if success else "failed"
                break
        
        # Update success/error counts
        if success:
            self.success_counts[operation_name] += 1
        else:
            self.error_counts[operation_name] += 1
    
    def record_memory_usage(self):
        """Record current memory usage."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            self.memory_usage.append({
                "timestamp": time.time(),
                "rss_mb": memory_info.rss / 1024 / 1024,  # RSS in MB
                "vms_mb": memory_info.vms / 1024 / 1024,  # VMS in MB
                "percent": process.memory_percent()
            })
        except Exception as e:
            print(f"Error recording memory usage: {e}")
    
    def record_cpu_usage(self):
        """Record current CPU usage."""
        try:
            process = psutil.Process()
            cpu_percent = process.cpu_percent()
            
            self.cpu_usage.append({
                "timestamp": time.time(),
                "cpu_percent": cpu_percent
            })
        except Exception as e:
            print(f"Error recording CPU usage: {e}")
    
    def start_monitoring(self, interval: float = 1.0):
        """Start real-time monitoring."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self, interval: float):
        """Monitoring loop for real-time metrics."""
        while self.monitoring_active:
            self.record_memory_usage()
            self.record_cpu_usage()
            time.sleep(interval)
    
    def get_operation_stats(self, operation_name: str = None) -> Dict[str, Any]:
        """Get statistics for operations."""
        if operation_name:
            operations = self.operation_times.get(operation_name, [])
        else:
            operations = []
            for ops in self.operation_times.values():
                operations.extend(ops)
        
        if not operations:
            return {"count": 0, "avg_duration": 0, "success_rate": 0}
        
        completed_ops = [op for op in operations if op.get("status") == "completed"]
        failed_ops = [op for op in operations if op.get("status") == "failed"]
        
        total_count = len(operations)
        completed_count = len(completed_ops)
        failed_count = len(failed_ops)
        
        if completed_ops:
            avg_duration = sum(op.get("duration", 0) for op in completed_ops) / len(completed_ops)
            min_duration = min(op.get("duration", 0) for op in completed_ops)
            max_duration = max(op.get("duration", 0) for op in completed_ops)
        else:
            avg_duration = min_duration = max_duration = 0
        
        success_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        return {
            "count": total_count,
            "completed": completed_count,
            "failed": failed_count,
            "avg_duration_seconds": round(avg_duration, 3),
            "min_duration_seconds": round(min_duration, 3),
            "max_duration_seconds": round(max_duration, 3),
            "success_rate_percent": round(success_rate, 2)
        }
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        if not self.memory_usage:
            return {"current_mb": 0, "avg_mb": 0, "max_mb": 0}
        
        current = self.memory_usage[-1] if self.memory_usage else {"rss_mb": 0}
        rss_values = [entry["rss_mb"] for entry in self.memory_usage]
        
        return {
            "current_mb": round(current["rss_mb"], 2),
            "avg_mb": round(sum(rss_values) / len(rss_values), 2),
            "max_mb": round(max(rss_values), 2),
            "min_mb": round(min(rss_values), 2)
        }
    
    def get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU usage statistics."""
        if not self.cpu_usage:
            return {"current_percent": 0, "avg_percent": 0, "max_percent": 0}
        
        current = self.cpu_usage[-1] if self.cpu_usage else {"cpu_percent": 0}
        cpu_values = [entry["cpu_percent"] for entry in self.cpu_usage]
        
        return {
            "current_percent": round(current["cpu_percent"], 2),
            "avg_percent": round(sum(cpu_values) / len(cpu_values), 2),
            "max_percent": round(max(cpu_values), 2),
            "min_percent": round(min(cpu_values), 2)
        }
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall performance statistics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "operations": {
                name: self.get_operation_stats(name) 
                for name in self.operation_times.keys()
            },
            "memory": self.get_memory_stats(),
            "cpu": self.get_cpu_stats(),
            "success_rates": {
                name: (self.success_counts[name] / (self.success_counts[name] + self.error_counts[name]) * 100)
                if (self.success_counts[name] + self.error_counts[name]) > 0 else 0
                for name in set(list(self.success_counts.keys()) + list(self.error_counts.keys()))
            }
        }
    
    def save_metrics(self, filename: str = None):
        """Save current metrics to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
        
        metrics_file = self.metrics_dir / filename
        
        metrics_data = {
            "timestamp": datetime.now().isoformat(),
            "operation_times": dict(self.operation_times),
            "memory_usage": list(self.memory_usage),
            "cpu_usage": list(self.cpu_usage),
            "success_counts": dict(self.success_counts),
            "error_counts": dict(self.error_counts),
            "overall_stats": self.get_overall_stats()
        }
        
        try:
            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            print(f"✅ Metrics saved to: {metrics_file}")
        except Exception as e:
            print(f"❌ Error saving metrics: {e}")
    
    def _load_historical_metrics(self):
        """Load historical metrics from files."""
        try:
            # Load the most recent metrics file
            metrics_files = list(self.metrics_dir.glob("metrics_*.json"))
            if metrics_files:
                latest_file = max(metrics_files, key=lambda f: f.stat().st_mtime)
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                
                # Restore some historical data
                if "success_counts" in data:
                    self.success_counts.update(data["success_counts"])
                if "error_counts" in data:
                    self.error_counts.update(data["error_counts"])
                
                print(f"📊 Loaded historical metrics from: {latest_file}")
        except Exception as e:
            print(f"⚠️ Could not load historical metrics: {e}")
    
    def generate_performance_report(self) -> str:
        """Generate a human-readable performance report."""
        stats = self.get_overall_stats()
        
        report = f"""
# AutoDevCore Performance Report
Generated: {stats['timestamp']}

## System Resources
- **Memory Usage**: {stats['memory']['current_mb']} MB (avg: {stats['memory']['avg_mb']} MB, max: {stats['memory']['max_mb']} MB)
- **CPU Usage**: {stats['cpu']['current_percent']}% (avg: {stats['cpu']['avg_percent']}%, max: {stats['cpu']['max_percent']}%)

## Operation Performance
"""
        
        for op_name, op_stats in stats['operations'].items():
            report += f"""
### {op_name}
- **Total Operations**: {op_stats['count']}
- **Success Rate**: {op_stats['success_rate_percent']}%
- **Average Duration**: {op_stats['avg_duration_seconds']} seconds
- **Min/Max Duration**: {op_stats['min_duration_seconds']}s / {op_stats['max_duration_seconds']}s
"""
        
        report += f"""
## Success Rates by Operation
"""
        
        for op_name, success_rate in stats['success_rates'].items():
            report += f"- **{op_name}**: {success_rate:.1f}%\n"
        
        return report
    
    def print_summary(self):
        """Print a summary of current performance metrics."""
        stats = self.get_overall_stats()
        
        print("📊 AutoDevCore Performance Summary")
        print("=" * 50)
        print(f"Memory: {stats['memory']['current_mb']} MB (avg: {stats['memory']['avg_mb']} MB)")
        print(f"CPU: {stats['cpu']['current_percent']}% (avg: {stats['cpu']['avg_percent']}%)")
        print()
        
        print("Operation Performance:")
        for op_name, op_stats in stats['operations'].items():
            print(f"  {op_name}: {op_stats['avg_duration_seconds']}s avg, {op_stats['success_rate_percent']}% success")
        
        print()
        print("Success Rates:")
        for op_name, success_rate in stats['success_rates'].items():
            print(f"  {op_name}: {success_rate:.1f}%")


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def track_operation(operation_name: str):
    """Decorator to track operation performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            op_id = performance_monitor.start_operation(operation_name)
            try:
                result = func(*args, **kwargs)
                performance_monitor.end_operation(operation_name, op_id, success=True)
                return result
            except Exception as e:
                performance_monitor.end_operation(operation_name, op_id, success=False)
                raise e
        return wrapper
    return decorator
