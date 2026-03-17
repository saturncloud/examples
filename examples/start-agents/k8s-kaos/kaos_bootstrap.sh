#!/bin/bash
set -e

echo "======================================================="
echo "🚀 KAOS V2: FULL-STACK WEB ARCHITECTURE BOOTSTRAP 🚀"
echo "======================================================="

echo "🔄 Phase 1: Installing Dependencies (Requires Sudo)..."
sudo apt-get update
sudo apt-get install -y curl docker.io
unset DOCKER_HOST
sudo systemctl enable docker
sudo systemctl start docker

echo "📦 Installing kubectl & minikube..."
curl -LO --retry 3 "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
curl -LO --retry 3 https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

echo "🚀 Starting Minikube cluster..."
minikube start --driver=docker

echo "======================================================="
echo "📁 Phase 2: Writing Full-Stack Microservices..."
echo "======================================================="
mkdir -p kaos_starter/src/mcp kaos_starter/src/agent kaos_starter/src/frontend kaos_starter/manifests
cd kaos_starter

echo "🛠️ 1/3: Writing MCP Server..."
cat << 'INNER_EOF' > src/mcp/server.py
from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/tools/calculate")
def calculate():
    return {"tool": "calculator", "result": "The Kubernetes cluster is active and routing web traffic!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
INNER_EOF

cat << 'INNER_EOF' > src/mcp/Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY server.py .
CMD ["python", "server.py"]
INNER_EOF

echo "🧠 2/3: Writing FastAPI Agent Backend..."
cat << 'INNER_EOF' > src/agent/app.py
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
INNER_EOF

cat << 'INNER_EOF' > src/agent/Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn pydantic requests
COPY app.py .
CMD ["python", "app.py"]
INNER_EOF

echo "🖥️ 3/3: Writing Streamlit Web Frontend..."
cat << 'INNER_EOF' > src/frontend/app.py
import streamlit as st
import requests
import os

AGENT_API_URL = os.getenv("AGENT_HOST", "http://agent-service.kaos-system.svc.cluster.local:8080/chat")
st.title("☸️ KAOS Web Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask the KAOS swarm..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Agent is thinking..."):
        try:
            res = requests.post(AGENT_API_URL, json={"message": prompt})
            reply = res.json().get("reply", "No response from agent.")
        except Exception as e:
            reply = f"Error connecting to agent: {e}"
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
INNER_EOF

cat << 'INNER_EOF' > src/frontend/Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install streamlit requests
COPY app.py .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
INNER_EOF

echo "======================================================="
echo "🐳 Phase 3: Building & Injecting Images..."
echo "======================================================="
sudo -E docker build -t kaos-mcp:latest ./src/mcp
sudo -E docker build -t kaos-agent:latest ./src/agent
sudo -E docker build -t kaos-frontend:latest ./src/frontend

minikube image load kaos-mcp:latest
minikube image load kaos-agent:latest
minikube image load kaos-frontend:latest

echo "======================================================="
echo "☸️ Phase 4: Deploying Kubernetes Manifests..."
echo "======================================================="
cat << 'INNER_EOF' > manifests/00-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: kaos-system
INNER_EOF

cat << 'INNER_EOF' > manifests/01-llm-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kaos-llm
  namespace: kaos-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kaos-llm
  template:
    metadata:
      labels:
        app: kaos-llm
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
---
apiVersion: v1
kind: Service
metadata:
  name: llm-service
  namespace: kaos-system
spec:
  selector:
    app: kaos-llm
  ports:
    - protocol: TCP
      port: 11434
      targetPort: 11434
INNER_EOF

cat << 'INNER_EOF' > manifests/02-mcp-server.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kaos-mcp
  namespace: kaos-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kaos-mcp
  template:
    metadata:
      labels:
        app: kaos-mcp
    spec:
      containers:
      - name: mcp-server
        image: kaos-mcp:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-service
  namespace: kaos-system
spec:
  selector:
    app: kaos-mcp
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
INNER_EOF

cat << 'INNER_EOF' > manifests/03-agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kaos-agent
  namespace: kaos-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kaos-agent
  template:
    metadata:
      labels:
        app: kaos-agent
    spec:
      containers:
      - name: agent-engine
        image: kaos-agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: agent-service
  namespace: kaos-system
spec:
  selector:
    app: kaos-agent
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
INNER_EOF

cat << 'INNER_EOF' > manifests/04-frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kaos-frontend
  namespace: kaos-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kaos-frontend
  template:
    metadata:
      labels:
        app: kaos-frontend
    spec:
      containers:
      - name: frontend
        image: kaos-frontend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8501
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: kaos-system
spec:
  type: NodePort
  selector:
    app: kaos-frontend
  ports:
    - protocol: TCP
      port: 8501
      targetPort: 8501
INNER_EOF

kubectl apply -f manifests/

echo "======================================================="
echo "⏳ Phase 5: Waiting for Infrastructure to Boot..."
echo "======================================================="
kubectl wait --for=condition=ready pod -l app=kaos-llm -n kaos-system --timeout=300s
echo "🧠 Downloading the Qwen AI brain into the LLM pod..."
kubectl exec deployment/kaos-llm -n kaos-system -- ollama pull qwen2.5:0.5b

echo "======================================================="
echo "🎉 SUCCESS! Your Full-Stack KAOS Swarm is ALIVE!"
echo "======================================================="
echo "To open the Web UI in your browser, run this exact command:"
echo ""
echo "    minikube service frontend-service -n kaos-system"
echo ""
echo "======================================================="
