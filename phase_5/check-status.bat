@echo off
echo Checking status of Todo Chatbot Application...

REM Navigate to the project directory
cd /d "%~dp0"

echo.
echo Current container status:
docker-compose ps

echo.
echo Checking if containers are running...
for /f "tokens=*" %%i in ('docker-compose ps --format "table {{.Name}}\t{{.State}}" ^| findstr "Up"') do (
    echo Container is running: %%i
)

echo.
echo To stop the application: docker-compose down
echo To view logs: docker-compose logs backend
echo                     docker-compose logs frontend
echo                     docker-compose logs mcp-server
echo                     docker-compose logs postgres
echo.
pause