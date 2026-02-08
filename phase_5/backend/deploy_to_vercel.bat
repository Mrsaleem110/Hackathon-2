@echo off
REM Deployment script for Vercel backend (Windows)
REM This script helps verify configuration before deploying to Vercel

echo 🔍 Verifying backend configuration for Vercel deployment...

REM Check if we're in the backend directory
if not exist "vercel.json" (
    echo ❌ Error: vercel.json not found. Please run this script from the backend directory.
    exit /b 1
)

echo ✅ Found vercel.json configuration

REM Check Python dependencies
if not exist "requirements-vercel.txt" (
    echo ❌ Error: requirements-vercel.txt not found.
    exit /b 1
)

echo ✅ Found requirements-vercel.txt

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Vercel CLI not found. Installing...
    npm install -g vercel
)

echo ✅ Vercel CLI is available

REM Display important environment variables status
echo.
echo 📋 Environment variable status check:
echo    Check that DATABASE_URL, SECRET_KEY, and BETTER_AUTH_SECRET are set in Vercel dashboard
echo    Secrets should be at least 32 characters long

REM Check if there are any pending git changes
git status --porcelain >nul 2>&1
if not errorlevel 1 (
    echo.
    echo ⚠️  Warning: Check git status for uncommitted changes before deployment
)

echo.
echo 🚀 To deploy to Vercel, run:
echo    vercel --prod
echo.
echo 📝 For more details, see VERCEL_DEPLOYMENT_CHECKLIST.md

pause