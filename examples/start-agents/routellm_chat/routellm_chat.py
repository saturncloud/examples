import os
import sys
from dotenv import load_dotenv
from routellm.controller import Controller

# Load environment variables
load_dotenv()

# Verify keys
openai_key = os.getenv("OPENAI_API_KEY")
nebius_key = os.getenv("NEBIUS_API_KEY")

if not openai_key or not nebius_key:
    print("❌ Error: Both OPENAI_API_KEY and NEBIUS_API_KEY must be set in your .env file.")
    sys.exit(1)

# 🛠️ The LiteLLM Routing Trick:
# Since both GPT-4o-mini and Nebius Llama use the OpenAI SDK format, we map Nebius 
# to the 'hosted_vllm' provider prefix. This prevents the API Base URLs from colliding!
os.environ["HOSTED_VLLM_API_KEY"] = nebius_key
os.environ["HOSTED_VLLM_API_BASE"] = "https://api.studio.nebius.ai/v1"

# Initialize the RouteLLM Controller
# We use the Matrix Factorization (mf) router, trained on Chatbot Arena preference data
client = Controller(
    routers=["mf"],
    strong_model="hosted_vllm/meta-llama/Llama-3.3-70B-Instruct",
    weak_model="gpt-4o-mini",
)

print("==================================================")
print("🚦 RouteLLM Intelligent Router Initialized")
print("💪 Strong Model: Nebius Llama 3.3 70B")
print("🏃 Weak Model:  GPT-4o-mini")
print("💡 Type 'exit' to quit.")
print("==================================================\n")

# Use a calibrated cost threshold of 0.11593 
# (This routes approximately 50% strong / 50% weak based on public benchmarks)
ROUTER_MODEL = "router-mf-0.11593"

while True:
    try:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Ending session. Goodbye!")
            break
        if not user_input.strip():
            continue

        print("🚦 Routing query... ", end="", flush=True)
        
        # RouteLLM automatically decides which model to use based on prompt complexity
        response = client.chat.completions.create(
            model=ROUTER_MODEL,
            messages=[{"role": "user", "content": user_input}]
        )

        model_used = response.model
        content = response.choices[0].message.content

        # Clean up the model name for a better UI display
        display_model = "Llama-3.3-70B (Nebius)" if "llama" in model_used.lower() else "GPT-4o-mini (OpenAI)"

        print(f"✨ [Routed to: {display_model}]")
        print(f"🤖 {content}")

    except KeyboardInterrupt:
        print("\n👋 Session interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")