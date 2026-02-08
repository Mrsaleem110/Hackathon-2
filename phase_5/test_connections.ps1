# PowerShell script to test connections for Todo AI Chatbot

Write-Host "Testing connections for Todo AI Chatbot..." -ForegroundColor Green

Write-Host ""
Write-Host "=== Testing Backend Server ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/" -Method Get -TimeoutSec 10
    Write-Host "✓ Backend server is accessible" -ForegroundColor Green
    $response | ConvertTo-Json
}
catch {
    Write-Host "✗ Backend server is not accessible at http://localhost:8001" -ForegroundColor Red
    Write-Host "Please start the backend with: cd backend && python run_server.py" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== Testing Backend Health Endpoint ===" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get -TimeoutSec 10
    Write-Host "✓ Backend health endpoint is accessible" -ForegroundColor Green
    $health | ConvertTo-Json
}
catch {
    Write-Host "✗ Backend health endpoint is not accessible" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing Better Auth Server ===" -ForegroundColor Yellow
try {
    $authHealth = Invoke-RestMethod -Uri "http://localhost:3000/health" -Method Get -TimeoutSec 10
    Write-Host "✓ Better Auth server is accessible" -ForegroundColor Green
    $authHealth | ConvertTo-Json
}
catch {
    Write-Host "✗ Better Auth server is not accessible at http://localhost:3000" -ForegroundColor Red
    Write-Host "Please start the auth server with: npm start" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== Testing Database Connection ===" -ForegroundColor Yellow
try {
    $result = & cmd /c "cd backend && python -c `"from src.database.connection import get_engine; engine = get_engine(); conn = engine.connect(); print('✓ Database connection successful'); conn.close();`""
    Write-Host $result -ForegroundColor Green
}
catch {
    Write-Host "✗ Database connection test failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Environment Configuration Check ===" -ForegroundColor Yellow
Write-Host "Backend port configuration:" -ForegroundColor Cyan
Get-Content backend/run_server.py | Select-String "port"

Write-Host ""
Write-Host "Frontend API base URL (check if it points to local backend):" -ForegroundColor Cyan
if (Test-Path "frontend/.env") {
    Get-Content frontend/.env | Select-String "VITE_API_BASE_URL"
} else {
    Write-Host "frontend/.env file not found"
}

Write-Host ""
Write-Host "=== Setup Instructions ===" -ForegroundColor Magenta
Write-Host "1. Start Better Auth: npm start"
Write-Host "2. Start Backend: cd backend && python run_server.py"
Write-Host "3. Start Frontend: cd frontend && npm run dev"
Write-Host "4. Access frontend at: http://localhost:5173"