#!/bin/bash
# Connection test script for Todo AI Chatbot

echo "Testing connections for Todo AI Chatbot..."

echo ""
echo "=== Testing Backend Server ==="
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo "✓ Backend server is accessible"
    curl -s http://localhost:8001/ | python -m json.tool 2>/dev/null || echo "Backend responded (non-JSON response)"
else
    echo "✗ Backend server is not accessible at http://localhost:8001"
    echo "Please start the backend with: cd backend && python run_server.py"
fi

echo ""
echo "=== Testing Backend Health Endpoint ==="
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✓ Backend health endpoint is accessible"
    curl -s http://localhost:8001/health | python -m json.tool
else
    echo "✗ Backend health endpoint is not accessible"
fi

echo ""
echo "=== Testing Better Auth Server ==="
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "✓ Better Auth server is accessible"
    curl -s http://localhost:3000/health | python -m json.tool
else
    echo "✗ Better Auth server is not accessible at http://localhost:3000"
    echo "Please start the auth server with: npm start"
fi

echo ""
echo "=== Testing Database Connection ==="
cd backend && python -c "
try:
    from src.database.connection import get_engine
    engine = get_engine()
    conn = engine.connect()
    print('✓ Database connection successful')
    conn.close()
except Exception as e:
    print(f'✗ Database connection failed: {e}')
"

echo ""
echo "=== Environment Configuration Check ==="
echo "Backend port configuration:"
grep -r "port" backend/run_server.py

echo ""
echo "Frontend API base URL (check if it points to local backend):"
if [ -f "frontend/.env" ]; then
    grep VITE_API_BASE_URL frontend/.env
else
    echo "frontend/.env file not found"
fi

echo ""
echo "=== Setup Instructions ==="
echo "1. Start Better Auth: npm start"
echo "2. Start Backend: cd backend && python run_server.py"
echo "3. Start Frontend: cd frontend && npm run dev"
echo "4. Access frontend at: http://localhost:5173"