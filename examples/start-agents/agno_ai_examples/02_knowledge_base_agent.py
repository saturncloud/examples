from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.lancedb import LanceDb

print("📚 Booting Knowledge Keeper & Embedding Data...")

knowledge_base = TextKnowledgeBase(
    path="data",
    vector_db=LanceDb(table_name="acme_history", uri="./lancedb"),
)
knowledge_base.load(recreate=True)

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    description="You are an internal corporate archivist. You answer questions strictly based on the provided knowledge base.",
    markdown=True
)

agent.print_response("When was Acme Corp founded, and what is their secret project?")