from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

print("🌐 Booting Web Researcher...")
agent = Agent(
    tools=[DuckDuckGoTools()],
    description="You are a senior web researcher. Always find the most recent information.",
    instructions=["Always cite your sources."],
    markdown=True
)

agent.print_response("What are the biggest AI news headlines today?")