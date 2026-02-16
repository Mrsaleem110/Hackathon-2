# Standard Docker Commands for Todo Chatbot Application

This document provides standard Docker CLI commands as an alternative to Gordon (Docker AI Agent) when it's unavailable in your region or tier.

## Prerequisites

Ensure you have Docker installed and running:
```bash
docker --version
docker ps  # Should work without errors
```

## Building Images

### Build Individual Services

```bash
# Backend Service
docker build -t todo-chatbot-backend:latest ./backend

# Frontend Service
docker build -t todo-chatbot-frontend:latest ./frontend

# MCP Server
docker build -t todo-chatbot-mcp-server:latest ./mcp_server
```

### Build with Platform Specification
```bash
# For specific platform (useful for Apple Silicon Macs)
docker build --platform linux/amd64 -t todo-chatbot-backend:latest ./backend
docker build --platform linux/amd64 -t todo-chatbot-frontend:latest ./frontend
docker build --platform linux/amd64 -t todo-chatbot-mcp-server:latest ./mcp_server
```

### Build with Build Arguments
```bash
# Frontend with environment-specific build args
docker build \
  --build-arg NODE_ENV=production \
  --build-arg API_URL=http://localhost:8000 \
  -t todo-chatbot-frontend:latest ./frontend
```

## Running Individual Containers

### Backend Service
```bash
# Run backend with environment variables
docker run -d \
  --name todo-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://localhost:5432/todo_db \
  -e OPENAI_API_KEY=your_openai_key_here \
  -e SECRET_KEY=your_secret_key_here \
  todo-chatbot-backend:latest
```

### Frontend Service
```bash
# Run frontend (assumes backend is accessible)
docker run -d \
  --name todo-frontend \
  -p 3000:80 \
  --link todo-backend \
  todo-chatbot-frontend:latest
```

### MCP Server
```bash
# Run MCP server with environment variables
docker run -d \
  --name todo-mcp-server \
  -p 8001:8001 \
  -e DATABASE_URL=postgresql://localhost:5432/todo_db \
  -e OPENAI_API_KEY=your_openai_key_here \
  todo-chatbot-mcp-server:latest
```

## Multi-Container Setup with Docker Networks

### Create Network
```bash
# Create a dedicated network for the application
docker network create todo-network
```

### Run Database Container
```bash
# Run PostgreSQL database
docker run -d \
  --name todo-postgres \
  --network todo-network \
  -e POSTGRES_DB=todo_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15
```

### Run Services with Network
```bash
# Run backend connected to database
docker run -d \
  --name todo-backend \
  --network todo-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://todo-postgres:5432/todo_db \
  -e OPENAI_API_KEY=your_openai_key_here \
  -e SECRET_KEY=your_secret_key_here \
  todo-chatbot-backend:latest

# Run MCP server connected to database
docker run -d \
  --name todo-mcp-server \
  --network todo-network \
  -p 8001:8001 \
  -e DATABASE_URL=postgresql://todo-postgres:5432/todo_db \
  -e OPENAI_API_KEY=your_openai_key_here \
  todo-chatbot-mcp-server:latest

# Run frontend connected to other services
docker run -d \
  --name todo-frontend \
  --network todo-network \
  -p 3000:80 \
  todo-chatbot-frontend:latest
```

## Using Docker Compose (Recommended)

Instead of running individual containers, use the provided `docker-compose.yml`:

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# View running services
docker-compose ps

# Scale specific services
docker-compose up -d --scale backend=2 frontend=2
```

## Image Management

### List Images
```bash
# List all todo-chatbot images
docker images | grep todo-chatbot

# List all images with details
docker images
```

### Clean Up
```bash
# Remove unused images
docker image prune

# Remove specific images
docker rmi todo-chatbot-backend:latest
docker rmi todo-chatbot-frontend:latest
docker rmi todo-chatbot-mcp-server:latest

# Remove all images (use with caution)
docker system prune -a
```

### Image Optimization
```bash
# Build without cache (clean build)
docker build --no-cache -t todo-chatbot-backend:latest ./backend

# Check image layers and size
docker history todo-chatbot-backend:latest

# Analyze image with dive tool (if installed)
# dive todo-chatbot-backend:latest
```

## Container Management

### View Running Containers
```bash
# List all running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Filter for todo-chatbot containers
docker ps -a | grep todo-chatbot
```

### Container Logs
```bash
# View logs for a specific container
docker logs todo-backend
docker logs todo-frontend
docker logs todo-mcp-server

# Follow logs in real-time
docker logs -f todo-backend

# View last 100 lines of logs
docker logs --tail 100 todo-backend
```

### Container Exec & Inspection
```bash
# Execute commands inside running container
docker exec -it todo-backend /bin/sh
docker exec -it todo-frontend /bin/sh

# Inspect container details
docker inspect todo-backend

# Get container IP
docker inspect todo-backend | grep IPAddress
```

### Resource Management
```bash
# Run with memory and CPU limits
docker run -d \
  --name todo-backend-limited \
  --memory=512m \
  --cpus=1.0 \
  -p 8000:8000 \
  todo-chatbot-backend:latest

# Update resource limits for running container
docker update --memory=1g todo-backend
```

## Volume Management

### Named Volumes
```bash
# Create named volume for database persistence
docker volume create todo-postgres-data

# Run database with named volume
docker run -d \
  --name todo-postgres \
  -v todo-postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_DB=todo_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  postgres:15
```

### Bind Mounts
```bash
# Mount local directory to container
docker run -d \
  --name todo-backend-dev \
  -v ./backend:/app \
  -p 8000:8000 \
  todo-chatbot-backend:latest
```

## Troubleshooting Commands

### Common Issues
```bash
# Check if containers are running
docker ps

# Check container logs for errors
docker logs <container-name>

# Check network connectivity between containers
docker exec -it todo-backend ping todo-postgres

# Check if ports are bound correctly
docker port todo-backend

# Check container resource usage
docker stats todo-backend
```

### Cleanup Commands
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all volumes (be careful!)
docker volume prune

# Remove all networks (be careful!)
docker network prune
```

## Environment Variables

### Setting Environment Variables
```bash
# Using environment file
docker run -d \
  --name todo-backend \
  --env-file ./.env \
  -p 8000:8000 \
  todo-chatbot-backend:latest

# Setting individual variables
docker run -d \
  --name todo-backend \
  -e DATABASE_URL=postgresql://localhost:5432/todo_db \
  -e OPENAI_API_KEY=your_key \
  -e SECRET_KEY=your_secret \
  -p 8000:8000 \
  todo-chatbot-backend:latest
```

## Docker Security Best Practices

### Non-root User
```bash
# Run container as non-root user (if supported by image)
docker run -d \
  --name todo-backend \
  --user 1000:1000 \
  -p 8000:8000 \
  todo-chatbot-backend:latest
```

### Read-only Root Filesystem
```bash
# Run with read-only root filesystem (where possible)
docker run -d \
  --name todo-backend \
  --read-only \
  -p 8000:8000 \
  todo-chatbot-backend:latest
```

## Docker Build Optimization

### Multi-stage Builds
If you want to create optimized multi-stage builds, you can modify the Dockerfiles:

```dockerfile
# Example multi-stage Dockerfile for backend
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

These commands provide a complete alternative to Gordon (Docker AI Agent) for managing the Todo Chatbot application containers. Use these when Gordon is unavailable in your region or tier.