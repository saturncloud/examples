import os
import streamlit as st
from dotenv import load_dotenv
from routellm.controller import Controller

# Load environment variables
load_dotenv()

st.set_page_config(page_title="RouteLLM Dashboard", page_icon="🚦", layout="wide")

# Verify keys
openai_key = os.getenv("OPENAI_API_KEY")
nebius_key = os.getenv("NEBIUS_API_KEY")

if not openai_key or not nebius_key:
    st.error("❌ Error: Both OPENAI_API_KEY and NEBIUS_API_KEY must be set in your .env file.")
    st.stop()

# 🛠️ The LiteLLM Routing Trick: Map Nebius to the hosted_vllm prefix
os.environ["HOSTED_VLLM_API_KEY"] = nebius_key
os.environ["HOSTED_VLLM_API_BASE"] = "https://api.studio.nebius.ai/v1"

# Initialize the RouteLLM Controller
@st.cache_resource
def get_router():
    return Controller(
        routers=["mf"],
        strong_model="hosted_vllm/meta-llama/Llama-3.3-70B-Instruct",
        weak_model="gpt-4o-mini",
    )

client = get_router()
ROUTER_MODEL = "router-mf-0.11593"

# --- UI Sidebar ---
st.sidebar.title("🚦 Intelligent Router")
st.sidebar.markdown("**Strong Model:** Llama-3.3-70B (Nebius)")
st.sidebar.markdown("**Weak Model:** GPT-4o-mini (OpenAI)")
st.sidebar.info("RouteLLM dynamically analyzes your prompt's complexity to route trivial questions to the cheap model, and complex questions to the strong model!")

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# --- Main Chat UI ---
st.title("🚦 RouteLLM Intelligent Dashboard")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "model" in msg:
            st.caption(f"✨ *Routed to: {msg['model']}*")
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("E.g., What is 2+2? vs Write a complex C memory allocator..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing complexity and routing query..."):
            # RouteLLM handles the decision logic internally
            response = client.chat.completions.create(
                model=ROUTER_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            
            model_used = response.model
            content = response.choices[0].message.content
            
            # Clean up the model name for a better UI display
            display_model = "Llama-3.3-70B (Nebius)" if "llama" in model_used.lower() else "GPT-4o-mini (OpenAI)"
            
            st.caption(f"✨ *Routed to: **{display_model}***")
            st.markdown(content)
            
    # Save to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": content, 
        "model": display_model
    })
