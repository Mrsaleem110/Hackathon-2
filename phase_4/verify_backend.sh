#!/bin/bash
# Quick verification script for deployed backend endpoints

echo "Vercel Backend Verification Script"
echo "=================================="

if [ -z "$1" ]; then
    echo "Usage: $0 <backend-url>"
    echo "Example: $0 https://your-backend-project.vercel.app"
    exit 1
fi

BACKEND_URL=$1

echo "Testing backend: $BACKEND_URL"
echo ""

echo "1. Testing health endpoint..."
curl -s -w "\n%{http_code}\n" -o /dev/null "$BACKEND_URL/health"

echo ""
echo "2. Testing debug routes..."
curl -s -w "\n%{http_code}\n" -o /dev/null "$BACKEND_URL/debug/routes"

echo ""
echo "3. Testing auth endpoints availability..."
curl -s -w "\n%{http_code}\n" -o /dev/null "$BACKEND_URL/auth/test"

echo ""
echo "4. Testing if backend recognizes serverless environment..."
curl -s -w "\n%{http_code}\n" -o /dev/null "$BACKEND_URL/debug/test"

echo ""
echo "Verification complete. Check HTTP status codes above:"
echo "200 - Success"
echo "404 - Endpoint not found"
echo "405 - Method not allowed (expected for some endpoints)"
echo "Other codes - Potential issues"