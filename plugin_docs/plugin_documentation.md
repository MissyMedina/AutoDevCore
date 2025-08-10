# AutoDevCore Plugin Documentation

## Overview

This document provides comprehensive documentation for all available AutoDevCore plugins.

## Plugin Development Guide

### Creating a Plugin

1. Create a Python file in the `plugins/` directory
2. Implement a `run(context)` function
3. Add metadata (optional): `__author__`, `__version__`, `__description__`
4. Test your plugin with `python cli.py --mode plugin --name your_plugin`

### Plugin Template

```python
"""
Your Plugin Description
"""

__author__ = "Your Name"
__version__ = "1.0.0"
__description__ = "What your plugin does"

def run(context):
    """
    Main plugin function.
    
    Args:
        context (dict): Execution context with plugin_name, output_dir, verbose
    
    Returns:
        Any: Plugin execution result
    """
    # Your plugin logic here
    return {'status': 'success', 'message': 'Plugin executed'}
```

## Available Plugins

### security_scanner

**Description**: Scans code for common security vulnerabilities and provides remediation advice

**Author**: AutoDevCore Team

**Version**: 1.0.0

**Status**: ✅ Ready

**Functions**:
- `run`

---

### code_analyzer

**Description**: Analyzes code complexity, quality metrics, and provides recommendations

**Author**: AutoDevCore Team

**Version**: 1.0.0

**Status**: ✅ Ready

**Functions**:
- `run`
- `calculate_complexity`

---

### ascii_weather

**Description**: 
ASCII Weather Plugin for AutoDevCore
A simple plugin that generates ASCII weather art


**Author**: Unknown

**Version**: 1.0.0

**Status**: ✅ Ready

**Functions**:
- `run`
- `_get_weather_ascii`

---

