#!/bin/bash
# 1. Activate the isolated environment
source virt-env/bin/activate

# 2. Set defaults for RunPod environment
# If SATURN_GPUS_PER_NODE is empty, use the number of GPUs detected by nvidia-smi
DETECTOR_GPUS=$(nvidia-smi -L | wc -l)
NUM_GPUS=${SATURN_GPUS_PER_NODE:-$DETECTOR_GPUS}

# If SATURN variables are missing, default to a standalone single node
NODE_RANK=${SATURN_NODE_RANK:-0}
MASTER_ADDR=${SATURN_MASTER_ADDR:-"127.0.0.1"}
NUM_NODES=${SATURN_NUM_NODES:-1}

echo "🚀 Starting Distributed Training on RunPod..."
echo "📊 GPUs detected/used: $NUM_GPUS"
echo "🌐 Node Rank: $NODE_RANK"

# 3. Launch with torchrun
# Use --standalone for single-node RunPod testing
torchrun \
    --nproc_per_node=$NUM_GPUS \
    --nnodes=$NUM_NODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --master_port=12355 \
    src/train_fsdp.py