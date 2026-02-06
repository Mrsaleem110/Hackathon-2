# Phase IV: Local Kubernetes Deployment

This document describes the deployment of the Todo Chatbot application using Kubernetes with Minikube, Helm Charts, and AI-assisted tools.

## Overview

The Todo Chatbot application is deployed using a cloud-native approach with the following technologies:

- **Containerization**: Docker with AI-assisted operations (Gordon)
- **Orchestration**: Kubernetes (Minikube for local deployment)
- **Package Management**: Helm Charts
- **AI DevOps Tools**: kubectl-ai, kagent
- **Application Components**:
  - Frontend (React/Vite)
  - Backend (FastAPI)
  - MCP Server (AI Integration)
  - PostgreSQL Database

## Prerequisites

Before deploying, ensure you have the following tools installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Gordon beta feature enabled)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Helm](https://helm.sh/docs/intro/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [kubectl-ai](https://github.com/itaysk/kubectl-ai) (optional)
- [kagent](https://github.com/ibm/kagent) (optional)

### Enabling Gordon (Docker AI Agent)

To enable Gordon in Docker Desktop:
1. Open Docker Desktop Settings
2. Go to "Features in development" or "Beta features"
3. Toggle "Gordon (AI commands)" to ON
4. Restart Docker Desktop

Verify Gordon is available:
```bash
docker ai "What can you do?"
```

## Architecture

The application consists of four main services:

1. **PostgreSQL**: Database service (managed by PostgreSQL Helm chart)
2. **Backend**: FastAPI application serving REST APIs
3. **MCP Server**: AI integration service
4. **Frontend**: React application serving the user interface

## Deployment Steps

### 1. Containerization

Each component is containerized using Docker:

- `./backend/Dockerfile`: FastAPI backend container
- `./frontend/Dockerfile`: React frontend container
- `./mcp_server/Dockerfile`: MCP server container
- `./docker-compose.yml`: Local orchestration file

### 2. Kubernetes Deployment

The application is deployed to Kubernetes using Helm:

- `./helm/todo-chatbot/`: Helm chart directory
- `Chart.yaml`: Chart definition
- `values.yaml`: Default configuration values
- `templates/`: Kubernetes manifest templates

### 3. AI-Assisted Operations

Several AI-powered tools enhance the deployment process:

- **kubectl-ai**: AI-assisted kubectl commands
- **kagent**: Advanced Kubernetes AI operations
- **Gordon**: AI-assisted Docker operations

## Quick Deployment

### Using Shell Script (Linux/Mac/WSL):

```bash
chmod +x deploy-k8s.sh
./deploy-k8s.sh
```

### Using PowerShell Script (Windows):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy-k8s.ps1
```

## Manual Deployment Steps

### 1. Start Minikube

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### 2. Build Docker Images

```bash
# Configure Docker to use Minikube's container registry
eval $(minikube docker-env)

# Build images
docker build -t todo-chatbot-backend:latest ./backend
docker build -t todo-chatbot-frontend:latest ./frontend
docker build -t todo-chatbot-mcp-server:latest ./mcp_server
```

### 3. Deploy with Helm

```bash
cd helm/todo-chatbot
helm install todo-chatbot . \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --set mcpServer.image.tag=latest
```

### 4. Access the Application

```bash
# Get the Minikube IP
minikube ip

# Or use port forwarding for testing
kubectl port-forward svc/todo-chatbot-frontend 8080:80
```

## AI-Assisted Operations

### Using kubectl-ai

```bash
# Deploy with AI assistance
kubectl-ai "deploy the todo frontend with 2 replicas"

# Scale backend to handle more load
kubectl-ai "scale the backend to handle more load"

# Troubleshoot failing pods
kubectl-ai "check why the pods are failing"

# Get cluster overview
kubectl-ai "get cluster overview"
```

### Using kagent

```bash
# Analyze cluster health
kagent "analyze the cluster health"

# Optimize resource allocation
kagent "optimize resource allocation"

# Identify performance bottlenecks
kagent "identify potential performance bottlenecks"
```

### Using Gordon (Docker AI Agent)

```bash
# Optimize Dockerfile
docker ai "optimize the Dockerfile for smaller image size"

# Security recommendations
docker ai "suggest security improvements for the container"

# Explain Docker commands
docker ai "explain what this Dockerfile does"
```

## Configuration

The Helm chart can be customized using the `values.yaml` file or command-line overrides:

```bash
# Override values during installation
helm install todo-chatbot . \
  --set backend.replicaCount=2 \
  --set frontend.resources.requests.cpu=100m
```

## Monitoring and Management

### Check Deployment Status

```bash
# View all resources
kubectl get all

# Check pod status
kubectl get pods

# Check service endpoints
kubectl get services

# View logs
kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend
```

### Upgrade the Deployment

```bash
# Update the chart after making changes
helm upgrade todo-chatbot . --reuse-values
```

### Uninstall

```bash
# Remove the release
helm uninstall todo-chatbot
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure you've configured Docker to use Minikube's registry:
   ```bash
   eval $(minikube docker-env)
   ```

2. **Insufficient resources**: Increase Minikube resources:
   ```bash
   minikube start --driver=docker --memory=4096 --cpus=4
   ```

3. **Service not accessible**: Check if the ingress controller is running:
   ```bash
   minikube addons enable ingress
   ```

### Using AI for Troubleshooting

```bash
# Diagnose pod issues
kubectl-ai "why is the backend pod not starting?"

# Resource analysis
kubectl-ai "show me resource usage by namespace"

# Network connectivity
kubectl-ai "check if frontend can reach backend service"
```

## Development Workflow

### Local Development

1. Make changes to the code
2. Rebuild the Docker image:
   ```bash
   docker build -t todo-chatbot-backend:latest ./backend
   ```
3. Restart the affected deployment:
   ```bash
   kubectl rollout restart deployment/todo-chatbot-backend
   ```

### Testing Changes

```bash
# Test configuration changes
helm install todo-chatbot-test . --dry-run --debug

# Validate the chart
helm lint .
```

## Security Considerations

- Store sensitive data (API keys, passwords) in Kubernetes Secrets
- Use RBAC to limit permissions
- Scan images for vulnerabilities
- Enable network policies for pod isolation

## Scaling

The application can be scaled using standard Kubernetes mechanisms:

```bash
# Scale backend deployment
kubectl scale deployment/todo-chatbot-backend --replicas=3

# Or using kubectl-ai
kubectl-ai "scale the backend to 3 replicas"
```

## Conclusion

This deployment provides a complete cloud-native solution for the Todo Chatbot application using modern Kubernetes practices enhanced with AI-assisted tools. The setup enables scalable, reliable, and maintainable deployment of the application with intelligent automation capabilities.