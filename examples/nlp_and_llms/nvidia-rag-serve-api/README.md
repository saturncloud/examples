# 📘 Ray Serve LLM API — Qwen 1.5B (vLLM)

This template shows how to deploy a **Qwen2.5-1.5B-Instruct LLM** using:

* **Ray Serve**
* **vLLM**
* **OpenAI-compatible API format**

You get a local inference server running at:

```
http://127.0.0.1:8000/v1/chat/completions
```

This template is designed for **Saturn Cloud custom templates** so users can plug-and-play LLM inference environments with GPU acceleration.

🔗 **Back to Saturn Cloud → [https://saturncloud.io](https://saturncloud.io)**

---

## 🚀 Features

* Fully OpenAI-compatible API endpoint
* Deploys Qwen 1.5B using vLLM (fast inference)
* Simple Ray Serve deployment
* Example client request included
* Clean and minimal code structure
* Works inside Jupyter or full terminal environment

---

## 📦 Requirements

The notebook installs everything automatically:

```
torch
transformers
ray[serve, llm]
fastapi
uvicorn
requests
huggingface_hub
```

GPU recommended for optimal performance.

---

## 📁 Project Structure

```
nvidia-rag-serve-api/
│
└── ray_serve_llm_template.ipynb   # Full Jupyter notebook template (generated)
```

---

## ▶️ How It Works

### 1. Write your Ray Serve deployment file

Defines:

* Model ID (`Qwen2.5-1.5B-Instruct`)
* Engine config
* Autoscaling
* OpenAI-compatible app

### 2. Start Ray and deploy the model

Ray Serve loads the model via vLLM and exposes the API.

### 3. Send a test request

JSON API format identical to OpenAI:

```python
payload = {
    "model": "qwen-1.5b",
    "messages": [{"role": "user", "content": "Explain API design."}]
}
```

### 4. Extract the assistant text

```python
res = out.json()["choices"][0]["message"]["content"]
```

---

## 🏁 Conclusion

This template provides a clean, reproducible Ray Serve LLM deployment that works both in Jupyter and full terminal mode.
You can adapt it to larger models, scale it across nodes, or wrap it inside FastAPI.

🔗 **Back to Saturn Cloud → [https://saturncloud.io](https://saturncloud.io)**

---

