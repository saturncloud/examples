#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Auto-ML Setup...${NC}"

# 1. Robust Python Detection
if command -v python3 &> /dev/null; then
    PY_CMD="python3"
elif command -v python &> /dev/null; then
    PY_CMD="python"
else
    echo "❌ Error: Could not find 'python3' or 'python' in your PATH."
    exit 1
fi

# 2. Create Virtual Environment
echo -e "${BLUE}📦 Creating Virtual Environment 'venv'...${NC}"
$PY_CMD -m venv venv

# 3. Install Dependencies
echo -e "${BLUE}⬇️  Installing libraries...${NC}"
. venv/bin/activate
pip install --upgrade pip
# Core stack: Ray Tune (HPO), Optuna (Search), FastAPI (Serving), Scikit-Learn (Model)
pip install "ray[tune]" "optuna>=3.0.0" scikit-learn pandas numpy fastapi uvicorn joblib

echo -e "${GREEN}✅ Environment Ready!${NC}"
echo "-------------------------------------------------------"
echo "1. Tune & Save Model:   python tune_hpo.py"
echo "2. Serve Model:         python app.py"
echo "-------------------------------------------------------"