# 📅 Template: Production Scheduling Agent Dashboard

*Deploy this autonomous AI agent instantly on [Saturn Cloud](https://saturncloud.io/) — The premier platform for scalable Python workspaces and AI deployment.*

**Hardware:** CPU | **Resource:** Streamlit Web App | **Tech Stack:** Python, Agno, Nebius AI, Cal.com API, Streamlit

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-Agno-FF6F00?style=for-the-badge" alt="Agno">
  <img src="https://img.shields.io/badge/LLM-Nebius_AI-8A2BE2?style=for-the-badge" alt="Nebius AI">
  <img src="https://img.shields.io/badge/Tool-Cal.com_API-24292e?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Cal.com">
</p>

## 📖 Overview
This template provides a **production-grade dashboard** for an Autonomous Scheduling Agent. Built with **Streamlit** and the **Agno** framework, it allows users to interact with an AI that can take real actions on their calendar.

Unlike static chatbots, this agent connects directly to your **Cal.com** account. Through a chat interface, you can ask it to check availability, book meetings, or list upcoming events, and it will execute those tasks autonomously.

### 🌟 Why Run This on Saturn Cloud?
By deploying this agent on [Saturn Cloud](https://saturncloud.io/), you get a true production environment out of the box:
* **Always-On Workspaces:** Keep your Streamlit server running securely in the background.
* **Secure Secrets Management:** Keep your API keys safe using `.env` files without risking accidental exposure.
* **Instant Environments:** Launch a pre-configured Python environment in seconds without cluttering your local machine.

---

## ✅ Prerequisites
1. **Saturn Cloud Workspace:** [Sign up for free](https://saturncloud.io/) and spin up a CPU workspace.
2. **Nebius API Key:** Get your LLM token from the [Nebius Token Factory](https://studio.nebius.ai/).
3. **Cal.com API Key:** Go to **Settings -> Developer -> API Keys** in your free [Cal.com](https://cal.com/) account and create a key that never expires.

---

## 🏗️ Setup & Deployment

Open a terminal in your Saturn Cloud workspace and run the following commands.

**1. Create Virtual Environment & Install**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Secrets**
Create your `.env` file and securely add your two API keys.

```bash
cp .env.example .env
nano .env
# Paste NEBIUS_API_KEY and CALCOM_API_KEY. Save and exit (Ctrl+O, Enter, Ctrl+X).

```

**3. Launch the Dashboard**
Start the Streamlit server safely inside your workspace.

```bash
streamlit run app.py

```

Click the **Local URL** provided in the terminal (usually `http://localhost:8501`) to open the dashboard.

---

## 💡 How to Use the Dashboard

1. **Dynamic Configuration:** Use the sidebar on the left to configure the agent.
* Search for and select your exact **Timezone** from the dropdown menu.
* Select the **Meeting Type** you want the agent to book (e.g., "15 Min Meeting"). The app fetches these dynamically from your Cal.com account!


2. **Chat:** In the main chat bar, give natural language commands.

**Example Prompts:**

* *"Check my availability for tomorrow between 9am and 12pm."*
* *"Book a meeting with 'Saturn Test' at test@example.com for tomorrow at 10am."*
* *"What bookings do I have coming up for test@example.com?"*

The agent will show a spinner while it thinks, interacts with the APIs, and executes the scheduling.

---

## 📚 Official Documentation & References

To customize this template further, refer to the official documentation for the stack used in this project:

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Agent Framework:** [Agno (PhiData) Documentation](https://docs.agno.com/)
* **LLM Provider:** [Nebius AI Studio Documentation](https://docs.nebius.com/studio/)
* **Scheduling Engine:** [Cal.com API Reference](https://www.google.com/search?q=https://cal.com/docs/introduction/api)
* **Web UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
