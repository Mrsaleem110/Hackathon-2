# PowerShell Deployment script for AI Todo Chatbot (Frontend and Backend)

Write-Host "🚀 AI Todo Chatbot Deployment Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Function to check if vercel CLI is installed
function Check-VercelCLI {
    try {
        $vercelVersion = vercel --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Vercel CLI is installed" -ForegroundColor Green
        } else {
            Write-Host "❌ Vercel CLI is not installed." -ForegroundColor Red
            Write-Host "Please install it with: npm install -g vercel" -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "❌ Vercel CLI is not installed." -ForegroundColor Red
        Write-Host "Please install it with: npm install -g vercel" -ForegroundColor Yellow
        exit 1
    }
}

# Function to login to vercel
function Login-ToVercel {
    Write-Host ""
    Write-Host "🔐 Logging in to Vercel..." -ForegroundColor Cyan
    vercel login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to login to Vercel" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Successfully logged in to Vercel" -ForegroundColor Green
}

# Function to deploy backend
function Deploy-Backend {
    Write-Host ""
    Write-Host "📦 Deploying Backend..." -ForegroundColor Cyan
    Set-Location backend

    # Check if vercel project is linked
    if (!(Test-Path ".vercel/project.json")) {
        Write-Host "🔗 Linking backend to Vercel project..." -ForegroundColor Yellow
        vercel
    } else {
        Write-Host "🔗 Backend already linked to Vercel project" -ForegroundColor Green
    }

    # Deploy to production
    Write-Host "📤 Deploying backend to production..." -ForegroundColor Cyan
    vercel --prod --confirm

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend deployed successfully!" -ForegroundColor Green
        # Note: Getting the actual URL after deployment might require parsing vercel output
        Write-Host "🌐 Please check your Vercel dashboard for the backend URL" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Backend deployment failed!" -ForegroundColor Red
        Set-Location ..
        exit 1
    }

    Set-Location ..
}

# Function to deploy frontend
function Deploy-Frontend {
    Write-Host ""
    Write-Host "📦 Deploying Frontend..." -ForegroundColor Cyan
    Set-Location frontend

    # Check if vercel project is linked
    if (!(Test-Path ".vercel/project.json")) {
        Write-Host "🔗 Linking frontend to Vercel project..." -ForegroundColor Yellow
        vercel
    } else {
        Write-Host "🔗 Frontend already linked to Vercel project" -ForegroundColor Green
    }

    # Deploy to production
    Write-Host "📤 Deploying frontend to production..." -ForegroundColor Cyan
    vercel --prod --confirm

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend deployed successfully!" -ForegroundColor Green
        # Note: Getting the actual URL after deployment might require parsing vercel output
        Write-Host "🌐 Please check your Vercel dashboard for the frontend URL" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Frontend deployment failed!" -ForegroundColor Red
        Set-Location ..
        exit 1
    }

    Set-Location ..
}

# Main deployment process
function Main {
    Write-Host "Starting deployment process..." -ForegroundColor Cyan

    Check-VercelCLI
    Login-ToVercel

    Write-Host ""
    $deployBackend = Read-Host "Do you want to deploy the backend first? (y/n)"
    if ($deployBackend -match "[Yy]") {
        Deploy-Backend
    }

    Write-Host ""
    $deployFrontend = Read-Host "Do you want to deploy the frontend? (y/n)"
    if ($deployFrontend -match "[Yy]") {
        Deploy-Frontend
    }

    Write-Host ""
    Write-Host "🎉 Deployment process completed!" -ForegroundColor Green
    Write-Host "Remember to:" -ForegroundColor Yellow
    Write-Host "1. Add all required environment variables to both projects" -ForegroundColor Yellow
    Write-Host "2. Update CORS settings in backend if needed" -ForegroundColor Yellow
    Write-Host "3. Test your deployed application" -ForegroundColor Yellow
}

# Run the main function
Main