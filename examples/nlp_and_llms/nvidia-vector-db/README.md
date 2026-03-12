
# 🚀 **Vector DB Menu (FAISS • Zilliz Milvus • Neon PGVector)**

> A unified FastAPI search service that lets you test and compare **FAISS (local)**, **Milvus (Zilliz Cloud free tier)**, and **PostgreSQL with PGVector (Neon free tier)** using a common API.

🔗 **Built for the Saturn Cloud AI Community**
👉 [https://saturncloud.io/](https://saturncloud.io/)

---

## 🧠 Overview

This project loads a public dataset (State of the Union speeches), embeds it with `sentence-transformers/all-MiniLM-L6-v2`, stores vectors in **three different databases**, and exposes a **FastAPI endpoint** to query them interchangeably.

### ✅ What’s included:

* FAISS (local in-memory vector search)
* Milvus (via **Zilliz Cloud free tier**)
* PostgreSQL + PGVector (via **Neon free tier**)
* FastAPI for querying all 3 backends
* CLI & Browser UI testing
* Modular, deploy-ready architecture

---

## ⚠️ Free-Tier Credentials Notice

This repo includes **working test credentials** for quick validation.
However, because they are **free-tier**, they may:

⚠️ expire at any time
⚠️ be rate-limited
⚠️ be deleted automatically

✅ You are **strongly encouraged to create your own accounts** using the setup guide below.

---

---

# 🛠️ **1. Project Setup**

### Clone Repository

```sh
git clone https://github.com/your-repo/nvidia-vector-db.git
cd nvidia-vector-db
```

---

### Create and Activate Virtual Environment

#### Windows (PowerShell)

```sh
python -m venv vectordb-env
vectordb-env\Scripts\activate
```

#### macOS / Linux

```sh
python3 -m venv vectordb-env
source vectordb-env/bin/activate
```

---

### Install Dependencies

```sh
pip install -r requirements.txt
```

---

# ☁️ **2. Create Neon (PostgreSQL + PGVector) Free Account**

1. Visit: [https://neon.tech/](https://neon.tech/)
2. Click **Sign Up** (free tier)
3. Create a new project
4. Go to **Dashboard → Connection Details**
5. Copy the connection string:

   ```
   postgresql://<user>:<password>@<host>.neon.tech/<db>?sslmode=require
   ```
6. Edit it to SQLAlchemy format for this project:

   ```
   postgresql+psycopg2://<user>:<password>@<host>.neon.tech/<db>?sslmode=require
   ```

---

# ☁️ **3. Create Zilliz Cloud (Milvus) Free Account**

1. Visit: [https://cloud.zilliz.com/signup](https://cloud.zilliz.com/signup)
2. Create account (Free tier)
3. Create a new **Serverless cluster**
4. Go to **API Keys**
5. Copy:

   * `Public Endpoint (URI)`
   * `API Key (Token)`

Example:

```
ZILLIZ_URI=https://in03-xxxx.serverless.aws-eu-central-1.cloud.zilliz.com
ZILLIZ_TOKEN=xxxxxxxxxxxxxxxxxxxx
```

---

# 🧩 **4. Configure Environment Variables**

Create a `.env` file in the project root:

```
PG_CONNECTION=postgresql+psycopg2://your-user:your-pass@your-host.neon.tech/your-db?sslmode=require

ZILLIZ_URI=https://your-zilliz-endpoint.serverless.aws-xyz.cloud.zilliz.com
ZILLIZ_TOKEN=your-zilliz-api-key
```

> ⚠️ You may test with the current free credentials included in the code, but replace them when creating yours.

---

# 🧱 **5. Load Dataset & Build Vector Stores**

Run:

```sh
python data_loader.py
```

Expected output:

```
✅ Split into X chunks
🚀 Loading FAISS...
🚀 Connecting to Zilliz Cloud...
🚀 Connecting to PGVector (Neon)...
✅ All vector stores ready!
```

---

# 🚀 **6. Start the FastAPI Server**

```sh
uvicorn app:app --reload
```

Server should start at:

```
http://127.0.0.1:8000
```

Swagger UI (API testing interface):

```
http://127.0.0.1:8000/docs
```

---

# 🧪 **7. Test the API**

## ✅ Browser UI (Swagger)

1. Open: `http://127.0.0.1:8000/docs`
2. Go to **POST /search**
3. Test queries like:

```json
{
  "db": "faiss",
  "query": "Who talked about peace?",
  "k": 3
}
```

Try other DBs:

```json
{ "db": "milvus", "query": "war economy", "k": 3 }
{ "db": "pgvector", "query": "mars mission", "k": 3 }
```

---

## ✅ CLI Testing with `curl`

```sh
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"db":"faiss", "query":"state of the economy", "k":2}'
```

```sh
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"db":"milvus", "query":"foreign policy", "k":2}'
```

```sh
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"db":"pgvector", "query":"education reform", "k":2}'
```

---

# 🧬 Supported Vector Backends

| Backend           | Type           | Notes                                |
| ----------------- | -------------- | ------------------------------------ |
| **FAISS**         | Local          | Fastest, no cloud, resets on restart |
| **Zilliz Milvus** | Cloud          | Free tier, scalable, best for prod   |
| **Neon PGVector** | Cloud Postgres | SQL + vectors, persistent, queryable |


# 🌎 About Saturn Cloud

If you're experimenting with **GPU workloads, LLM inference, vector search, or MLOps**, check out the best community platform for AI builders:

🔗 **[https://saturncloud.io/](https://saturncloud.io/)**

