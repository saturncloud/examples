import os
import sys
from dotenv import load_dotenv
import autogen
from autogen.coding import LocalCommandLineCodeExecutor

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

work_dir = "coding"
os.makedirs(work_dir, exist_ok=True)

llm_config = {"model": "gpt-4o-mini", "api_key": api_key}

print("==================================================")
print("🤖 Microsoft AutoGen Starter Initialized")
print("🛠️  Mode: Collaborative Coding & Local Execution (CLI)")
print(f"📂 Workspace: ./{work_dir}/")
print("==================================================\n")

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
    system_message="""You are a helpful AI assistant. You write Python code to solve tasks. 
Always wrap your code in standard markdown code blocks.
The user proxy will execute your code and report the output back to you.
DO NOT output 'TERMINATE' in the same message where you write code. 
WAIT for the user proxy to run the code and confirm it worked. 
ONLY output 'TERMINATE' when the user proxy confirms the execution was successful and the task is fully complete.""",
)

executor = LocalCommandLineCodeExecutor(timeout=60, work_dir=work_dir)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"executor": executor},
)

task = input("🎯 What would you like the agents to build today?\n> ")

if not task.strip():
    print("No task provided. Exiting.")
    sys.exit(0)

print("\n💬 Starting agent conversation...\n")

user_proxy.initiate_chat(assistant, message=task)
print("\n✅ Task Complete! Check the 'coding' folder for any generated scripts or files.")
