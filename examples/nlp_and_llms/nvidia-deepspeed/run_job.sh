#!/bin/bash
source virt-env/bin/activate
# Automatically uses all detected GPUs for ZeRO-3 sharding
deepspeed src/train_transformers.py