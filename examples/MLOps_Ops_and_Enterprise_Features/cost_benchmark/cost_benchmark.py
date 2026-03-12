import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
import logging
import sys
import numpy as np

# --- Configuration & Constants ---
# Use the correct GPU pricing for your cloud provider (e.g., Saturn Cloud, AWS, GCP)
# Example: NVIDIA A100 pricing (approximate, for demonstration)
GPU_HOURLY_RATE = 100000  # $/hour for a high-end GPU (Must be updated manually)
LOG_FILE = "benchmark_results.log"

# Hyperparameters for the simulated job
EPOCHS = 5
BATCH_SIZE = 32
TOTAL_SAMPLES = 50000 
TOTAL_TOKENS_PER_SAMPLE = 100 # Represents tokens in an NLP task or features in an image
TOTAL_TOKENS = TOTAL_SAMPLES * TOTAL_TOKENS_PER_SAMPLE

# --- Custom Logger Setup ---

def setup_logger():
    """Configures the logger to write structured output to a file."""
    # Create the logger object
    logger = logging.getLogger('BenchmarkLogger')
    logger.setLevel(logging.INFO)
    
    # Define a custom format that includes time and specific placeholders
    # We use a custom format to easily parse the final report later
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s'
    )
    
    # File Handler
    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console Handler (for real-time feedback)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger

# --- Model & Timing Functions ---

class SimpleModel(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)
    def forward(self, x):
        return self.linear(x)

def run_training_benchmark(logger, device):
    
    logger.info(f"--- STARTING BENCHMARK ON {device.type.upper()} ---")
    
    # Configuration based on device
    INPUT_SIZE = 512
    OUTPUT_SIZE = 1
    
    # Model and Data Setup (on the target device)
    model = SimpleModel(INPUT_SIZE, OUTPUT_SIZE).to(device)
    dummy_input = torch.randn(BATCH_SIZE, INPUT_SIZE, device=device)
    dummy_target = torch.randn(BATCH_SIZE, OUTPUT_SIZE, device=device)
    optimizer = optim.Adam(model.parameters())
    criterion = nn.MSELoss()

    # Total estimated cost
    total_estimated_cost = 0.0

    # Synchronization is crucial for accurate GPU timing
    if device.type == 'cuda':
        # Warm-up run is necessary to avoid compilation time bias
        logger.info("Performing CUDA warm-up run...")
        _ = model(dummy_input)
        torch.cuda.synchronize()

    # Start timing the entire job
    job_start_time = time.time()
    
    for epoch in range(1, EPOCHS + 1):
        
        if device.type == 'cuda':
            # Use synchronized CUDA events for precise timing
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)
            start_event.record()
        else:
            start_event = time.time()
        
        # --- Simulated Training Step ---
        optimizer.zero_grad()
        output = model(dummy_input)
        loss = criterion(output, dummy_target)
        loss.backward()
        optimizer.step()
        # --- End Simulated Training Step ---

        if device.type == 'cuda':
            end_event.record()
            torch.cuda.synchronize() # Wait for GPU to finish
            # elapsed_time returns milliseconds, convert to seconds
            epoch_time_s = start_event.elapsed_time(end_event) / 1000.0
        else:
            epoch_time_s = time.time() - start_event
            
        # --- COST AND PERFORMANCE CALCULATION ---
        
        # 1. Cost Calculation
        cost_per_epoch = (epoch_time_s / 3600.0) * GPU_HOURLY_RATE
        total_estimated_cost += cost_per_epoch

        # 2. Performance Calculation (Throughput)
        throughput_samples_sec = BATCH_SIZE / epoch_time_s
        throughput_tokens_sec = (BATCH_SIZE * TOTAL_TOKENS_PER_SAMPLE) / epoch_time_s
        
        # --- LOGGING THE RESULTS ---
        logger.info(
            f"EPOCH: {epoch}/{EPOCHS} | "
            f"Time: {epoch_time_s:.4f}s | "
            f"Cost: ${cost_per_epoch:.5f} | "
            f"Tokens/s: {throughput_tokens_sec:.0f}"
        )

    job_total_time = time.time() - job_start_time
    
    # --- FINAL REPORT ---
    logger.info("--- JOB SUMMARY ---")
    logger.info(f"FINAL_COST: ${total_estimated_cost:.4f}")
    logger.info(f"TOTAL_TIME: {job_total_time:.2f}s")
    logger.info(f"TOTAL_TOKENS_PROCESSED: {TOTAL_TOKENS * EPOCHS}")
    logger.info(f"-------------------")


def main():
    logger = setup_logger()
    logger.info(f"Configuration: GPU Hourly Rate = ${GPU_HOURLY_RATE}/hr")

    # 1. Check for GPU availability
    if torch.cuda.is_available():
        device = torch.device("cuda")
        logger.info("GPU detected. Running GPU Benchmark.")
    else:
        device = torch.device("cpu")
        logger.warning("GPU not detected. Running CPU Benchmark.")

    run_training_benchmark(logger, device)

if __name__ == "__main__":
    main()