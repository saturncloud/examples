import streamlit as st
import asyncio
from metagpt.team import Team
from metagpt.roles import ProductManager, Architect, ProjectManager, Engineer

# UI Setup
st.set_page_config(page_title="MetaGPT Factory", layout="wide")
st.title("🏗️ AI Software Factory")

idea = st.text_area("What should the factory build?", placeholder="e.g. Create a CLI-based Password Manager in Python")

if st.button("Start Production"):
    if idea:
        async def run_factory():
            # The engine finds the config automatically via the Docker ENV variable
            team = Team()
            team.hire([ProductManager(), Architect(), ProjectManager(), Engineer()])
            team.invest(3.0)
            
            # Run_project is a sync method in 0.8.2
            team.run_project(idea) 
            
            # This is the part that actually runs the agents
            await team.run(n_round=5)
            st.success("Software Production Complete! Check your /workspace folder.")

        with st.spinner("Agents are collaborating... check terminal for live logs."):
            try:
                # We use a new event loop to avoid conflicts with Streamlit's loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(run_factory())
            except Exception as e:
                st.error(f"Execution Error: {e}")
    else:
        st.warning("Please enter a project idea.")