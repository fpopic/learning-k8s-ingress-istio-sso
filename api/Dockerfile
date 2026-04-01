# Use a specific, stable base image
FROM python:3.9-slim-bookworm

# Install uv (extremely fast Rust-based Python package installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
# 1. Prevent Python from writing .pyc files
# 2. Force stdout/stderr to be unbuffered
# 3. Compile Python bytecode to increase startup performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    PORT=80

WORKDIR /app

# Install dependencies using uv (much faster than pip)
# --system: Install into the container's system Python environment
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

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
