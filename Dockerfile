# ==========================================
# STAGE 1: Builder
# We use a builder stage to compile dependencies 
# and keep the final image lean by excluding 
# build tools (compilers, etc.)
# ==========================================
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
# This ensures logs are sent straight to the terminal without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install build dependencies if any C-extensions are needed 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching.
# If requirements.txt doesn't change, Docker skips the install step.
COPY requirements.txt .

# Install dependencies into a local folder ('/install')
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==========================================
# STAGE 2: Final Runtime
# ==========================================
FROM python:3.12-slim

# Environment variables for Python optimization & server configuration
# In Kubernetes, scaling horizontally (pod replicas) with 1-2 workers per container
# is preferred over high worker count per container to avoid OOMKills.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}" \
    WORKERS=2 \
    PORT=8000

# Set the working directory
WORKDIR /app

# Create a non-root user for security. 
# Running as root in a container is a major security risk.
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application source code
COPY app/ ./app/
COPY .env.example .env.example

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Add container-level healthcheck instruction
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

# Start using Gunicorn with Uvicorn workers, honoring WORKERS and PORT environment variables
CMD ["sh", "-c", "exec gunicorn -w ${WORKERS:-2} -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT:-8000}"]
