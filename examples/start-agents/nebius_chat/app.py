import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Nebius Chat UI", page_icon="💬", layout="wide")

# Ensure API key is present
api_key = os.getenv("NEBIUS_API_KEY")
if not api_key:
    st.error("❌ Error: NEBIUS_API_KEY not found in .env file.")
    st.stop()

# Initialize the OpenAI client pointing to Nebius Token Factory
@st.cache_resource
def get_client():
    return OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=api_key,
    )

client = get_client()

# --- UI Sidebar ---
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("Swap between open-source models instantly!")
model_name = st.sidebar.selectbox(
    "Active Model:",
    [
        "meta-llama/Llama-3.3-70B-Instruct",
        "deepseek-ai/DeepSeek-V3.2",
        "Qwen/Qwen3-Coder-480B-A35B-Instruct"
    ]
)

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, highly intelligent AI assistant powered by Nebius Token Factory."}
    ]
    st.rerun()

# --- Main Chat UI ---
st.title("💬 Nebius Token Factory Dashboard")
st.markdown("A production-grade chat interface connected to Nebius AI Studio via the OpenAI SDK.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, highly intelligent AI assistant powered by Nebius Token Factory."}
    ]

# Display chat messages from history on app rerun (skipping the hidden system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("E.g., Write a python script to reverse a string..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Stream the response from the Nebius API
        stream = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages,
            stream=True,
            temperature=0.7,
        )
        
        # Streamlit natively handles chunk streaming from OpenAI clients!
        response = st.write_stream(stream)
        
    # Add assistant response to memory so it remembers context
    st.session_state.messages.append({"role": "assistant", "content": response})
