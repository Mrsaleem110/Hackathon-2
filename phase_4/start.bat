@echo off
REM Startup batch file for AI Todo Chatbot Docker deployment

echo Starting AI Todo Chatbot services...

REM Build and start all services
docker-compose up --build

echo Services stopped. To restart, run: start.bat