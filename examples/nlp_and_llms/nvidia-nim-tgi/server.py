from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
from backend_tgi import tgi_chat
from backend_nim import nim_chat

app = FastAPI(title="NIM / TGI Drop-in API Server")

@app.post("/chat/local")
def chat_local(prompt: str = Form(...)):
    response = tgi_chat(prompt)
    return {"backend": "tgi-local", "response": response}


@app.post("/chat/nim")
def chat_nim(prompt: str = Form(...), stream: bool = False):
    if stream:
        generator = nim_chat(prompt, stream=True)
        return StreamingResponse(generator, media_type="text/event-stream")

    response = nim_chat(prompt, stream=False)
    return {"backend": "nvidia-nim", "response": response}


@app.get("/")
def root():
    return {"message": "NIM/TGI Server Running", "endpoints": ["/chat/local", "/chat/nim"]}
