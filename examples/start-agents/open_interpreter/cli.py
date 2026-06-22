import sys
from src.agent import SystemAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    agent = SystemAgent()
    print("\n🚀 Open Interpreter CLI (Saturn Cloud Edition)")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            query = input("User > ")
            if query.lower() in ["exit", "quit"]:
                break
            
            print("\nAgent > ", end="", flush=True)
            for chunk in agent.chat(query):
                if 'content' in chunk:
                    print(chunk['content'], end="", flush=True)
            print("\n")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
