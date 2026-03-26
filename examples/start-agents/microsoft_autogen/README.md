# 🤖 Microsoft AutoGen Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** AutoGen, Python, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-AutoGen-0078D4?style=for-the-badge" alt="AutoGen">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

This template provides a production-ready framework for multi-agent conversations using **Microsoft AutoGen**. It demonstrates how to orchestrate autonomous AI agents that can collaborate, write code, and execute it locally on the host machine to solve complex tasks.

### 🧩 Key Features
1. **The Assistant Agent:** Acts as the cognitive engine, generating Python code to fulfill custom user requests.
2. **The User Proxy Agent:** Acts as the execution engine, taking the Assistant's code, running it in a secure local environment, and feeding any terminal errors back to the Assistant for autonomous debugging.
3. **Local Code Execution:** Utilizes `LocalCommandLineCodeExecutor` to sandbox file creation, script execution, and artifact generation into a dedicated `/coding` directory.
4. **Dynamic Artifact Rendering:** The Streamlit UI automatically scans the workspace and renders any generated image files directly in the chat interface.

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

This repository includes both a CLI terminal script and a full interactive Web Dashboard. Both interfaces allow you to type custom requests for the agents to execute.

### Phase 1: The Terminal CLI
Launch the lightweight terminal interface:
```bash
python autogen_cli.py
```

### Phase 2: The Streamlit Web Dashboard
Launch the visual interface to see the conversation history and generated artifacts directly in your browser:
```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow:**
Once the app is running, paste these prompts into the chat box to test the agents' coding and debugging capabilities:

**1. The Data Visualization Test:**
> *"Fetch the Year-To-Date (YTD) stock prices for NVDA and MSFT using yfinance. Plot the prices on a single line chart using matplotlib. Save the plot to a file named 'tech_stocks.png'."*
*(Watch the agents fetch live data, handle missing dependencies if necessary, and render the chart in your browser!)*

**2. The Algorithm & File System Test:**
> *"Write a Python script that calculates the first 50 Fibonacci numbers, saves them to a CSV file called 'fibonacci.csv', and then plots a line chart showing their exponential growth. Save the chart as a PNG."*
*(Verifies the agents can write custom mathematical algorithms, interact with your local file system, and dynamically save multiple file types).*

---

## ☁️ Cloud Deployment

To deploy this multi-agent workflow to production as a Web App on [Saturn Cloud](https://saturncloud.io/):

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance.
3. **Environment Variables:** Inject your `OPENAI_API_KEY` directly into the Saturn Cloud secrets manager (do not commit your `.env` file to version control).
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Agent Framework:** [AutoGen Official Docs](https://microsoft.github.io/autogen/)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)
