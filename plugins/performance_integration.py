"""
Performance Integration for AutoDevCore
Integrates performance optimization with existing systems for Phase 4.3
"""

import asyncio
import threading
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import logging

from .performance_optimizer import (
    PerformanceOptimizer,
    cache_result,
    monitor_performance,
    CacheConfig,
    CacheStrategy,
)
from .monitoring_dashboard import MonitoringDashboard
from .multi_model_ai import MultiModelAI
from .ai_orchestrator import AIOrchestrator


class PerformanceIntegration:
    """Integrates performance optimization with AutoDevCore systems"""

    def __init__(self):
        self.performance_optimizer = PerformanceOptimizer()
        self.monitoring_dashboard = MonitoringDashboard()
        self.multi_model_ai = MultiModelAI()
        self.ai_orchestrator = AIOrchestrator()

        # Performance configuration
        self.cache_config = CacheConfig(
            strategy=CacheStrategy.TTL,
            ttl_seconds=3600,
            max_size=1000,
            enable_compression=True,
            enable_stats=True,
        )

        # Performance metrics
        self.performance_metrics = {
            "ai_operations": [],
            "code_generation": [],
            "plugin_operations": [],
            "collaboration_operations": [],
        }

        # Start background optimization
        self._start_background_optimization()

    def _start_background_optimization(self):
        """Start background performance optimization"""

        def background_optimization():
            while True:
                try:
                    # Run optimization every 5 minutes
                    time.sleep(300)
                    self._run_background_optimization()
                except Exception as e:
                    logging.error(f"Background optimization error: {e}")

        thread = threading.Thread(target=background_optimization, daemon=True)
        thread.start()

    def _run_background_optimization(self):
        """Run background performance optimization"""
        try:
            # Run full optimization
            results = self.performance_optimizer.run_full_optimization()

            # Update monitoring dashboard
            self.monitoring_dashboard.add_metric(
                "performance_optimization",
                {
                    "overall_improvement": results["overall_improvement"],
                    "cache_hit_rate": results["cache_optimization"]["hit_rate"],
                    "memory_usage": results.get("memory_optimization", {})
                    .get("analysis", {})
                    .get("percent_used", 0),
                    "cpu_usage": results.get("cpu_optimization", {})
                    .get("analysis", {})
                    .get("cpu_percent", 0),
                },
            )

            logging.info(
                f"Background optimization completed: {results['overall_improvement']}% improvement"
            )

        except Exception as e:
            logging.error(f"Background optimization failed: {e}")

    @cache_result(ttl=1800)  # Cache for 30 minutes
    @monitor_performance("ai_generation")
    def optimized_ai_generation(
        self, prompt: str, model_type: str = "auto"
    ) -> Dict[str, Any]:
        """Optimized AI generation with caching and monitoring"""
        return self.ai_orchestrator.generate_response(prompt, model_type)

    @cache_result(ttl=3600)  # Cache for 1 hour
    @monitor_performance("app_plan_generation")
    def optimized_app_plan_generation(self, idea: str) -> Dict[str, Any]:
        """Optimized app plan generation with caching"""
        return self.ai_orchestrator.generate_app_plan(idea)

    @cache_result(ttl=7200)  # Cache for 2 hours
    @monitor_performance("code_generation")
    def optimized_code_generation(self, app_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Optimized code generation with caching"""
        return self.ai_orchestrator.generate_code(app_plan)

    @monitor_performance("plugin_operation")
    def optimized_plugin_operation(
        self, plugin_name: str, operation: str, **kwargs
    ) -> Dict[str, Any]:
        """Optimized plugin operations with monitoring"""
        # Import plugin manager dynamically to avoid circular imports
        from .plugin_manager import PluginManager

        plugin_manager = PluginManager()

        if operation == "install":
            return plugin_manager.install_plugin(plugin_name)
        elif operation == "uninstall":
            return plugin_manager.uninstall_plugin(plugin_name)
        elif operation == "list":
            return plugin_manager.list_plugins()
        elif operation == "search":
            return plugin_manager.search_plugins(kwargs.get("query", ""))
        else:
            raise ValueError(f"Unknown plugin operation: {operation}")

    @monitor_performance("collaboration_operation")
    def optimized_collaboration_operation(
        self, operation: str, **kwargs
    ) -> Dict[str, Any]:
        """Optimized collaboration operations with monitoring"""
        # Import collaboration platform dynamically
        from .collaboration_platform import CollaborationPlatform

        collaboration_platform = CollaborationPlatform()

        if operation == "create_project":
            return collaboration_platform.create_collaborative_project(
                kwargs.get("name"), kwargs.get("description"), kwargs.get("owner_id")
            )
        elif operation == "invite_user":
            return collaboration_platform.invite_to_project(
                kwargs.get("project_id"), kwargs.get("email"), kwargs.get("role")
            )
        elif operation == "get_status":
            return collaboration_platform.get_project_status(kwargs.get("project_id"))
        else:
            raise ValueError(f"Unknown collaboration operation: {operation}")

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        # Get performance optimizer report
        optimizer_report = self.performance_optimizer.get_performance_report()

        # Get monitoring dashboard metrics
        dashboard_metrics = self.monitoring_dashboard.get_dashboard_data()

        # Get cache statistics
        cache_stats = self.performance_optimizer.redis_cache.get_stats()

        # Calculate performance score
        performance_score = self._calculate_performance_score(
            optimizer_report, dashboard_metrics, cache_stats
        )

        return {
            "performance_score": performance_score,
            "optimizer_report": optimizer_report,
            "dashboard_metrics": dashboard_metrics,
            "cache_performance": cache_stats,
            "recommendations": self._generate_performance_recommendations(
                optimizer_report, dashboard_metrics, cache_stats
            ),
        }

    def _calculate_performance_score(
        self,
        optimizer_report: Dict[str, Any],
        dashboard_metrics: Dict[str, Any],
        cache_stats: Dict[str, Any],
    ) -> int:
        """Calculate overall performance score (0-100)"""
        score = 100

        # Deduct based on response times
        if "summary" in optimizer_report:
            avg_duration = optimizer_report["summary"].get("avg_duration_ms", 0)
            if avg_duration > 2000:  # More than 2 seconds
                score -= 30
            elif avg_duration > 1000:  # More than 1 second
                score -= 15
            elif avg_duration > 500:  # More than 500ms
                score -= 5

        # Deduct based on cache hit rate
        hit_rate = cache_stats.get("hit_rate", 0)
        if hit_rate < 0.5:
            score -= 20
        elif hit_rate < 0.7:
            score -= 10

        # Deduct based on system metrics
        if "system_metrics" in optimizer_report:
            memory_percent = optimizer_report["system_metrics"].get("memory_percent", 0)
            cpu_percent = optimizer_report["system_metrics"].get("cpu_percent", 0)

            if memory_percent > 90:
                score -= 20
            elif memory_percent > 80:
                score -= 10

            if cpu_percent > 90:
                score -= 20
            elif cpu_percent > 80:
                score -= 10

        return max(0, score)

    def _generate_performance_recommendations(
        self,
        optimizer_report: Dict[str, Any],
        dashboard_metrics: Dict[str, Any],
        cache_stats: Dict[str, Any],
    ) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        # Response time recommendations
        if "summary" in optimizer_report:
            avg_duration = optimizer_report["summary"].get("avg_duration_ms", 0)
            if avg_duration > 1000:
                recommendations.append(
                    "🚀 **High response times detected** - Consider implementing caching for slow operations"
                )
                recommendations.append(
                    "⚡ **Optimize database queries** - Review query performance and add indexes"
                )

        # Cache recommendations
        hit_rate = cache_stats.get("hit_rate", 0)
        if hit_rate < 0.7:
            recommendations.append(
                "🔄 **Low cache hit rate** - Increase cache TTL or implement more aggressive caching"
            )

        # System resource recommendations
        if "system_metrics" in optimizer_report:
            memory_percent = optimizer_report["system_metrics"].get("memory_percent", 0)
            cpu_percent = optimizer_report["system_metrics"].get("cpu_percent", 0)

            if memory_percent > 80:
                recommendations.append(
                    "💾 **High memory usage** - Consider memory optimization or scaling"
                )

            if cpu_percent > 80:
                recommendations.append(
                    "🖥️ **High CPU usage** - Consider async operations or horizontal scaling"
                )

        # General recommendations
        recommendations.extend(
            [
                "📊 **Monitor performance metrics** - Set up alerts for performance degradation",
                "🔧 **Regular optimization** - Run performance optimization regularly",
                "⚡ **Consider CDN** - For static assets and API responses",
                "🔄 **Implement connection pooling** - For database connections",
            ]
        )

        return recommendations

    def run_performance_audit(self) -> Dict[str, Any]:
        """Run comprehensive performance audit"""
        audit_results = {
            "timestamp": time.time(),
            "performance_score": 0,
            "optimizations_applied": [],
            "issues_found": [],
            "recommendations": [],
            "metrics": {},
        }

        try:
            # Run full optimization
            optimization_results = self.performance_optimizer.run_full_optimization()
            audit_results["optimizations_applied"] = optimization_results.get(
                "performance_improvements", []
            )

            # Get performance summary
            performance_summary = self.get_performance_summary()
            audit_results["performance_score"] = performance_summary[
                "performance_score"
            ]
            audit_results["recommendations"] = performance_summary["recommendations"]
            audit_results["metrics"] = performance_summary["optimizer_report"]

            # Identify issues
            if performance_summary["performance_score"] < 70:
                audit_results["issues_found"].append(
                    "Low performance score - optimization needed"
                )

            cache_stats = performance_summary["cache_performance"]
            if cache_stats.get("hit_rate", 0) < 0.5:
                audit_results["issues_found"].append(
                    "Low cache hit rate - caching strategy needs improvement"
                )

            if "system_metrics" in performance_summary["optimizer_report"]:
                system_metrics = performance_summary["optimizer_report"][
                    "system_metrics"
                ]
                if system_metrics.get("memory_percent", 0) > 80:
                    audit_results["issues_found"].append("High memory usage detected")
                if system_metrics.get("cpu_percent", 0) > 80:
                    audit_results["issues_found"].append("High CPU usage detected")

        except Exception as e:
            audit_results["issues_found"].append(f"Performance audit error: {e}")
            logging.error(f"Performance audit failed: {e}")

        return audit_results

    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report"""
        audit_results = self.run_performance_audit()

        report = []
        report.append("# ⚡ AutoDevCore Performance Report")
        report.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(
            f"**Performance Score:** {audit_results['performance_score']}/100"
        )
        report.append("")

        # Performance Score
        score = audit_results["performance_score"]
        if score >= 90:
            report.append("## 🟢 Excellent Performance")
        elif score >= 80:
            report.append("## 🟡 Good Performance")
        elif score >= 70:
            report.append("## 🟠 Fair Performance")
        else:
            report.append("## 🔴 Poor Performance")

        report.append(f"**Overall Score:** {score}/100")
        report.append("")

        # Metrics Summary
        if "metrics" in audit_results and "summary" in audit_results["metrics"]:
            metrics = audit_results["metrics"]["summary"]
            report.append("## 📊 Performance Metrics")
            report.append(
                f"- **Total Operations:** {metrics.get('total_operations', 0):,}"
            )
            report.append(
                f"- **Average Response Time:** {metrics.get('avg_duration_ms', 0):.2f}ms"
            )
            report.append(
                f"- **Average Memory Usage:** {metrics.get('avg_memory_mb', 0):.2f}MB"
            )
            report.append(
                f"- **Average CPU Usage:** {metrics.get('avg_cpu_percent', 0):.2f}%"
            )
            report.append("")

        # Cache Performance
        if (
            "metrics" in audit_results
            and "cache_performance" in audit_results["metrics"]
        ):
            cache_stats = audit_results["metrics"]["cache_performance"]
            report.append("## 🔄 Cache Performance")
            report.append(f"- **Hit Rate:** {cache_stats.get('hit_rate', 0):.2%}")
            report.append(
                f"- **Total Operations:** {cache_stats.get('total_operations', 0):,}"
            )
            report.append(f"- **Hits:** {cache_stats.get('hits', 0):,}")
            report.append(f"- **Misses:** {cache_stats.get('misses', 0):,}")
            report.append("")

        # Issues Found
        if audit_results["issues_found"]:
            report.append("## ⚠️ Issues Found")
            for issue in audit_results["issues_found"]:
                report.append(f"- {issue}")
            report.append("")

        # Optimizations Applied
        if audit_results["optimizations_applied"]:
            report.append("## ✅ Optimizations Applied")
            for optimization in audit_results["optimizations_applied"]:
                report.append(f"- {optimization}")
            report.append("")

        # Recommendations
        if audit_results["recommendations"]:
            report.append("## 💡 Recommendations")
            for recommendation in audit_results["recommendations"]:
                report.append(f"- {recommendation}")
            report.append("")

        return "\n".join(report)


# Global performance integration instance
performance_integration = PerformanceIntegration()


if __name__ == "__main__":
    # Run performance audit and generate report
    print("⚡ Running AutoDevCore Performance Audit...")

    integration = PerformanceIntegration()
    report = integration.generate_performance_report()

    # Save report
    with open("PERFORMANCE_REPORT.md", "w") as f:
        f.write(report)

    print("✅ Performance audit complete!")
    print("📄 Report saved to: PERFORMANCE_REPORT.md")

    # Print summary
    summary = integration.get_performance_summary()
    print(f"\n📊 Performance Score: {summary['performance_score']}/100")
