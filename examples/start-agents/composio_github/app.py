import streamlit as st
from src.agent import GitHubReviewer

# Page Configuration
st.set_page_config(page_title="AI GitHub Reviewer", page_icon="🤖", layout="wide")

st.title("🤖 AI GitHub Reviewer")
st.markdown("---")

# Sidebar for Status
with st.sidebar:
    st.success("Connected to Composio ✅")
    st.info("Powered by LangGraph & GPT-4o")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about your GitHub repositories..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Initialize the working agent
                reviewer = GitHubReviewer()
                response = reviewer.run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
