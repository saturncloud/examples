# Small Transformer Inference (CPU Baseline)

This template implements a **CPU-optimized inference** workflow for Natural Language Processing (NLP). It utilizes **DistilBERT**, a compressed version of the BERT architecture, and demonstrates optimization via **Dynamic Quantization** to achieve low-latency performance on CPU-only infrastructure.

**Infrastructure:** [Saturn Cloud](https://saturncloud.io/)
**Resource:** Jupyter Notebook
**Hardware:** CPU
**Tech Stack:** PyTorch, Hugging Face Transformers, Scikit-Learn

---

## 📖 Overview

Large Language Models (LLMs) often require high-memory GPUs, specific tasks like **Sentiment Analysis** or **Named Entity Recognition (NER)** can be executed effectively using "distilled" transformers. These models offer reduced computational overhead and lower operational costs on standard CPU hardware.

This repository provides a **CPU-optimized baseline**:

1. **Sentiment Analysis:** Utilizing `distilbert-base-uncased`.
2. **Named Entity Recognition (NER):** Utilizing `distilbert-base-cased`.
3. **Optimization:** Implements PyTorch **Dynamic Quantization** to increase inference throughput by ~2x and reduce memory footprint by ~40%.

---

## 🚀 Quick Start

### 1. Workflow

1. Open **`small_transformer_cpu.ipynb`** in the Jupyter interface.
2. **Run All Cells**:

* **Install:** Installs `transformers` and `torch` dependencies.
* **Download:** Pulls the DistilBERT weights from the Hugging Face Hub.
* **Benchmark (FP32):** Measures the baseline latency of the standard 32-bit floating point model.
* **Quantize (INT8):** Converts linear layer weights to 8-bit integers during runtime.
* **Compare:** Evaluates the execution speedup (typically **1.5x - 2.0x**).

---

## 🧠 Architecture: "Distill & Quantize"

The implementation uses a two-stage optimization strategy to maximize efficiency on commodity hardware.

### 1. Distillation

**DistilBERT** is a student model trained to approximate the output distributions of the larger BERT model.

* **40% fewer parameters** than BERT.
* **60% reduction** in inference latency.
* **97% accuracy retention** on standard GLUE benchmarks.

### 2. Dynamic Quantization

Standard model weights are stored as 32-bit floating point numbers (FP32). This workflow uses **Dynamic Quantization** to convert linear layer weights to **8-bit integers (INT8)**.

* **Size Reduction:** Reduces the model binary size by ~40% (e.g., 255MB → 130MB).
* **Speedup:** Leverages CPU-optimized integer arithmetic to reduce latency per request compared to floating-point operations.

---

## 🏁 Conclusion

This implementation demonstrates that specialized NLP tasks can be served efficiently on CPU hardware. A quantized DistilBERT model can support high-throughput request processing without the requirement for GPU acceleration.

To scale this workload—for batch processing or deployment as a production API—this workflow can be migrated to a [Saturn Cloud](https://saturncloud.io/) CPU cluster.