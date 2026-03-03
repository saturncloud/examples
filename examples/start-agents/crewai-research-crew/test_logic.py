from src.crew import ResearchCrew
from dotenv import load_dotenv
import os

load_dotenv() # Loads keys from .env

def test():
    print("🚀 Starting Logic Test...")
    crew = ResearchCrew().crew()
    result = crew.kickoff(inputs={'topic': 'Standardization of AI Agent Protocols 2026'})
    print("\n✅ Test Result:\n", result)

if __name__ == "__main__":
    test()