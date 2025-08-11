# AutoDevCore Docker Image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/teams output logs

# Set permissions
RUN chmod +x cli.py

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash autodev && \
    chown -R autodev:autodev /app
USER autodev

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from integrations.gpt_oss import gpt_oss_client; print('Health check: OK')" || exit 1

# Expose port for web interface (future)
EXPOSE 8000

# Default command
CMD ["python", "cli.py", "--help"]
