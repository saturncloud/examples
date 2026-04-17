import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory

load_dotenv()

class BusinessLogicPlugin:
    @kernel_function(
        description="Calculates the project completion date based on start date and duration.",
        name="CalculateTimeline"
    )
    def calculate_timeline(self, start_date: str, weeks: int) -> str:
        return f"Based on a start date of {start_date}, the project will conclude in {weeks} weeks."

async def main():
    api_key = os.getenv("OPENAI_API_KEY")
    model_id = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o")

    if not api_key or api_key == "sk-...":
        print("❌ ERROR: OpenAI API Key is missing or default in .env file.")
        return

    # 1. Initialize the Kernel
    kernel = Kernel()

    # 2. Add the AI Service
    service_id = "chat-gpt"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=model_id,
            api_key=api_key,
        )
    )

    # 3. Register Plugins
    kernel.add_plugin(BusinessLogicPlugin(), plugin_name="ProjectManager")

    # 4. Initialize Chat History
    history = ChatHistory()
    history.add_system_message("You are an enterprise assistant. Use the ProjectManager plugin for timeline queries.")

    print(f"🧩 Semantic Kernel Copilot Active [Model: {model_id}]")
    print("(Type 'exit' to quit)")
    
    # 💡 THE FIX: Use FunctionChoiceBehavior instead of manual tool_choice
    # This tells the service to automatically discover and send tools to OpenAI.
    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id=service_id, 
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == "exit":
            break

        history.add_user_message(user_input)
        
        try:
            # The Kernel now handles the tool mapping automatically
            result = await kernel.get_service(service_id).get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel,
            )
            
            print(f"Copilot: {result.content}")
            history.add_assistant_message(result.content)
            
        except Exception as e:
            print(f"❌ API ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
