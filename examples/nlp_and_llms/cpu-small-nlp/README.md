# Small Transformer Inference (CPU Baseline)

This template implements a **high-efficiency CPU inference** workflow for Natural Language Processing (NLP). It uses **DistilBERT**, a smaller, faster version of BERT, and demonstrates how to further optimize it using **Dynamic Quantization** to achieve production-grade performance without GPUs.

**Infrastructure:** [Saturn Cloud](https://saturncloud.io/)
**Resource:** Jupyter Notebook
**Hardware:** CPU
**Tech Stack:** PyTorch, Hugging Face Transformers, Scikit-Learn

---

## 📖 Overview

Deploying massive Large Language Models (LLMs) often requires expensive GPUs. However, for specific enterprise tasks like **Sentiment Analysis** or **Named Entity Recognition (NER)**, smaller "distilled" transformers running on standard CPUs are often sufficient, faster, and significantly cheaper.

This template provides a **CPU-optimized baseline**:
1.  **Sentiment Analysis:** Using `distilbert-base-uncased`.
2.  **Named Entity Recognition (NER):** Using `distilbert-base-cased`.
3.  **Optimization:** Applies PyTorch **Dynamic Quantization** to boost inference speed by ~2x and reduce memory usage by ~40%.

---

## 🚀 Quick Start

### 1. Workflow

1. Open **`small_transformer_cpu.ipynb`** in the Jupyter interface.
2. **Run All Cells**:
* **Install:** Sets up `transformers` and `torch` in the current environment.
* **Download:** Fetches the public DistilBERT model (no login required).
* **Benchmark (FP32):** Measures the baseline latency of the standard 32-bit floating point model.
* **Quantize (INT8):** Converts the model weights to 8-bit integers on the fly.
* **Compare:** Validates the speedup (typically **1.5x - 2.0x faster**).

---

## 🧠 Architecture: "Distill & Quantize"

We use a two-step optimization strategy to ensure the model runs efficiently on commodity hardware.

### 1. Distillation

We use **DistilBERT**, which acts as a student model trained to mimic the behavior of the larger BERT model.

* **40% fewer parameters** than BERT.
* **60% faster** inference.
* **97% retained accuracy** on standard benchmarks.

### 2. Dynamic Quantization

Standard models store weights as 32-bit floating point numbers (FP32). This template uses **Dynamic Quantization** to convert the linear layer weights to **8-bit integers (INT8)**.

* **Size Reduction:** The model file shrinks by ~40% (e.g., 255MB → 130MB).
* **Speedup:** CPUs can process 8-bit integer math significantly faster than 32-bit float math, resulting in lower latency per request.

---

## 🏁 Conclusion

This template proves that you don't always need a GPU for NLP. For targeted tasks, a quantized DistilBERT on a modern CPU can handle hundreds of requests per second with minimal cost.

To scale this solution—for example, processing millions of documents or deploying this as a serverless API—consider moving this workload to a [Saturn Cloud](https://saturncloud.io/) CPU cluster.

```

