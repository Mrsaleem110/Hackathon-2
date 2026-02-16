FROM python:3.11

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]