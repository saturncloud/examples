# 🕸️ LangChain-LangGraph Starter

*Deploy this AI workflow on [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU | **Resource:** Jupyter Notebook, Streamlit Web App | **Tech Stack:** LangChain, LangGraph, Python, Streamlit

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-LangChain-1C3C3C?style=for-the-badge" alt="LangChain">
  <img src="https://img.shields.io/badge/Framework-LangGraph-FF0000?style=for-the-badge" alt="LangGraph">
</p>

## 📖 Overview

This template provides a foundational implementation of a stateful, tool-calling agent workflow utilizing **LangChain** and **LangGraph**. It demonstrates the transition from linear LLM execution to cyclic, graph-based orchestration with conditional edge routing.

By defining a `StateGraph`, the architecture supports complex agentic capabilities. The system utilizes LangGraph's conditional routing to autonomously determine when to answer directly and when to route execution to an external computational tool (`calculate_multiply`) before returning the final response.

### Infrastructure Deployment (Saturn Cloud)

Deploying this architecture on [Saturn Cloud](https://saturncloud.io/) provides several environment benefits:
* **Dual Interfaces:** Provisions robust CPU instances capable of simultaneously running JupyterLab for backend graph prototyping and Streamlit for frontend client access.
* **State Management:** Maintains the Streamlit server process in the background, isolating client session states.
* **Environment Isolation:** Secures API keys within `.env` configurations and manages package dependencies via virtual environments.

---

## ✅ Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **OpenAI API Key:** Generate an API token via the [OpenAI Developer Platform](https://platform.openai.com/).

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
Create your `.env` file and define your API key.

```bash
cp .env.example .env
nano .env
# Define OPENAI_API_KEY. Save and exit (Ctrl+O, Enter, Ctrl+X).

```

**3. Register Jupyter Kernel (Optional for Notebook Development)**

```bash
python -m ipykernel install --user --name=venv --display-name="Python (venv)"

```

---

## 💡 Execution Methods

### Method A: Production Web Interface (Streamlit)

To launch the production-grade graphical interface with live tool calling:

```bash
streamlit run app.py

```

* Navigate to the **Local URL** output in the terminal (default: `http://localhost:8501`).
* **Test Prompts:** * *"Explain LangGraph in one sentence."* (Executes direct LLM response path)
* *"What is 456 multiplied by 789?"* (Triggers the conditional tool-calling edge)



### Method B: Interactive Backend Prototyping (Jupyter)

1. Open `workflow_starter.ipynb` in the Jupyter interface.
2. Ensure the kernel is set to **Python (venv)**.
3. Execute the cells sequentially to test the graph compilation and internal state manipulation prior to UI deployment.

---

## 🧪 Testing

This template includes automated testing capabilities utilizing `pytest` and `nbmake` to validate the Jupyter Notebook's graph schema execution.

```bash
pytest --nbmake workflow_starter.ipynb

```

---

## 📚 Official Documentation & References

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **AI Framework:** [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
* **Graph Orchestration:** [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
* **Web UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
