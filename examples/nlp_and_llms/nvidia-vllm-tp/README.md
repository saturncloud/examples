# **vLLM Server for Meta-Llama-3-70B-Instruct**

This template provides a **production-ready deployment environment** on **Saturn Cloud** to serve the **Meta-Llama-3-70B-Instruct** model using the high-performance **vLLM** inference engine and a FastAPI web API.

➡️ **Saturn Cloud lets you quickly launch multi-GPU machines to run large-scale models like Llama-3 70B. Learn more:**
[https://saturncloud.io](https://saturncloud.io)

---

## **🔎 Overview**

The **Meta-Llama-3-70B-Instruct** model is a powerful open-source LLM from Meta AI.
This template demonstrates how to deploy it efficiently using:

* **Model:** `meta-llama/Meta-Llama-3-70B-Instruct`
* **Inference Engine:** vLLM
* **API Interface:** FastAPI (OpenAI-compatible)
* **Precision:** bfloat16
* **Parallelism:** Tensor Parallelism across 4 GPUs
* **Use Cases:** Chatbots, RAG systems, model serving backends, enterprise AI apps

vLLM provides optimized **PagedAttention**, **continuous batching**, and multi-GPU scaling—resulting in **significantly faster inference** compared to HuggingFace Transformers.

---

## **💻 Requirements & Setup**

Running a 70B parameter model requires substantial hardware and proper authentication.

---

### **1. Hardware Requirements**

To run Llama-3 70B with vLLM, you need:

| Component              | Minimum Requirement                                |
| ---------------------- | -------------------------------------------------- |
| **GPUs**               | 4× GPUs (A40 48GB, RTX 3090/4090, or 2× A100 80GB) |
| **VRAM**               | ~140GB total (bfloat16 precision)                  |
| **Disk Space**         | **150GB+** to store model weights                  |
| **Tensor Parallelism** | `tensor_parallel_size = 4`                         |

This template is suited for Saturn Cloud multi-GPU instances.

---

### **2. Hugging Face Authentication (Required)**

Llama-3 models are **license-restricted** ("gated").
You must authenticate before downloading.

#### **Steps:**

1. **Accept the License**
   Visit:
   [https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct)

2. **Log in via CLI**

   ```bash
   hf auth login
   ```

   Paste your HF access token.

3. **Token in Script**
   A placeholder token is included for testing, but **you must use your own token** in production.


---

### **3. Environment Setup**

#### Create & activate your Python environment:

```bash
python3 -m venv env
source env/bin/activate
```

#### Install dependencies:

```bash
pip install -r requirements.txt
```

All required libraries (vLLM, FastAPI, Uvicorn, HF Hub support) are included inside `requirements.txt`.

---

## **🚀 Running the Model**

### **Step 1 — Start the API Server**

Launch the vLLM FastAPI server:

```bash
python start_server.py
```

You will see logs for:

* GPU detection
* Model download progress
* Tensor parallel initialization
* Engine warm-up

When ready:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Your vLLM server is now live and accepting OpenAI-style requests.

---

### **Step 2 — Test Using the Client Script**

In a separate terminal window:

```bash
source env/bin/activate
python test_client.py
```

You will receive a JSON response similar to:

```json
{
  "choices": [
    {
      "message": {
        "content": "Tensor parallelism is a technique that..."
      }
    }
  ]
}
```

This confirms the vLLM server is functioning correctly.

---

## **📌 Notes for Saturn Cloud Users**

This template is ideal for running on **Saturn Cloud GPU clusters**, which provide:

* Multi-GPU instances compatible with vLLM
* Prebuilt CUDA, NCCL, Python environments
* Fast storage needed for models of this size
* Ability to schedule long-running inference servers

➡️ Learn more or launch GPU resources: [https://saturncloud.io](https://saturncloud.io)

---

## **🏁 Conclusion**

This template demonstrates how to deploy **Meta-Llama-3-70B-Instruct** efficiently using the **vLLM inference engine** with **tensor parallelism** across multiple GPUs.
It provides a fast and scalable foundation for real-world applications such as chat systems, RAG pipelines, or large-scale AI services.

By combining vLLM’s optimizations with infrastructure from **Saturn Cloud**, you get a robust, production-grade environment for serving massive open-source LLMs.

