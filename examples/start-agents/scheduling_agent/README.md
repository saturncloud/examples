# 📅 Scheduling Agent Dashboard

*Deploy this AI agent on [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU | **Resource:** Streamlit Web App | **Tech Stack:** Python, Agno, Nebius AI, Cal.com API, Streamlit

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-Agno-FF6F00?style=for-the-badge" alt="Agno">
  <img src="https://img.shields.io/badge/LLM-Nebius_AI-8A2BE2?style=for-the-badge" alt="Nebius AI">
  <img src="https://img.shields.io/badge/Tool-Cal.com_API-24292e?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Cal.com">
</p>

## 📖 Overview

This template provides a Streamlit web interface for an Autonomous Scheduling Agent. Built using the **Agno** framework, it enables users to interact with an AI agent capable of executing calendar operations via tool calling.

The agent integrates directly with the **Cal.com** API. Through the chat interface, users can query availability, create bookings, or retrieve upcoming events. The agent autonomously handles the routing and API execution required to fulfill these requests.

### Infrastructure Deployment (Saturn Cloud)

Deploying this architecture on [Saturn Cloud](https://saturncloud.io/) provides several environment benefits:
* **Persistent Compute:** Maintains the Streamlit server process in the background.
* **Secrets Management:** Secures API keys and environment variables via isolated `.env` configurations.
* **Environment Isolation:** Provisions dedicated compute resources for Python package execution without local dependency conflicts.

---

## ✅ Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **Nebius API Key:** Generate an LLM API token via the [Nebius Token Factory](https://studio.nebius.ai/).
3. **Cal.com API Key:** Generate an API key from **Settings -> Developer -> API Keys** in your [Cal.com](https://cal.com/) account.

---

## 🏗️ Setup & Deployment

Open a terminal in your Saturn Cloud workspace and execute the following commands.

**1. Create Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment Variables**
Create your `.env` file and define your API keys.

```bash
cp .env.example .env
nano .env
# Define NEBIUS_API_KEY and CALCOM_API_KEY. Save and exit (Ctrl+O, Enter, Ctrl+X).

```

**3. Initialize the Application**
Start the Streamlit server process.

```bash
streamlit run app.py

```

Navigate to the **Local URL** provided in the terminal output (default: `http://localhost:8501`) to access the web interface.

---

## 💡 Usage Guide

1. **Configuration:** Use the left sidebar to set the agent parameters.

* Select your target **Timezone** (IANA format) from the dropdown menu.
* Select the **Meeting Type** you wish to book (e.g., "15 Min Meeting"). The application fetches these dynamically via the Cal.com API.

2. **Execution:** Input natural language commands in the main chat interface.

**Example Prompts:**

* *"Check my availability for tomorrow between 9am and 12pm."*
* *"Book a meeting with 'Saturn Test' at test@example.com for tomorrow at 10am."*
* *"What bookings do I have coming up for test@example.com?"*

The UI will indicate a processing state while the agent interfaces with the LLM and Cal.com APIs to execute the scheduling logic.

---

## 📚 Official Documentation & References

For further customization, refer to the official documentation for the stack components used in this project:

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Agent Framework:** [Agno (PhiData) Documentation](https://docs.agno.com/)
* **LLM Provider:** [Nebius AI Studio Documentation](https://docs.nebius.com/studio/)
* **Scheduling Engine:** [Cal.com API Reference](https://www.google.com/search?q=https://cal.com/docs/introduction/api)
* **Web UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)

