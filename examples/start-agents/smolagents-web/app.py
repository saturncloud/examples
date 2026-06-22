import os
import re
import io
from contextlib import redirect_stdout, redirect_stderr
import streamlit as st
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

load_dotenv()

st.set_page_config(page_title="smolagents UI", page_icon="🤗", layout="wide")

if not os.getenv("HF_TOKEN"):
    st.error("❌ HF_TOKEN not found in .env file.")
    st.stop()

@st.cache_resource
def get_agent():
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
    
    custom_instructions = """You are a Code Agent. Your job is to search the web and provide answers.
CRITICAL RULES FOR TEXT PARSING:
1. NEVER write Python code to parse, clean, or format text. 
2. NEVER use RegEx (re.search, re.findall) or string manipulation (.split, .replace) on search results.
3. Once you call the web_search tool, simply READ the output in your context window, and pass a natural language summary directly into the final_answer() tool."""

    return CodeAgent(
        tools=[DuckDuckGoSearchTool()], 
        model=model,
        additional_authorized_imports=["datetime", "math"],
        instructions=custom_instructions
    )

agent = get_agent()

def strip_ansi(text):
    """Removes weird terminal color codes from the output so it looks clean in Streamlit."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# --- UI Setup ---
st.title("🤗 Hugging Face smolagents")
st.markdown("A lightweight Code Agent that writes Python on the fly to search the web and solve problems.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🗑️ Reset Conversation"):
    st.session_state.messages = []
    st.rerun()

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("E.g., Search the web for the distance between Earth and Mars right now..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Create a beautiful expandable status box
        with st.status("🤖 Agent is writing Python code and searching the web...", expanded=True) as status:
            
            # Create a string buffer to capture terminal output
            f = io.StringIO()
            
            try:
                # Secretly hijack both standard output and error logs
                with redirect_stdout(f), redirect_stderr(f):
                    response = agent.run(prompt)
                
                # Clean the captured terminal logs and display them!
                terminal_logs = strip_ansi(f.getvalue())
                st.code(terminal_logs, language="text")
                
                # Close the status box once finished
                status.update(label="✅ Agent finished its task!", state="complete", expanded=False)
                
            except Exception as e:
                # If it crashes, still show the terminal logs so you can debug!
                terminal_logs = strip_ansi(f.getvalue())
                st.code(terminal_logs, language="text")
                st.error(f"Error executing agent: {e}")
                status.update(label="❌ Agent crashed!", state="error", expanded=True)
                st.stop()
        
        # Display the final, polished answer outside the box
        st.markdown(f"**Final Answer:** {response}")
        st.session_state.messages.append({"role": "assistant", "content": f"**Final Answer:** {response}"})
