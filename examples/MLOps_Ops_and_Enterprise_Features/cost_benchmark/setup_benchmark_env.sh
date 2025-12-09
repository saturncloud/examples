#!/bin/bash

ENV_NAME="cost_benchmark_env"
PYTHON_VERSION="3.12" 

echo "--- Setting up Cost/Performance Benchmark Environment ---"

# 1. Create and Activate Stable VENV
rm -rf $ENV_NAME
python$PYTHON_VERSION -m venv $ENV_NAME
source $ENV_NAME/bin/activate

# 2. Install PyTorch (GPU version for CUDA 12)
# We need PyTorch for accurate CUDA timing events.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. Install Helpers
pip install numpy pandas psutil

echo "✅ Environment setup complete."