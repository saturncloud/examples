import os
import time
import streamlit as st
from dotenv import load_dotenv
from letta_client import Letta

load_dotenv()

st.set_page_config(page_title="Letta Companion", page_icon="🧠", layout="wide")

if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found in .env file.")
    st.stop()

@st.cache_resource
def init_letta_client():
    try:
        # Connects to your Dockerized Letta Server
        return Letta(base_url="http://localhost:8283")
    except Exception:
        return None

client = init_letta_client()

if not client:
    st.error("❌ Cannot connect to Letta Server. Is Docker running?")
    st.stop()

@st.cache_resource
def get_or_create_agent():
    # Initializing the default memory for your agent
    memory_blocks = [
        {"label": "human", "value": "User information is unknown. Ask the user for their name and preferences."},
        {"label": "persona", "value": "Your name is Echo. You are a personalized, highly empathetic AI companion. You actively update your database to remember facts about the user."}
    ]
    return client.agents.create(
        name=f"echo-ui-{int(time.time())}",
        model="openai/gpt-4o-mini",
        embedding="openai/text-embedding-3-small",
        memory_blocks=memory_blocks,
    )

agent_state = get_or_create_agent()

# --- UI Setup ---
st.title("🧠 Letta (MemGPT) Companion")
st.markdown("A stateful AI companion with perpetual memory. Watch it edit its own PostgreSQL database to remember what you tell it!")

col1, col2 = st.columns([2, 1])

with col1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("🗑️ Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("E.g., Hi, my name is Alex and my favorite color is blue..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Echo is thinking (and updating its Postgres database)..."):
                try:
                    response = client.agents.messages.create(
                        agent_id=agent_state.id,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    final_answer = ""
                    for msg in response.messages:
                        if hasattr(msg, 'message_type'):
                            # Capture internal thoughts
                            if msg.message_type == 'internal_monologue':
                                with st.expander("💭 Agent Thought Process"):
                                    st.write(msg.content)
                            # Capture final spoken message
                            elif msg.message_type == 'assistant_message' and msg.content:
                                final_answer = msg.content
                                st.markdown(final_answer)
                                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                except Exception as e:
                    st.error(f"Error executing agent: {e}")

with col2:
    st.subheader("🗂️ Postgres DB Inspector")
    st.info("Watch the agent edit its Core Memory in real-time!")
    
    # We use a button to manually refresh the view of the database
    if st.button("🔄 Refresh Database"):
        pass 
        
    try:
        # Fetch live memory blocks directly from the Letta Server
        human_block = client.agents.blocks.retrieve(agent_id=agent_state.id, block_label="human")
        persona_block = client.agents.blocks.retrieve(agent_id=agent_state.id, block_label="persona")
        
        st.markdown("**User (Human) Block:**")
        st.code(human_block.value, language="text")
        
        st.markdown("**Agent (Persona) Block:**")
        st.code(persona_block.value, language="text")
    except Exception as e:
        st.warning("Memory blocks initializing...")
