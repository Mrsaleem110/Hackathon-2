# PowerShell verification script for deployed backend endpoints

param(
    [Parameter(Mandatory=$true)]
    [string]$BackendUrl
)

Write-Host "Vercel Backend Verification Script" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "`nTesting backend: $BackendUrl" -ForegroundColor Yellow

Write-Host "`n1. Testing health endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$BackendUrl/health" -Method Get -TimeoutSec 10
    Write-Host "Status: Healthy" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n2. Testing debug routes..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$BackendUrl/debug/routes" -Method Get -TimeoutSec 10
    Write-Host "Status: Success" -ForegroundColor Green
    Write-Host "Total Routes: $($response.total_routes)" -ForegroundColor White
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3. Testing auth endpoints availability..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$BackendUrl/auth/test" -Method Get -TimeoutSec 10
    Write-Host "Status: Success" -ForegroundColor Green
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n4. Testing if backend recognizes serverless environment..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$BackendUrl/debug/test" -Method Get -TimeoutSec 10
    Write-Host "Status: Success" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)"
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nVerification complete." -ForegroundColor Green