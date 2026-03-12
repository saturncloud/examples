# ⚡ **FastAPI Embeddings Service (FAISS + Transformers)**

*A Jupyter notebook example template demonstrating how to build a lightweight embeddings and semantic search API using FastAPI, FAISS, and Transformers — all running interactively within [Saturn Cloud](https://saturncloud.io/).*

---
This is perfect for quickly prototyping or demonstrating **retrieval-based workflows** on **[Saturn Cloud](https://saturncloud.io/)**.

---

## ⚙️ **1. Install Dependencies**

> First, install all required Python libraries.
> These packages handle embedding generation, FAISS indexing, and API serving.

```python
!pip install torch transformers sentence-transformers faiss-cpu fastapi uvicorn[standard] pydantic requests numpy
```
---

## 🧩 **2. Load Embedding Model and Initialize FAISS**

> We load a pre-trained SentenceTransformer model (`all-MiniLM-L6-v2`)
> and initialize a FAISS index to store embeddings in memory.

> FAISS (Facebook AI Similarity Search) provides an efficient vector index for fast nearest-neighbor queries.

---

## 🧠 **3. Define Core Embedding and Search Functions**

> These helper functions form the “machine” behind the API:
>
> * `add_text()`: Encodes a new text and stores it in FAISS
> * `search_texts()`: Finds similar texts to a given query

---

## ⚡ **4. Create the FastAPI Application**

> Now we wrap the embedding and search logic into a FastAPI service.
> It exposes three main endpoints:
>
> * `/add_text`: Add and embed new text
> * `/search`: Retrieve similar texts
> * `/healthz`: API health check

---

## 🌐 **5. Run the API Server Inside Jupyter**

> Since Jupyter runs its own event loop, we launch Uvicorn in a **background thread**.

---

## ▶️ **6. Start the FastAPI Service**

> Launch the service.
> Once it starts, open your browser to **[http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)** to explore the Swagger UI.

```python
start_api_in_thread()
```

---

## 🧪 **7. Test the API**

> We can interact with the service directly from the notebook using HTTP requests.
> Try adding a text and then searching for semantically similar content.

### ➕ Add Text

```python
requests.post("http://127.0.0.1:8002/add_text",
              json={"text": "The quick brown fox jumps over the lazy dog."}).json()
```

### 🔍 Search Texts

```python
requests.post("http://127.0.0.1:8002/search",
              json={"query": "A fast brown animal jumps over a sleepy dog", "top_k": 3}).json()
```

---

## ⏹️ **8. Stop the API**

> When you’re done testing, stop the running FastAPI service gracefully.

```python
stop_api()
```

---

## ☁️ **9. Run This Template on Saturn Cloud**

This notebook is designed for **[Saturn Cloud](https://saturncloud.io/)** — it runs entirely inside Jupyter, without needing an external process.

**To deploy:**

1. Create a new **Jupyter Server** resource on Saturn Cloud.
2. Upload this notebook and install dependencies.
3. Run the cells sequentially.
4. Open **Port 8002** in your Saturn environment to access the running API.
5. Use `/add_text` and `/search` to interact with your live embeddings service.

🔗 Learn more at: [https://saturncloud.io/docs](https://saturncloud.io/docs)

---

## 🙌 **Credits**

Built with ❤️ using:

* 🤗 **Transformers**
* 🧮 **FAISS**
* ⚡ **FastAPI**
* 🧠 **SentenceTransformers**
* ☁️ **[Saturn Cloud](https://saturncloud.io/)**