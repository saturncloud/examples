import os
from dotenv import load_dotenv

# Import the shared agent logic from your app package
from app.agent import invoke_agent

# Initialize environment variables
load_dotenv()

if __name__ == "__main__":
    print("--- AWS Strands Agent Starter (CLI Mode) ---")
    print("Framework: Strands SDK | Provider: OpenAI")
    print("Agent is ready. (Type 'exit' to quit)")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY is missing from your .env file.")
        exit(1)
    
    while True:
        user_query = input("\nAsk for the weather: ")
        
        if user_query.lower() in ['exit', 'quit']:
            print("Terminating CLI process.")
            break
            
        if user_query.strip():
            try:
                # Execute the Strands agent loop via the shared application logic
                response = invoke_agent(user_query)
                print(f"\nAgent: {response}")
            except Exception as e:
                print(f"\nExecution Error: {e}")