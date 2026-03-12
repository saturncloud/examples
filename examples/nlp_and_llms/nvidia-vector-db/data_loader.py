from datasets import load_dataset
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_chunk():
    print("📥 Loading dataset...")
    ds = load_dataset("jsulz/state-of-the-union-addresses")

    texts = [row["speech_html"] for row in ds["train"]]
    docs = [Document(page_content=t) for t in texts]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)
