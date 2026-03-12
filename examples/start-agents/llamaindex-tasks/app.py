import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI

# Initialize environment variables
load_dotenv()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="Task Assistant | LlamaIndex RAG",
    page_icon="⚙️",
    layout="centered",
)

st.title("LlamaIndex Task Assistant")
st.markdown("Retrieval-Augmented Generation interface for local task data.")

# Verify Environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Environment Error: OPENAI_API_KEY is not defined.")
    st.stop()

# --- CORE RAG PIPELINE ---
@st.cache_resource(show_spinner=False)
def initialize_query_engine():
    """Reads local data and initializes the vector index. Caches the output."""
    data_dir = "./data"
    
    if not os.path.exists(data_dir) or not os.listdir(data_dir):
        st.error(f"Initialization Error: The '{data_dir}' directory is missing or empty.")
        st.stop()
        
    # Configure deterministic LLM settings
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    
    # Ingest and Index
    documents = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    
    return index.as_query_engine()

# Initialize the engine
with st.spinner("Building vector index from local data..."):
    query_engine = initialize_query_engine()

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Vector index initialized. What information do you need regarding your tasks?"}
    ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- EXECUTION LOGIC ---
if prompt := st.chat_input("Query your localized data..."):
    
    # Append and render user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Execute RAG query and render response
    with st.chat_message("assistant"):
        try:
            response = query_engine.query(prompt)
            st.markdown(response.response)
            
            # Append final output to state
            st.session_state.messages.append({"role": "assistant", "content": response.response})
            
        except Exception as e:
            st.error(f"API Execution Error: {str(e)}")