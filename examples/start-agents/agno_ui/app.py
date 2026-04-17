import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# Load API keys
load_dotenv()

st.set_page_config(page_title="Agno Agent UI", page_icon="📈", layout="wide")

# --- UI Sidebar ---
st.sidebar.title("🤖 Agent Selector")
st.sidebar.markdown("Choose which AI agent you want to interact with:")
agent_type = st.sidebar.radio(
    "Active Agent:",
    ["🌐 Web Researcher", "📈 Finance Analyst", "👔 Finance Swarm"]
)

# --- Agent Initialization ---
@st.cache_resource
def get_agent(choice):
    # 🛡️ HARDENED TOOLS: 
    # 1. Disable DDG's flaky 'news' endpoint using the correct 'enable_' syntax
    safe_web_tools = [DuckDuckGoTools(enable_search=True, enable_news=False)]
    # 2. Ensure all finance tools are explicitly enabled
    safe_finance_tools = [YFinanceTools(enable_stock_price=True, enable_analyst_recommendations=True, enable_company_info=True)]

    if choice == "🌐 Web Researcher":
        return Agent(
            name="Web Researcher",
            role="Search the web for real-time information.",
            tools=safe_web_tools,
            markdown=True
        )
    elif choice == "📈 Finance Analyst":
        return Agent(
            name="Finance Analyst",
            role="Analyze live stock data, fundamentals, and analyst recommendations.",
            tools=safe_finance_tools,
            markdown=True
        )
    else:
        # The Swarm Team
        web = Agent(name="Web Researcher", tools=safe_web_tools, markdown=True)
        finance = Agent(name="Finance Analyst", tools=safe_finance_tools, markdown=True)
        return Team(
            name="Finance Swarm",
            members=[web, finance],
            instructions=[
                "1. Ask the Finance Analyst to pull the company's live stock data and recommendations.",
                "2. Ask the Web Researcher to find the latest public news about the company.",
                "3. Synthesize both into a comprehensive investment report."
            ],
            markdown=True
        )

# Get the currently selected agent
active_agent = get_agent(choice=agent_type)

# --- Chat Interface ---
st.title(f"{active_agent.name} 💬")

# Provide fallback description if the active agent is a Team
agent_role = getattr(active_agent, "role", "Orchestrate the Web and Finance agents to write a comprehensive report.")
st.markdown(f"**Role:** {agent_role}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("E.g., Analyze NVDA's recent performance..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner(f"{active_agent.name} is working..."):
            response = active_agent.run(prompt)
            st.markdown(response.content)
            
    st.session_state.messages.append({"role": "assistant", "content": response.content})
