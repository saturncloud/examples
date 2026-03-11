import uuid
import asyncio  # <-- NEW: Import asyncio
import streamlit as st
from dotenv import load_dotenv

# ADK Programmatic Imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import our custom ADK agent package
from my_agent.agent import root_agent

# 1. Page Configuration
st.set_page_config(page_title="Google ADK Production UI", page_icon="☁️", layout="centered")
load_dotenv()

st.title("☁️ Google ADK Production Dashboard")
st.markdown("Interact with an enterprise-grade Google ADK agent connected to live APIs.")

# 2. Initialize ADK Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    
    # Create the ADK session manager
    st.session_state.session_service = InMemorySessionService()
    
    # <-- FIX: Wrap the async creation step in asyncio.run() -->
    asyncio.run(
        st.session_state.session_service.create_session(
            app_name="streamlit_dashboard", 
            user_id="web_user", 
            session_id=st.session_state.session_id
        )
    )
    
    # Attach the agent to the runner
    st.session_state.runner = Runner(
        agent=root_agent, 
        app_name="streamlit_dashboard", 
        session_service=st.session_state.session_service
    )

# 3. Render previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
# 4. Handle new user input
user_input = st.chat_input("Ask about the live weather anywhere in the world...")

if user_input:
    # Display user prompt
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Agent is calling external APIs..."):
            try:
                # Format the message for Google GenAI
                content = types.Content(
                    role="user", 
                    parts=[types.Part(text=user_input)]
                )
                
                # Execute the ADK Runner asynchronously
                events = st.session_state.runner.run(
                    user_id="web_user", 
                    session_id=st.session_state.session_id, 
                    new_message=content
                )
                
                # ADK streams back multiple events; we want to catch the final generated text
                final_response = "Error: Agent returned no content."
                for event in events:
                    if event.is_final_response():
                        final_response = event.content.parts[0].text
                
                # Render to UI and save to memory
                st.write(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                st.error(f"ADK Execution Error: {str(e)}")