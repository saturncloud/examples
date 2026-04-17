import sys
from src.agent import DataAnalystAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    print("\n--- 📊 TaskWeaver Data Analyst CLI ---")
    try:
        agent = DataAnalystAgent()
    except Exception as e:
        print(f"Initialization Error: {e}")
        return
    
    while True:
        try:
            query = input("\nQuery (or 'exit'): ")
            if query.lower() == 'exit': break
            
            print("\nAnalyst is thinking (generating and executing code)...")
            response = agent.run(query)
            print(f"\n[RESPONSE]:\n{response}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
