#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting SPX Classification Backend${NC}"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: ${python_version}${NC}"

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Run environment check
echo ""
echo -e "${YELLOW}Checking environment configuration...${NC}"
python3 check_env.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Environment check failed${NC}"
    echo -e "${YELLOW}Please fix the configuration issues above${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Starting server on http://localhost:8000${NC}"
echo -e "${GREEN}✓ API docs available at http://localhost:8000/docs${NC}"
echo ""

# Run the server
cd ..
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
