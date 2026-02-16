#!/bin/bash

# Deployment script for Todo Chatbot on Kubernetes using Minikube, Helm, kubectl-ai, and kagent

set -e  # Exit on any error

echo "🚀 Starting Todo Chatbot Kubernetes Deployment..."

# Check if required tools are installed
echo "🔍 Checking for required tools..."

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed. Please install minikube first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed. Please install helm first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if kubectl-ai is available (optional)
if command -v kubectl-ai &> /dev/null; then
    KUBECTL_AI_AVAILABLE=true
    echo "✅ kubectl-ai is available"
else
    KUBECTL_AI_AVAILABLE=false
    echo "⚠️  kubectl-ai is not available, will use standard kubectl"
fi

# Check if kagent is available (optional)
if command -v kagent &> /dev/null; then
    KAGENT_AVAILABLE=true
    echo "✅ kagent is available"
else
    KAGENT_AVAILABLE=false
    echo "⚠️  kagent is not available"
fi

# Start Minikube if not already running
echo "☸️  Starting Minikube..."
if ! minikube status &> /dev/null; then
    minikube start --driver=docker
else
    echo "Minikube is already running"
fi

# Enable ingress addon if needed
echo "🌐 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Build Docker images for all services
echo "🐳 Building Docker images..."

# Build backend image
echo "📦 Building backend image..."
eval $(minikube docker-env)
docker build -t todo-chatbot-backend:latest ./backend

# Build frontend image
echo "📦 Building frontend image..."
docker build -t todo-chatbot-frontend:latest ./frontend

# Build MCP server image
echo "📦 Building MCP server image..."
docker build -t todo-chatbot-mcp-server:latest ./mcp_server

# If Gordon (Docker AI Agent) is available, we can use it for advanced operations
if command -v docker &> /dev/null; then
    if docker ai "What can you do?" &> /dev/null; then
        echo "🤖 Gordon (Docker AI Agent) is available"
        echo "💡 You can use Gordon for intelligent Docker operations:"
        echo "   docker ai \"optimize the Dockerfile for smaller image size\""
        echo "   docker ai \"suggest security improvements for the container\""
    fi
fi

# Deploy using Helm
echo "🚢 Deploying Todo Chatbot using Helm..."

# Navigate to Helm chart directory
cd helm/todo-chatbot

# Install/upgrade the release
if helm status todo-chatbot &> /dev/null; then
    echo "🔄 Upgrading existing release..."
    helm upgrade todo-chatbot . --set backend.image.tag=latest --set frontend.image.tag=latest --set mcpServer.image.tag=latest
else
    echo "📥 Installing new release..."
    helm install todo-chatbot . --set backend.image.tag=latest --set frontend.image.tag=latest --set mcpServer.image.tag=latest
fi

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-chatbot-mcp-server --timeout=300s

# If kubectl-ai is available, demonstrate its usage
if [ "$KUBECTL_AI_AVAILABLE" = true ]; then
    echo "🤖 Using kubectl-ai for cluster analysis..."

    echo "📊 Getting cluster overview..."
    kubectl-ai "get cluster overview"

    echo "🔍 Analyzing deployment status..."
    kubectl-ai "check why pods are running and show resource usage"

    echo "📈 Scaling backend if needed..."
    kubectl-ai "scale the backend to handle more load"
fi

# If kagent is available, demonstrate its usage
if [ "$KAGENT_AVAILABLE" = true ]; then
    echo "🤖 Using kagent for advanced operations..."

    echo "🔍 Analyzing cluster health..."
    kagent "analyze the cluster health"

    echo "🔧 Optimizing resource allocation..."
    kagent "optimize resource allocation"

    echo "🔍 Checking for potential issues..."
    kagent "identify potential performance bottlenecks"
fi

# Get service information
echo "🌐 Getting service information..."
kubectl get services

# If ingress is enabled, get the ingress IP
if kubectl get ingress &> /dev/null; then
    echo "🏠 Ingress information:"
    kubectl get ingress
    MINIKUBE_IP=$(minikube ip)
    echo "Access the application at: http://$MINIKUBE_IP"
fi

# Display deployment status
echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "   - Minikube cluster: Running"
echo "   - Helm release: todo-chatbot"
echo "   - Backend service: Running on port 8000"
echo "   - Frontend service: Running on port 80"
echo "   - MCP server: Running on port 8001"
echo "   - PostgreSQL: Running as part of the deployment"

echo ""
echo "🔧 Useful commands:"
echo "   # Check all pods"
echo "   kubectl get pods"
echo ""
echo "   # Check all services"
echo "   kubectl get services"
echo ""
echo "   # Check logs for backend"
echo "   kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend"
echo ""
echo "   # Port forward to access backend locally"
echo "   kubectl port-forward svc/todo-chatbot-backend 8000:8000"
echo ""
echo "   # Uninstall the release"
echo "   helm uninstall todo-chatbot"
echo ""
echo "   # Stop Minikube"
echo "   minikube stop"

echo ""
echo "🎉 Todo Chatbot is now deployed on your local Kubernetes cluster!"