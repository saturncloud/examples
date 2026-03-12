# 🧠 RAG Mini Docs Q&A

A lightweight **Retrieval-Augmented Generation (RAG)** system that lets you drop `.txt` files into a folder and ask natural-language questions about them.

This template combines:

* **SentenceTransformers** for document embeddings
* **ChromaDB** for vector storage & retrieval
* **🤗 Transformers (FLAN-T5)** for answer generation
* **FastAPI** for serving an interactive Q&A API

Designed for fast prototyping and educational use on **[Saturn Cloud](https://saturncloud.io/)**.

---

## 🚀 1. Get Started – Understand the Folder Layout

Before you start coding, review the project structure below.
Each file serves a clear role; ensure you’re working from the correct one.

```
NVIDIA_RAG-MINI/
├─ data/                 # Folder for your .txt documents
│   └─ saturndoc.txt     # Sample document included for testing
├─ rag_machine.py        # Core logic: embeddings, Chroma, QA engine
├─ rag-api.py            # REST API built with FastAPI
└─ requirements.txt
```

👉 **Action:** Create or upload `.txt` files into the `data/` folder before running the template.
A sample file named **`saturndoc.txt`** is already included — you can use it immediately to test model training and query responses.

---

## 🧩 2. Set Up the Environment

To run this project, you’ll need Python ≥ 3.10.
If you’re using **Saturn Cloud**, create a new environment and install dependencies from `requirements.txt`.

### ✍️ Step-by-step

```bash
# (optional) create a fresh virtual environment
python -m venv rag-env
source rag-env/bin/activate   # or .\rag-env\Scripts\activate on Windows

# install dependencies
pip install -r requirements.txt
```

### 📦 requirements.txt

```text
torch>=2.2.0
transformers>=4.44.0
sentence-transformers>=3.0.0
chromadb>=0.5.0
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
tqdm>=4.66.0
```

👉 **Action:** Run the install command inside your active environment before executing any Python file.

---

## ⚙️ 3. Configure Models and Paths

All configuration happens inside **`rag_machine.py`**.
Defaults are already suitable for most cases:

```python
CHROMA_DIR   = "rag_chroma_store"                  # Persistent database for embeddings
DATA_DIR     = Path("data")                        # Directory containing your .txt files
EMBED_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL    = "google/flan-t5-base"
```

👉 **Action:**
If you want faster inference, you can change `LLM_MODEL` to `google/flan-t5-small`.
If you have a GPU, keep `flan-t5-base` or try `flan-t5-large`.

---

## 💻 4. Run in CLI Mode – Test the RAG Machine

Use this mode for quick experimentation.
The script loads models, indexes your `.txt` files, and opens an interactive prompt.

```bash
python rag_machine.py
```

You’ll see output similar to:

```
🧠 Starting RAG Machine (Transformers + Chroma)...
♻️ Reindexing documents...
📚 Indexing 5 documents...
✅ Indexed 5 documents successfully.
📊 Current collection size: 5 documents
❓ Enter your question (or 'exit'):
```

👉 **Action:**
Type a question like
`What is this project about?`
and the model will respond based on your documents.

> You can use the included **`saturndoc.txt`** file for your first run — it’s already in the `data/` folder and serves as a ready-made example for testing and model training.

---

## 🌐 5. Run as an API – Serve Questions via HTTP

Now, let’s turn your RAG engine into a service.
Start the FastAPI server with Uvicorn:

```bash
uvicorn rag-api:app --reload
```

Once running, open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
to explore the built-in Swagger interface.

### 🧭 Endpoints

| Endpoint               | Method | Description                                        |
| ---------------------- | ------ | -------------------------------------------------- |
| `/query`               | POST   | Submit a question and get an answer                |
| `/reload` *(optional)* | POST   | Reindex `.txt` files without restarting the server |

### Example Query

```bash
curl -X POST "http://127.0.0.1:8000/query" \
     -H "Content-Type: application/json" \
     -d "{\"query\": \"What does the onboarding doc say?\"}"
```

Response:

```json
{
  "result": "The onboarding doc explains the project setup and data structure."
}
```

👉 **Action:** Use `/query` to test, and `/reload` whenever you add new `.txt` files.

---

## 🔍 6. How It Works (Conceptually)

1. **Document Loading** – Reads all `.txt` files from `data/`.
2. **Embedding Generation** – Converts text into dense vectors using SentenceTransformers.
3. **Vector Storage** – Saves these embeddings persistently in **ChromaDB** (`rag_chroma_store/`).
4. **Retrieval** – Finds the most relevant text chunks for your query.
5. **LLM Answering** – Passes retrieved context + query into **FLAN-T5** to generate the final answer.

👉 **Action:** Skim through `rag_machine.py` to see how each step is implemented—you can easily swap models or add chunking later.

---

## 🔁 7. Reindex vs Reuse

* **`reindex=True`** → Clears and rebuilds embeddings from scratch
* **`reindex=False`** → Loads existing persistent store (faster)

```python
index_documents(reindex=True)   # rebuild everything
index_documents(reindex=False)  # reuse old vectors
```

👉 **Action:**
Use reindexing only after you add or update text files in `data/`.
The included **`saturndoc.txt`** is already indexed by default when you run the script for the first time — so you can test immediately without adding new documents.

---

## 🧩 8. Best Practices

* Keep each text file focused on one topic for cleaner retrieval.
* For long documents, consider manually splitting them into sections.
* If using CPU only, choose smaller models for faster inference.
* Delete the `rag_chroma_store/` folder to fully reset the database.

---

## 🛰️ 9. Deploying on Saturn Cloud

You can easily host this on **Saturn Cloud**:

1. Create a new Jupyter or VS Code resource.
2. Upload this project folder.
3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```
4. Run `python rag_machine.py` to test indexing.
5. Launch the API:

   ```bash
   uvicorn rag-api:app --host 0.0.0.0 --port 8000
   ```
6. Expose port **8000** in your Saturn environment to access it externally.

👉 Learn more about Saturn Cloud and GPU-accelerated workflows at **[https://saturncloud.io](https://saturncloud.io)**

---

## 🙌 Credits

Built with ❤️ using:

* 🤗 **Transformers**
* 🧠 **SentenceTransformers**
* 💾 **ChromaDB**
* ⚡ **FastAPI**
* and hosted proudly on **[Saturn Cloud](https://saturncloud.io/)**