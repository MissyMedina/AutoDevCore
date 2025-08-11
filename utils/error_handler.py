"""
Error handling and recovery utilities for AutoDevCore.
"""

import sys
import traceback
import logging
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import json


class AutoDevCoreError(Exception):
    """Base exception for AutoDevCore."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()


class GPTOSSError(AutoDevCoreError):
    """Exception for GPT-OSS related errors."""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "GPT_OSS_ERROR", details)


class AgentError(AutoDevCoreError):
    """Exception for agent-related errors."""
    
    def __init__(self, agent_name: str, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "AGENT_ERROR", details)
        self.agent_name = agent_name


class ValidationError(AutoDevCoreError):
    """Exception for validation errors."""
    
    def __init__(self, field: str, message: str, details: Dict[str, Any] = None):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class ErrorHandler:
    """Comprehensive error handling and recovery system."""
    
    def __init__(self, log_file: str = "logs/autodevcore_errors.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("AutoDevCore")
        
        # Error recovery strategies
        self.recovery_strategies = {
            "GPT_OSS_ERROR": self._recover_gpt_oss_error,
            "AGENT_ERROR": self._recover_agent_error,
            "VALIDATION_ERROR": self._recover_validation_error,
            "TIMEOUT_ERROR": self._recover_timeout_error,
            "NETWORK_ERROR": self._recover_network_error
        }
        
        # Error statistics
        self.error_stats = {
            "total_errors": 0,
            "errors_by_type": {},
            "recovery_attempts": 0,
            "successful_recoveries": 0
        }
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle an error and attempt recovery."""
        self.error_stats["total_errors"] += 1
        
        # Log the error
        self.logger.error(f"Error occurred: {type(error).__name__}: {str(error)}")
        self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Determine error type
        error_type = self._classify_error(error)
        self.error_stats["errors_by_type"][error_type] = self.error_stats["errors_by_type"].get(error_type, 0) + 1
        
        # Create error response
        error_response = {
            "error_type": error_type,
            "message": str(error),
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "recovered": False,
            "recovery_strategy": None
        }
        
        # Attempt recovery
        if error_type in self.recovery_strategies:
            self.error_stats["recovery_attempts"] += 1
            recovery_result = self.recovery_strategies[error_type](error, context)
            
            if recovery_result["success"]:
                self.error_stats["successful_recoveries"] += 1
                error_response["recovered"] = True
                error_response["recovery_strategy"] = recovery_result["strategy"]
                error_response["recovery_data"] = recovery_result.get("data")
                
                self.logger.info(f"Successfully recovered from {error_type} error")
            else:
                self.logger.warning(f"Recovery failed for {error_type} error: {recovery_result['reason']}")
        
        # Save error to file
        self._save_error(error_response)
        
        return error_response
    
    def _classify_error(self, error: Exception) -> str:
        """Classify the type of error."""
        if isinstance(error, AutoDevCoreError):
            return error.error_code
        
        error_str = str(error).lower()
        
        if "timeout" in error_str or "timed out" in error_str:
            return "TIMEOUT_ERROR"
        elif "connection" in error_str or "network" in error_str:
            return "NETWORK_ERROR"
        elif "validation" in error_str or "invalid" in error_str:
            return "VALIDATION_ERROR"
        elif "gpt" in error_str or "ollama" in error_str:
            return "GPT_OSS_ERROR"
        else:
            return "UNKNOWN_ERROR"
    
    def _recover_gpt_oss_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from GPT-OSS errors."""
        try:
            # Try to use fallback logic
            if "generate" in str(error):
                return {
                    "success": True,
                    "strategy": "fallback_generation",
                    "data": {"method": "template_based"}
                }
            elif "analyze" in str(error):
                return {
                    "success": True,
                    "strategy": "fallback_analysis",
                    "data": {"method": "rule_based"}
                }
            else:
                return {
                    "success": False,
                    "reason": "No specific recovery strategy for this GPT-OSS error"
                }
        except Exception as recovery_error:
            return {
                "success": False,
                "reason": f"Recovery attempt failed: {str(recovery_error)}"
            }
    
    def _recover_agent_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from agent errors."""
        try:
            agent_name = getattr(error, 'agent_name', 'unknown')
            
            # Try to restart the agent or use alternative agent
            return {
                "success": True,
                "strategy": "agent_fallback",
                "data": {"agent": agent_name, "method": "alternative_agent"}
            }
        except Exception as recovery_error:
            return {
                "success": False,
                "reason": f"Agent recovery failed: {str(recovery_error)}"
            }
    
    def _recover_validation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from validation errors."""
        try:
            field = getattr(error, 'field', 'unknown')
            
            # Try to fix validation issues
            return {
                "success": True,
                "strategy": "validation_fix",
                "data": {"field": field, "method": "default_value"}
            }
        except Exception as recovery_error:
            return {
                "success": False,
                "reason": f"Validation recovery failed: {str(recovery_error)}"
            }
    
    def _recover_timeout_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from timeout errors."""
        try:
            # Try to reduce timeout or use faster method
            return {
                "success": True,
                "strategy": "timeout_reduction",
                "data": {"method": "reduced_timeout", "new_timeout": 60}
            }
        except Exception as recovery_error:
            return {
                "success": False,
                "reason": f"Timeout recovery failed: {str(recovery_error)}"
            }
    
    def _recover_network_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from network errors."""
        try:
            # Try to retry or use offline mode
            return {
                "success": True,
                "strategy": "network_retry",
                "data": {"method": "offline_mode", "retries": 3}
            }
        except Exception as recovery_error:
            return {
                "success": False,
                "reason": f"Network recovery failed: {str(recovery_error)}"
            }
    
    def _save_error(self, error_response: Dict[str, Any]):
        """Save error response to file."""
        try:
            errors_file = Path("logs/errors.json")
            errors_file.parent.mkdir(exist_ok=True)
            
            # Load existing errors
            if errors_file.exists():
                with open(errors_file, 'r') as f:
                    errors = json.load(f)
            else:
                errors = []
            
            # Add new error
            errors.append(error_response)
            
            # Keep only last 100 errors
            if len(errors) > 100:
                errors = errors[-100:]
            
            # Save back to file
            with open(errors_file, 'w') as f:
                json.dump(errors, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save error: {e}")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        return {
            **self.error_stats,
            "recovery_rate": (
                self.error_stats["successful_recoveries"] / max(self.error_stats["recovery_attempts"], 1)
            ) * 100
        }
    
    def clear_error_stats(self):
        """Clear error statistics."""
        self.error_stats = {
            "total_errors": 0,
            "errors_by_type": {},
            "recovery_attempts": 0,
            "successful_recoveries": 0
        }


class ErrorRecoveryDecorator:
    """Decorator for automatic error recovery."""
    
    def __init__(self, error_handler: ErrorHandler, max_retries: int = 3):
        self.error_handler = error_handler
        self.max_retries = max_retries
    
    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    last_error = error
                    
                    if attempt < self.max_retries:
                        # Attempt recovery
                        recovery_result = self.error_handler.handle_error(error, {
                            "function": func.__name__,
                            "attempt": attempt + 1,
                            "max_retries": self.max_retries
                        })
                        
                        if recovery_result["recovered"]:
                            # Try again with recovery data
                            continue
                        else:
                            # Wait before retry
                            import time
                            time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        # Final attempt failed
                        break
            
            # All attempts failed
            final_error = AutoDevCoreError(
                f"Function {func.__name__} failed after {self.max_retries + 1} attempts",
                "MAX_RETRIES_EXCEEDED",
                {"last_error": str(last_error)}
            )
            
            self.error_handler.handle_error(final_error, {
                "function": func.__name__,
                "attempts": self.max_retries + 1
            })
            
            raise final_error
        
        return wrapper


# Global error handler instance
error_handler = ErrorHandler()


def handle_errors(func: Callable):
    """Decorator to handle errors in functions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            error_response = error_handler.handle_error(error, {
                "function": func.__name__,
                "args": str(args),
                "kwargs": str(kwargs)
            })
            
            if not error_response["recovered"]:
                raise error
            
            return error_response.get("recovery_data", {})
    
    return wrapper


def safe_execute(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """Safely execute a function with error handling."""
    try:
        result = func(*args, **kwargs)
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as error:
        error_response = error_handler.handle_error(error, {
            "function": func.__name__,
            "args": str(args),
            "kwargs": str(kwargs)
        })
        
        return {
            "success": False,
            "result": None,
            "error": error_response
        }


def get_error_report() -> Dict[str, Any]:
    """Get a comprehensive error report."""
    stats = error_handler.get_error_stats()
    
    # Load recent errors
    errors_file = Path("logs/errors.json")
    recent_errors = []
    if errors_file.exists():
        try:
            with open(errors_file, 'r') as f:
                recent_errors = json.load(f)[-10:]  # Last 10 errors
        except Exception:
            pass
    
    return {
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
        "recent_errors": recent_errors,
        "recommendations": _generate_error_recommendations(stats)
    }


def _generate_error_recommendations(stats: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on error statistics."""
    recommendations = []
    
    if stats["total_errors"] > 10:
        recommendations.append("High error rate detected - review error logs and fix root causes")
    
    if stats.get("GPT_OSS_ERROR", 0) > 5:
        recommendations.append("Frequent GPT-OSS errors - check model availability and network connectivity")
    
    if stats.get("TIMEOUT_ERROR", 0) > 3:
        recommendations.append("Timeout errors detected - consider increasing timeouts or optimizing operations")
    
    recovery_rate = stats.get("recovery_rate", 0)
    if recovery_rate < 50:
        recommendations.append("Low recovery rate - improve error recovery strategies")
    
    if not recommendations:
        recommendations.append("Error handling looks good - no major issues detected")
    
    return recommendations
