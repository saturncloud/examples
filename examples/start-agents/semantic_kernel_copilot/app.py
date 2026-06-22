import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory

load_dotenv()

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="SK Copilot", page_icon="🧩", layout="wide")

# --- 2. DEFINE PLUGINS ---
class ProjectManagerPlugin:
    @kernel_function(
        description="Calculates project completion date based on weeks.",
        name="CalculateTimeline"
    )
    def calculate_timeline(self, start_date: str, weeks: int) -> str:
        return f"📅 Analysis: Starting {start_date}, completion is scheduled in {weeks} weeks."

# --- 3. KERNEL INITIALIZATION (Cached) ---
@st.cache_resource
def create_kernel():
    kernel = Kernel()
    api_key = os.getenv("OPENAI_API_KEY")
    model_id = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")
    service_id = "chat-gpt"

    kernel.add_service(
        OpenAIChatCompletion(service_id=service_id, ai_model_id=model_id, api_key=api_key)
    )
    kernel.add_plugin(ProjectManagerPlugin(), plugin_name="ProjectManager")
    return kernel, service_id

# --- 4. UI COMPONENTS ---
st.title("🧩 Semantic Kernel Copilot")
st.markdown("Enterprise-grade orchestration with Native Python Plugins.")

if "messages" not in st.session_state:
    st.session_state.messages = ChatHistory()
    st.session_state.messages.add_system_message("You are an enterprise assistant. Use the ProjectManager plugin for timeline queries.")

# Display chat history
for msg in st.session_state.messages.messages:
    if msg.role == "system": continue
    with st.chat_message(msg.role):
        st.markdown(msg.content)

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ask about your project timeline..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.add_user_message(prompt)

    async def generate_response():
        kernel, service_id = create_kernel()
        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id, 
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )
        
        result = await kernel.get_service(service_id).get_chat_message_content(
            chat_history=st.session_state.messages,
            settings=execution_settings,
            kernel=kernel,
        )
        return result.content

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run the async kernel in the streamlit loop
                response = asyncio.run(generate_response())
                st.markdown(response)
                st.session_state.messages.add_assistant_message(response)
            except Exception as e:
                st.error(f"Kernel Error: {str(e)}")
