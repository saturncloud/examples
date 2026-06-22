# 🐝 OpenAI Swarm Triage

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** OpenAI Swarm, Python, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Swarm-000000?style=for-the-badge&logo=openai&logoColor=white" alt="Swarm">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

## 📖 Overview

This template provides a lightweight, highly effective multi-agent system using **OpenAI Swarm**. It demonstrates seamless agent-to-agent handoffs for a customer support routing scenario.

Instead of a monolithic prompt, this architecture relies on a specialized **Triage Agent** that assesses the user's intent and dynamically transfers the conversation to the specialized **Sales**, **Tech Support**, or **Billing** agents by utilizing Python functions as handoff triggers.

---

## 🏗️ Local Setup & Installation

**1. Create the Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

**1. Create your `.env` file:**
```bash
cp .env.example .env
```

**2. Add your Provider Keys:**
Open the `.env` file and insert your active API key.
```text
OPENAI_API_KEY="sk-your-openai-key-goes-here"
```

---

## 🚀 Execution & Testing

This repository includes both a terminal script and a full interactive Web Dashboard.

### Phase 1: The Terminal CLI
Watch the agents seamlessly hand off the conversation in your terminal:
```bash
python triage_cli.py
```

### Phase 2: The Streamlit Web Dashboard
Launch the visual interface to track exactly which agent is currently active via the sidebar indicator:
```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow:**
To see the Triage agent properly hand off the conversation, try typing these distinct scenarios one by one:
1. **The Sales Test:** *"Hi, I am looking to upgrade my account to the enterprise tier. How much is it?"*
2. **The Billing Test:** *"Wait, I actually need a refund for my last invoice. It charged me twice."*
3. **The Tech Test:** *"Also, my application keeps throwing an 'Error 500' when I try to log in. Please fix it."*

*(Watch how the active agent name changes to handle each specific domain!)*

---

## ☁️ Cloud Deployment

To deploy this multi-agent routing system to production on [Saturn Cloud](https://saturncloud.io/):

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance (Swarm orchestration is extremely lightweight).
3. **Environment Variables:** Inject your `OPENAI_API_KEY` directly into the Saturn Cloud secrets manager.
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Agent Framework:** [OpenAI Swarm GitHub](https://github.com/openai/swarm)
EOF
```

### 🚀 Let's Test It!
Make sure to add your OpenAI key to your `.env` file, then run `streamlit run app.py`. Pay close attention to the sidebar—you will see the "Currently speaking with" status dynamically change from *Triage Agent* to *Tech Support Agent* based purely on what you ask!
