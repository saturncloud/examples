from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import invoke_agent

# Initialize the FastAPI application
app = FastAPI(
    title="AWS Strands Weather Agent API",
    description="A production-ready microservice utilizing the AWS Strands SDK.",
    version="1.0.0"
)

# Define the expected JSON payload schema
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

# Health check endpoint for load balancers and container orchestrators
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# The primary AI interaction endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Route the query to the Strands agent logic
        agent_reply = invoke_agent(request.query)
        return ChatResponse(response=agent_reply)
    except Exception as e:
        # Gracefully handle framework or network errors
        raise HTTPException(status_code=500, detail=f"Agent Execution Error: {str(e)}")