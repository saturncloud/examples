import os
import time
from dotenv import load_dotenv
from prettytable import PrettyTable

# Core CAMEL-AI imports
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent

# Initialize environment variables
load_dotenv()

def run_benchmark():
    print("--- 🐫 CAMEL-AI Benchmarking Tool (CLI Mode) ---")
    print("Providers: OpenAI | Nebius AI | Crusoe Inference\n")
    
    # Define the models based on your exact API keys
    models_to_test = [
        {
            "name": "OpenAI (GPT-4o-Mini)",
            "platform": ModelPlatformType.OPENAI,
            "type": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "url": None
        },
        {
            "name": "Nebius Studio (DeepSeek-V3.2)",
            "platform": ModelPlatformType.NEBIUS,
            "type": "deepseek-ai/DeepSeek-V3.2",     
            "api_key": os.getenv("NEBIUS_API_KEY"),
            "url": None
        },
        {
            "name": "Crusoe Inference (Qwen-3-235B)",
            "platform": ModelPlatformType.OPENAI,           
            "type": "Qwen/Qwen3-235B-A22B-Instruct-2507", 
            "api_key": os.getenv("CRUSOE_API_KEY"),
            "url": os.getenv("CRUSOE_API_BASE")             
        }
    ]

    test_prompt = (
        "Write a concise, high-level overview of the history of artificial intelligence, "
        "highlighting the major winters and breakthroughs. Keep it strictly under 150 words."
    )
    
    results = PrettyTable()
    results.field_names = ["Provider / Model Name", "Status", "Exec Time (s)", "Response Length (chars)"]
    results.align = "l"

    print(f"Executing benchmark prompt across {len(models_to_test)} endpoints...")
    print(f"Prompt: '{test_prompt}'\n")

    for m in models_to_test:
        if not m["api_key"]:
            print(f"   [Skipping] {m['name']} - No API Key found in .env")
            results.add_row([m['name'], "⚠️ Skipped (No Key)", "-", "-"])
            continue
            
        print(f"Testing {m['name']}...")
        try:
            # Build the dynamic arguments
            factory_kwargs = {
                "model_platform": m['platform'],
                "model_type": m['type'],
                "model_config_dict": {"temperature": 0.0},
                "api_key": m['api_key']
            }
            if m['url']:
                factory_kwargs["url"] = m['url']

            camel_model = ModelFactory.create(**factory_kwargs)
            agent = ChatAgent(system_message="You are a highly efficient, objective technical writer.", model=camel_model)
            
            start_time = time.time()
            response = agent.step(test_prompt)
            end_time = time.time()
            
            exec_time = round(end_time - start_time, 2)
            content = response.msgs[0].content if hasattr(response, 'msgs') else response.msg.content
            
            results.add_row([m['name'], "✅ Success", exec_time, len(content)])
            
        except Exception as e:
            print(f"   [Error] Failed to execute {m['name']}: {str(e)[:100]}...")
            results.add_row([m['name'], "❌ Failed", "-", "-"])

    print("\n--- Benchmark Results ---")
    print(results)

if __name__ == "__main__":
    run_benchmark()