import os, requests
from fastapi import FastAPI
from pydantic import BaseModel

LLM_HOST = os.getenv("LLM_HOST", "http://llm-service.kaos-system.svc.cluster.local:11434")
MCP_HOST = os.getenv("MCP_HOST", "http://mcp-service.kaos-system.svc.cluster.local:8000")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    print(f"📥 Received: {req.message}", flush=True)
    try:
        mcp_res = requests.get(f"{MCP_HOST}/tools/calculate").json()
        tool_data = mcp_res.get("result", "No data")
    except Exception:
        tool_data = "Tool offline."

    dynamic_prompt = f"System Data: '{tool_data}'. User asks: '{req.message}'. Provide a helpful response."
    llm_payload = {"model": "qwen2.5:0.5b", "prompt": dynamic_prompt, "stream": False}
    
    llm_res = requests.post(f"{LLM_HOST}/api/generate", json=llm_payload).json()
    return {"reply": llm_res.get('response', 'Error generating response')}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
