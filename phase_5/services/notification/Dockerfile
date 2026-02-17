# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/src/ ./backend/src/
COPY services/notification/app/ ./notification/app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "notification.app.job_handler:app", "--host", "0.0.0.0", "--port", "8000"]