# 🐫 CAMEL-AI Model Benchmarker

*Deploy this AI Agent instantly on [Saturn Cloud](https://saturncloud.io/) — The premier platform for scalable Python workspaces and AI deployment.*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** CAMEL-AI, Streamlit, Pandas, Python

<p align="left">
  <img src="https://img.shields.io/badge/Type-Python_Script-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Script">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-CAMEL--AI-FF9900?style=for-the-badge" alt="CAMEL-AI">
  <img src="https://img.shields.io/badge/Testing-Benchmarking-00B0FF?style=for-the-badge" alt="Benchmarking">
</p>

## 📖 Overview

This template provides a robust, dual-entrypoint architecture for benchmarking Large Language Models (LLMs) using the **CAMEL-AI** multi-agent framework. 

It is specifically engineered to test execution latency and output generation across multiple distinct cloud infrastructures simultaneously. By leveraging CAMEL-AI's modular `ModelFactory`, developers can test an unlimited number of foundation models without having to rewrite the core agent orchestration logic.

### ✨ Key Capabilities
* **Dynamic Multi-Model Queue:** Queue up multiple models from entirely different cloud providers (OpenAI, Nebius, Crusoe) and benchmark them in a single, automated execution loop.
* **Per-Model Infrastructure Routing:** Easily benchmark custom or local infrastructure. The UI allows you to inject unique API keys and custom Base URLs for *each individual model* in your queue.
* **Smart Credential Fallbacks:** Leave the Key and URL fields blank in the UI to intelligently inherit default credentials securely from your `.env` file.
* **Privacy-First UI:** API keys entered into the dashboard are masked and stored strictly in temporary browser session state.
* **Dual-Entrypoint:** Execute benchmarks visually via the Streamlit web dashboard or headlessly via the terminal CLI.

---

## 🏗️ Setup & Installation

**1. Create Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment Variables**
Create an environment file to securely store your default credentials. The application will use these as fallbacks if you don't manually specify keys in the UI.

```bash
cp .env.example .env
nano .env
# Input your OpenAI, Nebius, and Crusoe keys. Save and exit.

```

---

## 💻 Method 1: Interactive Web Dashboard (Streamlit)

Spin up a local web server to visually build a queue of models, configure custom infrastructure endpoints, and visualize execution latency through automated charts.

```bash
streamlit run app.py

```

*The dashboard will automatically open in your default web browser (usually at `http://localhost:8501`).*

**How to use the UI:**

1. Select your target framework integration (e.g., Nebius Studio, OpenAI-Compatible).
2. Enter the Model ID (e.g., `deepseek-ai/DeepSeek-V3.2`).
3. *(Optional)* Enter a custom API key and Base URL. If testing Crusoe Inference, enter their proxy endpoint here. If left blank, the app will securely pull your default credentials from the `.env` file.
4. Click **Run Benchmark** to generate latency metrics and a visual comparison chart.

---

## 🖥️ Method 2: Headless CLI Script (Terminal)

For rapid execution, automated CI/CD pipelines, or remote SSH environments, run the terminal-based benchmarker. This script completely bypasses the UI, pulling credentials directly from your `.env` file and outputting a formatted tracking table.

```bash
python benchmark.py

```

---

## ⚙️ Supported Providers

This template natively routes requests to:

1. **OpenAI:** Uses the standard `ModelPlatformType.OPENAI` framework.
2. **Nebius AI Studio:** Uses CAMEL's native `ModelPlatformType.NEBIUS` integration.
3. **Crusoe Inference & Custom Clouds:** Uses `ModelPlatformType.OPENAI` but overrides the routing mechanism with custom Base URLs. Ensure your proxy endpoints stop at `/v1` (do not append `/chat/completions`).

---

## 📚 Official Documentation & References

* **Saturn Cloud Platform:** [Start building for free](https://saturncloud.io/)
* **Framework:** [CAMEL-AI Documentation](https://docs.camel-ai.org/)
* **Model Integration:** [CAMEL Models Guide](https://docs.camel-ai.org/key_modules/models)
* **UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)
