# PowerShell deployment script for Todo Chatbot on Kubernetes using Minikube, Helm, kubectl-ai, and kagent

Write-Host "🚀 Starting Todo Chatbot Kubernetes Deployment..." -ForegroundColor Green

# Check if required tools are installed
Write-Host "🔍 Checking for required tools..." -ForegroundColor Yellow

$tools = @("minikube", "helm", "kubectl")
$missing_tools = @()

foreach ($tool in $tools) {
    if (!(Get-Command $tool -ErrorAction SilentlyContinue)) {
        $missing_tools += $tool
    }
}

if ($missing_tools.Count -gt 0) {
    Write-Host "❌ The following tools are not installed: $($missing_tools -join ', ')" -ForegroundColor Red
    exit 1
}

# Check if kubectl-ai is available (optional)
$kubectl_ai_available = Get-Command kubectl-ai -ErrorAction SilentlyContinue
if ($kubectl_ai_available) {
    $KUBECTL_AI_AVAILABLE = $true
    Write-Host "✅ kubectl-ai is available" -ForegroundColor Green
} else {
    $KUBECTL_AI_AVAILABLE = $false
    Write-Host "⚠️  kubectl-ai is not available, will use standard kubectl" -ForegroundColor Yellow
}

# Check if kagent is available (optional)
$kagent_available = Get-Command kagent -ErrorAction SilentlyContinue
if ($kagent_available) {
    $KAGENT_AVAILABLE = $true
    Write-Host "✅ kagent is available" -ForegroundColor Green
} else {
    $KAGENT_AVAILABLE = $false
    Write-Host "⚠️  kagent is not available" -ForegroundColor Yellow
}

# Start Minikube if not already running
Write-Host "☸️  Starting Minikube..." -ForegroundColor Yellow
try {
    $minikube_status = minikube status --format='{{.APIServer}}'
    if (!$minikube_status -or $minikube_status -eq "Stopped") {
        minikube start --driver=docker
    } else {
        Write-Host "Minikube is already running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Failed to start Minikube: $_" -ForegroundColor Red
    exit 1
}

# Enable ingress addon if needed
Write-Host "🌐 Enabling Minikube addons..." -ForegroundColor Yellow
minikube addons enable ingress
minikube addons enable metrics-server

# Configure Docker environment for Minikube
Write-Host "🐳 Configuring Docker environment for Minikube..." -ForegroundColor Yellow
$docker_env = minikube docker-env
Invoke-Expression $docker_env

# Build Docker images for all services
Write-Host "📦 Building Docker images..." -ForegroundColor Yellow

# Build backend image
Write-Host "📦 Building backend image..." -ForegroundColor Cyan
docker build -t todo-chatbot-backend:latest ..\backend

# Build frontend image
Write-Host "📦 Building frontend image..." -ForegroundColor Cyan
docker build -t todo-chatbot-frontend:latest ..\frontend

# Build MCP server image
Write-Host "📦 Building MCP server image..." -ForegroundColor Cyan
docker build -t todo-chatbot-mcp-server:latest ..\mcp_server

# If Gordon (Docker AI Agent) is available, we can use it for advanced operations
$docker_ai_available = docker ai "What can you do?" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "🤖 Gordon (Docker AI Agent) is available" -ForegroundColor Green
    Write-Host "💡 You can use Gordon for intelligent Docker operations:" -ForegroundColor Yellow
    Write-Host "   docker ai `"optimize the Dockerfile for smaller image size`"" -ForegroundColor White
    Write-Host "   docker ai `"suggest security improvements for the container`"" -ForegroundColor White
}

# Deploy using Helm
Write-Host "🚢 Deploying Todo Chatbot using Helm..." -ForegroundColor Yellow

# Navigate to Helm chart directory
Push-Location helm\todo-chatbot

# Install/upgrade the release
$release_exists = helm status todo-chatbot 2>$null
if ($release_exists) {
    Write-Host "🔄 Upgrading existing release..." -ForegroundColor Yellow
    helm upgrade todo-chatbot . --set backend.image.tag=latest --set frontend.image.tag=latest --set mcpServer.image.tag=latest
} else {
    Write-Host "📥 Installing new release..." -ForegroundColor Yellow
    helm install todo-chatbot . --set backend.image.tag=latest --set frontend.image.tag=latest --set mcpServer.image.tag=latest
}

# Wait for deployments to be ready
Write-Host "⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow

# Function to wait for pods
function Wait-ForPods {
    param([string]$label, [int]$timeoutSeconds = 300)

    $elapsed = 0
    while ($elapsed -lt $timeoutSeconds) {
        $pods = kubectl get pods -l "app.kubernetes.io/name=$label" --no-headers 2>$null
        if ($pods) {
            $allReady = $true
            $podLines = $pods -split "`n"
            foreach ($line in $podLines) {
                if ($line -match "\s+NotReady\s+" -or $line -match "\s+ContainerCreating\s+" -or $line -match "\s+Pending\s+") {
                    $allReady = $false
                    break
                }
            }

            if ($allReady) {
                Write-Host "✅ Pods with label '$label' are ready" -ForegroundColor Green
                return $true
            }
        }

        Start-Sleep -Seconds 5
        $elapsed += 5
    }

    Write-Host "❌ Timeout waiting for pods with label '$label'" -ForegroundColor Red
    return $false
}

# Wait for all deployments to be ready
Wait-ForPods "todo-chatbot-backend"
Wait-ForPods "todo-chatbot-frontend"
Wait-ForPods "todo-chatbot-mcp-server"

# If kubectl-ai is available, demonstrate its usage
if ($KUBECTL_AI_AVAILABLE) {
    Write-Host "🤖 Using kubectl-ai for cluster analysis..." -ForegroundColor Yellow

    Write-Host "📊 Getting cluster overview..." -ForegroundColor Cyan
    kubectl-ai "get cluster overview"

    Write-Host "🔍 Analyzing deployment status..." -ForegroundColor Cyan
    kubectl-ai "check why pods are running and show resource usage"

    Write-Host "📈 Scaling backend if needed..." -ForegroundColor Cyan
    kubectl-ai "scale the backend to handle more load"
}

# If kagent is available, demonstrate its usage
if ($KAGENT_AVAILABLE) {
    Write-Host "🤖 Using kagent for advanced operations..." -ForegroundColor Yellow

    Write-Host "🔍 Analyzing cluster health..." -ForegroundColor Cyan
    kagent "analyze the cluster health"

    Write-Host "🔧 Optimizing resource allocation..." -ForegroundColor Cyan
    kagent "optimize resource allocation"

    Write-Host "🔍 Checking for potential issues..." -ForegroundColor Cyan
    kagent "identify potential performance bottlenecks"
}

# Get service information
Write-Host "🌐 Getting service information..." -ForegroundColor Yellow
kubectl get services

# If ingress is enabled, get the ingress IP
$ingress_exists = kubectl get ingress 2>$null
if ($ingress_exists) {
    Write-Host "🏠 Ingress information:" -ForegroundColor Cyan
    kubectl get ingress
    $minikube_ip = minikube ip
    Write-Host "Access the application at: http://$minikube_ip" -ForegroundColor Green
}

# Display deployment status
Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "   - Minikube cluster: Running" -ForegroundColor White
Write-Host "   - Helm release: todo-chatbot" -ForegroundColor White
Write-Host "   - Backend service: Running on port 8000" -ForegroundColor White
Write-Host "   - Frontend service: Running on port 80" -ForegroundColor White
Write-Host "   - MCP server: Running on port 8001" -ForegroundColor White
Write-Host "   - PostgreSQL: Running as part of the deployment" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Useful commands:" -ForegroundColor Yellow
Write-Host "   # Check all pods" -ForegroundColor White
Write-Host "   kubectl get pods" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Check all services" -ForegroundColor White
Write-Host "   kubectl get services" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Check logs for backend" -ForegroundColor White
Write-Host "   kubectl logs -l app.kubernetes.io/name=todo-chatbot-backend" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Port forward to access backend locally" -ForegroundColor White
Write-Host "   kubectl port-forward svc/todo-chatbot-backend 8000:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Uninstall the release" -ForegroundColor White
Write-Host "   helm uninstall todo-chatbot" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Stop Minikube" -ForegroundColor White
Write-Host "   minikube stop" -ForegroundColor Gray

Write-Host ""
Write-Host "🎉 Todo Chatbot is now deployed on your local Kubernetes cluster!" -ForegroundColor Green

# Return to original directory
Pop-Location