#!/bin/bash
# 1. Update system and install virtual environment tools
apt-get update && apt-get install -y python3-venv python3-pip ninja-build

# 2. Create and activate the virtual environment
python3 -m venv virt-env
source virt-env/bin/activate

# 3. Install core dependencies
# We recommend installing deepspeed from source for best hardware matching
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install "transformers[deepspeed]>=4.31.0" datasets accelerate tqdm

# 4. Optional: Install DeepSpeed with optimized ops
# This step builds the C++/CUDA extensions required for high performance
DS_BUILD_OPS=1 pip install deepspeed

# 5. Pre-cache dataset to prevent network timeouts during training
echo "📦 Pre-caching WikiText-2 dataset..."
python3 -c "from datasets import load_dataset; load_dataset('wikitext', 'wikitext-2-raw-v1', cache_dir='./data')"

echo "✅ Saturn Cloud Environment Setup Complete."