import streamlit as st
from src.agent import PrivacyAgent

st.set_page_config(page_title="Privacy Agent", page_icon="🔒")
st.title("Ollama Privacy Agent")

if "agent" not in st.session_state:
    st.session_state.agent = PrivacyAgent()
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]): st.markdown(chat["content"])

if prompt := st.chat_input("Ask me something privately..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.agent.chat(prompt, st.session_state.chat_history[:-1])
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
