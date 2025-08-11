"""
Performance Optimizer for AutoDevCore
Comprehensive performance optimization system for Phase 4.3
"""

import asyncio
import hashlib
import json
import logging
import pickle
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import psutil
import redis


class CacheStrategy(Enum):
    """Cache strategy types"""

    LRU = "lru"
    TTL = "ttl"
    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"


class OptimizationType(Enum):
    """Performance optimization types"""

    CACHE = "cache"
    DATABASE = "database"
    MEMORY = "memory"
    CPU = "cpu"
    NETWORK = "network"


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""

    operation: str
    duration_ms: float
    memory_mb: float
    cpu_percent: float
    cache_hits: int = 0
    cache_misses: int = 0
    database_queries: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class CacheConfig:
    """Cache configuration"""

    strategy: CacheStrategy = CacheStrategy.TTL
    ttl_seconds: int = 3600  # 1 hour default
    max_size: int = 1000
    enable_compression: bool = True
    enable_stats: bool = True


class RedisCache:
    """Redis-based caching system"""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                self.stats["hits"] += 1
                return json.loads(value)
            else:
                self.stats["misses"] += 1
                return None
        except Exception as e:
            logging.error(f"Redis get error: {e}")
            self.stats["misses"] += 1
            return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache"""
        try:
            serialized = json.dumps(value)
            result = self.redis_client.setex(key, ttl, serialized)
            self.stats["sets"] += 1
            return result
        except Exception as e:
            logging.error(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            result = self.redis_client.delete(key)
            self.stats["deletes"] += 1
            return result > 0
        except Exception as e:
            logging.error(f"Redis delete error: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        hit_rate = 0
        if self.stats["hits"] + self.stats["misses"] > 0:
            hit_rate = self.stats["hits"] / (self.stats["hits"] + self.stats["misses"])

        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "deletes": self.stats["deletes"],
            "hit_rate": hit_rate,
            "total_operations": self.stats["hits"]
            + self.stats["misses"]
            + self.stats["sets"]
            + self.stats["deletes"],
        }


class DatabaseOptimizer:
    """Database performance optimization"""

    def __init__(self, db_path: str = "data/autodevcore.db"):
        self.db_path = db_path
        self.connection_pool = {}
        self.query_stats = {"total_queries": 0, "slow_queries": 0, "avg_query_time": 0}

    def optimize_queries(self) -> Dict[str, Any]:
        """Analyze and optimize database queries"""
        optimizations = {
            "indexes_created": [],
            "queries_optimized": [],
            "performance_improvements": [],
        }

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Analyze table structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]

                # Check for missing indexes
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()

                if not indexes:
                    # Create basic indexes
                    cursor.execute(
                        f"CREATE INDEX IF NOT EXISTS idx_{table_name}_id ON {table_name}(id)"
                    )
                    optimizations["indexes_created"].append(f"idx_{table_name}_id")

                # Analyze query performance
                cursor.execute(f"ANALYZE {table_name}")

            # Enable WAL mode for better concurrency
            cursor.execute("PRAGMA journal_mode=WAL")

            # Set cache size
            cursor.execute("PRAGMA cache_size=10000")

            # Enable foreign keys
            cursor.execute("PRAGMA foreign_keys=ON")

            conn.commit()
            conn.close()

            optimizations["performance_improvements"].extend(
                [
                    "WAL mode enabled for better concurrency",
                    "Cache size increased to 10MB",
                    "Foreign key constraints enabled",
                ]
            )

        except Exception as e:
            logging.error(f"Database optimization error: {e}")

        return optimizations

    def get_query_stats(self) -> Dict[str, Any]:
        """Get database query statistics"""
        return self.query_stats


class MemoryOptimizer:
    """Memory usage optimization"""

    def __init__(self):
        self.memory_threshold = 80  # 80% memory usage threshold
        self.optimization_history = []

    def analyze_memory_usage(self) -> Dict[str, Any]:
        """Analyze current memory usage"""
        memory = psutil.virtual_memory()

        analysis = {
            "total_mb": memory.total / (1024 * 1024),
            "available_mb": memory.available / (1024 * 1024),
            "used_mb": memory.used / (1024 * 1024),
            "percent_used": memory.percent,
            "is_optimization_needed": memory.percent > self.memory_threshold,
            "recommendations": [],
        }

        if analysis["is_optimization_needed"]:
            analysis["recommendations"].extend(
                [
                    "Consider implementing object pooling",
                    "Review memory-intensive operations",
                    "Implement lazy loading for large datasets",
                    "Consider using generators for large iterations",
                ]
            )

        return analysis

    def optimize_memory(self) -> Dict[str, Any]:
        """Perform memory optimization"""
        optimizations = {
            "garbage_collection": False,
            "object_pooling": False,
            "memory_cleared_mb": 0,
        }

        # Force garbage collection
        import gc

        collected = gc.collect()
        optimizations["garbage_collection"] = True

        # Clear Python cache
        import sys

        if hasattr(sys, "getsizeof"):
            before_size = sum(sys.getsizeof(obj) for obj in gc.get_objects())
            gc.collect()
            after_size = sum(sys.getsizeof(obj) for obj in gc.get_objects())
            optimizations["memory_cleared_mb"] = (before_size - after_size) / (
                1024 * 1024
            )

        return optimizations


class CPUOptimizer:
    """CPU usage optimization"""

    def __init__(self):
        self.cpu_threshold = 80  # 80% CPU usage threshold
        self.thread_pool = None

    def analyze_cpu_usage(self) -> Dict[str, Any]:
        """Analyze current CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)

        analysis = {
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count(),
            "is_optimization_needed": cpu_percent > self.cpu_threshold,
            "recommendations": [],
        }

        if analysis["is_optimization_needed"]:
            analysis["recommendations"].extend(
                [
                    "Consider using async/await for I/O operations",
                    "Implement thread pooling for CPU-intensive tasks",
                    "Review algorithm complexity",
                    "Consider caching expensive computations",
                ]
            )

        return analysis

    def optimize_cpu(self) -> Dict[str, Any]:
        """Perform CPU optimization"""
        optimizations = {
            "thread_pool_created": False,
            "async_operations": False,
            "cpu_intensive_tasks_cached": False,
        }

        # Create thread pool if needed
        if not self.thread_pool:
            import concurrent.futures

            self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
            optimizations["thread_pool_created"] = True

        return optimizations


class PerformanceOptimizer:
    """Main performance optimization orchestrator"""

    def __init__(self, cache_config: CacheConfig = None):
        self.cache_config = cache_config or CacheConfig()
        self.redis_cache = RedisCache()
        self.db_optimizer = DatabaseOptimizer()
        self.memory_optimizer = MemoryOptimizer()
        self.cpu_optimizer = CPUOptimizer()
        self.metrics_history: List[PerformanceMetrics] = []
        self.optimization_enabled = True

    def cache_decorator(self, ttl: int = 3600):
        """Decorator for caching function results"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.optimization_enabled:
                    return func(*args, **kwargs)

                # Generate cache key
                key_parts = [func.__name__]
                key_parts.extend([str(arg) for arg in args])
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
                cache_key = hashlib.md5(":".join(key_parts).encode()).hexdigest()

                # Try to get from cache
                cached_result = self.redis_cache.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Execute function and cache result
                result = func(*args, **kwargs)
                self.redis_cache.set(cache_key, result, ttl)
                return result

            return wrapper

        return decorator

    def monitor_performance(self, operation: str):
        """Decorator for monitoring function performance"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / (1024 * 1024)
                start_cpu = psutil.cpu_percent()

                try:
                    result = func(*args, **kwargs)

                    # Record metrics
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / (1024 * 1024)
                    end_cpu = psutil.cpu_percent()

                    metrics = PerformanceMetrics(
                        operation=operation,
                        duration_ms=(end_time - start_time) * 1000,
                        memory_mb=end_memory - start_memory,
                        cpu_percent=end_cpu - start_cpu,
                    )

                    self.metrics_history.append(metrics)

                    return result
                except Exception as e:
                    logging.error(f"Performance monitoring error in {operation}: {e}")
                    raise

            return wrapper

        return decorator

    def run_full_optimization(self) -> Dict[str, Any]:
        """Run comprehensive performance optimization"""
        results = {
            "cache_optimization": {},
            "database_optimization": {},
            "memory_optimization": {},
            "cpu_optimization": {},
            "overall_improvement": 0,
        }

        # Cache optimization
        cache_stats = self.redis_cache.get_stats()
        results["cache_optimization"] = {
            "hit_rate": cache_stats["hit_rate"],
            "total_operations": cache_stats["total_operations"],
            "recommendations": [],
        }

        if cache_stats["hit_rate"] < 0.7:
            results["cache_optimization"]["recommendations"].append(
                "Consider increasing cache TTL or cache size"
            )

        # Database optimization
        db_optimizations = self.db_optimizer.optimize_queries()
        results["database_optimization"] = db_optimizations

        # Memory optimization
        memory_analysis = self.memory_optimizer.analyze_memory_usage()
        if memory_analysis["is_optimization_needed"]:
            memory_optimizations = self.memory_optimizer.optimize_memory()
            results["memory_optimization"] = {
                "analysis": memory_analysis,
                "optimizations": memory_optimizations,
            }

        # CPU optimization
        cpu_analysis = self.cpu_optimizer.analyze_cpu_usage()
        if cpu_analysis["is_optimization_needed"]:
            cpu_optimizations = self.cpu_optimizer.optimize_cpu()
            results["cpu_optimization"] = {
                "analysis": cpu_analysis,
                "optimizations": cpu_optimizations,
            }

        # Calculate overall improvement
        improvements = []
        if cache_stats["hit_rate"] > 0.8:
            improvements.append(20)
        if db_optimizations["indexes_created"]:
            improvements.append(15)
        if memory_analysis["percent_used"] < 70:
            improvements.append(10)
        if cpu_analysis["cpu_percent"] < 70:
            improvements.append(10)

        results["overall_improvement"] = sum(improvements)

        return results

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.metrics_history:
            return {"error": "No performance metrics available"}

        # Calculate averages
        avg_duration = sum(m.duration_ms for m in self.metrics_history) / len(
            self.metrics_history
        )
        avg_memory = sum(m.memory_mb for m in self.metrics_history) / len(
            self.metrics_history
        )
        avg_cpu = sum(m.cpu_percent for m in self.metrics_history) / len(
            self.metrics_history
        )

        # Find slowest operations
        slowest_operations = sorted(
            self.metrics_history, key=lambda x: x.duration_ms, reverse=True
        )[:5]

        # Cache statistics
        cache_stats = self.redis_cache.get_stats()

        # System metrics
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()

        return {
            "summary": {
                "total_operations": len(self.metrics_history),
                "avg_duration_ms": avg_duration,
                "avg_memory_mb": avg_memory,
                "avg_cpu_percent": avg_cpu,
            },
            "slowest_operations": [
                {
                    "operation": m.operation,
                    "duration_ms": m.duration_ms,
                    "memory_mb": m.memory_mb,
                    "cpu_percent": m.cpu_percent,
                }
                for m in slowest_operations
            ],
            "cache_performance": cache_stats,
            "system_metrics": {
                "memory_percent": memory.percent,
                "cpu_percent": cpu,
                "memory_available_mb": memory.available / (1024 * 1024),
            },
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if self.metrics_history:
            avg_duration = sum(m.duration_ms for m in self.metrics_history) / len(
                self.metrics_history
            )
            if avg_duration > 1000:  # More than 1 second
                recommendations.append(
                    "Consider implementing caching for slow operations"
                )

            avg_memory = sum(m.memory_mb for m in self.metrics_history) / len(
                self.metrics_history
            )
            if avg_memory > 100:  # More than 100MB
                recommendations.append("Review memory usage in operations")

        cache_stats = self.redis_cache.get_stats()
        if cache_stats["hit_rate"] < 0.7:
            recommendations.append("Optimize cache strategy to improve hit rate")

        memory = psutil.virtual_memory()
        if memory.percent > 80:
            recommendations.append(
                "System memory usage is high - consider optimization"
            )

        return recommendations


# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()


# Example usage decorators
def cache_result(ttl: int = 3600):
    """Cache function result for specified TTL"""
    return performance_optimizer.cache_decorator(ttl)


def monitor_performance(operation: str):
    """Monitor function performance"""
    return performance_optimizer.monitor_performance(operation)


if __name__ == "__main__":
    # Example usage
    @cache_result(ttl=1800)  # Cache for 30 minutes
    @monitor_performance("example_operation")
    def expensive_operation(data: str) -> Dict[str, Any]:
        """Example expensive operation"""
        time.sleep(0.1)  # Simulate work
        return {"result": f"processed_{data}", "timestamp": time.time()}

    # Run optimization
    results = performance_optimizer.run_full_optimization()
    print("Performance Optimization Results:")
    print(json.dumps(results, indent=2))

    # Generate report
    report = performance_optimizer.get_performance_report()
    print("\nPerformance Report:")
    print(json.dumps(report, indent=2))
