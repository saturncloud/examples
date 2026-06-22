import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent
# Note: Switching from langchain_openai to the native browser_use wrapper
from browser_use.llm import ChatOpenAI

load_dotenv()

async def main():
    # The native wrapper handles all 'provider' and 'ainvoke' issues internally
    llm = ChatOpenAI(model="gpt-4o")
    
    task = "Go to https://news.ycombinator.com and tell me the title of the top post."
    
    agent = Agent(
        task=task,
        llm=llm,
        # We increase the failure limit slightly for complex sites
        max_failures=5 
    )
    
    print(f"🚀 Running Production Task: {task}")
    try:
        result = await agent.run()
        print("\n✅ Final Report:")
        print(result)
    except Exception as e:
        print(f"❌ Automation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
