#!/bin/bash

echo "Testing deployed backend routes..."

BACKEND_URL="https://hackathon-2-p-3-backend.vercel.app"

echo "Testing health endpoint..."
curl -s -o /dev/null -w "Health: %{http_code}\n" "$BACKEND_URL/health"

echo "Testing root endpoint..."
curl -s -o /dev/null -w "Root: %{http_code}\n" "$BACKEND_URL/"

echo "Testing auth endpoints..."
curl -s -o /dev/null -w "Auth/login: %{http_code}\n" "$BACKEND_URL/auth/login" -X POST -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test"}'

echo "Testing tasks endpoint (should return 200 if fixed)..."
curl -s -o /dev/null -w "Tasks: %{http_code}\n" "$BACKEND_URL/tasks/"

echo "Testing dashboard stats endpoint (should return 200 if fixed)..."
curl -s -o /dev/null -w "Dashboard stats: %{http_code}\n" "$BACKEND_URL/dashboard/stats"

echo "Testing chat endpoint (should return 405 Method Not Allowed if exists, not 404)..."
curl -s -o /dev/null -w "Chat (GET): %{http_code}\n" "$BACKEND_URL/chat"

echo "Testing analysis insights endpoint (should return 200 if fixed)..."
curl -s -o /dev/null -w "Analysis insights: %{http_code}\n" "$BACKEND_URL/analysis/user-insights"

echo "Test complete!"