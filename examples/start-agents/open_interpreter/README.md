# 🤖 Open Interpreter CLI (System-Level Agent)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script | **Tech Stack:** Open Interpreter, Streamlit, Python

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Provider-OpenAI-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

This template provides a high-authority **System-Level Agent** powered by Open Interpreter. Unlike standard chatbots, this agent has direct access to the local shell, allowing it to execute terminal commands, install system dependencies, and modify the file system through natural language. It is designed to act as a "DevOps Partner" within your Saturn Cloud instance.

### 🧩 Key Features

1.  **Autonomous OS Interaction:** The agent can navigate directories, read system logs, and manage local processes directly through the bash terminal.
2.  **Multi-Language Execution:** Capable of writing and running Python, JavaScript, and Shell scripts in real-time to solve complex system tasks.
3.  **Human-in-the-Loop Safety:** Configured with `auto_run: False` by default, ensuring all system-altering commands require user verification before execution.

-----

## 🏗️ Setup & Installation

To support the latest **Python 3.13** runtime on Linux/Kali, system-level build tools are required for Rust-based dependencies like `tiktoken`.

```bash
# 1. Install System Dependencies (Required for Rust/Python 3.13 builds)
sudo apt update && sudo apt install rustc cargo python3-tk -y

# 2. Create and Activate Environment
python3 -m venv venv
source venv/bin/activate

# 3. Configure Build Environment (Crucial for Python 3.13)
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# 4. Install Project
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

-----

## ⚙️ Infrastructure & Configuration

**1. Environment Variables:**
Create a `.env` file in the root directory:

  * `OPENAI_API_KEY`: Your OpenAI Secret Key.
  * `INTERPRETER_MODEL`: Set to `gpt-4o` for optimal system reasoning.
  * `AUTO_RUN`: Set to `False` (Recommended) to review commands before they run.

-----

## 🚀 Execution & Testing (Phased Approach)

### Phase 1: The CLI (Direct Shell Access)

Test the agent's ability to "see" your Saturn Cloud environment.

```bash
python cli.py
```

### Phase 2: The UI (Streaming Dashboard)

Launch the web interface for a cleaner, logged interaction.

```bash
streamlit run app.py
```

### 🧪 Recommended Testing Flow

1.  **System Audit:** *"Check my current disk usage and list the top 5 largest files in the current project folder."*
2.  **File Manipulation:** *"Create a python script named 'hello.py' that prints 'Saturn Cloud' ten times, then execute that script and show me the output."*

-----

## ☁️ Cloud Deployment Specs

| Component | Specification |
| :--- | :--- |
| **Resource Type** | Streamlit Deployment / Python Project |
| **Hardware (Min)** | CPU - 2 Cores | 4GB RAM |
| **Hardware (Rec)** | GPU - T4 (For local model offloading) |
| **Env Variables** | `OPENAI_API_KEY`, `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` |
| **Start Command** | `streamlit run app.py --server.port 8000 --server.address 0.0.0.0` |

-----

## 📚 Official Documentation & References

  * [Open Interpreter Documentation](https://docs.openinterpreter.com/)
  * [Saturn Cloud Custom Templates](https://saturncloud.io/docs/)
  * [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)

**Developed for Saturn Cloud Custom Templates.**


