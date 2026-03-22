from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.lancedb import LanceDb

print("👔 Booting the Swarm...")

web_agent = Agent(
    name="Web Researcher",
    role="Search the web for real-time information",
    tools=[DuckDuckGoTools()],
    markdown=True
)

knowledge_base = TextKnowledgeBase(
    path="data",
    vector_db=LanceDb(table_name="acme_history", uri="./lancedb"),
)
knowledge_agent = Agent(
    name="Knowledge Keeper",
    role="Search the internal company knowledge base",
    knowledge=knowledge_base,
    search_knowledge=True,
    markdown=True
)

editor_agent = Agent(
    name="Lead Editor",
    role="Synthesize web and internal data into a cohesive report",
    team=[web_agent, knowledge_agent],
    instructions=[
        "First, ask the Knowledge Keeper for internal context on Acme Corp's Quantum AI Engine.",
        "Second, ask the Web Researcher to find current public news about 'Quantum AI'.",
        "Finally, write a comparative report synthesizing both sources."
    ],
    markdown=True
)

editor_agent.print_response("Write the comparative report on Acme Corp vs the current public market.", stream=True)