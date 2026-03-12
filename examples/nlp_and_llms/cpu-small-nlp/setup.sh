#!/bin/bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting Small Transformer Setup...${NC}"

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
echo "📦 Creating Virtual Environment 'venv'..."
$PY_CMD -m venv venv

# 3. Install Dependencies
echo "⬇️  Installing libraries..."
. venv/bin/activate
pip install --upgrade pip
# Core stack: PyTorch (CPU), Transformers (Hugging Face), Scikit-Learn (Metrics)
pip install torch transformers scikit-learn numpy pandas

echo -e "${GREEN}✅ Environment Ready!${NC}"
echo "-------------------------------------------------------"
echo "To generate the notebook:"
echo "   $PY_CMD generate_notebook.py"
echo "-------------------------------------------------------"