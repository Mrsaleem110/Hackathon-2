# PowerShell script to check Gordon (Docker AI Agent) availability and provide Docker CLI alternatives

Write-Host "🔍 Checking Gordon (Docker AI Agent) availability..." -ForegroundColor Yellow

# Check if Docker is available
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker is installed" -ForegroundColor Green

# Test Gordon availability
Write-Host "🧪 Testing Gordon (Docker AI Agent) availability..." -ForegroundColor Yellow

$gordon_test = docker ai "ping" 2>$null
$gordon_available = ($LASTEXITCODE -eq 0) -and ($gordon_test -ne $null)

if ($gordon_available) {
    Write-Host "✅ Gordon (Docker AI Agent) is AVAILABLE in your region!" -ForegroundColor Green
    Write-Host "You can use Gordon for intelligent Docker operations:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  docker ai `"optimize the Dockerfile for smaller image size`"" -ForegroundColor Gray
    Write-Host "  docker ai `"suggest security improvements for the container`"" -ForegroundColor Gray
    Write-Host "  docker ai `"explain what this Dockerfile does`"" -ForegroundColor Gray
    Write-Host "  docker ai `"create a multi-stage Dockerfile for this project`"" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Gordon is available and ready to assist with:" -ForegroundColor White
    Write-Host "  • Dockerfile optimization" -ForegroundColor Gray
    Write-Host "  • Security improvements" -ForegroundColor Gray
    Write-Host "  • Multi-stage builds" -ForegroundColor Gray
    Write-Host "  • Performance tuning" -ForegroundColor Gray
    Write-Host "  • Troubleshooting" -ForegroundColor Gray
} else {
    Write-Host "❌ Gordon (Docker AI Agent) is NOT AVAILABLE in your region or tier" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔄 FALLING BACK TO STANDARD DOCKER CLI COMMANDS" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Here are the standard Docker commands for the Todo Chatbot:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# Build all services:" -ForegroundColor White
    Write-Host "docker build -t todo-chatbot-backend:latest .\backend" -ForegroundColor Gray
    Write-Host "docker build -t todo-chatbot-frontend:latest .\frontend" -ForegroundColor Gray
    Write-Host "docker build -t todo-chatbot-mcp-server:latest .\mcp_server" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Run individual services:" -ForegroundColor White
    Write-Host "docker run -d --name todo-backend -p 8000:8000 `" -ForegroundColor Gray
    Write-Host "  -e DATABASE_URL=postgresql://localhost:5432/todo_db `" -ForegroundColor Gray
    Write-Host "  -e OPENAI_API_KEY=`$env:OPENAI_API_KEY `" -ForegroundColor Gray
    Write-Host "  -e SECRET_KEY=`$env:SECRET_KEY `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-backend:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "docker run -d --name todo-frontend -p 3000:80 `" -ForegroundColor Gray
    Write-Host "  --link todo-backend `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-frontend:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "docker run -d --name todo-mcp-server -p 8001:8001 `" -ForegroundColor Gray
    Write-Host "  -e DATABASE_URL=postgresql://localhost:5432/todo_db `" -ForegroundColor Gray
    Write-Host "  -e OPENAI_API_KEY=`$env:OPENAI_API_KEY `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-mcp-server:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Or use docker-compose for orchestrated deployment:" -ForegroundColor White
    Write-Host "docker-compose up -d --build" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Docker CLI alternatives for common operations:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# Build with specific platform:" -ForegroundColor White
    Write-Host "docker build --platform linux/amd64 -t todo-chatbot-backend:latest .\backend" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Build with build arguments:" -ForegroundColor White
    Write-Host "docker build --build-arg NODE_ENV=production -t todo-chatbot-frontend:latest .\frontend" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Run with resource limits:" -ForegroundColor White
    Write-Host "docker run -d --name todo-backend `" -ForegroundColor Gray
    Write-Host "  --memory=512m --cpus=1.0 `" -ForegroundColor Gray
    Write-Host "  -p 8000:8000 `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-backend:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Docker network setup:" -ForegroundColor White
    Write-Host "docker network create todo-network" -ForegroundColor Gray
    Write-Host "docker run -d --name postgres --network todo-network `" -ForegroundColor Gray
    Write-Host "  -e POSTGRES_DB=todo_db `" -ForegroundColor Gray
    Write-Host "  -e POSTGRES_USER=postgres `" -ForegroundColor Gray
    Write-Host "  -e POSTGRES_PASSWORD=postgres `" -ForegroundColor Gray
    Write-Host "  postgres:15" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Multi-container orchestration:" -ForegroundColor White
    Write-Host "docker run -d --name todo-backend --network todo-network `" -ForegroundColor Gray
    Write-Host "  -e DATABASE_URL=postgresql://postgres:5432/todo_db `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-backend:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "docker run -d --name todo-frontend --network todo-network `" -ForegroundColor Gray
    Write-Host "  -p 3000:80 `" -ForegroundColor Gray
    Write-Host "  todo-chatbot-frontend:latest" -ForegroundColor Gray
    Write-Host ""
    Write-Host "# Docker image optimization commands:" -ForegroundColor White
    Write-Host "docker images | Select-String todo-chatbot  # List all todo-chatbot images" -ForegroundColor Gray
    Write-Host "docker image prune  # Remove unused images" -ForegroundColor Gray
    Write-Host "docker build --no-cache -t todo-chatbot-backend:latest .\backend  # Clean build" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📝 TIP: Use the docker-compose.yml file in this directory for easier multi-service management!" -ForegroundColor Green
}