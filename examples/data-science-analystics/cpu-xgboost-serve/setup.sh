#!/bin/bash

# Define colors for output
GREEN='\033[0-32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting setup for XGBoost Train & Serve...${NC}"

# 1. Create Virtual Environment
echo "Creating virtual environment 'venv_xgboost'..."
python3 -m venv venv_xgboost

# 2. Activate Environment and Install Requirements
echo "Installing dependencies from requirements.txt..."
source venv_xgboost/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Initial Model Training
echo "Performing initial model training on Titanic dataset..."
python train.py

echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "To start the server, run:"
echo "source venv_xgboost/bin/activate && uvicorn main:app --reload"