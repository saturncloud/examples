#!/bin/bash
# 1. Update system packages
apt update && apt install -y python3-venv

# 2. Create the virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv virt-env

# 3. Activate the environment
source virt-env/bin/activate

# 4. Install high-performance libraries
echo "🚀 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Environment ready."