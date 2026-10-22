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
# (psycopg2-binary usually doesn't need this, but standard psycopg2 does)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching.
# If requirements.txt doesn't change, Docker skips the install step.
COPY requirements.txt .

# Install dependencies into a local folder ('/install')
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==========================================
# STAGE 2: Final Runtime
# ==========================================
FROM python:3.12-slim

# Environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Create a non-root user for security. 
# Running as root in a container is a security risk.
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application source code
# We copy the 'app' directory and any necessary config files
COPY app/ ./app/
COPY .env.example .env.example

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Start the application using Gunicorn with Uvicorn workers.
# Gunicorn is a production-grade WSGI server that manages multiple worker processes.
# -w 4: Use 4 worker processes (standard formula: 2 x cores + 1)
# -k uvicorn.workers.UvicornWorker: Use the Uvicorn worker to handle ASGI (FastAPI)
# --bind 0.0.0.0:8000: Listen on all interfaces on port 8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
