# 🤖 Template: HackerNews Analysis Agent

*Deploy this AI Agent instantly on [Saturn Cloud](https://saturncloud.io/) — The premier platform for scalable Python workspaces and AI deployment.*

**Hardware:** CPU | **Resource:** Terminal & Streamlit | **Tech Stack:** Python, Agno, Nebius AI, SQLite

![Hackernew Analyst Agent](image.png)

## 📖 Overview

This template provides a ready-to-deploy **HackerNews Analyst Agent** built with the [Agno](https://github.com/agno-agi/agno) framework. Powered by the highly capable **Nebius AI** model (`Qwen/Qwen3-30B-A3B-Instruct-2507`), this agent acts as your personal tech news curator.

It is deployed as an interactive Streamlit web application that tracks trending topics, analyzes user engagement, and features **SQLite persistent memory** so it remembers your conversation history across different chat sessions.

### 🌟 Why Run This on Saturn Cloud?

Building AI agents locally can be a headache due to dependency conflicts, hardware limitations, and secure key management. By running this template on [Saturn Cloud](https://saturncloud.io/), you get:

* **Pre-configured Compute:** Launch a CPU or GPU workspace in seconds.
* **Always-On Workspaces:** Keep your Streamlit server running in the background.
* **Secure Secrets:** Safely manage your API keys using `.env` files within a secure cloud boundary.

---

## ✅ Prerequisites

1. **Saturn Cloud Account:** Sign up for free at [saturncloud.io](https://saturncloud.io/).
2. **Nebius API Key:** Get your LLM access token from the [Nebius Token Factory](https://studio.nebius.ai/).

---

## 🏗️ Phase 1: Environment Setup

Using a Python virtual environment ensures your dependencies are perfectly isolated. Open a terminal in your Saturn Cloud workspace and run the following:

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

**3. Configure your `.env` File**
Copy the example file and add your actual API key securely:

```bash
cp .env.example .env
nano .env  # Open the file and insert your Nebius API Key

```

---

## 🚀 Phase 2: Running the Agent (Streamlit UI)

The Tech News Analyst is designed as a fully interactive web application. It uses Agno's native `HackerNewsTools` to pull live internet data and a local **SQLite Database** (`agent_memory.db`) to remember your past questions.

1. Ensure your virtual environment is activated, then start the Streamlit server:
```bash
streamlit run app.py

```


2. Open the provided `Local URL` (usually `http://localhost:8501`) in your web browser.
3. Try asking the agent natural language questions like:
* *"What are the most discussed topics on HackerNews today?"*
* *"Can you compare that to the trends from last week?"* (The agent will remember your previous questions!)



---

## 🐘 Scaling Up to Production

By default, this template uses a local **SQLite** database because it requires zero configuration to get started inside your Saturn Cloud environment. However, if you plan to deploy this agent for multiple users, you should upgrade to **PostgreSQL**.

**How to Switch (Zero Logic Changes Required):**

1. Provision a Postgres Database.
2. Install the Postgres driver in your terminal: `pip install psycopg2-binary`
3. In `app.py`, simply swap the Agno storage backend from SQLite to Postgres:
```python
from agno.db.postgres import PostgresDb

# Replace the SQLite line in get_agent() with:
db=PostgresDb(
    table_name="hn_agent_sessions", 
    db_url="postgresql+psycopg2://user:password@host:5432/dbname"
)

```



---

## 📚 Learn More & Resources

Ready to build even more complex AI agents? Check out these resources:

* **Saturn Cloud Platform:** [Start building for free](https://saturncloud.io/)
* **Saturn Cloud Documentation:** [Explore deployment guides](https://saturncloud.io/docs/)
* **Saturn Cloud Blog:** [Read the latest AI tutorials](https://saturncloud.io/blog/)

## 🤝 Contributing

Contributions to expand the agent's capabilities are welcome!

* Built with the **Agno Framework**
* Powered by **Nebius Token Factory**

---