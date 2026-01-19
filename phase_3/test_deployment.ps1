# PowerShell script to test deployed Vercel backend
# Replace YOUR_BACKEND_URL with your actual deployed backend URL

$backendUrl = "https://hackathon-2-phase-3-backend.vercel.app"  # Replace with your actual URL

Write-Host "Testing deployed backend at: $backendUrl" -ForegroundColor Green

Write-Host ""
Write-Host "=== Testing Root Endpoint ===" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/" -Method Get -TimeoutSec 15
    Write-Host "✓ Backend root endpoint accessible" -ForegroundColor Green
    $response | ConvertTo-Json
}
catch {
    Write-Host "✗ Backend root endpoint not accessible" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing Health Endpoint ===" -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$backendUrl/health" -Method Get -TimeoutSec 15
    Write-Host "✓ Health endpoint accessible" -ForegroundColor Green
    $health | ConvertTo-Json
}
catch {
    Write-Host "✗ Health endpoint not accessible" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing CORS Headers ===" -ForegroundColor Yellow
try {
    $webResponse = Invoke-WebRequest -Uri "$backendUrl/" -Method Options -TimeoutSec 15
    $corsHeaders = $webResponse.Headers | Where-Object { $_.Key -like "*CORS*" -or $_.Key -eq "Access-Control-Allow-Origin" }
    if ($corsHeaders) {
        Write-Host "✓ CORS headers present:" -ForegroundColor Green
        $corsHeaders | ForEach-Object { Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor Cyan }
    } else {
        Write-Host "⚠️  No explicit CORS headers found, but this may be normal for OPTIONS requests" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "✗ Could not test CORS headers" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing Expected API Endpoints ===" -ForegroundColor Yellow
$endpoints = @("/docs", "/redoc")

foreach ($endpoint in $endpoints) {
    try {
        $result = Invoke-WebRequest -Uri "$backendUrl$endpoint" -Method Get -TimeoutSec 10
        if ($result.StatusCode -eq 200) {
            Write-Host "✓ $endpoint accessible (Status: $($result.StatusCode))" -ForegroundColor Green
        } else {
            Write-Host "✗ $endpoint returned status $($result.StatusCode)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "✗ $endpoint not accessible" -ForegroundColor Red
    }
}