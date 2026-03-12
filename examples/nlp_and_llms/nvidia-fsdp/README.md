# 🚀 GPT-2 FSDP Training & Inference Template

This repository provides a production-ready setup for fine-tuning GPT-2 on the WikiText-103 dataset using **Fully Sharded Data Parallel (FSDP)**. It is designed for researchers who need to validate models quickly without running exhaustive training cycles.

### ✨ Key Features

* **FSDP Optimization**: Efficiently shards model parameters across available GPUs.
* **Automated Lifecycle**: Training automatically saves checkpoints every 100 steps and terminates after 3 saves to manage cloud costs.
* **Dynamic Disk Management**: Automatically cleans up old checkpoints to prevent storage exhaustion.
* **Robust Inference**: A dedicated validation script that identifies and loads the latest healthy checkpoint.

---

## 🛠️ 1. Setup and Environment

Initialize your environment once per Saturn Cloud resource to install dependencies and cache the dataset.

### Procedural Setup

1. **Permissions**: Make the utility scripts executable.
```bash
chmod +x setup_saturn.sh run_job.sh

```


2. **Environment Build**: This script creates the `virt-env` and pre-downloads the WikiText shards to the local `./data` folder.
```bash
./setup_saturn.sh

```



---

## 🏃 2. Running the Model

### A. Distributed Training

Launch the training process using the job runner. It automatically handles distributed initialization.

```bash
./run_job.sh

```

* **What to Expect**: The console will log Loss and VRAM metrics every 10 steps.
* **Checkpointing**: Every 100 steps, a `.bin` file is saved to the `checkpoints/` directory.
* **Auto-Termination**: The script exits gracefully after saving 3 checkpoints.

### B. Validation Inference

You can test the model as soon as the first checkpoint is saved.

```bash
source virt-env/bin/activate
python test_inference.py

```

**Expected Result**:
The script will load the latest `.bin` file and generate a text completion.

> **Output example**:
> `🔄 Attempting to load: checkpoints/gpt2_wikitext_epoch0_step100.bin`
> `✅ Successfully loaded: checkpoints/gpt2_wikitext_epoch0_step100.bin`
> `--- Result ---`
> `The history of WikiText is a collection of high-quality articles used for benchmarking language models...`

---

## 📂 Project Structure

* **`checkpoints/`**: Auto-managed directory for model weights.
* **`src/train_fsdp.py`**: Core logic for sharding and training.
* **`test_inference.py`**: Script for model weight validation.
* **`data/`**: Local cache for the WikiText-103 dataset.

---

## 🌐 Powered by Saturn Cloud

This template is built to run seamlessly on the **[Saturn Cloud Platform](https://saturncloud.io/)**. For advanced scaling, multi-node configurations, or persistent storage volumes, refer to the **[Saturn Cloud Documentation](https://saturncloud.io/docs/)**.
