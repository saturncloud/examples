# 💬 Nebius Chat (Token Factory Interface)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** Nebius AI, OpenAI SDK, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Provider-Nebius_AI-8A2BE2?style=for-the-badge" alt="Nebius">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

This template provides a production-ready, streaming chat interface for the **Nebius Token Factory** (Nebius AI Studio). 

Because Nebius provides an OpenAI-compatible API endpoint, this repository demonstrates how to seamlessly drop high-performance, open-source models (like Llama 3.3, Qwen, or DeepSeek) into existing OpenAI workflows simply by overriding the `base_url`.

### 🧩 Key Features
1. **Interactive Web UI:** A full Streamlit dashboard for a ChatGPT-like experience.
2. **Model Hot-Swapping:** Use the UI sidebar to instantly switch between Llama, DeepSeek, and Qwen without changing code.
3. **Contextual Memory:** Automatically maintains message history, allowing the models to remember prior questions and handle follow-up queries contextually.

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
Open the `.env` file and insert your active Nebius Token Factory API key. *(You can generate a free key at [studio.nebius.ai](https://studio.nebius.ai/))*.
```text
NEBIUS_API_KEY="your-actual-api-key-goes-here"
```

---

## 🚀 Execution & Testing

This repository is designed progressively. You can interact with Nebius via the terminal, or launch the full production dashboard.

### Phase 1: The Terminal CLI
Launch the lightweight, streaming terminal interface:
```bash
python nebius_chat.py
```

### Phase 2: The Streamlit Web Dashboard
Launch the interactive web UI to chat and hot-swap models:
```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow (Testing Memory):**
Once the UI boots up, test its contextual awareness by asking a multi-part question:
1. **Prompt 1:** *"I am traveling to Tokyo next week. What are three must-see neighborhoods?"*
2. **Prompt 2:** *"Which of those three is best for finding vintage electronics?"*
*(If the history array is working correctly, it will remember the three neighborhoods it just suggested and single out Akihabara without you needing to repeat yourself).*

---

## ☁️ Cloud Deployment

To deploy this multi-agent web application to production, you can provision a resource on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance (since the heavy inference processing is completely offloaded to Nebius's high-speed GPU endpoints).
3. **Environment Variables:** Inject your `NEBIUS_API_KEY` directly into the Saturn Cloud secrets manager (do not commit your `.env` file to version control).
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Model Provider:** [Nebius Token Factory Docs](https://docs.tokenfactory.nebius.com/)
* **SDK Reference:** [OpenAI Python Library](https://github.com/openai/openai-python)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)
