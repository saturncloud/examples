import os
import sys
import time
import functools
import torch
import torch.distributed as dist
import torch.nn as nn
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

# FSDP Specific Imports
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    MixedPrecision,
    ShardingStrategy,
    CPUOffload,
    StateDictType,      
    FullStateDictConfig,
)
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from transformers.models.gpt2.modeling_gpt2 import GPT2Block
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import (
    checkpoint_wrapper,
    CheckpointImpl,
    apply_activation_checkpointing,
)



def setup():
    """Initializes the distributed process group for NCCL."""
    dist.init_process_group("nccl")

def cleanup():
    """Cleans up the distributed process group."""
    dist.destroy_process_group()

def log_stats(epoch, batch_idx, loss, start_time):
    """Logs training progress, throughput, and GPU memory efficiency."""
    if dist.get_rank() == 0:
        # 1. Calculate Throughput (Samples per Second)
        elapsed = time.time() - start_time
        samples_per_sec = (batch_idx + 1) * 4 * dist.get_world_size() / elapsed
        
        # 2. Get Memory Metrics in GB
        peak_mem = torch.cuda.max_memory_allocated() / (1024 ** 3) 
        reserved_mem = torch.cuda.memory_reserved() / (1024 ** 3)

        print(f"| Epoch: {epoch} | Batch: {batch_idx} | Loss: {loss:.4f} |")
        print(f"| Speed: {samples_per_sec:.2f} samples/sec | Peak Mem: {peak_mem:.2f} GB | Reserved: {reserved_mem:.2f} GB |")
        print("-" * 60)

def train_one_epoch(model, dataloader, optimizer, epoch):
    model.train()
    start_time = time.time()
    
    # --- CONFIGURATION FOR QUICK TESTING ---
    save_every_n_steps = 100    # Save a checkpoint every 100 steps
    max_total_steps = 300      # Stop training completely after 300 steps
    # ----------------------------------------

    for batch_idx, batch in enumerate(dataloader):
        if batch_idx >= max_total_steps:
            if dist.get_rank() == 0:
                print(f"🛑 Reached max steps ({max_total_steps}). Terminating training.")
            return # Exit the function and stop training

        input_ids = batch["input_ids"].to(torch.cuda.current_device())
        optimizer.zero_grad()
        loss = model(input_ids, labels=input_ids).loss
        loss.backward()
        optimizer.step()
        
        if batch_idx % 10 == 0:
            log_stats(epoch, batch_idx, loss.item(), start_time)

        # Save Checkpoint
        if batch_idx > 0 and batch_idx % save_every_n_steps == 0:
            if dist.get_rank() == 0:
                os.makedirs("checkpoints", exist_ok=True)
                checkpoint_path = f"checkpoints/gpt2_step_{batch_idx}.bin"
                # Standard FSDP state dict gathering
                with FSDP.state_dict_type(model, StateDictType.FULL_STATE_DICT):
                    state_dict = model.state_dict()
                    torch.save(state_dict, checkpoint_path)
                print(f"💾 Checkpoint saved at {checkpoint_path}")


def main():
    setup()
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)

    # 1. Load Data: WikiText-103
    dataset = load_dataset("wikitext", "wikitext-103-v1", split="train")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    tokenized_dataset.set_format("torch")
    
    sampler = DistributedSampler(tokenized_dataset, num_replicas=dist.get_world_size(), rank=dist.get_rank())
    dataloader = DataLoader(tokenized_dataset, batch_size=4, sampler=sampler)

    # 2. Configure FSDP Policies
    # Use BF16 Mixed Precision for Ampere (A100/H100) efficiency
    mp_policy = MixedPrecision(param_dtype=torch.bfloat16, reduce_dtype=torch.bfloat16)
    
    gpt2_auto_wrap_policy = functools.partial(
        transformer_auto_wrap_policy,
        transformer_layer_cls={GPT2Block},
    )

    # 3. Initialize and Wrap Model
    model = AutoModelForCausalLM.from_pretrained("gpt2").to(local_rank)
    
    model = FSDP(
        model,
        auto_wrap_policy=gpt2_auto_wrap_policy,
        mixed_precision=mp_policy,
        sharding_strategy=ShardingStrategy.FULL_SHARD, # Max memory efficiency
        device_id=local_rank
    )

    # 4. Apply Activation Checkpointing to each Transformer Block
    non_reentrant_wrapper = functools.partial(checkpoint_wrapper, offload_to_cpu=False)
    for module in model.modules():
        if isinstance(module, GPT2Block):
            module = non_reentrant_wrapper(module)

    # 5. Initialize Optimizer AFTER FSDP Wrapping
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

    # 6. Execute Training
    for epoch in range(1):
        train_one_epoch(model, dataloader, optimizer, epoch)

    cleanup()

if __name__ == "__main__":
    main()