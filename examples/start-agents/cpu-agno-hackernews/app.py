import streamlit as st
from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.models.nebius import Nebius
from agno.db.sqlite import SqliteDb
import os
from dotenv import load_dotenv

# Load keys from the .env file
load_dotenv()

# Set up the Streamlit UI
st.set_page_config(page_title="Tech News Analyst", page_icon="🤖", layout="wide")
st.title("🤖 Tech News Analyst")
st.markdown("Ask me anything about trending topics, engagement patterns, or tech news on HackerNews!")

# Initialize the Agent with SQLite Memory
@st.cache_resource
def get_agent():
    return Agent(
        name="Tech News Analyst",
        tools=[HackerNewsTools()],
        model=Nebius(
            id="Qwen/Qwen3-235B-A22B-Thinking-2507",
            api_key=os.getenv("NEBIUS_API_KEY")
        ),
        # Attach SQLite storage to give the agent a persistent memory using v2 syntax
        db=SqliteDb(db_file="agent_memory.db"),
        # Use the updated v2 syntax for adding history context
        add_history_to_context=True, 
        # (Optional) You can limit how many previous runs to remember to save API costs
        num_history_runs=3,
        markdown=True
    )

agent = get_agent()

# Initialize UI chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What are the top stories on HackerNews right now?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing HackerNews..."):
            response = agent.run(prompt)
            st.markdown(response.content)
            
    st.session_state.messages.append({"role": "assistant", "content": response.content})