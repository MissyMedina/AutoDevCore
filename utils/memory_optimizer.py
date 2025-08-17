#!/usr/bin/env python3
"""
Memory Optimization Utilities
Implements object pooling, memory leak detection, and efficient data structures.
"""

import gc
import sys
import weakref
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass
from threading import Lock
from typing import Any, Dict, List, Optional, Type, TypeVar

import psutil

T = TypeVar("T")


@dataclass
class MemoryStats:
    """Memory usage statistics."""

    total_mb: float
    available_mb: float
    used_mb: float
    percent_used: float
    python_objects: int
    gc_collections: int


class ObjectPool:
    """Generic object pool for memory optimization."""

    def __init__(self, factory_func, max_size: int = 100):
        self.factory_func = factory_func
        self.max_size = max_size
        self._pool = deque()
        self._lock = Lock()
        self._created_count = 0
        self._reused_count = 0

    def acquire(self) -> Any:
        """Get an object from the pool."""
        with self._lock:
            if self._pool:
                self._reused_count += 1
                return self._pool.popleft()
            else:
                self._created_count += 1
                return self.factory_func()

    def release(self, obj: Any) -> None:
        """Return an object to the pool."""
        with self._lock:
            if len(self._pool) < self.max_size:
                # Reset object state if it has a reset method
                if hasattr(obj, "reset"):
                    obj.reset()
                self._pool.append(obj)

    @contextmanager
    def get_object(self):
        """Context manager for automatic object lifecycle."""
        obj = self.acquire()
        try:
            yield obj
        finally:
            self.release(obj)

    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        return {
            "pool_size": len(self._pool),
            "created_count": self._created_count,
            "reused_count": self._reused_count,
            "efficiency": self._reused_count
            / max(1, self._created_count + self._reused_count),
        }


class MemoryLeakDetector:
    """Detect potential memory leaks."""

    def __init__(self):
        self._object_counts = defaultdict(int)
        self._weak_refs = set()
        self._snapshots = []

    def take_snapshot(self, label: str = None) -> Dict[str, Any]:
        """Take a memory snapshot."""
        gc.collect()  # Force garbage collection

        # Get object counts by type
        object_counts = defaultdict(int)
        for obj in gc.get_objects():
            obj_type = type(obj).__name__
            object_counts[obj_type] += 1

        # Get memory usage
        memory = psutil.virtual_memory()

        snapshot = {
            "label": label or f"snapshot_{len(self._snapshots)}",
            "timestamp": psutil.boot_time(),
            "memory_mb": memory.used / (1024 * 1024),
            "object_counts": dict(object_counts),
            "total_objects": len(gc.get_objects()),
            "gc_stats": gc.get_stats(),
        }

        self._snapshots.append(snapshot)
        return snapshot

    def compare_snapshots(
        self, snapshot1_idx: int = -2, snapshot2_idx: int = -1
    ) -> Dict[str, Any]:
        """Compare two snapshots to detect leaks."""
        if len(self._snapshots) < 2:
            return {"error": "Need at least 2 snapshots to compare"}

        snap1 = self._snapshots[snapshot1_idx]
        snap2 = self._snapshots[snapshot2_idx]

        # Memory difference
        memory_diff = snap2["memory_mb"] - snap1["memory_mb"]

        # Object count differences
        object_diffs = {}
        all_types = set(snap1["object_counts"].keys()) | set(
            snap2["object_counts"].keys()
        )

        for obj_type in all_types:
            count1 = snap1["object_counts"].get(obj_type, 0)
            count2 = snap2["object_counts"].get(obj_type, 0)
            diff = count2 - count1
            if diff != 0:
                object_diffs[obj_type] = diff

        # Sort by largest increases
        sorted_diffs = sorted(object_diffs.items(), key=lambda x: x[1], reverse=True)

        return {
            "memory_diff_mb": memory_diff,
            "object_differences": dict(sorted_diffs[:10]),  # Top 10 changes
            "potential_leaks": [
                obj_type for obj_type, diff in sorted_diffs[:5] if diff > 100
            ],
            "total_object_diff": snap2["total_objects"] - snap1["total_objects"],
        }

    def track_object(self, obj: Any) -> None:
        """Track an object for lifecycle monitoring."""

        def cleanup_callback(ref):
            self._weak_refs.discard(ref)

        weak_ref = weakref.ref(obj, cleanup_callback)
        self._weak_refs.add(weak_ref)


class EfficientDataStructures:
    """Optimized data structures for common use cases."""

    @staticmethod
    def create_string_builder(initial_capacity: int = 1024) -> List[str]:
        """Create an efficient string builder using list."""
        return []

    @staticmethod
    def join_strings(string_list: List[str]) -> str:
        """Efficiently join strings."""
        return "".join(string_list)

    @staticmethod
    def create_lru_cache(maxsize: int = 128):
        """Create an LRU cache with specified size."""

        from functools import lru_cache

        return lru_cache(maxsize=maxsize)

    @staticmethod
    def batch_process(items: List[Any], batch_size: int = 100):
        """Process items in batches to reduce memory usage."""
        for i in range(0, len(items), batch_size):
            yield items[i : i + batch_size]


class MemoryOptimizer:
    """Main memory optimization coordinator."""

    def __init__(self):
        self.pools = {}
        self.leak_detector = MemoryLeakDetector()
        self._monitoring = False

    def create_pool(self, name: str, factory_func, max_size: int = 100) -> ObjectPool:
        """Create a named object pool."""
        pool = ObjectPool(factory_func, max_size)
        self.pools[name] = pool
        return pool

    def get_pool(self, name: str) -> Optional[ObjectPool]:
        """Get a named object pool."""
        return self.pools.get(name)

    def get_memory_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        memory = psutil.virtual_memory()
        gc.collect()

        return MemoryStats(
            total_mb=memory.total / (1024 * 1024),
            available_mb=memory.available / (1024 * 1024),
            used_mb=memory.used / (1024 * 1024),
            percent_used=memory.percent,
            python_objects=len(gc.get_objects()),
            gc_collections=sum(
                gc.get_stats()[i]["collections"] for i in range(len(gc.get_stats()))
            ),
        )

    def optimize_memory(self) -> Dict[str, Any]:
        """Run memory optimization."""
        before_stats = self.get_memory_stats()

        # Force garbage collection
        collected = gc.collect()

        # Clear internal caches
        sys.intern.__dict__.clear() if hasattr(sys.intern, "__dict__") else None

        after_stats = self.get_memory_stats()

        return {
            "before_mb": before_stats.used_mb,
            "after_mb": after_stats.used_mb,
            "freed_mb": before_stats.used_mb - after_stats.used_mb,
            "objects_collected": collected,
            "pools_stats": {
                name: pool.get_stats() for name, pool in self.pools.items()
            },
        }

    def start_monitoring(self, interval_seconds: int = 60):
        """Start memory monitoring."""

        import threading
        import time

        def monitor():
            while self._monitoring:
                self.leak_detector.take_snapshot()
                time.sleep(interval_seconds)

        self._monitoring = True
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def stop_monitoring(self):
        """Stop memory monitoring."""
        self._monitoring = False


# Global memory optimizer instance
memory_optimizer = MemoryOptimizer()

# Common object pools
string_pool = memory_optimizer.create_pool("strings", lambda: [], max_size=50)
dict_pool = memory_optimizer.create_pool("dicts", dict, max_size=100)
list_pool = memory_optimizer.create_pool("lists", list, max_size=100)


def optimize_memory():
    """Convenience function for memory optimization."""
    return memory_optimizer.optimize_memory()


def get_memory_stats():
    """Convenience function for memory stats."""
    return memory_optimizer.get_memory_stats()
