# 🔒 Ollama Privacy Agent (Offline AI)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** Ollama, Llama 3.1, Python

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Provider-Ollama_Local-orange?style=for-the-badge" alt="Ollama">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

This template provides a production-ready implementation of a **100% Offline AI Agent** designed for high-security environments.

By leveraging **Ollama** and **Llama 3.1**, this agent can process sensitive data, execute local Python tools, and answer complex queries—all without a single byte of data leaving your Saturn Cloud instance. This is the ideal "source of truth" for clients requiring absolute data sovereignty.

### 🧩 Key Features

1.  **Absolute Privacy:** No external API calls; all inference happens on your local hardware.
2.  **Native Tool-Calling:** Demonstrates how local LLMs can "pause" reasoning to execute specialized Python functions (e.g., calculators, time-checkers).
3.  **Dual Interface:** Includes a lightweight developer CLI and a polished Streamlit web dashboard.

-----

## 🏗️ Local Setup & Installation

**1. Create the Environment & Install Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

-----

## ⚙️ Infrastructure Configuration

Unlike cloud-based agents, this template requires a local model server.

**1. Run the Automated Setup Script:**
This script installs the Ollama binary and pulls the **Llama 3.1** weights (approx. 4.7GB).

```bash
chmod +x setup_ollama.sh
./setup_ollama.sh
```

**2. Model Customization (Optional):**
If your hardware is limited (less than 15GB RAM), you can switch to a smaller model in `src/config.py`:

```python
OLLAMA_MODEL="llama3.2:1b"
```

-----

## 🚀 Execution & Testing

This repository is designed progressively. You can test the agent logic via the terminal or launch the full production dashboard.

### Phase 1: The Terminal CLI

Test the agent's tool-calling capabilities directly from your terminal:

```bash
python cli.py "Hey, what time is it right now?"
```

### Phase 2: The Streamlit Web Dashboard

Launch the interactive web UI for a ChatGPT-like experience with built-in tool execution:

```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow (Testing Tools):**
Once the UI is running, test the agent's ability to trigger its local Python tools:

1.  **Prompt 1:** *"What is the current time?"* (Triggers `get_current_time`)
2.  **Prompt 2:** *"If I invest $5,000 at 7% for 10 years, what is the growth?"* (Triggers `calculate_investment_growth`)

-----

## ☁️ Cloud Deployment

To deploy this privacy-first agent to production, use [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1.  **Resource Type:** Streamlit Deployment / Python Server.
2.  **Hardware:** - **Recommended:** GPU instance (NVIDIA T4 or L4) for zero-latency response.
      - **Minimum:** CPU instance with at least **16GB RAM** to support Llama 3.1 8B.
3.  **Persistent Storage:** Ensure the `/data` folder is mapped to persistent storage to avoid re-downloading model weights on restart.
4.  **Start Command:** `./setup_ollama.sh && streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

-----

## 📚 Official Documentation & References

  * **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
  * **Model Engine:** [Ollama Library](https://ollama.com/library)
  * **Core Model:** [Meta Llama 3.1](https://llama.meta.com/)
  * **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)
