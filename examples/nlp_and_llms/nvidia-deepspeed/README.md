# DeepSpeed ZeRO-3 Training
This template provides a robust environment for training large-scale Transformer models (like GPT-2 Large) using **DeepSpeed ZeRO-Stage 3**. By partitioning model parameters, gradients, and optimizer states across multiple GPUs, this setup overcomes the memory limitations of a single device.

For more information on the underlying platform, visit the [Saturn Cloud Documentation](https://saturncloud.io/docs/).
## 📂 Project Structure

* **`setup_saturn.sh`**: Environment initialization script to install DeepSpeed and dependencies.
* **`src/train_transformers.py`**: Main training script using Hugging Face `Trainer` and DeepSpeed.
* **`ds_config_zero3.json`**: Configuration file for ZeRO-3 sharding and CPU offloading.
* **`run_job.sh`**: Distributed training launcher script.
* **`test_inference.py`**: Optimized generation script using DeepSpeed Inference kernels.

---

## 🚀 Complete Procedure

### 1. Environment Setup

Before running any code, you must initialize the virtual environment to install the necessary DeepSpeed and Torch libraries. Refer to the [Saturn Cloud Docs for Setup Guide](https://saturncloud.io/docs/) for advanced configuration.

```bash
chmod +x setup_saturn.sh
./setup_saturn.sh

```

### 2. Hardware Preparation

To prevent filesystem errors during kernel compilation on Saturn Cloud's distributed architecture, create the Triton autotune directory:

```bash
mkdir -p /root/.triton/autotune

```

### 3. Training Execution

Launch the training process across your GPUs using the provided job script:

```bash
./run_job.sh

```

* **The "Silent Phase"**: Note that ZeRO-3 requires a period of "silence" (usually 2-5 minutes for GPT-2) while it shards the model parameters before the first step appears.
* **Automatic Consolidation**: The script is configured to automatically gather sharded 16-bit weights into a single `model.safetensors` file upon saving.

### 4. Inference Testing

After training completes and a checkpoint folder (e.g., `checkpoint-65`) is created, run the optimized inference test.

**Update `test_inference.py`:**
Ensure the `model_path` variable matches your checkpoint folder:

```python
model_path = "./checkpoints/checkpoint-65"

```

**Launch Inference:**
Ensure the virtual environment is activated and then run the python test script:

```bash
python test_inference.py

```

---

## 🛠️ Key Configurations

### ZeRO-3 Optimization (`ds_config_zero3.json`)

* **`stage3_gather_16bit_weights_on_model_save`**: Set to `true` to ensure your checkpoints are saved in a standard format for easy testing.
* **`overlap_comm`**: Set to `false` in this template to maximize stability and prevent deadlocks on virtualized interconnects.

### Training Stability (`src/train_transformers.py`)

* **NCCL Flags**: The script forces `NCCL_P2P_DISABLE=1` to ensure reliable communication on cloud-based GPU clusters.
* **Data Collator**: Uses `DataCollatorForLanguageModeling` to handle padding and ensure uniform tensor shapes during training, preventing "ValueError" crashes.

---

## 📈 Scaling Guide

To scale from the verified test to a production-level run:

1. **Model**: Change `model_id` to `"gpt2-large"` in `src/train_transformers.py`.
2. **Dataset**: Remove the `[:1%]` slice to train on the full dataset.
3. **Sequence Length**: Increase `max_length` to `512` or `1024` in the `tokenize_function`.

For more community support, visit the [Saturn Cloud Community Slack](https://www.google.com/search?q=https://saturncloud.io/community/).

---