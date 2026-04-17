import streamlit as st
import requests
import os

AGENT_API_URL = os.getenv("AGENT_HOST", "http://agent-service.kaos-system.svc.cluster.local:8080/chat")
st.title("☸️ KAOS Web Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask the KAOS swarm..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Agent is thinking..."):
        try:
            res = requests.post(AGENT_API_URL, json={"message": prompt})
            reply = res.json().get("reply", "No response from agent.")
        except Exception as e:
            reply = f"Error connecting to agent: {e}"
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
