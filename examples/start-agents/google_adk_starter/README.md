# 🤖 Google ADK Production Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Project & Web App | **Tech Stack:** Google ADK, Streamlit, Gemini 2.5, Open-Meteo API

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Type-Python_Project-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Script">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-Google_ADK-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google ADK">
</p>

## 📖 Overview

This template provides an enterprise-grade implementation of an AI agent using the open-source **Google Agent Development Kit (ADK)**. 

While Google ADK ships with a built-in development CLI (`adk web`), Google explicitly states it is not meant for production deployment. This template bridges that gap by demonstrating how to **programmatically execute ADK agents** inside a custom **Streamlit** dashboard using ADK's native `Runner` and `SessionService` classes.

### ✨ Key Capabilities
* **Programmatic ADK Execution:** Bypasses the ADK command line and embeds the agent directly into a custom Python application.
* **Asynchronous Session Management:** Uses Python's `asyncio` to securely mount ADK's `InMemorySessionService` inside Streamlit's synchronous execution loop.
* **Live API Tools:** Swaps out mocked data for real-world API connections, allowing the agent to fetch live, geocoded weather data from the open web using the Open-Meteo API.
* **Model Agnostic Routing:** Easily toggle between the free Google AI Studio endpoint (for local dev) and enterprise Google Cloud Vertex AI (for production).

---

## 🏗️ Local Setup & Installation

**1. Create Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment Variables**
Create an environment file to securely store your Gemini API key.

```bash
cp .env.example .env
nano .env

```

Inside your `.env` file, ensure you have the following configured:

```env
GOOGLE_API_KEY="your-gemini-api-key-here"
GOOGLE_GENAI_USE_VERTEXAI=FALSE

```

*(Note: Setting `USE_VERTEXAI=FALSE` instructs ADK to route via the Google AI Studio endpoint. Set this to `TRUE` if executing within a Google Cloud project).*

---

## 🚀 Execution & UI

Because this architecture utilizes a custom frontend, do **not** use the `adk web` or `adk run` terminal commands.

Launch the interactive Streamlit application directly:

```bash
streamlit run app.py

```

*The local server will initialize and bind to `http://localhost:8501`.*

---

## ☁️ Cloud Deployment

This repository is structured for containerized web hosting. To deploy this ADK application to a production environment, you can provision a resource on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Environment Variables:** Inject `GOOGLE_API_KEY` directly into the Saturn Cloud secrets manager. Do not commit your `.env` file.
3. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`
4. **Network Routing:** Ensure the deployment's exposed port matches the Streamlit configuration.

---

## 📁 Project Architecture

* `my_agent/agent.py`: Contains the core ADK `root_agent` definition and the Python functions that act as its toolset.
* `my_agent/__init__.py`: Required module initialization for the ADK framework.
* `app.py`: The custom Streamlit frontend that initializes the asynchronous ADK `Runner` and manages UI state.

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **ADK GitHub Repository:** [Google ADK Python](https://github.com/google/adk-python)
* **ADK Official Docs:** [Google ADK Documentation](https://google.github.io/adk-docs/)
* **UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
