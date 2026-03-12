# 🚀 NIM / TGI Server — Drop-In API

**Tech Stack:** NVIDIA NIM + TGI (Text Generation Inference)
**Built for:** Saturn Cloud Custom Templates
➡️ [https://saturncloud.io/](https://saturncloud.io/)

---

## 🧠 Overview

This template provides a **plug-and-play inference server** that supports **two interchangeable LLM backends**:

| Backend              | Description                                                  | Use Case                                                        |
| -------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| **NVIDIA NIM Cloud** | Fully hosted LLMs on NVIDIA's high-performance GPU cloud     | High-accuracy, large models (Qwen 80B, Mistral, Nemotron, etc.) |
| **Local TGI Server** | Lightweight local model running via HuggingFace Transformers | Fast prototyping, offline usage                                 |

The API exposes **the same unified interface** for both backends, so users can switch engines without changing frontend code.

This is ideal for **Saturn Cloud Data Science workflows**, allowing teams to quickly integrate LLM inference inside their notebooks, pipelines, or applications.

---

# 📂 Project Structure

```
NIM-TGI-Server/
│
├── server.py               # Main FastAPI server (unified interface)
├── backend_tgi.py          # Local TGI backend (SmolLM)
├── backend_nim.py          # NVIDIA cloud backend
├── cli.py                  # CLI tool (select backend from terminal)
├── requirements.txt
└── README.md               # (this file)
```

---

# ⚙️ 1. Environment Setup

## **Create and activate a virtual environment**

### Linux / MacOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## **Install dependencies**

```bash
pip install -r requirements.txt
```

---

# 🔑 2. Getting a NVIDIA NIM API Key

To use the **NIM Cloud backend**, you need an **NVIDIA AI Foundation API Key**.

### Steps:

1. Visit:
   👉 [https://build.nvidia.com/explore/discover](https://build.nvidia.com/explore/discover)
2. Sign in with NVIDIA account
3. Open your "API Keys" panel
4. Click **Create New API Key**
5. Copy the key
6. **Paste it into `backend_nim.py`**, replacing:

```python
API_KEY = "nvapi-xxxxxxxxxxxxxxxxxxxx"
```

⚠️ **Note:**
This template currently embeds the key directly for simplicity, but in production you should store it in environment variables or a secret manager.

---

# 🧠 3. Backend Models

## **A. NVIDIA NIM Backend (Cloud)**

* Model used: `qwen/qwen3-next-80b-a3b-instruct`
* Endpoint: `https://integrate.api.nvidia.com/v1`
* Requires API Key
* Supports streaming + large prompts

## **B. Local TGI Backend (Lightweight CPU/GPU)**

* Model: `HuggingFaceTB/SmolLM-1.7B-Instruct`
* Runs entirely inside Python (no Docker needed)
* Great for local experimentation

---

# 🚀 4. Running the Server

Start FastAPI server:

```bash
uvicorn server:app --reload
```

You’ll see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

# 🧪 5. Testing the Server

## A. Test Local TGI Model

**POST /chat/local**

### Curl:

```bash
curl -X POST -F "prompt=Explain machine learning" http://localhost:8000/chat/local
```

### Expected Response:

```json
{
  "backend": "tgi-local",
  "response": "Machine learning is..."
}
```

---

## B. Test NVIDIA NIM Model

**POST /chat/nim**

### Curl:

```bash
curl -X POST -F "prompt=Write a short poem" http://localhost:8000/chat/nim
```

### Streaming:

```bash
curl -N -X POST -F "prompt=Tell me a story" -F "stream=true" http://localhost:8000/chat/nim
```

---

# 🖥️ 6. Command-Line Interface (CLI)

The template includes a **CLI wrapper**:

### Local TGI:

```bash
python cli.py --backend local "Explain photosynthesis"
```

### NVIDIA NIM:

```bash
python cli.py --backend nim "Write 5 facts about Jupiter"
```

Streaming output works automatically.

---

# 💡 7. Using with Saturn Cloud

This template is designed as a **plug-and-play server component** inside Saturn Cloud:

* Run the server inside a Jupyter workspace
* Use the API from notebooks or external apps
* Swap between local inference (TGI) and cloud inference (NIM)
* Ideal for ML research, RAG systems, agent development, and batch inference jobs

Saturn Cloud provides scalable Jupyter environments with GPUs:
👉 [https://saturncloud.io/](https://saturncloud.io/)

---

# ✔️ 8. Summary

This template provides:

### **✔ A drop-in inference server**

Supports both NVIDIA Cloud NIM and local TGI backends.

### **✔ Ready to use in Saturn Cloud**

Works inside a GPU instance or CPU instance.

### **✔ Unified API**

Same route structure for both engines.

### **✔ Full CLI + server support**

### **✔ Ideal foundation for:**

* Chatbots
* RAG pipelines
* Model comparison apps
* AI feature development
* ML/DS experimentation