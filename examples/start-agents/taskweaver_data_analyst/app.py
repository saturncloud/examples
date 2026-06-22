import streamlit as st
import os
from src.agent import DataAnalystAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="TaskWeaver Data Analyst", page_icon="📊", layout="wide")

st.title("📊 TaskWeaver Data Analyst")
st.markdown("---")

if "agent" not in st.session_state:
    try:
        st.session_state.agent = DataAnalystAgent()
        st.sidebar.success("Agent Connected ✅")
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for file uploads
with st.sidebar:
    st.header("Upload Data")
    uploaded_files = st.file_uploader("Upload CSV/Excel", accept_multiple_files=True)
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing and executing code..."):
            file_paths = []
            if uploaded_files:
                os.makedirs("project/data", exist_ok=True)
                for f in uploaded_files:
                    path = os.path.join("project/data", f.name)
                    with open(path, "wb") as buffer:
                        buffer.write(f.getbuffer())
                    file_paths.append(path)

            response = st.session_state.agent.run(prompt, files=file_paths)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
