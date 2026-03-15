# 🐳 Docker Agent (Multi-Agent) Production Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** YAML Configuration & Web App | **Tech Stack:** Docker Agent, Python, MCP, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Docker_Agent-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Protocol-MCP-8E75B2?style=for-the-badge" alt="MCP">
</p>

## 📖 Overview

This template provides a production-grade multi-agent system. It utilizes **Docker Agent** as the declarative backend orchestration engine (handling memory, tool routing, and sub-agent delegation via YAML), and wraps it in a **Streamlit** web dashboard for end-user interaction.

By decoupling the CLI runtime from the frontend using a headless execution pattern (`docker agent exec`), this architecture behaves exactly like a modern AI microservice.

---

## 🏗️ Local Setup & Installation

**1. Install Python Dependencies**
Ensure you have Python installed for the MCP server and Streamlit frontend.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Install Docker Agent**

* **Mac/Windows:** Install **Docker Desktop 4.63+**, which includes the `docker agent` CLI plugin natively.
* **Linux (or Podman users):** Download the standalone binary directly from the official repository to bypass local container runtime conflicts:
```bash
curl -L -o docker-agent [https://github.com/docker/docker-agent/releases/latest/download/docker-agent-linux-amd64](https://github.com/docker/docker-agent/releases/latest/download/docker-agent-linux-amd64)
chmod +x docker-agent

```



---

## 🔐 Environment Configuration

Docker Agent runs as a compiled binary, meaning it reads environment variables directly from your active terminal session rather than automatically parsing `.env` files.

**1. Create your `.env` file:**

```bash
cp .env.example .env
# Edit .env and add your API keys (e.g., OPENAI_API_KEY or GOOGLE_API_KEY)

```

**2. Inject the variables into your terminal session:**
Run the following command before starting the agent to auto-export your `.env` contents into your active shell environment:

```bash
set -a; source .env; set +a

```

---

## 🚀 Execution Methods

This template supports two distinct ways to interact with the multi-agent system: an interactive terminal for debugging, and a web dashboard for production usage.

### Method 1: Interactive Terminal (TUI)

Great for debugging and watching the agents collaborate step-by-step in real-time.

**Run the command:**
*(If using Docker Desktop, use `docker agent run agent.yaml`)*

```bash
./docker-agent run agent.yaml

```

**Test Prompts:**
Paste these into the terminal sequentially to verify the tools and memory:

1. *"Please analyze the following text for me: 'Docker Agent allows developers to build complex multi-agent systems using a declarative YAML syntax. It is incredibly fast and modular.'"* (Tests Python MCP execution).
2. *"From now on, I want you to remember a strict formatting preference. Whenever you write an analysis report, you must output the final result entirely in markdown bullet points, and add a short, funny haiku at the very end."* (Tests SQLite Memory database).

### Method 2: Web Dashboard (Streamlit)

Great for end-user interaction. The web server programmatically executes the Docker Agent headlessly in the background.

**Run the command:**

```bash
streamlit run app.py

```

*The dashboard will automatically open in your browser at `http://localhost:8501`. Type your tasks into the chat box, and the UI will stream the final output once the backend agents complete their collaboration.*

---

## ☁️ Cloud Deployment

To deploy this multi-agent web application to production, you can provision a resource on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Environment Variables:** Inject your chosen model provider's API key directly into the Saturn Cloud secrets manager (do not commit your `.env` file).
3. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`
4. **Binary Inclusion:** Ensure the Linux `docker-agent` binary is downloaded and made executable within the container workspace during the build phase so the Streamlit subprocess can successfully call it.

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Docker Agent Repository:** [Docker Agent GitHub](https://github.com/docker/docker-agent)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)

