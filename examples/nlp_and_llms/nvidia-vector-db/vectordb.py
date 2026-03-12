import os
from langchain_community.vectorstores import FAISS
from langchain_postgres.vectorstores import PGVector
from langchain_milvus import Milvus
from pymilvus import connections
from sqlalchemy import create_engine


from data_loader import load_and_chunk
from embed import get_embeddings

# Load data + embeddings
docs = load_and_chunk()
embeddings = get_embeddings()

# ---------- FAISS ----------
print("🚀 Loading FAISS...")
faiss_db = FAISS.from_documents(docs, embeddings)

# ---------- Milvus (Zilliz) ----------
print("🚀 Connecting to Zilliz Cloud...")
connections.connect(
    alias="default",
    uri=os.getenv("ZILLIZ_URI"),
    token=os.getenv("ZILLIZ_TOKEN")
)
milvus_db = Milvus.from_documents(
    docs,
    embeddings,
    collection_name="state_union_collection",
    connection_args={"alias": "default"},
)

# ---------- PGVector ----------
print("🚀 Connecting to PGVector...")
NEON_CONN = os.getenv("PG_CONNECTION")  # must contain full neon URL
print("🚀 Connecting to Neon PGVector...")
engine = create_engine(NEON_CONN)

pg_db = PGVector.from_documents(
    docs,
    embeddings,
    connection=engine,
    collection_name="state_union_pg"
)

print("✅ PGVector (Neon) loaded!")

print("✅ All vector DBs ready!")

# Generic search method
def search(db: str, query: str, k: int = 3):
    if db == "faiss":
        return faiss_db.similarity_search(query, k)
    if db == "milvus":
        return milvus_db.similarity_search(query, k)
    if db == "pgvector":
        return pg_db.similarity_search(query, k)
    return []
