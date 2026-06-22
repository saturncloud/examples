# 🐝 Agno AI Examples (Market Intelligence Swarm)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Repository & Web App | **Tech Stack:** Agno (v2.5+), LanceDB, Streamlit, DuckDuckGo Search

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Agno-F2E222?style=for-the-badge&logoColor=black" alt="Agno">
  <img src="https://img.shields.io/badge/Vector_DB-LanceDB-FF4B4B?style=for-the-badge" alt="LanceDB">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

## 📖 Overview

This template provides a simple, progressive introduction to building production-grade multi-agent systems with web search and local knowledge bases. It utilizes **Agno** (formerly Phidata) to abstract away the complexities of tool calling, unified vector embeddings, and RAG (Retrieval-Augmented Generation), wrapping the final architecture in an interactive **Streamlit** Web UI.

### 🧩 The Market Intelligence Swarm
The final application deploys a cohesive `Team` of specialized AI agents:
1. **🌐 Web Researcher:** Scours the live internet for breaking news using DuckDuckGo.
2. **📚 Knowledge Keeper:** Reads and answers questions based on private internal documents using a local LanceDB vector database.
3. **👔 Lead Editor:** The swarm leader. It takes your prompt from the chat UI, delegates research tasks to the Web and Knowledge agents, and synthesizes their findings into a polished report.

---

## 🏗️ Local Setup & Installation

Because this architecture relies on a local vector database (LanceDB) rather than heavy containerization, it can be run entirely within a standard Python virtual environment.

**1. Create the Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Prepare the Dummy Knowledge Base**
Create a `data/` folder and add a test file for the Knowledge agent to read. For example, create `data/company_history.txt`:
```text
CONFIDENTIAL INTERNAL MEMO
Company: Acme Corp
Founded: 2010

Major Milestones:
- 2015: Reached $1M in annual recurring revenue.
- 2022: Survived the great market crash by pivoting to cloud infrastructure.
- 2025: Secretly launched the "Quantum AI Engine", which boosted internal efficiency by 200%. The CEO plans to make this public later this year.
```

---

## 🔐 Environment Configuration

Agno securely loads your API keys via the `python-dotenv` library.

**1. Create your `.env` file:**
```bash
cp .env.example .env
```

**2. Add your Provider Keys:**
Open the `.env` file and insert your active API key.
```text
OPENAI_API_KEY="sk-your-actual-api-key-goes-here"
```

---

## 🚀 Execution Methods & Testing

This repository is designed progressively. Run the scripts in order to see how single agents evolve into a multi-agent swarm, culminating in a full Web UI.

### Phase 1: CLI Fundamentals
Test the basic building blocks in your terminal:
```bash
# 1. Test basic tool calling and live web connectivity
python 01_simple_search_agent.py

# 2. Test the RAG pipeline (Embeds the data/ folder into LanceDB)
python 02_knowledge_base_agent.py

# 3. Test agentic delegation (Editor orchestrates the Researcher and Keeper)
python 03_multi_agent_swarm.py
```

### Phase 2: Production Web Dashboard
Launch the interactive Streamlit UI to chat with the Lead Editor from your browser:
```bash
streamlit run 04_streamlit_ui.py
```

**🧪 The Ultimate Swarm Test Prompt:**
Once the Streamlit UI opens in your browser (`http://localhost:8501`), paste this exact question into the chat box to force the Swarm to combine your private PDF data with live internet data:

> *"What is Acme Corp's secret project, and how does it compare to the biggest AI news today?"*

Watch the UI as the Lead Editor seamlessly tasks the Knowledge Keeper to read the internal memo, tasks the Web Researcher to browse the internet, and synthesizes both into a final market intelligence report!

---

## ☁️ Cloud Deployment

To deploy this multi-agent web application to production, you can provision a resource on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance (or GPU if swapping OpenAI for a local open-weight model).
3. **Environment Variables:** Inject your `OPENAI_API_KEY` directly into the Saturn Cloud secrets manager (do not commit your `.env` file to version control).
4. **Start Command:** `streamlit run 04_streamlit_ui.py --server.port 8000 --server.address 0.0.0.0`
5. **Persistent Storage:** Ensure your `data/` and `lancedb/` directories are mounted to persistent storage so your vector embeddings survive container restarts.

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Agent Framework:** [Agno Official Docs](https://docs.agno.com/)
* **Vector Database:** [LanceDB Documentation](https://lancedb.github.io/lancedb/)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)
