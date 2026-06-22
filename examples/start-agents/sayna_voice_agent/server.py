import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()

# The exact JSON you copied from Deepgram!
AGENT_SETTINGS = {
  "type": "Settings",
  "audio": {
    "input": {
      "encoding": "linear16",
      "sample_rate": 16000 # Adjusted to standard browser mic rate
    },
    "output": {
      "encoding": "linear16",
      "sample_rate": 24000,
      "container": "none"
    }
  },
  "agent": {
    "language": "en",
    "speak": {
      "provider": {
        "type": "deepgram",
        "model": "aura-2-odysseus-en"
      }
    },
    "listen": {
      "provider": {
        "type": "deepgram",
        "version": "v2",
        "model": "flux-general-en"
      }
    },
    "think": {
      "provider": {
        "type": "google",
        "model": "gemini-2.5-flash"
      },
      "prompt": "You are Sayna, a highly intelligent, warm, and concise voice assistant. Keep all responses to 1-2 sentences maximum. Do not use markdown."
    },
    "greeting": "Hello! I am Sayna, your voice agent. How can I help you?"
  }
}

async def handle_client(client_ws):
    """Handles the connection from the frontend browser."""
    print("🟢 Browser frontend connected.")
    
    # Connect directly to Deepgram's conversational Agent API
    dg_uri = "wss://agent.deepgram.com/v1/agent/converse"
    headers = {"Authorization": f"Token {os.getenv('DEEPGRAM_API_KEY')}"}
    
    try:
        async with websockets.connect(dg_uri, additional_headers=headers) as dg_ws:
            print("🚀 Connected to Deepgram Voice Agent API!")
            
            # 1. Send the Settings JSON first to configure the brain/ears/mouth
            await dg_ws.send(json.dumps(AGENT_SETTINGS))
            
            # 2. Task to forward User Microphone -> Deepgram
            async def mic_to_deepgram():
                async for message in client_ws:
                    # Only forward binary audio data to Deepgram
                    if isinstance(message, bytes):
                        await dg_ws.send(message)
            
            # 3. Task to forward Deepgram Audio/Events -> User Browser
            async def deepgram_to_speaker():
                async for message in dg_ws:
                    await client_ws.send(message)
                    
                    # Optional: Print out the text logs so you can see what the agent is thinking
                    if isinstance(message, str):
                        data = json.loads(message)
                        if data.get("type") == "ConversationText":
                            role = data.get("role", "unknown")
                            content = data.get("content", "")
                            print(f"[{role.upper()}]: {content}")
                            
            # Run both streaming tasks at the same time
            await asyncio.gather(mic_to_deepgram(), deepgram_to_speaker())
            
    except Exception as e:
        print(f"🔴 Connection closed: {e}")

async def main():
    print("📡 Sayna Voice Server listening on ws://localhost:8000")
    async with websockets.serve(handle_client, "localhost", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())