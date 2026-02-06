Write-Host "Testing deployed backend routes..." -ForegroundColor Green

$backendUrl = "https://hackathon-2-p-3-backend.vercel.app"

Write-Host "`nTesting health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/health" -Method GET -TimeoutSec 10
    Write-Host "Health: 200 - OK" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
} catch {
    Write-Host "Health: $($_.Exception.Response.StatusCode.value__) - $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
}

Write-Host "`nTesting root endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/" -Method GET -TimeoutSec 10
    Write-Host "Root: 200 - OK" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Cyan
} catch {
    Write-Host "Root: $($_.Exception.Response.StatusCode.value__) - $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
}

Write-Host "`nTesting auth endpoints..." -ForegroundColor Yellow
try {
    $headers = @{ "Content-Type" = "application/json" }
    $body = @{ email = "test@test.com"; password = "test" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "$backendUrl/auth/login" -Method POST -Headers $headers -Body $body -TimeoutSec 10
    Write-Host "Auth/login: 200 - OK" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Auth/login: $statusCode - $($_.Exception.Response.StatusDescription)" -ForegroundColor $(if ($statusCode -eq 401) { "Yellow" } else { "Red" })
}

Write-Host "`nTesting tasks endpoint (should return 200 if fixed)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/tasks/" -Method GET -TimeoutSec 10
    Write-Host "Tasks: 200 - OK (Routes are working!)" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Tasks: $statusCode - $($_.Exception.Response.StatusDescription) (Routes not available yet)" -ForegroundColor $(if ($statusCode -eq 404) { "Red" } else { "Yellow" })
}

Write-Host "`nTesting dashboard stats endpoint (should return 200 if fixed)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/dashboard/stats" -Method GET -TimeoutSec 10
    Write-Host "Dashboard stats: 200 - OK (Routes are working!)" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Dashboard stats: $statusCode - $($_.Exception.Response.StatusDescription) (Routes not available yet)" -ForegroundColor $(if ($statusCode -eq 404) { "Red" } else { "Yellow" })
}

Write-Host "`nTesting chat endpoint (should return 405 Method Not Allowed if exists, not 404)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/chat" -Method GET -TimeoutSec 10
    Write-Host "Chat (GET): 200 - OK" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 405) {
        Write-Host "Chat (GET): 405 - Method Not Allowed (Route exists!)" -ForegroundColor Green
    } else {
        Write-Host "Chat (GET): $statusCode - $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    }
}

Write-Host "`nTesting analysis insights endpoint (should return 200 if fixed)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/analysis/user-insights" -Method GET -TimeoutSec 10
    Write-Host "Analysis insights: 200 - OK (Routes are working!)" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Host "Analysis insights: $statusCode - $($_.Exception.Response.StatusDescription) (Routes not available yet)" -ForegroundColor $(if ($statusCode -eq 404) { "Red" } else { "Yellow" })
}

Write-Host "`n`nTest complete!" -ForegroundColor Green
Write-Host "If you see 200s or 405s for tasks, dashboard, chat, and analysis endpoints, the routes are working correctly." -ForegroundColor Cyan
Write-Host "If you still see 404s, the backend hasn't been updated with the modular routes yet." -ForegroundColor Yellow