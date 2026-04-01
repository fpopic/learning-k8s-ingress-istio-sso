# Use a specific, stable base image
FROM python:3.9-slim-bookworm

# Set environment variables
# 1. Prevent Python from writing .pyc files
# 2. Force stdout/stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=80

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser /app
USER appuser

# Copy application code from src
COPY src/ .

# Inform Docker that the container listens on the specified port at runtime
EXPOSE 80

# Use a signal-aware start command (module path changed to main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
