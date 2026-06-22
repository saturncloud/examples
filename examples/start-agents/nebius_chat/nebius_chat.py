import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Ensure API key is present
api_key = os.getenv("NEBIUS_API_KEY")
if not api_key:
    print("❌ Error: NEBIUS_API_KEY not found in .env file.")
    sys.exit(1)

# Initialize the OpenAI client pointing to Nebius Token Factory
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=api_key,
)

# You can easily swap this out for "Qwen/Qwen2.5-72B", "deepseek-ai/DeepSeek-V3", etc.
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct" 

print("==================================================")
print(f"💬 Nebius Token Factory Chat Initialized")
print(f"🧠 Active Model: {MODEL_NAME}")
print("💡 Type 'exit' or 'quit' to end the conversation.")
print("==================================================\n")

# Store conversation history for contextual awareness
messages = [
    {"role": "system", "content": "You are a helpful, highly intelligent AI assistant powered by Nebius Token Factory. Provide clear, concise, and accurate answers."}
]

while True:
    try:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Ending session. Goodbye!")
            break
        if not user_input.strip():
            continue

        # Add user message to memory
        messages.append({"role": "user", "content": user_input})

        print("🤖 Nebius: ", end="", flush=True)
        
        # Stream the response from the Nebius API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            stream=True
        )

        assistant_reply = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                assistant_reply += text
        
        print() # Add a newline after the streaming completes
        
        # Add assistant response to memory so it remembers context
        messages.append({"role": "assistant", "content": assistant_reply})

    except KeyboardInterrupt:
        print("\n👋 Session interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        # Remove the last user message if the API call failed so we don't corrupt history
        if messages and messages[-1]["role"] == "user":
            messages.pop()