import os
import dask
import pandas as pd
import numpy as np
import time

# --- Dask-CUDA/RAPIDS Imports ---
# These imports rely on the 'cudf-cu12' and 'dask-cuda' packages
from dask_cuda import LocalCUDACluster
from dask.distributed import Client
import cudf
import dask_cudf

# --- Configuration ---
# LocalCUDACluster will autodetect GPUs, but we calculate the count for partitioning.
# If you wanted to restrict to GPUs 0 and 1, you would use: CUDA_VISIBLE_DEVICES="0,1"
# N_GPUS = int(os.environ.get('CUDA_VISIBLE_DEVICES', '0').count(',')) + 1 

try:
    visible_devices = os.environ.get('CUDA_VISIBLE_DEVICES')
    if visible_devices:
        N_GPUS = len(visible_devices.split(','))
    else:
        # Fallback if the variable isn't set, so you can input Your GPU number here
        N_GPUS = 2
except Exception:
    N_GPUS = 2

# Define a reasonable synthetic workload size (e.g., 2 GB)
FILE_SIZE_MB = 2048 

# --- ETL Logic ---

def generate_data(size_mb, n_partitions):
    """
    E: Extract (Simulate large data creation)
    Generates synthetic data on the CPU, then transfers it to Dask-cuDF on the GPU.
    """
    n_rows = int((size_mb * 1024 * 1024) / 8 / 5) 
    print(f"Generating ~{n_rows / 1e6:.1f} Million rows of data...")
    
    # Create the base DataFrame using Pandas (on CPU)
    df_cpu = pd.DataFrame({
        'user_id': np.random.randint(0, 500_000, n_rows),
        'timestamp_s': np.random.randint(1609459200, 1640995200, n_rows),
        'revenue': np.random.rand(n_rows) * 100,
        'region': np.random.choice(['East', 'West', 'Central'], n_rows),
    })
    
    # Convert to Dask DataFrame, partitioned by the number of available GPUs
    ddf_base = dask.dataframe.from_pandas(df_cpu, npartitions=n_partitions)
    
    # Map partitions to cuDF: CRITICAL STEP to move data to GPU memory
    ddf_gpu = ddf_base.map_partitions(cudf.from_pandas).persist()
    print(f"✅ Data generated, loaded, and persisted across {n_partitions} GPU(s) as Dask-cuDF.")
    
    return ddf_gpu

def run_etl(ddf_in):
    """
    T: Transform (GPU-accelerated operations)
    Performs filtering, feature engineering, and aggregation on the GPUs.
    """
    
    print("\n--- Starting Multi-GPU ETL ---")
    
    # 1. Filter and Persist
    ddf_filtered = ddf_in[
        (ddf_in['revenue'] > 50.0) & 
        (ddf_in['region'] == 'East')
    ].persist()
    print("   - Filtering complete. Persisting intermediate result.")
    
    # 2. Feature Engineering: Calculate log-transformed revenue
    ddf_derived = ddf_filtered.assign(
        log_revenue=np.log(ddf_filtered['revenue'])
    )
    
    # 3. Aggregation: Use standard dictionary aggregation syntax
    ddf_grouped = ddf_derived.groupby('user_id').agg({
        'revenue': 'sum',
        'log_revenue': 'mean',
        'timestamp_s': 'count'
    })
    
    # Rename the columns explicitly after aggregation for clarity (L: Load)
    ddf_grouped = ddf_grouped.rename(columns={
        'revenue': 'total_revenue',
        'log_revenue': 'avg_log_revenue',
        'timestamp_s': 'transaction_count'
    })

    # Trigger computation
    start_time = time.time()
    result_df_cpu = ddf_grouped.compute() 
    end_time = time.time()
    
    print("--- ETL Complete ---")
    print(f"Total GPU processing time: {end_time - start_time:.4f} seconds.")
    return result_df_cpu

# --- Main Execution ---
def main():
    cluster = None
    client = None
    
    # 1. Start the Dask Multi-GPU Cluster
    try:
        print(f"Starting LocalCUDACluster with {N_GPUS} GPU worker(s)...")
        cluster = LocalCUDACluster(n_workers=N_GPUS) 
        client = Client(cluster)
        
        print(f"🌐 Dask Dashboard link: {client.dashboard_link}")
        print(f"Cluster started with {len(client.scheduler_info()['workers'])} GPU worker(s).")
        
        # 2. Extract Data
        ddf_in = generate_data(FILE_SIZE_MB, N_GPUS)
        
        # 3. Transform and Load
        result_df_cpu = run_etl(ddf_in)
        
        # 4. Final Output and Verification
        print("\n=== Final Aggregated Result (CPU Pandas) ===")
        print(result_df_cpu.head())
        
    except Exception as e:
        print(f"\n❌ An error occurred during Dask-CUDA execution.")
        print(f"Error: {e}")
        
    finally:
        # 5. Cleanup: Critical step to release GPU memory and resources
        if client:
            client.close()
        if cluster:
            cluster.close()
        print("\n🛑 Dask Cluster shutdown.")

if __name__ == "__main__":
    main()