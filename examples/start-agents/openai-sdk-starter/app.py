import streamlit as st
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="OpenAI SDK Agent Application",
    page_icon="⚙️", # Changed to a standard gear icon for a more technical look
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("OpenAI SDK Agent")
st.markdown("Interface for executing system prompts via the OpenAI Python SDK.")

# --- INITIALIZATION ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Environment Error: OPENAI_API_KEY is not defined in the environment variables.")
    st.stop()

# Instantiate the OpenAI Client
client = OpenAI(api_key=api_key)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Agent Configuration")

model_choice = st.sidebar.selectbox(
    "Target Model", 
    ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
    help="Select the OpenAI model to process the completions."
)

agent_type = st.sidebar.radio(
    "Agent Persona",
    ["Email Helper", "Haiku Writer"]
)

temperature = st.sidebar.slider(
    "Temperature", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.7, 
    step=0.1,
    help="Higher values produce more randomized output. Lower values produce deterministic output."
)

# Define system instruction logic based on persona
if agent_type == "Email Helper":
    system_prompt = "You are a professional executive assistant. Your primary function is to draft, refine, and summarize professional emails based on user context. Maintain a formal, concise tone."
else:
    system_prompt = "You are a master poet. You must respond to all user inputs strictly in the form of a haiku (5-7-5 syllable structure). Do not provide any conversational filler."

# --- STATE MANAGEMENT ---
# Initialize or reset chat history if the user switches the agent persona
if "current_agent" not in st.session_state or st.session_state.current_agent != agent_type:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.current_agent = agent_type

# Render chat history (excluding the hidden system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- EXECUTION LOGIC ---
if prompt := st.chat_input(f"Send a message to the {agent_type}..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Execute API call with streaming enabled
            stream = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True
            )
            
            # Stream the response to the UI (Streamlit 1.32+ supports OpenAI streams natively)
            response = st.write_stream(stream)
            
            # Append final output to state
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except openai.AuthenticationError:
            st.error("API Execution Error: Authentication Failed (401). Verify your OPENAI_API_KEY.")
        except openai.RateLimitError:
            st.error("API Execution Error: Rate Limit or Quota Exceeded (429). Check your billing dashboard.")
        except Exception as e:
            st.error(f"API Execution Error: {str(e)}")