#!/bin/bash

echo "🔄 Clearing and Testing Frontend"
echo "================================"
echo ""

# Stop frontend
echo "1. Stopping frontend..."
docker-compose -f docker-compose-fullstack.yml stop frontend

# Remove old container
echo "2. Removing old container..."
docker-compose -f docker-compose-fullstack.yml rm -f frontend

# Remove old image
echo "3. Removing old image..."
docker rmi spx_new_112025-frontend 2>/dev/null || true

# Rebuild
echo "4. Rebuilding frontend..."
docker-compose -f docker-compose-fullstack.yml build --no-cache frontend

# Start
echo "5. Starting frontend..."
docker-compose -f docker-compose-fullstack.yml up -d frontend

# Wait
echo "6. Waiting for frontend to start..."
sleep 5

# Check
echo "7. Checking status..."
docker ps | grep spx_frontend

echo ""
echo "8. Testing pages..."
curl -s http://localhost:3000 | grep -o "Redirecting to login" && echo "✅ Home page OK"
curl -s http://localhost:3000/login | grep -o "SPX Classification" | head -1 && echo "✅ Login page OK"

echo ""
echo "✅ Done! Please:"
echo "   1. Open browser in Incognito/Private mode"
echo "   2. Go to http://localhost:3000"
echo "   3. Login with admin/admin123"
echo ""
echo "If still seeing error, press F12 and check Console tab"
