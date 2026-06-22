import os
import sys
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

load_dotenv()

if not os.getenv("HF_TOKEN"):
    print("❌ Error: HF_TOKEN not found in .env file.")
    sys.exit(1)

model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

custom_instructions = """You are a Code Agent. Your job is to search the web and provide answers.
CRITICAL RULES FOR TEXT PARSING:
1. NEVER write Python code to parse, clean, or format text. 
2. NEVER use RegEx (re.search, re.findall) or string manipulation (.split, .replace) on search results.
3. Once you call the web_search tool, simply READ the output in your context window, and pass a natural language summary directly into the final_answer() tool."""


# Notice the change here: 'instructions' instead of 'system_prompt'
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()], 
    model=model,
    additional_authorized_imports=["datetime", "math"],
    instructions=custom_instructions
)

print("==================================================")
print("🤗 Hugging Face smolagents Initialized")
print("🛠️  Mode: Minimalist Web-Surfing Code Agent")
print("💡 Type 'exit' to quit.")
print("==================================================\n")

while True:
    try:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        if not user_input.strip():
            continue

        print("🤖 Agent is thinking and writing code...\n")
        response = agent.run(user_input)
        print(f"\n✨ Final Answer: {response}")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
