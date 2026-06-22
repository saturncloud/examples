import streamlit as st
from src.agent import SystemAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Open Interpreter UI", page_icon="🤖", layout="wide")

st.title("🤖 Open Interpreter")
st.caption("System-level agent for command execution and file management.")

if "agent" not in st.session_state:
    st.session_state.agent = SystemAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Enter a system command or task..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # 🎯 Robust parsing of the interpreter stream
        for chunk in st.session_state.agent.chat(prompt):
            if 'content' in chunk:
                content = chunk['content']
                
                # Only concatenate if it's a string
                if isinstance(content, str):
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
                # If it's a dict (code or tool), we can choose to display it or stringify it
                elif isinstance(content, dict):
                    pass 

        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
