# 🔒 Composio GitHub Reviewer (Agentic DevOps)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/). Optimized for **Python 3.13** and **LangGraph v0.3**.*

**Hardware:** CPU/GPU | **Resource:** Python Project & Web App | **Tech Stack:** Composio, LangChain, OpenAI, LangGraph

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Provider-Composio-8A2BE2?style=for-the-badge" alt="Composio">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Architecture-LangGraph-orange?style=for-the-badge" alt="LangGraph">
</p>

## 📖 Overview

This template provides a production-ready **Agentic Workflow** for automated GitHub management. Built on the 2026 **ReAct (Reason + Action)** architecture, this agent uses a stateful graph to interact directly with the GitHub API. It doesn't just "talk"—it "does."

### 🧩 Key Features

1.  **Stateful ReAct Graph:** Uses LangGraph to ensure the agent never "hallucinates" a refusal; it is forced to use its tools to fetch real-time data.
2.  **OAuth 2.0 Provider:** Implements a professional-grade authentication bridge via Composio, moving beyond fragile Personal Access Tokens.
3.  **Filtered Tooling:** Optimized to use a curated set of GitHub actions, reducing token noise and increasing reasoning accuracy.

-----

## 🏗️ Local Setup & Installation

```bash
# Recommendation: Use Python 3.13
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

-----

## ⚙️ Phase 1: GitHub & Composio Integration (Crucial)

To give the agent "hands," you must establish the OAuth bridge between Composio and GitHub.

### 1\. Register GitHub OAuth App

  * Go to your [GitHub Developer Settings](https://github.com/settings/developers) \> **OAuth Apps** \> **New OAuth App**.
  * **Application Name:** `Saturn_Cloud_Reviewer`
  * **Homepage URL:** `https://composio.dev`
  * **Authorization callback URL:** `https://backend.composio.dev/api/v3/toolkits/auth/callback`
  * Register, then **Generate a Client Secret**. Copy both the **Client ID** and **Client Secret**.

### 2\. Configure Composio Auth

  * Go to the [Composio Auth Configs](https://www.google.com/search?q=https://app.composio.dev/auth-configs).
  * Create a **New Auth Config** for **GitHub**.
  * Set **Authentication Method** to `OAuth 2.0`.
  * Toggle **"Use your own developer credentials"** to **ON**.
  * Paste your GitHub **Client ID** and **Client Secret**.
  * Click **Create Auth Config**, then click **Connect Account** and complete the GitHub login.

### 3\. Retrieve your User ID

  * In the Composio sidebar, click **Users**.
  * Copy your unique **ID** (e.g., `user_abc123...`). You will need this for your `.env`.

-----

## 🔑 Phase 2: Environment Variables

Copy `.env.example` to `.env` and fill in the following:

  * `OPENAI_API_KEY`: Your OpenAI Secret Key.
  * `COMPOSIO_API_KEY`: Found in the [Composio Dashboard](https://www.google.com/search?q=https://app.composio.dev/settings/api-keys).
  * `COMPOSIO_USER_ID`: The unique User ID from the Composio "Users" tab.
  * `MODEL_NAME`: Default is `gpt-4o`.

-----

## 🚀 Execution & Testing

### The Terminal CLI

Verify the agent's ability to fetch GitHub data:

```bash
python cli.py "List the first 3 repositories in [your-username] github"
```

### The Streamlit Web Dashboard

Launch the professional interface for ongoing PR management:

```bash
streamlit run app.py
```

-----

## ☁️ Cloud Deployment (Saturn Cloud)

1.  **Resource:** Streamlit Deployment.
2.  **Hardware:** CPU (Minimum 4GB RAM).
3.  **Secrets:** Inject `OPENAI_API_KEY`, `COMPOSIO_API_KEY`, and `COMPOSIO_USER_ID` via Saturn Cloud Secrets.
4.  **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

-----

## 📚 References

  * [Composio v1.2 Documentation](https://docs.composio.dev/)
  * [LangGraph Prebuilt Agents](https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/)
  * [Saturn Cloud Documentation](https://saturncloud.io/docs/)
  * [Composio Toolset Docs](https://docs.composio.dev/)
  * [LangChain Agents Guide](https://python.langchain.com/docs/modules/agents/)



