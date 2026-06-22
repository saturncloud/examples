import streamlit as st
import asyncio
import os
from browser_use import Agent
from browser_use.llm import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Browser-Use Automator", page_icon="🤖", layout="wide")

st.title("🌐 Browser-Use Automator")
st.markdown("---")

# Native wrapper for stability
class BrowserUseLLM(ChatOpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

with st.sidebar:
    st.header("⚙️ Configuration")
    model_name = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini"])
    st.info("💡 **Pro Tip:** Use gpt-4o for complex navigation tasks.")

prompt = st.text_area("🎯 Enter Automation Task:", "Go to news.ycombinator.com and find the top story title.", height=100)

if st.button("🚀 Execute Automation", use_container_width=True):
    if not prompt:
        st.warning("Please enter a task first.")
    else:
        async def run_automation():
            llm = ChatOpenAI(model=model_name)
            agent = Agent(task=prompt, llm=llm)
            return await agent.run()

        with st.status("🤖 Agent is navigating the web...", expanded=True) as status:
            try:
                st.write("Initializing Browser...")
                result = asyncio.run(run_automation())
                status.update(label="✅ Automation Complete!", state="complete", expanded=False)
                
                st.subheader("🏁 Final Result")
                # Extract the final string answer from the history list
                final_answer = result.final_result()
                st.success(final_answer)
                
                with st.expander("🛠️ View Technical Execution Logs (JSON)"):
                    st.json(result.model_dump())
                    
            except Exception as e:
                st.error(f"❌ Automation failed: {e}")
