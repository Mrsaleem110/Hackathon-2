# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies if any packages require compilation
# Although psycopg2-binary is used, some other packages might need them.
# Only install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies into a virtual environment and cache pip
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt --default-timeout=120

# Stage 2: Final
FROM python:3.11-slim

WORKDIR /app

# Copy only curl for healthcheck from builder stage, avoid full apt-get update/install again
COPY --from=builder /usr/bin/curl /usr/bin/curl

# Copy virtual environment from builder stage
COPY --from=builder /venv /venv

# Set PATH to include virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]