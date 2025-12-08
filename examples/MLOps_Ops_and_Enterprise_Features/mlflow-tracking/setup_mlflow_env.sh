#!/bin/bash

ENV_NAME="mlflow_gpu_env_stable"
PYTHON_VERSION="3.12" 
CUDA_VERSION="12" 

echo "================================================="
echo "🚀 Setting up MLflow GPU Tracking Environment (Python $PYTHON_VERSION)"
echo "================================================="

# --- 1. Create and Activate Stable VENV ---
rm -rf $ENV_NAME
python$PYTHON_VERSION -m venv $ENV_NAME
source $ENV_NAME/bin/activate
echo "✅ Virtual Environment created and activated."

# --- 2. Install Core Libraries ---
echo "--- Installing Core MLflow and PyTorch Libraries ---"

# Install PyTorch (GPU version for CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install MLflow and helper libraries
pip install mlflow==2.11.3 numpy scikit-learn pandas

# --- 3. Replace Deprecated PYNVML for System Metrics ---
echo "--- Replacing deprecated pynvml with nvidia-ml-py ---"

# Uninstall old package (if it exists)
pip uninstall -y pynvml 

# Install the correct GPU monitoring package and prerequisites
pip install psutil nvidia-ml-py

echo "--- Installation Complete ---"
echo "✅ Environment is ready. Run 'source $ENV_NAME/bin/activate' before executing the Python script."