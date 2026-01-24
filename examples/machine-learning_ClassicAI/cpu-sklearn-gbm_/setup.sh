#!/bin/bash
set -e

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Python Server Setup...${NC}"

# 1. robust Python Detection
# We check for 'python3' first, then 'python'
if command -v python3 &> /dev/null; then
    PY_CMD="python3"
elif command -v python &> /dev/null; then
    PY_CMD="python"
else
    echo -e "${RED}❌ Error: Could not find 'python3' or 'python' in your PATH.${NC}"
    echo "Please install Python 3 before continuing."
    exit 1
fi

echo -e "✅ Found Python executable: ${BLUE}$PY_CMD${NC}"

# 2. Create Virtual Environment
echo -e "${BLUE}📦 Creating Virtual Environment 'venv'...${NC}"
$PY_CMD -m venv venv

# 3. Install Dependencies
echo -e "${BLUE}⬇️  Installing libraries...${NC}"
source venv/bin/activate
pip install --upgrade pip
# Installing all required libraries for the Demo + API
pip install scikit-learn pandas numpy matplotlib seaborn fastapi uvicorn joblib

echo -e "${GREEN}✅ Environment Ready!${NC}"
echo "-------------------------------------------------------"
echo "To run the full pipeline:"
echo "1. Train & Save Model:  python baseline.py"
echo "2. Start API Server:    python app.py"
echo "-------------------------------------------------------"