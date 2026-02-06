@echo off
echo 🧹 Cleaning existing Vercel configuration...
cd backend

REM Remove Vercel configuration
if exist .vercel rmdir /s /q .vercel
if exist .env.local del /f .env.local

echo.
echo 🚀 Starting fresh deployment...
echo.

REM Deploy to Vercel
vercel --prod --force --confirm

echo.
echo Deployment completed!
echo Check your Vercel dashboard for the deployment URL
pause