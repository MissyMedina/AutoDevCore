# 📊 AutoDevCore Metrics Package

## 🏗️ **Architecture Overview**

The metrics system is organized into two main components:

### **1. `metrics/` - Monitoring Code Package**
```
metrics/
├── __init__.py              # Package initialization and unified API
├── api.py                   # High-level metrics API
├── config.py                # Configuration and thresholds
├── storage.py               # Unified data storage management
├── performance.py           # Core performance monitoring
├── performance_monitor.py   # Legacy performance monitor
├── monitoring_dashboard.py  # Enterprise monitoring dashboard
├── performance_optimizer.py # Performance optimization tools
└── performance_integration.py # Integration with other systems
```

### **2. `logs/metrics/` - Data Storage Location**
```
logs/metrics/
├── metrics.db               # SQLite database for structured metrics
├── performance.json         # Performance operation data
├── system.json             # System metrics data
├── alerts.json             # Alert configurations and history
└── health.json             # Health check results
```

## 🔄 **Data Flow**

```
Application Code
       ↓
   Metrics API
       ↓
   Unified Storage
       ↓
   logs/metrics/
   ├── metrics.db (SQLite)
   └── *.json files
```

## 🚀 **Quick Start**

### **Basic Usage:**
```python
from metrics import MetricsAPI, record_metric, get_system_metrics

# Get the API
api = MetricsAPI()

# Record a custom metric
result = record_metric('user_login', 1.0, {'user_id': '123'})

# Get system metrics
system_metrics = get_system_metrics()

# Start comprehensive monitoring
monitoring_result = api.start_monitoring()
```

### **Storage Operations:**
```python
from metrics import get_storage

storage = get_storage()

# Store a metric
storage.store_metric('cpu_usage', 75.5, {'server': 'web-01'})

# Get metrics history
metrics = storage.get_metrics('cpu_usage', hours=24)

# Store an alert
storage.store_alert('High CPU', 'warning', 'CPU usage is high')

# Get health status
health = storage.get_health_status()
```

## 📊 **Available Metrics**

### **System Metrics:**
- **CPU Usage** - Real-time CPU monitoring
- **Memory Usage** - Memory consumption tracking
- **Disk Usage** - Storage monitoring
- **Network I/O** - Network performance

### **Application Metrics:**
- **Response Times** - API and operation timing
- **Error Rates** - Error tracking and alerting
- **Throughput** - Request/operation counts
- **Custom Metrics** - User-defined metrics

### **Performance Metrics:**
- **Operation Timing** - Detailed performance analysis
- **Resource Utilization** - System resource tracking
- **Performance Trends** - Historical performance data

## ⚙️ **Configuration**

### **Alert Thresholds:**
```python
from metrics.config import get_thresholds

thresholds = get_thresholds()
# {
#   'cpu_usage': {'warning': 70.0, 'critical': 90.0},
#   'memory_usage': {'warning': 80.0, 'critical': 95.0},
#   'response_time': {'warning': 2.0, 'critical': 5.0}
# }
```

### **Storage Configuration:**
```python
from metrics.config import get_config

config = get_config()
# {
#   'retention_days': 30,
#   'collection_interval': 60,
#   'database_path': 'logs/metrics.db'
# }
```

## 🔍 **Monitoring Dashboard**

### **Features:**
- **Real-time Metrics** - Live system monitoring
- **Performance Analytics** - Detailed performance analysis
- **Alert Management** - Configurable alert system
- **Health Monitoring** - System health checks
- **Data Export** - JSON, CSV export capabilities

### **Access:**
```python
from metrics import MonitoringDashboard

dashboard = MonitoringDashboard()
dashboard.start()  # Start the dashboard
```

## 📈 **Data Storage**

### **SQLite Database (`logs/metrics/metrics.db`):**
- **metrics** - Main metrics table
- **performance_ops** - Performance operations
- **alerts** - Alert history
- **health_checks** - Health check results

### **JSON Files:**
- **performance.json** - Performance operation data
- **system.json** - System metrics data
- **alerts.json** - Alert configurations
- **health.json** - Health check results

## 🧹 **Data Management**

### **Cleanup:**
```python
from metrics import get_storage

storage = get_storage()
storage.cleanup_old_data(days=30)  # Clean up old data
```

### **Export:**
```python
from metrics import get_storage

storage = get_storage()
data = storage.export_data(format='json', hours=24)
```

## 🔧 **Integration**

### **With AutoDevCore:**
```python
# In your application code
from metrics import record_metric

def process_request():
    record_metric('requests_total', 1.0)
    # ... process request
    record_metric('request_duration', 0.5)
```

### **With External Systems:**
```python
from metrics import MetricsAPI

api = MetricsAPI()
# Export metrics for external monitoring systems
export_data = api.export_metrics(format='json', hours=24)
```

## 📋 **API Reference**

### **Core Functions:**
- `record_metric(name, value, labels)` - Record a metric
- `get_system_metrics()` - Get current system metrics
- `start_monitoring()` - Start comprehensive monitoring
- `get_storage()` - Get storage instance

### **Storage Methods:**
- `store_metric()` - Store a metric
- `get_metrics()` - Retrieve metrics
- `store_alert()` - Store an alert
- `get_health_status()` - Get health status
- `export_data()` - Export data

## 🎯 **Best Practices**

1. **Use Descriptive Metric Names** - Clear, consistent naming
2. **Add Labels** - Include relevant context
3. **Set Appropriate Thresholds** - Configure meaningful alerts
4. **Regular Cleanup** - Clean up old data periodically
5. **Monitor Storage** - Watch database size and performance

## 🚨 **Troubleshooting**

### **Common Issues:**
- **Database Locked** - Check for concurrent access
- **Storage Full** - Clean up old data
- **Import Errors** - Check Python path and dependencies

### **Debug Mode:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
from metrics import MetricsAPI
```

## 📚 **Examples**

See the `examples/` directory for complete usage examples and integration patterns.
