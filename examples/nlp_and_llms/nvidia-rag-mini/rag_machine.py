# rag_machine.py
from pathlib import Path
import os
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import chromadb

# --------------------------
# 🔧 Configuration
# --------------------------
CHROMA_DIR = "rag_chroma_store"
DATA_DIR = Path("data")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

DATA_DIR.mkdir(exist_ok=True)
Path(CHROMA_DIR).mkdir(exist_ok=True)

# --------------------------
# ⚙️ Initialize Components
# --------------------------
print("🚀 Loading models...")
embedder = SentenceTransformer(EMBED_MODEL)
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
llm = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("rag_docs")

# --------------------------
# 📚 Document Loader
# --------------------------
def load_all_documents(data_dir: Path):
    docs = []
    for file in data_dir.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                docs.append({"file": file.name, "text": text})
                print(f"📄 Loaded: {file.name}")
    return docs

# --------------------------
# 🔢 Index Documents
# --------------------------
def index_documents(reindex: bool = False):
    """Rebuild or load existing document embeddings."""
    if reindex:
        print("♻️ Reindexing documents...")
        try:
            collection.reset()
            print("🧹 Cleared existing collection.")
        except AttributeError:
            ids = collection.get()["ids"]
            if ids:
                collection.delete(ids=ids)
                print("🧹 Deleted existing documents manually.")

        docs = load_all_documents(DATA_DIR)
        for i, d in enumerate(docs):
            emb = embedder.encode(d["text"])
            collection.add(
                ids=[str(i)],
                documents=[d["text"]],
                embeddings=[emb.tolist()],
                metadatas=[{"source": d["file"]}],
            )
        print("✅ Documents reindexed and stored in Chroma.")
    else:
        print("📦 Using existing Chroma store.")


# --------------------------
# 🔍 Query System
# --------------------------
def query_docs(question: str, top_k: int = 3):
    """Retrieve top-k relevant docs and generate an answer."""
    print(f"\n🔍 Question: {question}")

    # Embed the query and search
    q_emb = embedder.encode(question).tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=top_k)

    if not results["documents"]:
        return "No relevant documents found."

    context = "\n".join(results["documents"][0])
    prompt = f"Answer based on the following context:\n{context}\n\nQuestion: {question}"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = llm.generate(**inputs, max_length=512)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer

# --------------------------
# 🧪 CLI Test Mode
# --------------------------
if __name__ == "__main__":
    print("🧠 Starting RAG Machine (Transformers + Chroma)...")
    index_documents(reindex=True)

    while True:
        q = input("\n❓ Enter your question (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        try:
            ans = query_docs(q)
            print(f"\n💬 {ans}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")
