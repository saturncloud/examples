from vllm import LLM, SamplingParams
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

# -----------------------------
# ⚙️ Model Setup
# -----------------------------
# Use the Llama 3 model ID
MODEL_ID = "meta-llama/Meta-Llama-3-70B-Instruct"

# ---- Tensor Parallelism ----
TENSOR_PARALLEL = 4

# -----------------------------
# 🚀 Initialize vLLM
# -----------------------------
print(f"🔄 Loading model {MODEL_ID} using vLLM tensor parallelism...")
llm = LLM(
    model=MODEL_ID,
    tensor_parallel_size=TENSOR_PARALLEL,
    gpu_memory_utilization=0.95, # High utilization as recommended
    dtype="bfloat16",             # Use bfloat16 for Ampere GPUs (A40/3090/etc)
    enforce_eager=True,           # Fixes AsyncEngineDead issues
    max_model_len=8128,           # Matches the context length in the guide
)

sampling = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512
)

# -----------------------------
# 🌐 FastAPI (OpenAI-style API)
# -----------------------------
app = FastAPI(title="vLLM Tensor Parallel Server")


class ChatRequest(BaseModel):
    model: str
    messages: list



@app.post("/v1/chat/completions")
async def chat(req: ChatRequest):
    user_msg = req.messages[-1]["content"]

    outputs = llm.generate([user_msg], sampling)
    # Access the first element of the list before accessing attributes
    text = outputs[0].outputs[0].text 

    return {
        "id": "tensorpar-chat",
        "object": "chat.completion",
        "model": req.model,
        "choices": [
            {"index": 0, "message": {"role": "assistant", "content": text}}
        ]
    }


# -----------------------------
# ▶️ Run the Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
