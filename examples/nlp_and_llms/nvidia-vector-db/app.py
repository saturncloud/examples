from fastapi import FastAPI
from pydantic import BaseModel
from vectordb import search

app = FastAPI(title="RAG Vector DB Compare API")

class QueryRequest(BaseModel):
    db: str  # faiss | milvus | pgvector
    query: str
    k: int = 3

@app.post("/search")
def search_vectors(req: QueryRequest):
    results = search(req.db.lower(), req.query, req.k)
    return {
        "db": req.db,
        "query": req.query,
        "results": [r.page_content[:400] for r in results]
    }
