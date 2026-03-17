# ☸️ KAOS (Kubernetes Agent Orchestration System) Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Kubernetes YAML & Web App | **Tech Stack:** Kubernetes, FastAPI, Streamlit, MCP, In-Cluster LLM

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Protocol-MCP-8E75B2?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/In--Cluster_LLM-Ollama-white?style=for-the-badge&logo=ollama" alt="Ollama">
</p>

## 📖 Overview

This template provides a production-grade, distributed multi-agent web application built entirely on Kubernetes-native primitives. 

By decoupling the agent logic, the LLM, the tool server, and the web frontend into independent microservices, this architecture behaves exactly like a modern enterprise AI platform. It utilizes an **In-Cluster LLM** (Ollama) to guarantee zero data egress and zero per-token API costs.

### 🧩 Microservice Architecture
1. **Frontend (Streamlit):** Provides the user-facing web chat interface.
2. **Backend Agent (FastAPI):** Acts as the API. Receives user input from the frontend, queries MCP tools, and orchestrates the LLM.
3. **Tool Engine (MCP):** A Python server executing custom capabilities (e.g., calculations, system data fetching).
4. **AI Brain (Ollama):** Hosts the open-weight LLM (e.g., Qwen) entirely offline on the cluster.

---

## 🔐 Environment Configuration

Unlike traditional setups that rely on local `.env` files, KAOS uses Kubernetes internal DNS for secure microservice communication. 

The microservices find each other using internal URLs injected as environment variables inside the YAML manifests (e.g., `http://llm-service.kaos-system.svc.cluster.local:11434`). No internal backend traffic ever touches the public internet.

---

## 🚀 Local Setup & Execution Methods

Ensure you have Docker, `kubectl`, and Minikube installed on your host system (`minikube start --driver=docker`). This template supports two distinct ways to deploy:

### Method 1: Automated Full-Stack Bootstrap (Linux Recommended)

If you are running on a fresh Linux machine (like Kali or Ubuntu), use the included bootstrap script to automate the entire setup, build, and deployment process.

```bash
chmod +x kaos_bootstrap.sh
./kaos_bootstrap.sh
```
*This script provisions Minikube, builds all four microservice Docker images, injects them into the cluster, and downloads the `qwen2.5:0.5b` model into the LLM pod automatically.*

### Method 2: Manual Kubernetes Deployment

Great for learning the architecture, debugging, or making code changes.

**1. Build & Load the Docker Images**
Because Minikube runs in an isolated environment, you must build your custom images locally and explicitly load them into the cluster's internal registry:
```bash
sudo -E docker build -t kaos-mcp:latest ./src/mcp
sudo -E docker build -t kaos-agent:latest ./src/agent
sudo -E docker build -t kaos-frontend:latest ./src/frontend

minikube image load kaos-mcp:latest
minikube image load kaos-agent:latest
minikube image load kaos-frontend:latest
```

**2. Apply the Manifests & Download the Model**
```bash
kubectl apply -f manifests/
kubectl wait --for=condition=ready pod -l app=kaos-llm -n kaos-system --timeout=300s
kubectl exec deployment/kaos-llm -n kaos-system -- ollama pull qwen2.5:0.5b
```

---

## 🌐 Accessing the Web Dashboard

Because the Streamlit frontend is safely locked inside the Kubernetes cluster, you must explicitly route traffic from your host machine's browser into the cluster.

We achieve this using a Kubernetes `NodePort` service combined with Minikube's built-in routing command:

```bash
minikube service frontend-service -n kaos-system
```
*Running this command automatically locates the exposed port, builds a secure network bridge to your local machine, and opens the Streamlit chat interface directly in your default web browser.*

---

## ☁️ Cloud Deployment

To deploy this distributed agent architecture to production, migrate the local pods to **Saturn Cloud** resources. Saturn Cloud manages the Kubernetes control plane for you.

**Deployment Specifications:**

1. **The LLM Brain:** Saturn Cloud Deployment (GPU-backed, running `ollama/ollama:latest` with start script `ollama pull qwen2.5:0.5b`). *Must include Env Var: `OLLAMA_HOST=0.0.0.0:8000` to satisfy Saturn Cloud routing rules*.
2. **The MCP Tool Server:** Saturn Cloud Deployment (CPU-backed, running `python server.py`).
3. **The Agent API:** Saturn Cloud Deployment (CPU-backed, running `uvicorn app:app --host 0.0.0.0 --port 8000`). Update its `LLM_HOST` and `MCP_HOST` environment variables to point to the secure internal URLs of Deployments 1 & 2.
4. **The Web Frontend:** Saturn Cloud Deployment (CPU-backed, running `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`). Update its `AGENT_HOST` environment variable to point to Deployment 3. 

---

## 🧹 Clean Up

To safely destroy the local cluster and free up your system's RAM and CPU, use the included teardown script:

```bash
chmod +x teardown.sh
./teardown.sh
```
*(This safely deletes the namespace, terminates all pods, and stops Minikube).*

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Orchestration:** [Kubernetes Official Docs](https://kubernetes.io/docs/home/)
* **Local Testing:** [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)