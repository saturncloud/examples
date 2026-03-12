# 🌤️ PydanticAI Weather Agent 

*Deploy this AI agent on [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU | **Resource:** CLI Script, Streamlit Web App | **Tech Stack:** PydanticAI, Python, Streamlit

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-PydanticAI-E92063?style=for-the-badge" alt="PydanticAI">
  <img src="https://img.shields.io/badge/LLM-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Tool-Open--Meteo_API-00B0FF?style=for-the-badge" alt="Open-Meteo">
</p>

## 📖 Overview

This template provides a reference implementation for a Real-Time Weather Information Agent utilizing the **PydanticAI** framework. It demonstrates the framework's native capability to enforce strict type validation and schema generation during LLM tool calling.



The agent autonomously extracts location data from natural language queries, executes an external HTTP request to the open-source **Open-Meteo API** to retrieve geographical coordinates, and subsequently fetches real-time meteorological conditions. 

To facilitate both backend prototyping and production deployment, this repository provides two execution interfaces:
1. **Command-Line Interface (`weather_agent.py`):** A lightweight, interactive terminal loop for testing tool execution logic.
2. **Web Interface (`app.py`):** A Streamlit application utilizing session state management to render a production-grade conversational dashboard.

### Infrastructure Deployment (Saturn Cloud)

Deploying this architecture on [Saturn Cloud](https://saturncloud.io/) provides several environment benefits:
* **Persistent Compute:** Maintains the Streamlit server process and background terminal processes.
* **Secrets Management:** Secures API keys and environment variables via isolated `.env` configurations.
* **Rapid Provisioning:** Utilizes `uv` for high-speed package resolution and virtual environment creation.

---

## ✅ Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **OpenAI API Key:** Generate an LLM API token via the [OpenAI Developer Platform](https://platform.openai.com/). *(Note: The Open-Meteo API utilized for weather data is open-source and requires no authentication key).*

---

## 🏗️ Setup & Deployment

Open a terminal in your Saturn Cloud workspace and execute the following commands.

**1. Create Virtual Environment & Install Dependencies**
Utilize standard Python tools to provision the isolated environment and install the required packages.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure Environment Variables**
Create your `.env` file and define your API key.

```bash
cp .env.example .env
nano .env
# Define OPENAI_API_KEY. Save and exit (Ctrl+O, Enter, Ctrl+X).

```

---

## 💡 Execution Methods

### Method A: Command-Line Interface (Backend Testing)

To test the raw tool-calling logic and view system execution traces, initialize the terminal script:

```bash
python weather_agent.py

```

* Input your query when prompted. The system will log the Geocoding and Weather API calls before returning the final string.
* Input `exit` or `quit` to terminate the process.

### Method B: Web Application (Streamlit UI)

To launch the production-grade graphical interface, execute the Streamlit process:

```bash
streamlit run app.py

```

* Navigate to the **Local URL** output in the terminal (default: `http://localhost:8501`).
* Use the main chat interface to query the agent.

**Example Prompts:**

* *"What is the weather like in Tokyo right now?"*
* *"Should I wear a jacket in London today?"*
* *"Compare the current temperatures in New York and Sydney."*

---

## 📚 Official Documentation & References

For further customization, refer to the official documentation for the stack components used in this project:

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Agent Framework:** [PydanticAI Documentation](https://ai.pydantic.dev/)
* **LLM Provider:** [OpenAI API Reference](https://platform.openai.com/docs/)
* **Weather API Routing:** [Open-Meteo API Reference](https://open-meteo.com/en/docs)
* **Web UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)