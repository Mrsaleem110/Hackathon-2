#!/bin/bash

# Startup script for AI Todo Chatbot Docker deployment

echo "Starting AI Todo Chatbot services..."

# Build and start all services
docker-compose up --build

echo "Services stopped. To restart, run: ./start.sh"