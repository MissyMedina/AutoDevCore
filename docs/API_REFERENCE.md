# 🔌 AutoDevCore API Reference

## Overview

AutoDevCore provides a comprehensive REST API for programmatic access to all features. This reference documents all available endpoints, request/response formats, and authentication methods.

## Base URL

```
https://api.autodevcore.com/v1
```

## Authentication

AutoDevCore uses JWT (JSON Web Tokens) for authentication.

### Getting an Access Token

```bash
curl -X POST https://api.autodevcore.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "developer"
  }
}
```

### Using the Access Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://api.autodevcore.com/v1/applications
```

## Endpoints

### Applications

#### Generate Application

**POST** `/applications/generate`

Generate a new application from an idea.

**Request Body:**
```json
{
  "idea": "Task management system with user authentication",
  "complexity": "medium",
  "framework": "fastapi",
  "features": ["authentication", "database", "api"],
  "customizations": {
    "theme": "dark",
    "database": "postgresql"
  }
}
```

**Response:**
```json
{
  "id": "app_123",
  "status": "generating",
  "progress": 0,
  "estimated_completion": "2024-01-15T10:30:00Z",
  "webhook_url": "https://your-domain.com/webhooks/app_123"
}
```

#### Get Application Status

**GET** `/applications/{app_id}`

Get the current status of an application generation.

**Response:**
```json
{
  "id": "app_123",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:25:00Z",
  "download_url": "https://api.autodevcore.com/v1/applications/app_123/download",
  "preview_url": "https://api.autodevcore.com/v1/applications/app_123/preview",
  "metadata": {
    "framework": "fastapi",
    "complexity": "medium",
    "features": ["authentication", "database", "api"],
    "file_count": 45,
    "total_lines": 1250
  }
}
```

#### List Applications

**GET** `/applications`

List all applications for the authenticated user.

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20)
- `status` (string): Filter by status (generating, completed, failed)
- `framework` (string): Filter by framework
- `complexity` (string): Filter by complexity

**Response:**
```json
{
  "applications": [
    {
      "id": "app_123",
      "name": "Task Management System",
      "status": "completed",
      "framework": "fastapi",
      "complexity": "medium",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:25:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

#### Download Application

**GET** `/applications/{app_id}/download`

Download the generated application as a ZIP file.

**Response:** Binary ZIP file

#### Delete Application

**DELETE** `/applications/{app_id}`

Delete an application and all associated files.

**Response:**
```json
{
  "success": true,
  "message": "Application deleted successfully"
}
```

### AI Operations

#### Generate Code

**POST** `/ai/generate-code`

Generate code using AI models.

**Request Body:**
```json
{
  "prompt": "Create a FastAPI endpoint for user registration",
  "language": "python",
  "framework": "fastapi",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "code": "from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass UserCreate(BaseModel):\n    email: str\n    password: str\n    name: str\n\n@app.post(\"/users/register\")\nasync def register_user(user: UserCreate):\n    # Implementation here\n    return {\"message\": \"User registered successfully\"}",
  "language": "python",
  "model_used": "gpt-4",
  "tokens_used": 150,
  "execution_time": 2.5
}
```

#### Analyze Code

**POST** `/ai/analyze-code`

Analyze code quality and provide recommendations.

**Request Body:**
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "analysis_type": "performance"
}
```

**Response:**
```json
{
  "quality_score": 75,
  "analysis": {
    "performance": {
      "issues": ["Exponential time complexity"],
      "recommendations": ["Use memoization or iterative approach"]
    },
    "security": {
      "issues": [],
      "recommendations": []
    },
    "style": {
      "issues": [],
      "recommendations": ["Add type hints"]
    }
  },
  "suggestions": [
    "Consider using @lru_cache for memoization",
    "Add input validation for negative numbers"
  ]
}
```

#### Generate Documentation

**POST** `/ai/generate-docs`

Generate documentation for code.

**Request Body:**
```json
{
  "code": "def calculate_fibonacci(n):\n    return n if n <= 1 else calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
  "language": "python",
  "doc_type": "docstring"
}
```

**Response:**
```json
{
  "documentation": "def calculate_fibonacci(n):\n    \"\"\"\n    Calculate the nth Fibonacci number.\n    \n    Args:\n        n (int): The position in the Fibonacci sequence (0-indexed)\n    \n    Returns:\n        int: The nth Fibonacci number\n    \n    Raises:\n        RecursionError: If n is too large for recursive calculation\n    \n    Example:\n        >>> calculate_fibonacci(10)\n        55\n    \"\"\"\n    return n if n <= 1 else calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
  "doc_type": "docstring",
  "language": "python"
}
```

### Plugins

#### List Plugins

**GET** `/plugins`

List all available plugins.

**Response:**
```json
{
  "plugins": [
    {
      "id": "collaboration_platform",
      "name": "Collaboration Platform",
      "version": "1.0.0",
      "description": "Real-time collaboration features",
      "author": "AutoDevCore Team",
      "installed": true,
      "enabled": true,
      "dependencies": ["websockets", "redis"]
    }
  ]
}
```

#### Install Plugin

**POST** `/plugins/install`

Install a plugin.

**Request Body:**
```json
{
  "plugin_id": "collaboration_platform",
  "version": "1.0.0"
}
```

**Response:**
```json
{
  "success": true,
  "plugin": {
    "id": "collaboration_platform",
    "name": "Collaboration Platform",
    "version": "1.0.0",
    "installed": true,
    "enabled": true
  }
}
```

#### Uninstall Plugin

**DELETE** `/plugins/{plugin_id}`

Uninstall a plugin.

**Response:**
```json
{
  "success": true,
  "message": "Plugin uninstalled successfully"
}
```

#### Execute Plugin Operation

**POST** `/plugins/{plugin_id}/execute`

Execute a plugin operation.

**Request Body:**
```json
{
  "operation": "create_project",
  "parameters": {
    "name": "My Project",
    "description": "A collaborative project"
  }
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "project_id": "proj_123",
    "name": "My Project",
    "status": "created"
  }
}
```

### Collaboration

#### Create Project

**POST** `/collaboration/projects`

Create a new collaborative project.

**Request Body:**
```json
{
  "name": "Team Project",
  "description": "A collaborative development project",
  "visibility": "team",
  "settings": {
    "allow_guest_access": false,
    "require_approval": true
  }
}
```

**Response:**
```json
{
  "id": "proj_123",
  "name": "Team Project",
  "description": "A collaborative development project",
  "owner_id": "user123",
  "created_at": "2024-01-15T10:00:00Z",
  "workspace_url": "https://collab.autodevcore.com/proj_123",
  "invite_code": "ABC123"
}
```

#### Invite User

**POST** `/collaboration/projects/{project_id}/invite`

Invite a user to a project.

**Request Body:**
```json
{
  "email": "teammate@example.com",
  "role": "editor",
  "message": "Join our collaborative project!"
}
```

**Response:**
```json
{
  "invitation_id": "inv_123",
  "email": "teammate@example.com",
  "role": "editor",
  "status": "pending",
  "expires_at": "2024-01-22T10:00:00Z"
}
```

#### Get Project Status

**GET** `/collaboration/projects/{project_id}`

Get project status and member information.

**Response:**
```json
{
  "id": "proj_123",
  "name": "Team Project",
  "description": "A collaborative development project",
  "owner_id": "user123",
  "created_at": "2024-01-15T10:00:00Z",
  "members": [
    {
      "user_id": "user123",
      "email": "owner@example.com",
      "role": "owner",
      "joined_at": "2024-01-15T10:00:00Z",
      "last_active": "2024-01-15T12:30:00Z"
    }
  ],
  "files": [
    {
      "id": "file_123",
      "name": "main.py",
      "type": "python",
      "size": 1024,
      "last_modified": "2024-01-15T12:30:00Z"
    }
  ],
  "activity": [
    {
      "type": "file_edit",
      "user_id": "user123",
      "file_id": "file_123",
      "timestamp": "2024-01-15T12:30:00Z"
    }
  ]
}
```

### Performance

#### Get Performance Metrics

**GET** `/performance/metrics`

Get current performance metrics.

**Response:**
```json
{
  "system": {
    "cpu_percent": 45.2,
    "memory_percent": 67.8,
    "disk_usage_percent": 23.1,
    "network_io": {
      "bytes_sent": 1024000,
      "bytes_recv": 2048000
    }
  },
  "application": {
    "requests_per_second": 150.5,
    "average_response_time": 245.3,
    "error_rate": 0.02,
    "active_connections": 25
  },
  "cache": {
    "hit_rate": 0.85,
    "total_operations": 15000,
    "memory_usage": "256MB"
  },
  "database": {
    "active_connections": 5,
    "slow_queries": 2,
    "query_time_avg": 12.5
  }
}
```

#### Run Performance Audit

**POST** `/performance/audit`

Run a comprehensive performance audit.

**Request Body:**
```json
{
  "include_cache_analysis": true,
  "include_database_analysis": true,
  "include_memory_analysis": true,
  "include_cpu_analysis": true
}
```

**Response:**
```json
{
  "performance_score": 85,
  "audit_timestamp": "2024-01-15T12:00:00Z",
  "optimizations_applied": [
    "Database indexes created",
    "Cache TTL optimized",
    "Memory garbage collection performed"
  ],
  "issues_found": [
    {
      "severity": "medium",
      "category": "database",
      "description": "Missing index on users.email column",
      "recommendation": "Create index on users.email for faster lookups"
    }
  ],
  "recommendations": [
    "Consider implementing connection pooling",
    "Monitor cache hit rate and adjust TTL",
    "Review slow database queries"
  ]
}
```

### Security

#### Run Security Audit

**POST** `/security/audit`

Run a comprehensive security audit.

**Request Body:**
```json
{
  "include_code_analysis": true,
  "include_dependency_scan": true,
  "include_configuration_audit": true
}
```

**Response:**
```json
{
  "security_score": 80,
  "audit_timestamp": "2024-01-15T12:00:00Z",
  "critical_issues": [],
  "high_issues": [
    {
      "title": "Missing input validation",
      "description": "User input not properly validated",
      "file": "routes.py",
      "line": 45,
      "recommendation": "Implement comprehensive input validation"
    }
  ],
  "medium_issues": [
    {
      "title": "Outdated dependency",
      "description": "requests library version 2.25.0 has known vulnerabilities",
      "recommendation": "Update to requests 2.31.0 or later"
    }
  ],
  "low_issues": [],
  "recommendations": [
    "Implement comprehensive input validation",
    "Update outdated dependencies",
    "Enable security headers"
  ]
}
```

#### Get Security Report

**GET** `/security/report`

Get a detailed security report.

**Response:**
```json
{
  "overall_score": 80,
  "last_audit": "2024-01-15T12:00:00Z",
  "vulnerabilities": {
    "critical": 0,
    "high": 2,
    "medium": 1,
    "low": 0
  },
  "compliance": {
    "owasp_top_10": {
      "a01_broken_access_control": "pass",
      "a02_cryptographic_failures": "pass",
      "a03_injection": "warning",
      "a04_insecure_design": "pass",
      "a05_security_misconfiguration": "pass"
    }
  },
  "dependencies": {
    "total": 45,
    "vulnerable": 1,
    "outdated": 3
  }
}
```

### Monitoring

#### Get System Health

**GET** `/monitoring/health`

Get overall system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "services": {
    "api": {
      "status": "healthy",
      "response_time": 45.2,
      "uptime": "99.9%"
    },
    "database": {
      "status": "healthy",
      "connections": 5,
      "uptime": "99.8%"
    },
    "cache": {
      "status": "healthy",
      "hit_rate": 0.85,
      "uptime": "99.9%"
    },
    "ai_models": {
      "status": "healthy",
      "models_available": 4,
      "response_time": 1200.5
    }
  },
  "alerts": []
}
```

#### Set Alert

**POST** `/monitoring/alerts`

Create a new monitoring alert.

**Request Body:**
```json
{
  "name": "High CPU Alert",
  "condition": "cpu_percent > 80",
  "duration": "5m",
  "action": "send_notification",
  "notification": {
    "email": "admin@example.com",
    "webhook": "https://your-domain.com/webhooks/alerts"
  }
}
```

**Response:**
```json
{
  "alert_id": "alert_123",
  "name": "High CPU Alert",
  "status": "active",
  "created_at": "2024-01-15T12:00:00Z"
}
```

## Error Handling

### Error Response Format

All API errors follow a consistent format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "idea",
      "issue": "Required field is missing"
    },
    "timestamp": "2024-01-15T12:00:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTHENTICATION_ERROR` | 401 | Invalid or missing authentication |
| `AUTHORIZATION_ERROR` | 403 | Insufficient permissions |
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

### Rate Limiting

API requests are rate-limited to ensure fair usage:

- **Free Tier:** 100 requests per hour
- **Pro Tier:** 1,000 requests per hour
- **Enterprise Tier:** 10,000 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642248000
```

## Webhooks

### Webhook Events

AutoDevCore can send webhook notifications for various events:

- `application.completed` - Application generation completed
- `application.failed` - Application generation failed
- `plugin.installed` - Plugin installed successfully
- `security.alert` - Security vulnerability detected
- `performance.alert` - Performance threshold exceeded

### Webhook Format

```json
{
  "event": "application.completed",
  "timestamp": "2024-01-15T12:00:00Z",
  "data": {
    "application_id": "app_123",
    "status": "completed",
    "download_url": "https://api.autodevcore.com/v1/applications/app_123/download"
  }
}
```

### Setting Up Webhooks

```bash
curl -X POST https://api.autodevcore.com/v1/webhooks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhooks",
    "events": ["application.completed", "security.alert"],
    "secret": "your_webhook_secret"
  }'
```

## SDKs and Libraries

### Python SDK

```bash
pip install autodevcore-sdk
```

```python
from autodevcore import AutoDevCore

client = AutoDevCore(api_key="your_api_key")

# Generate an application
app = client.applications.generate(
    idea="Task management system",
    complexity="medium",
    framework="fastapi"
)

# Check status
status = client.applications.get_status(app.id)
```

### JavaScript SDK

```bash
npm install autodevcore-sdk
```

```javascript
const AutoDevCore = require('autodevcore-sdk');

const client = new AutoDevCore({ apiKey: 'your_api_key' });

// Generate an application
const app = await client.applications.generate({
  idea: 'Task management system',
  complexity: 'medium',
  framework: 'fastapi'
});

// Check status
const status = await client.applications.getStatus(app.id);
```

## Support

For API support and questions:

- **Documentation:** https://docs.autodevcore.com/api
- **GitHub Issues:** https://github.com/your-org/autodevcore/issues
- **Email Support:** api-support@autodevcore.com
- **Discord Community:** https://discord.gg/autodevcore

---

*This API reference is updated regularly. Check our [changelog](https://docs.autodevcore.com/changelog) for the latest updates.*
