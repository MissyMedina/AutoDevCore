# AutoDevCore Deployment Guide 🚀

## Overview

This guide covers deploying AutoDevCore in various environments, from local development to production.

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   AutoDevCore   │    │   Redis Cache   │
│   (Load Balancer)│    │   Application   │    │   & Sessions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SSL/TLS       │    │   PostgreSQL    │    │   Monitoring    │
│   Termination   │    │   Database      │    │   Stack         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start (Development)**

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd OpnAI_Hackathon
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start Development Environment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f autodevcore

# Access application
open http://localhost:8000
```

## 🏭 **Production Deployment**

### Option 1: Docker Compose (Recommended)

#### 1. Production Configuration
```bash
# Create production environment file
cp .env.example .env.production

# Configure production settings
nano .env.production
```

#### 2. Start Production Stack
```bash
# Start with production profile
docker-compose --env-file .env.production -f docker-compose.yml --profile production up -d

# Start with monitoring
docker-compose --env-file .env.production -f docker-compose.yml --profile production,monitoring up -d
```

#### 3. SSL Configuration
```bash
# Generate SSL certificates
mkdir ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/nginx.key -out ssl/nginx.crt
```

### Option 2: Kubernetes Deployment

#### 1. Create Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: autodevcore
```

#### 2. Deploy Application
```bash
kubectl apply -f k8s/
```

#### 3. Access Application
```bash
kubectl port-forward svc/autodevcore 8000:8000 -n autodevcore
```

## 🔧 **Configuration**

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Environment (development/production) | development | Yes |
| `DEBUG` | Debug mode | True | No |
| `SECRET_KEY` | Application secret key | auto-generated | Yes |
| `DATABASE_URL` | Database connection string | sqlite:///data/app.db | No |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 | No |
| `OPENAI_API_KEY` | OpenAI API key | None | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | None | No |

### Database Configuration

#### SQLite (Development)
```bash
# Default configuration
DATABASE_URL=sqlite:///data/app.db
```

#### PostgreSQL (Production)
```bash
# PostgreSQL configuration
DATABASE_URL=postgresql://user:password@localhost:5432/autodevcore
```

### Redis Configuration
```bash
# Redis for caching and sessions
REDIS_URL=redis://localhost:6379/0
```

## 📊 **Monitoring & Observability**

### 1. Prometheus Metrics
```bash
# Access Prometheus
open http://localhost:9090

# View AutoDevCore metrics
# - Request rates
# - Response times
# - Error rates
# - AI model performance
```

### 2. Grafana Dashboards
```bash
# Access Grafana
open http://localhost:3000
# Username: admin
# Password: admin

# Pre-configured dashboards:
# - AutoDevCore Overview
# - AI Performance Metrics
# - Collaboration Analytics
# - System Health
```

### 3. Application Logs
```bash
# View application logs
docker-compose logs -f autodevcore

# View structured logs
tail -f logs/app.log | jq
```

## 🔒 **Security Configuration**

### 1. SSL/TLS Setup
```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/nginx.key -out ssl/nginx.crt

# Configure nginx
cp nginx.conf.example nginx.conf
```

### 2. Security Headers
```nginx
# nginx.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000" always;
```

### 3. Environment Security
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in environment
export SECRET_KEY="your-generated-secret-key"
```

## 🧪 **Testing & Quality Assurance**

### 1. Run Test Suite
```bash
# Run all tests
pytest tests/ -v --cov=plugins --cov=integrations --cov=agents

# Run specific test categories
pytest tests/test_collaboration_platform.py -v
pytest tests/test_ai_integration.py -v
```

### 2. Code Quality Checks
```bash
# Format code
black .
isort .

# Type checking
mypy plugins/ integrations/ agents/

# Security scan
bandit -r .
safety check
```

### 3. Performance Testing
```bash
# Load testing with Locust
locust -f tests/locustfile.py --host=http://localhost:8000

# Performance benchmarks
python tests/performance_benchmarks.py
```

## 🔄 **CI/CD Pipeline**

### GitHub Actions Workflow
The CI/CD pipeline automatically:
1. **Code Quality**: Formatting, type checking, security scanning
2. **Testing**: Unit tests, integration tests, performance tests
3. **Building**: Docker image creation and testing
4. **Deployment**: Staging and production deployment
5. **Verification**: Post-deployment health checks

### Manual Pipeline Execution
```bash
# Run pipeline locally
./scripts/run-pipeline.sh

# Deploy to staging
./scripts/deploy-staging.sh

# Deploy to production
./scripts/deploy-production.sh
```

## 📈 **Scaling & Performance**

### 1. Horizontal Scaling
```bash
# Scale application instances
docker-compose up -d --scale autodevcore=3

# Load balancer configuration
# Nginx automatically distributes traffic
```

### 2. Database Scaling
```bash
# PostgreSQL read replicas
docker-compose up -d postgres-replica

# Redis clustering
docker-compose up -d redis-cluster
```

### 3. Performance Optimization
```bash
# Enable caching
export ENABLE_CACHE=true

# Configure connection pooling
export DB_POOL_SIZE=20

# Enable compression
export ENABLE_COMPRESSION=true
```

## 🚨 **Troubleshooting**

### Common Issues

#### 1. Application Won't Start
```bash
# Check logs
docker-compose logs autodevcore

# Check environment variables
docker-compose exec autodevcore env

# Verify dependencies
docker-compose exec autodevcore python -c "import integrations.gpt_oss"
```

#### 2. Database Connection Issues
```bash
# Test database connection
docker-compose exec autodevcore python -c "
from sqlalchemy import create_engine
engine = create_engine('$DATABASE_URL')
print('Database connection:', engine.connect())
"
```

#### 3. Performance Issues
```bash
# Check resource usage
docker stats

# Monitor application metrics
curl http://localhost:8000/metrics

# Check cache hit rates
redis-cli info memory
```

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

## 📚 **Additional Resources**

- [AutoDevCore Documentation](docs/)
- [API Reference](docs/api.md)
- [Plugin Development Guide](docs/plugins.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## 🆘 **Support**

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Verify configuration
4. Contact the development team

---

**Deployment Guide Version**: 1.0.0
**Last Updated**: 2025-08-10
**AutoDevCore Version**: v1.0.0
