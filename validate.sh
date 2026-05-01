#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Smart Travel Planner - Project Validation"
echo "==========================================="
echo ""

# Check required files
required_files=(
    "backend/app/main.py"
    "backend/app/core/config.py"
    "backend/app/models/schemas.py"
    "backend/app/routes/travel.py"
    "backend/app/services/agent_service.py"
    "backend/app/services/llm_service.py"
    "backend/app/tools/classifier_tool.py"
    "backend/app/tools/rag_tool.py"
    "backend/app/tools/weather_tool.py"
    "frontend/src/App.jsx"
    "frontend/src/main.jsx"
    "frontend/src/App.css"
    "frontend/package.json"
    "docker-compose.yml"
    "backend/Dockerfile"
    "frontend/Dockerfile"
    "pyproject.toml"
    "README.md"
)

echo "📋 Checking required files..."
missing=0
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (MISSING)"
        missing=$((missing + 1))
    fi
done

echo ""
if [ $missing -eq 0 ]; then
    echo -e "${GREEN}✅ All required files present!${NC}"
else
    echo -e "${RED}❌ Missing $missing file(s)${NC}"
fi

echo ""
echo "📝 Next steps:"
echo "1. Copy backend/.env.example to backend/.env"
echo "2. Add your API keys to backend/.env:"
echo "   - GOOGLE_API_KEY"
echo "   - LANGCHAIN_API_KEY"
echo "3. Run: docker-compose up --build"
echo "4. Visit: http://localhost:3000"
echo ""
echo "For detailed setup instructions, see SETUP.md"
