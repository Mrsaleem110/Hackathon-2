#!/bin/bash
# Quick test script to verify task functionality

echo "=== Phase 3 Task Management Test ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "1. Testing Backend Health..."
curl -s http://localhost:8001/health | jq . || echo "Backend not responding"

echo ""
echo "2. Testing Tasks Endpoint (without auth)..."
curl -s -H "Authorization: Bearer test-token" http://localhost:8001/tasks/ | jq . || echo "Tasks endpoint not responding"

echo ""
echo "3. Checking Routes..."
curl -s http://localhost:8001/debug/routes | jq '.all_routes[] | select(.path | contains("task"))' || echo "Routes endpoint not responding"

echo ""
echo "=== Test Complete ==="
