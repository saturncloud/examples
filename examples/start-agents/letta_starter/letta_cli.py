import os
import sys
import time
from dotenv import load_dotenv
from letta_client import Letta

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

try:
    client = Letta(base_url="http://localhost:8283")
except Exception:
    print("❌ Error: Could not connect to Letta server. Please run using `python run.py`")
    sys.exit(1)

print("==================================================")
print("🧠 Letta (MemGPT) CLI Companion")
print("💡 Type 'exit' to quit.")
print("==================================================\n")

memory_blocks = [
    {"label": "human", "value": "User information is unknown. Ask the user for their name and preferences."},
    {"label": "persona", "value": "Your name is Echo. You are a personalized, highly empathetic AI companion. You actively update your memory to remember facts about the user."}
]

agent_state = client.agents.create(
    name=f"echo-cli-{int(time.time())}",
    model="openai/gpt-4o-mini",
    embedding="openai/text-embedding-3-small",
    memory_blocks=memory_blocks,
)

while True:
    try:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        print("🤖 Echo is thinking...\n")
        
        response = client.agents.messages.create(
            agent_id=agent_state.id,
            messages=[{"role": "user", "content": user_input}]
        )
        
        for msg in response.messages:
            if hasattr(msg, 'message_type'):
                if msg.message_type == 'internal_monologue':
                    print(f"   [Thought: {msg.content}]")
                elif msg.message_type == 'assistant_message' and msg.content:
                    print(f"\n✨ Echo: {msg.content}")
                
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
