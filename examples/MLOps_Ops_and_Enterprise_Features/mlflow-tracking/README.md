# 📈 MLflow Experiment Tracking Template (GPU Ready)

## 🌟 Overview

This template provides a robust, reproducible framework for **tracking Deep Learning experiments** on GPU-accelerated hardware. It leverages **MLflow Tracking** to automatically log hyperparameters, model artifacts, and vital **GPU system utilization metrics** (memory, temperature, and usage) during the training process.

This system is essential for comparing model performance and hardware efficiency across different runs—a key capability for MLOps on platforms like **Saturn Cloud**.

### Key Features

  * **GPU Readiness:** Dynamically detects and utilizes available CUDA devices.
  * **Automatic Tracking:** Uses `mlflow.pytorch.autolog()` to capture hyperparameters and model architecture.
  * **System Metrics:** Logs GPU/CPU usage and memory over time using `log_system_metrics=True`.
  * **Centralized UI:** Easy verification and comparison of runs via the **MLflow UI table**.

-----

## 🛠️ How to Run the Template

### 1\. Project Setup (Bash Script)

This script sets up a stable Python environment, installs PyTorch, MLflow, and the necessary GPU monitoring packages (`nvidia-ml-py`).

#### File: `setup_mlflow_env.sh`

#### Step A: Grant Execution Permission

In your terminal, grant executable permission to the setup script.

```bash
chmod +x setup_mlflow_env.sh
```

#### Step B: Execute the Setup

Run the script to install all dependencies.

```bash
./setup_mlflow_env.sh
```

-----

### 2\. Procedures (Execution & Monitoring)

#### Step C: Activate the Environment

You must do this every time you open a new terminal session.

```bash
source mlflow_gpu_env_stable/bin/activate
```

#### Step D: Configure Tracking Location

The template uses the environment variable `MLFLOW_TRACKING_URI` to determine where to log data.

| Mode | Configuration (Terminal Command) | Use Case |
| :--- | :--- | :--- |
| **Local (Default)** | (No command needed) | Development and testing where logs are written to the local `mlruns/` folder. |
| **Remote (Server)** | `export MLFLOW_TRACKING_URI="http://<server-ip-or-host>:5000"` | Production jobs requiring centralized, shared tracking (e.g., **Saturn Cloud Managed MLflow**). |

#### Step E: Run the Tracking Sample

Execute the main pipeline script (`train_and_track.py`).

```bash
python train_and_track.py
```

#### Step F: Verification (Checking Tracked Data)

  * **Local UI Access:** If running locally, start the UI server:
    ```bash
    mlflow ui --host 0.0.0.0 --port 5000
    ```
    Then, access the exposed IP and port in your browser.
  * **Remote UI Access:** Navigate to the host address of your remote tracking server. The **MLflow UI Table** will display the run, confirming successful logging of all parameters, metrics, and **GPU utilization** (see image above).

-----

## 4\. 🔗 Conclusion and Scaling on Saturn Cloud

This template successfully creates a fully observable training environment, fulfilling the core requirements of MLOps for GPU-accelerated workloads. All run details—from hyperparameters to **GPU utilization metrics**—are now centralized and ready for comparison.

To maximize performance, streamline infrastructure management, and integrate MLOps practices, deploy this template on **Saturn Cloud**:

  * **Official Saturn Cloud Website:** [Saturn Cloud](https://saturncloud.io/)
  * **MLOps Guide:** Saturn Cloud enables a robust MLOps lifecycle by simplifying infrastructure, scaling, and experiment tracking. [A Practical Guide to MLOps](https://saturncloud.io/docs/design-principles/concepts/mlops/)
  * **GPU Clusters:** Easily provision and manage GPU-equipped compute resources, including high-performance NVIDIA A100/H100 GPUs, directly within **Saturn Cloud**. [Saturn Cloud Documentation](https://saturncloud.io/docs/user-guide/)

**Start building your scalable MLOps pipeline today on Saturn Cloud\!**