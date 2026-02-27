# Template: OpenAI SDK Starter

*Deployment Architecture: [Saturn Cloud](https://saturncloud.io/)*

**Hardware Requirements:** CPU | **Execution Interface:** Jupyter Notebook, Streamlit | **Stack:** Python, OpenAI SDK

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Type-Jupyter_Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/LLM-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## Overview

This template provides a reference implementation for the **OpenAI Python SDK**. It demonstrates system prompt configuration, conversational state management, and chat completion API execution.

The repository includes two execution interfaces:
1. **Interactive Prototyping (`openai_agents.ipynb`):** A Jupyter environment for executing raw SDK functions, formatting message arrays, and evaluating prompt structures.
2. **Web Interface (`app.py`):** A Streamlit application demonstrating state management and chunked streaming responses via a graphical interface.

Both implementations utilize two distinct system prompts: an **Email Helper** (professional drafting) and a **Haiku Writer** (structured constraint adherence).

### Deployment Infrastructure (Saturn Cloud)

Deploying this repository on [Saturn Cloud](https://saturncloud.io/) provides the following environment characteristics:
* **Compute Isolation:** Provisions dedicated instances for Python environment execution.
* **Process Persistence:** Maintains the Streamlit web server and Jupyter kernels in the background.
* **Configuration Management:** Isolates API keys and environment variables via `.env` configuration files.

---

## Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **OpenAI API Key:** Generate an API key via the [OpenAI Developer Platform](https://platform.openai.com/).

---

## Environment Initialization

Execute the following commands in the Saturn Cloud workspace terminal to configure the environment.

**1. Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate

```

**2. Install Package Dependencies**

```bash
pip install -r requirements.txt

```

**3. Configure Environment Variables**
Initialize the `.env` file and define the required API key.

```bash
cp .env.example .env
nano .env
# Define OPENAI_API_KEY. Save and exit the editor.

```

---

## Execution Methods

### Method A: Interactive Prototyping (Jupyter)

1. Initialize Jupyter Lab within the workspace.
2. Open `openai_agents.ipynb`.
3. Set the active kernel to the `venv` environment.
4. Execute the cells sequentially to evaluate the SDK parameters and prompt outputs.

### Method B: Web Interface (Streamlit)

1. Ensure the virtual environment is activated in the terminal.
2. Initialize the Streamlit server process:

```bash
streamlit run app.py

```

3. Navigate to the **Local URL** output in the terminal (default: `http://localhost:8501`).
4. **Interface Controls:**
* Select the target model (`gpt-3.5-turbo`, `gpt-4o-mini`, `gpt-4o`).
* Toggle between the predefined agent system prompts.
* Modulate the **Temperature** parameter (0.0 for deterministic output, >1.0 for randomized output).

---

## Official Documentation & References

For further architectural specification, refer to the official documentation:

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **SDK Reference:** [OpenAI Python SDK Repository](https://github.com/openai/openai-python)
* **Prompt Architecture:** [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
* **UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
