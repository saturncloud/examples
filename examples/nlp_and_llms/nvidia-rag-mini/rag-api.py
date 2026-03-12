from fastapi import FastAPI
from pydantic import BaseModel
from rag_machine import query_docs, index_documents

app = FastAPI(title="RAG Mini Docs Q&A")

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
def startup_event():
    index_documents(reindex=False)

@app.post("/query")
def query(req: QueryRequest):
    answer = query_docs(req.query)
    return {"result": answer}
