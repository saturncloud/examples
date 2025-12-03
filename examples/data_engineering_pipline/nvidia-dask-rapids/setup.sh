#!/bin/bash

ENV_NAME="dask_rapids_etl_venv"
CUDA_VERSION="12" # Based on nvcc output (12.8)

# 1. Create venv
rm -rf $ENV_NAME
python3 -m venv $ENV_NAME

# --- CRITICAL FIX: Set LD_LIBRARY_PATH immediately inside the environment ---
# This ensures the active shell session finds the CUDA libraries (12.8) that nvcc confirmed exist.
source $ENV_NAME/bin/activate
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:/usr/local/cuda/lib64:${LD_LIBRARY_PATH}" 
echo "✅ LD_LIBRARY_PATH set for active environment."

# --- 2. Install Core ETL Packages (Dask + RAPIDS cu12) ---
echo "--- Installing Core ETL Packages (Dask + RAPIDS cu12) ---"

# Install Dask and core libraries
pip install pandas numpy dask distributed

# Install core RAPIDS packages explicitly targeting CUDA 12 (cu12)
# We trust the NVIDIA index to provide the compatible 25.10 wheel for CUDA 12.8.
pip install \
    --extra-index-url=https://pypi.nvidia.com \
    "cudf-cu${CUDA_VERSION}==25.10.*" \
    "dask-cudf-cu${CUDA_VERSION}==25.10.*" \
    "dask-cuda"

echo "--- Installation Complete ---"
echo "✅ Core packages installed. Run 'python dask_hybrid_etl.py' now."