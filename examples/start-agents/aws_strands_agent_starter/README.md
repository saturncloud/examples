# 🌤️ AWS Strands Agent Starter (Dual-Entrypoint)

*Deploy this production-ready AI agent on [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Project & API | **Tech Stack:** AWS Strands SDK, FastAPI, OpenAI, Docker

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Framework-AWS_Strands-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS Strands">
  <img src="https://img.shields.io/badge/Provider-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Tool-Open--Meteo_API-00B0FF?style=for-the-badge" alt="Open-Meteo">
</p>

## 📖 Overview

This template provides a dual-entrypoint implementation of a model-driven AI Agent utilizing the open-source **AWS Strands SDK**. 

It features a shared core architecture (`app/agent.py`) that can be executed in two ways:
1. **Interactive CLI (`weather_agent.py`):** For rapid local prototyping and terminal-based debugging.
2. **Production Microservice (`app/main.py`):** A high-performance FastAPI backend that allows external applications to query the agent asynchronously via standard HTTP REST endpoints.

---

## 🏗️ Setup & Installation

**1. Create Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment Variables**
Create a `.env` file in the root directory.

```bash
cp .env.example .env
nano .env
# Define OPENAI_API_KEY. Save and exit.

```

---

## 💻 Method 1: Interactive CLI (Prototyping)

Use the CLI script to test new prompts, verify tool execution, and chat with the agent directly in your terminal.

```bash
python weather_agent.py

```

**Example Prompts:**

* *"What is the weather like in Tokyo right now?"*
* *"Should I wear a jacket in London today?"*

To terminate the interactive loop, input `exit`.

---

## 🌐 Method 2: FastAPI Microservice (Production)

Serve the agent as a RESTful web API for integration with frontends, mobile apps, or other microservices.

**Run the Server:**

```bash
uvicorn app.main:app --reload

```

**Test the API:**
Once the server is running, FastAPI automatically generates an interactive Swagger UI documentation page at `http://127.0.0.1:8000/docs`, allowing you to test the agent visually.

Alternatively, send a standard POST request:

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/api/chat](http://127.0.0.1:8000/api/chat)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What is the weather like in Tokyo right now?"
}'

```

---

### Install Docker and Build the Container

Run these commands one by one in your terminal to install and start the Docker engine:

**1. Update your package manager:**

```bash
sudo apt update

```

**2. Install Docker:**

```bash
sudo apt install -y docker.io

```

**3. Start the Docker service:**

```bash
sudo systemctl start docker
sudo systemctl enable docker

```

**4. Add your user to the Docker group (so you don't have to type `sudo` every time):**

```bash
sudo usermod -aG docker $USER
newgrp docker

## 🐳 Docker Deployment

To deploy this application to production environments (like AWS ECS or cloud container registries), build and run the included Dockerfile.

```bash
docker build -t strands-weather-agent .
docker run -p 8000:8000 --env-file .env strands-weather-agent

```

---

## 📚 Official Documentation & References

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Agent Framework:** [AWS Strands Agents Documentation](https://strandsagents.com/latest/)
* **API Framework:** [FastAPI Documentation](https://fastapi.tiangolo.com/)
* **Weather API Routing:** [Open-Meteo API Reference](https://open-meteo.com/en/docs)
