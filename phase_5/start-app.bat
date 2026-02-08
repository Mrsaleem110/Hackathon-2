@echo off
echo Starting Todo Chatbot Application...

REM Navigate to the project directory
cd /d "%~dp0"

echo Stopping any existing containers...
docker-compose down

echo Removing any old images...
docker rmi -f phase_4-backend:latest phase_4-frontend:latest phase_4-mcp-server:latest 2>nul

echo Building and starting the application...
docker-compose up --build -d

echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo Checking container status...
docker-compose ps

echo.
echo Application should now be accessible at http://localhost
echo Backend is available at http://localhost:8000
echo MCP Server is available at http://localhost:8001
echo.
echo To view logs: docker-compose logs -f
echo To stop the application: docker-compose down
echo.
pause