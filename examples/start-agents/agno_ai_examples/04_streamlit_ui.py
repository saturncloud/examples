import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

# Load environment variables (API Keys)
load_dotenv()

st.set_page_config(page_title="Market Intelligence Swarm", page_icon="🐝", layout="wide")
st.title("🐝 Market Intelligence Swarm")
st.markdown("Delegate tasks to the Lead Editor. It will coordinate the **Web Researcher** and **Knowledge Keeper** to write your report.")

@st.cache_resource
def get_swarm():
    # 1. Web Agent
    web_agent = Agent(
        name="Web Researcher",
        role="Search the web for real-time information",
        tools=[DuckDuckGoTools()],
        markdown=True
    )
    
    # 2. Knowledge Agent
    knowledge_base = Knowledge(
        vector_db=LanceDb(table_name="acme_history", uri="./lancedb"),
    )
    # This automatically reads and embeds everything in your data/ folder
    knowledge_base.insert(path="data")

    knowledge_agent = Agent(
        name="Knowledge Keeper",
        role="Search the internal company knowledge base",
        knowledge=knowledge_base,
        search_knowledge=True,
        markdown=True
    )

    # 3. The Lead Editor (Now uses the official Team class!)
    editor_agent = Team(
        name="Lead Editor",
        members=[web_agent, knowledge_agent],
        instructions=[
            "First, ask the Knowledge Keeper for internal context on the user's query.",
            "Second, ask the Web Researcher to find current public news regarding the query.",
            "Finally, write a comprehensive report synthesizing both sources."
        ],
        markdown=True
    )
    return editor_agent

# Initialize the swarm
editor_agent = get_swarm()

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("E.g., Compare Acme's secret project to today's public AI news..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("The Swarm is researching and writing (this may take a moment)..."):
            response = editor_agent.run(prompt)
            st.markdown(response.content)
            
    st.session_state.messages.append({"role": "assistant", "content": response.content})
