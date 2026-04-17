import os
import glob
import streamlit as st
from dotenv import load_dotenv
import autogen
from autogen.coding import LocalCommandLineCodeExecutor

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AutoGen Workspace", page_icon="🤖", layout="wide")

st.title("🤖 AutoGen Collaborative Workspace")
st.markdown("Ask the AI Assistant to write code. The User Proxy Agent will autonomously execute and debug it locally!")

if prompt := st.chat_input("E.g., Fetch TSLA stock prices for the last 30 days and plot them..."):
    st.chat_message("user").markdown(prompt)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY not found in .env file.")
        st.stop()

    work_dir = "coding"
    os.makedirs(work_dir, exist_ok=True)

    llm_config = {"model": "gpt-4o-mini", "api_key": api_key}
    
    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=llm_config,
        system_message="""You are a helpful AI assistant. You write Python code to solve tasks. 
Always wrap your code in standard markdown code blocks.
The user proxy will execute your code and report the output back to you.
DO NOT output 'TERMINATE' in the same message where you write code. 
WAIT for the user proxy to run the code and confirm it worked. 
ONLY output 'TERMINATE' when the user proxy confirms the execution was successful and the task is fully complete.""",
    )

    executor = LocalCommandLineCodeExecutor(timeout=60, work_dir=work_dir)
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"executor": executor},
    )

    with st.spinner("🤖 Agents are currently writing, executing, and debugging code... please wait!"):
        chat_result = user_proxy.initiate_chat(assistant, message=prompt)
        
    st.success("✅ Task Complete! Here is the conversation history:")
    
    for msg in chat_result.chat_history:
        role = "assistant" if msg["role"] == "assistant" else "user"
        name = msg.get("name", role)
        
        with st.chat_message(role):
            st.markdown(f"**{name}**")
            st.markdown(msg["content"])
            
    png_files = glob.glob(os.path.join(work_dir, "*.png"))
    if png_files:
        st.divider()
        st.subheader("📊 Generated Artifacts")
        for img_path in png_files:
            st.image(img_path, caption=os.path.basename(img_path))
