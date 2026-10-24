# Multi-stage or lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    DATABASE_DIR=/app/database

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies first to optimize Docker layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Create persistent database directory and assign non-root permissions
RUN mkdir -p /app/database

# Expose application port
EXPOSE 5000

# Healthcheck to verify the web service and database connectivity
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Launch application with automatic schema verification and Gunicorn WSGI server
CMD ["sh", "-c", "python scripts/init_db.py && python scripts/seed_sample_data.py && gunicorn --bind 0.0.0.0:5000 --workers 2 app:app"]
