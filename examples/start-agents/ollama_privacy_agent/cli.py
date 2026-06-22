import argparse
from src.agent import PrivacyAgent

def main():
    parser = argparse.ArgumentParser(description="Ollama Privacy Agent CLI")
    parser.add_argument("query", type=str, help="Your question")
    args = parser.parse_args()
    agent = PrivacyAgent()
    print("Thinking locally...")
    print(f"\nAgent: {agent.chat(args.query)}")

if __name__ == "__main__":
    main()
