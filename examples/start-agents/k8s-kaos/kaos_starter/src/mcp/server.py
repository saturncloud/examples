from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/tools/calculate")
def calculate():
    return {"tool": "calculator", "result": "The Kubernetes cluster is active and routing web traffic!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
