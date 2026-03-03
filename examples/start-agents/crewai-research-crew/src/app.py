import os
# Disable telemetry to avoid the signal/thread error
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

import streamlit as st
from crew import ResearchCrew
from dotenv import load_dotenv

# Load .env file at startup
load_dotenv()

st.set_page_config(page_title="Research Crew Dashboard", layout="wide")

st.title("🧠 Multi-Agent Research Crew")

# --- API Configuration Logic ---
# Check if key exists in system environment (.env)
env_key = os.getenv("OPENAI_API_KEY")

with st.sidebar:
    st.header("Settings")
    if env_key:
        st.success("✅ API Key loaded from .env")
        # Optional: allow override
        user_key = st.text_input("Override API Key (Optional)", type="password")
        if user_key:
            os.environ["OPENAI_API_KEY"] = user_key
    else:
        st.warning("⚠️ No API Key found in .env")
        user_key = st.text_input("Enter OpenAI API Key", type="password")
        if user_key:
            os.environ["OPENAI_API_KEY"] = user_key

# --- Main Interface ---
topic = st.text_input("Research Topic", placeholder="e.g. Advancements in Room-Temperature Superconductors")

if st.button("Run Research Crew"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Please provide an API Key to continue.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        # 1. Collapsible Thinking Section
        with st.expander("🕵️ View Agent Thinking & Process", expanded=True):
            thinking_container = st.empty()
            with st.status("Agents are working...", expanded=True) as status:
                st.write("🔍 **Researcher:** Accessing technical databases...")
                # In a basic setup, we use these write statements to track progress
                # For real-time "internal logs," CrewAI requires a custom callback, 
                # but these status updates serve the same visual purpose.
                
                try:
                    crew_obj = ResearchCrew().crew()
                    result = crew_obj.kickoff(inputs={'topic': topic})
                    
                    st.write("✍️ **Writer:** Synthesizing findings into report...")
                    status.update(label="✅ Research Complete!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Execution Error: {e}")
                    st.stop()

        # 2. Results Section
        st.divider()
        st.subheader("📄 Final Research Report")
        st.markdown(result)
        
        st.download_button(
            label="Download Report (.md)",
            data=str(result),
            file_name=f"research_report.md",
            mime="text/markdown"
        )