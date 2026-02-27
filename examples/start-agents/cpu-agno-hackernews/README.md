# Template: HackerNews Analysis Agent

*Deploy this AI agent on [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU | **Resource:** Terminal & Streamlit | **Tech Stack:** Python, Agno, Nebius AI, SQLite

![Hackernew Analyst Agent](image.png)

## 📖 Overview

This template provides a Streamlit web interface for a HackerNews Analyst Agent. Built using the [Agno](https://github.com/agno-agi/agno) framework and the **Nebius AI** model (`Qwen/Qwen3-30B-A3B-Instruct-2507`), this agent executes data retrieval and analysis of tech news.

The application tracks trending topics and analyzes user engagement. It utilizes a local **SQLite** database to maintain session state and conversation history across interactions.

### Infrastructure Deployment (Saturn Cloud)

Deploying this architecture on [Saturn Cloud](https://saturncloud.io/) provides several environment benefits:

* **Environment Isolation:** Provisions dedicated compute resources for Python package execution without local dependency conflicts.
* **Persistent Compute:** Maintains the Streamlit server process in the background.
* **Secrets Management:** Secures API keys and environment variables via isolated `.env` configurations.

---

## ✅ Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **Nebius API Key:** Generate an LLM API token via the [Nebius Token Factory](https://studio.nebius.ai/).

---

## 🏗️ Phase 1: Environment Setup

Open a terminal in your Saturn Cloud workspace and execute the following commands.

**1. Create and Activate the Virtual Environment**

```bash
# Create the virtual environment named 'venv'
python -m venv venv

# Activate it
source venv/bin/activate

```

**2. Install Dependencies**

```bash
pip install -r requirements.txt

```

**3. Configure Environment Variables**

Create your `.env` file and define your API key.

```bash
cp .env.example .env
nano .env  # Define NEBIUS_API_KEY. Save and exit.

```
---

## 🚀 Phase 2: Execution (Streamlit UI)

The application uses Agno's `HackerNewsTools` to query live data and a local **SQLite Database** (`agent_memory.db`) to persist conversation history.

1. Ensure your virtual environment is activated, then initialize the Streamlit server:

```bash
streamlit run app.py

```

2. Navigate to the **Local URL** provided in the terminal output (default: `http://localhost:8501`) to access the web interface.
3. Input natural language commands in the main chat interface.

**Example Prompts:**

* *"What are the most discussed topics on HackerNews today?"*
* *"Can you compare that to the trends from last week?"*

---

## 🐘 Production Scaling (PostgreSQL)

By default, this template uses a local **SQLite** database as it requires no initial configuration. For multi-user deployments, the architecture supports migrating to **PostgreSQL**.

**Migration Steps (No Application Logic Changes Required):**

1. Provision a Postgres Database.
2. Install the Postgres driver in your terminal: `pip install psycopg2-binary`
3. In `app.py`, modify the Agno storage backend from SQLite to Postgres:

```python
from agno.db.postgres import PostgresDb

# Replace the SQLite configuration in get_agent() with:
db=PostgresDb(
    table_name="hn_agent_sessions", 
    db_url="postgresql+psycopg2://user:password@host:5432/dbname"
)

```
---

## 📚 Official Documentation & References

For further customization, refer to the official documentation for the stack components used in this project:

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Agent Framework:** [Agno Framework](https://github.com/agno-agi/agno)
* **LLM Provider:** [Nebius AI Studio](https://docs.nebius.com/studio/)
* **Web UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
