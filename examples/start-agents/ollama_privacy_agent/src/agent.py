import ollama
from .tools import AVAILABLE_TOOLS
from .config import settings

class PrivacyAgent:
    def __init__(self):
        self.model = settings.ollama_model
        self.system_prompt = {
            'role': 'system', 
            'content': 'You are a helpful, privacy-first AI assistant with access to local tools. '
                       'When you use a tool, look at the result provided and use that information '
                       'to give a direct answer to the user. Do not just say you called the tool; '
                       'state the actual result (e.g., "The current time is 10:30 AM").'
        }

    def chat(self, user_input, history=None):
        if history is None: history = []
        
        # Build the initial message chain
        messages = [self.system_prompt] + history + [{'role': 'user', 'content': user_input}]
        
        # 1. First Call: Ask model if it needs a tool
        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=[
                {
                    'type': 'function',
                    'function': {
                        'name': 'get_current_time',
                        'description': 'Get the current local system time.',
                    },
                },
                {
                    'type': 'function',
                    'function': {
                        'name': 'calculate_investment_growth',
                        'description': 'Calculate financial growth using principal, rate, and years.',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'principal': {'type': 'number'},
                                'rate': {'type': 'number'},
                                'years': {'type': 'integer'},
                            },
                            'required': ['principal', 'rate', 'years'],
                        },
                    },
                },
            ],
        )

        message = response.get('message', {})
        
        # 2. Check for Tool Calls
        if message.get('tool_calls'):
            # The model wants to use a tool
            for tool in message['tool_calls']:
                name = tool['function']['name']
                args = tool['function']['arguments']
                
                if name in AVAILABLE_TOOLS:
                    print(f"🛠️ Executing local tool: {name}")
                    # Get actual data from Python
                    result = AVAILABLE_TOOLS[name](**args)
                    
                    # 3. SECOND CALL: Give the tool output back to the model for "Synthesis"
                    # We MUST include the model's tool_call message and the tool's response message
                    final_response = ollama.chat(
                        model=self.model,
                        messages=messages + [
                            message, 
                            {'role': 'tool', 'content': f"The tool returned: {result}"}
                        ]
                    )
                    return final_response['message']['content']
        
        # If no tool was needed, return the normal response
        return message.get('content', "I'm sorry, I couldn't process that.")
