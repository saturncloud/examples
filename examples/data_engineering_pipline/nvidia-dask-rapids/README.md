# 🚀 Dask-CUDA Multi-GPU ETL Template

## 🌟 Overview

This template provides an efficient, scalable solution for performing **Extract, Transform, and Load (ETL)** operations on datasets that are too large to fit in the memory of a single GPU or distributed GPU. It uses the **Dask** parallel computing library to orchestrate workers across multiple **NVIDIA GPUs**, leveraging the **RAPIDS cuDF** library for GPU-accelerated operations.

This architecture ensures maximum speedup for tasks involving filtering, feature engineering, and complex aggregations.

### Key Technologies

  * **Dask Distributed:** Handles cluster management and task scheduling across all GPUs.
  * **cuDF:** The GPU DataFrame library that provides a Pandas-like API for blazing-fast transformations.
  * **LocalCUDACluster:** Automatically configures one Dask worker per available GPU.
  * **Target Environment:** Linux with **CUDA Toolkit 12.x** installed (e.g., RunPod, AWS, or any **Saturn Cloud GPU instance**).

-----

## 🛠️ How to Run the Code

This template requires a specific setup to ensure the Python packages correctly link to the underlying NVIDIA CUDA libraries.

### 1\. Create the Environment

The `setup_env.sh` script creates an isolated Python virtual environment (`venv`), installs all necessary libraries, and sets the critical CUDA library paths.

```bash
#!/bin/bash

ENV_NAME="dask_rapids_etl_venv"
CUDA_VERSION="12" 

# 1. Create venv
rm -rf $ENV_NAME
python3 -m venv $ENV_NAME
echo "✅ Virtual Environment created."

...
```

**Execution:** Run the script once in your terminal:

```bash
bash setup_env.sh
```

-----

### 2\. Procedures (Job Execution)

Once the setup script finishes, follow these steps in your terminal.

#### Step A: Activate the Environment

You must do this every time you open a new terminal or shell session.

```bash
source dask_rapids_etl_venv/bin/activate
```

#### Step B: Run the ETL Pipeline

Save the main Python code as `dask_cuda_etl.py` and execute it.

```bash
python dask_cuda_etl.py
```

The script will automatically perform the following steps:

1.  **Cluster Startup:** Launch the `LocalCUDACluster` and create Dask workers (one per detected GPU, defaulting to 2 workers if the device count isn't explicitly set - note that you can easily change this to suite your resources availability).
2.  **Extraction:** Generate synthetic data and move it from CPU to GPU memory (`cudf.from_pandas`).
3.  **Transformation:** Execute GPU-accelerated filtering (`ddf_filtered`), log transformation (`np.log`), and distributed aggregation (`ddf_grouped`).
4.  **Load:** The final result is collected back to a CPU Pandas DataFrame using `.compute()`.

-----

## 3\. 🎯 Configuration

The template defaults to **2 GPUs**. If your machine has more or fewer visible GPUs, you can override the variable at the top of the `dask_cuda_etl.py` script:

```python
# --- Configuration Section in dask_cuda_etl.py ---
# To force 3 GPUs, change the default:
# N_GPUS = 3 

# try:
#     visible_devices = os.environ.get('CUDA_VISIBLE_DEVICES')
#     if visible_devices:
#         N_GPUS = len(visible_devices.split(','))
#     else:
#         # Fallback if the variable isn't set, so you can input Your GPU number here
#         N_GPUS = 2
# except Exception:
#     N_GPUS = 2
```

### Scaling and Deployment on Saturn Cloud

This template is an ideal starting point for production data science workflows. To move beyond local testing and leverage true scalability, we recommend deploying this project on **Saturn Cloud**:

  * **Scalable Clusters:** Easily provision GPU clusters with multiple nodes (not just multiple GPUs on a single node) for true cluster computing. [Learn about Saturn Cloud Clusters](https://saturncloud.io/docs/#about-saturn-cloud).
  * **Managed Environments:** Avoid complex `LD_LIBRARY_PATH` issues by using Saturn Cloud's fully managed RAPIDS/CUDA environment. [Explore Saturn Cloud Resources](https://saturncloud.io/docs/enterprise/).
  * **Production Jobs:** Schedule this exact Python script as a recurring job on Saturn Cloud for automated ETL processing. [Set up a Saturn Cloud Job](https://www.saturncloud.io/docs/).

-----

## 🎉 Conclusion

This template successfully demonstrates the power of parallel, GPU-accelerated computing for ETL. By leveraging the **Dask-CUDA** framework, we transform a large dataset in seconds, showcasing massive speedups compared to traditional CPU-bound pipelines. This foundation is essential for processing the large data volumes encountered in modern ML and analytics tasks, providing a seamless pathway to scaling up on **Saturn Cloud**.