# LlamaIndex Task Manager Agent

*Deployment Architecture: [Saturn Cloud](https://saturncloud.io/)*

**Hardware Requirements:** CPU | **Execution Interface:** CLI Script, Streamlit Web App | **Stack:** Python, LlamaIndex, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-LlamaIndex-black?style=for-the-badge" alt="LlamaIndex">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## Overview

This template provides a reference implementation for a Retrieval-Augmented Generation (RAG) pipeline utilizing **LlamaIndex**. It demonstrates context ingestion, vector indexing, and stateful natural language querying against localized data.



The architecture reads from a local `./data` directory to ingest context files. To facilitate both backend prototyping and production deployment, this repository provides two execution interfaces:

1. **Command-Line Interface (`task_manager.py`):** A lightweight, interactive terminal loop for testing vector indexing and raw query logic.
2. **Web Interface (`app.py`):** A Streamlit application utilizing session state management and resource caching (`@st.cache_resource`) to maintain the vector index in active memory, preventing redundant disk I/O operations.

In both implementations, the LLM temperature is strictly modulated (`0.1`) to prioritize deterministic data extraction over generative variance.

### Deployment Infrastructure (Saturn Cloud)

Deploying this repository on [Saturn Cloud](https://saturncloud.io/) provides the following environment characteristics:
* **Compute Isolation:** Provisions dedicated instances for Python environment execution and localized vector indexing.
* **Process Persistence:** Maintains the Streamlit web server and background terminal processes.
* **File System Access:** Grants the LlamaIndex `SimpleDirectoryReader` direct read access to the persistent `/data` directory.

---

## Prerequisites

1. **Saturn Cloud Workspace:** Provision a CPU workspace via [Saturn Cloud](https://saturncloud.io/).
2. **OpenAI API Key:** Generate an API key via the [OpenAI Developer Platform](https://platform.openai.com/). *Note: LlamaIndex requires an active OpenAI API key for embedding generation and text completion functions.*

---

## Environment Initialization

Execute the following commands in the workspace terminal to configure the environment.

**1. Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate

```

**2. Upgrade Build Tools**
To prevent dependency resolution failures with modern micro-packages, upgrade the core Python build tools prior to installation:

```bash
python -m pip install --upgrade pip setuptools wheel

```

**3. Install Package Dependencies**
Install the modular LlamaIndex integrations and UI framework utilizing the `--no-cache-dir` flag to ensure clean dependency resolution:

```bash
pip install --no-cache-dir -r requirements.txt

```

**4. Configure Environment Variables**
Initialize the `.env` file and define the required API key.

```bash
cp .env.example .env
nano .env
# Define OPENAI_API_KEY. Save and exit the editor.

```

**5. Data Provisioning**
Verify that target context files (e.g., `tasks.txt`) are present within the local `data/` directory prior to server initialization.

---

## Execution Methods

### Method A: Command-Line Interface (Backend Testing)

To test the raw RAG logic without initializing the web server, run the terminal script:

```bash
python task_manager.py

```

* Use standard input to query the indexed data.
* Input `exit` or `quit` to terminate the process.

### Method B: Web Application (Streamlit UI)

To launch the production-grade graphical interface, execute the Streamlit process:

```bash
streamlit run app.py

```

* Navigate to the **Local URL** output in the terminal (default: `http://localhost:8501`).
* The application will cache the vector index upon initialization to optimize subsequent conversational turns.

**Query Execution Examples:**

* "What are the pending items for Project Alpha?"
* "List all administrative tasks requiring attention before the 15th."
* "Are there any meetings scheduled with the design team?"

---

## Official Documentation & References

* **Deployment Platform:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Framework Reference:** [LlamaIndex Documentation](https://docs.llamaindex.ai/)
* **UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
