import os
from interpreter import interpreter
from .config import settings

class SystemAgent:
    def __init__(self):
        # 🎯 FIX: Force the environment variable into the OS
        # LiteLLM/OpenAI clients often require this even if attributes are set
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        
        # Standard configuration
        interpreter.llm.api_key = settings.openai_api_key
        interpreter.llm.model = settings.interpreter_model
        interpreter.auto_run = settings.auto_run
        
        interpreter.system_message += """
        You are a System-Level Agent running on a Saturn Cloud instance.
        You have authority to execute terminal commands and modify files.
        Always explain what a command does before running it.
        """

    def chat(self, message: str):
        return interpreter.chat(message, display=False, stream=True)

    def reset(self):
        interpreter.messages = []
