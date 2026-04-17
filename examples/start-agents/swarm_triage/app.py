import os
import streamlit as st
from dotenv import load_dotenv
from swarm import Swarm, Agent

load_dotenv()

st.set_page_config(page_title="Swarm Support", page_icon="🐝", layout="wide")

if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found in .env file.")
    st.stop()

@st.cache_resource
def get_swarm_client():
    return Swarm()

client = get_swarm_client()

# --- 1. Define Strict Agents ---
triage_agent = Agent(
    name="Triage Agent", 
    instructions="You are a routing agent. Determine the user's need and call the appropriate transfer function IMMEDIATELY. DO NOT output conversational text."
)
sales_agent = Agent(
    name="Sales Agent", 
    instructions="You handle sales inquiries and pricing. If the user asks about tech issues or billing, you MUST call the correct transfer tool immediately. DO NOT say 'I will transfer you', just execute the tool."
)
tech_agent = Agent(
    name="Tech Support Agent", 
    instructions="You handle tech issues and error codes. If the user asks about pricing or billing, you MUST call the correct transfer tool immediately. DO NOT say 'I will transfer you', just execute the tool."
)
billing_agent = Agent(
    name="Billing Agent", 
    instructions="You handle billing and refunds. If the user asks about pricing or tech issues, you MUST call the correct transfer tool immediately. DO NOT say 'I will transfer you', just execute the tool."
)
human_agent = Agent(
    name="Human Escalation", 
    instructions="You are the safety net. Tell the user a human will contact them. If they change their mind and ask about sales, tech, or billing, call the correct transfer tool immediately. DO NOT say 'I will transfer you', just execute the tool."
)

# --- 2. Define Strict Handoff Functions ---
def transfer_to_sales():
    """Call this tool immediately to transfer the user to Sales for pricing and purchases."""
    return sales_agent
def transfer_to_tech():
    """Call this tool immediately to transfer the user to Tech Support for bugs, crashes, and Error 500s."""
    return tech_agent
def transfer_to_billing():
    """Call this tool immediately to transfer the user to Billing for refunds and invoices."""
    return billing_agent
def transfer_to_triage():
    """Call this tool immediately to transfer the user to Triage to start over."""
    return triage_agent
def escalate_to_human():
    """Call this tool immediately to escalate to a human if the user is angry or demands a manager."""
    return human_agent

# --- 3. Attach Omni-Directional Routing ---
triage_agent.functions  = [transfer_to_sales, transfer_to_tech, transfer_to_billing, escalate_to_human]
sales_agent.functions   = [transfer_to_tech, transfer_to_billing, transfer_to_triage, escalate_to_human]
tech_agent.functions    = [transfer_to_sales, transfer_to_billing, transfer_to_triage, escalate_to_human]
billing_agent.functions = [transfer_to_sales, transfer_to_tech, transfer_to_triage, escalate_to_human]
human_agent.functions   = [transfer_to_sales, transfer_to_tech, transfer_to_billing, transfer_to_triage]

# --- Streamlit State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_agent" not in st.session_state:
    st.session_state.active_agent = triage_agent

# --- UI Setup ---
st.title("🐝 OpenAI Swarm Support Triage")
st.sidebar.title("🏢 Call Center Status")

status_color = "🔴" if st.session_state.active_agent.name == "Human Escalation" else "🟢"
st.sidebar.info(f"**Currently speaking with:**\n\n{status_color} {st.session_state.active_agent.name}")

if st.sidebar.button("🗑️ Reset Conversation"):
    st.session_state.messages = []
    st.session_state.active_agent = triage_agent
    st.rerun()

# Render chat history cleanly
for msg in st.session_state.messages:
    if msg["role"] == "assistant" and msg.get("content"):
        with st.chat_message("assistant"):
            sender = msg.get("sender", "Agent")
            st.markdown(f"**[{sender}]** {msg['content']}")
    elif msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("E.g., I want to buy a pro license, or my app keeps crashing..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner(f"{st.session_state.active_agent.name} is processing..."):
        response = client.run(
            agent=st.session_state.active_agent,
            messages=st.session_state.messages
        )
        
        st.session_state.messages = response.messages
        st.session_state.active_agent = response.agent
        
    # Trigger a clean UI reload so the history loop draws everything natively!
    st.rerun()
