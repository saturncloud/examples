# 🧠 Letta (MemGPT) Production Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Docker Compose & Python UI | **Tech Stack:** Letta, Streamlit, PostgreSQL, Docker

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Letta-8A2BE2?style=for-the-badge" alt="Letta">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

## 📖 Overview

This template provides a production-ready, full-stack implementation of **Letta (formerly MemGPT)**. 

Traditional LLMs suffer from context window limitations, causing them to forget information over time. Letta resolves this using an "LLM Operating System" architecture that divides memory into Core Memory (immediate context) and Archival Memory (infinite vector storage). The agent autonomously edits, appends, and replaces its own memory blocks, resulting in a perpetually stateful AI companion.

### Infrastructure Deployment
This template uses a decoupled microservice architecture for maximum scalability:
* **The Backend (Docker Compose):** Manages the Letta API Server and a dedicated PostgreSQL database. It utilizes an `init.sql` script to automatically inject the `pgvector` extension on boot, ensuring the Archival Memory tables compile perfectly.
* **The Frontend (Python Launcher):** A lightweight client layer (`run.py`) that connects to the backend API, allowing you to interface with the agent via a headless Terminal CLI or a rich Streamlit Web Dashboard.

---

## ✅ Prerequisites

1. **Docker & Docker Compose:** Required to run the Letta backend and PostgreSQL database.
2. **Python 3.10+:** Required for the frontend UI clients.
3. **OpenAI API Key:** Required for the core LLM and Embedding models. Generate one at the [OpenAI Developer Platform](https://platform.openai.com/api-keys).

---

## 🏗️ Setup & Deployment

**1. Configure Environment Variables**
```bash
cp .env.example .env
```
Open `.env` and add your active `OPENAI_API_KEY`. Ensure `LETTA_PG_URI` is pointing to the Dockerized database (`postgresql+asyncpg://letta:letta@letta_db:5432/letta`).

**2. Spin Up the Backend Services**
Launch the Letta Server and Postgres database. On the very first boot, the system will inject the `vector` extension and run ~150 Alembic schema migrations.
```bash
sudo docker compose up -d
```
*(Note: Wait ~15-30 seconds on the initial boot for the database tables to build before launching the frontend. You can verify readiness with `sudo docker logs letta-server`).*

**3. Setup the Frontend Environment**
Create a virtual environment and install the client dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Launch the UI**
Run the frontend orchestrator to connect to the backend:
```bash
python run.py
```
*(Select Option 1 for the Streamlit UI, or Option 2 for headless terminal testing).*

---

## 💡 Usage Guide

Once the Streamlit Web Dashboard is running, you can interact with the agent and monitor its internal state in real-time. Use the **Database Inspector** in the right-hand sidebar to visualize the agent actively editing its own Postgres memory blocks.

**Example Prompts to Test Stateful Memory:**
* *"Hi, my name is Alex and I am severely allergic to peanuts."* (Click 'Refresh Database' to watch the agent rewrite its 'Human' core memory block).
* *"I'm going to a baseball game today, what kind of snacks should I get?"* (The agent will proactively exclude peanuts based on its retained memory).
* *"What was my name again, and what did I tell you about my diet?"*

---

## 📚 Official Documentation & References

* [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* [Letta Official Documentation](https://docs.letta.com/)
* [pgvector Documentation](https://github.com/pgvector/pgvector)
