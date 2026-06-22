# 🌐 Browser-Use Automator

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script | **Tech Stack:** Browser-Use, Playwright, LangChain

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Browser--Use-orange?style=for-the-badge" alt="Browser-Use">
  <img src="https://img.shields.io/badge/Engine-Playwright-2EAD33?style=for-the-badge&logo=playwright" alt="Playwright">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
</p>

## 📖 Overview

The **Browser-Use Automator** is a production-grade template designed for AI-driven web navigation and data extraction. Unlike traditional scrapers that rely on fragile CSS selectors, this agent utilizes a vision-capable LLM to "see" the browser's Document Object Model (DOM). It interacts with elements (buttons, inputs, complex JS dropdowns) exactly like a human user, making it ideal for automating tasks across dynamic or authenticated websites.

### Infrastructure Deployment
* **Compute & Vision:** The agent requires an LLM with strong reasoning capabilities (GPT-4o) to process visual element coordinates and DOM trees.
* **Environment Isolation:** The template utilizes Playwright as the high-performance browser controller, supporting both **Headless** (background execution) and **Headed** (visible window) modes.
* **Binary Provisioning:** To ensure cross-distribution compatibility (e.g., Kali, Ubuntu, Debian), the setup script automatically handles fallback Chromium and FFmpeg binary installations.

---

## ✅ Prerequisites

1. **Python 3.10+**: Required for the asynchronous automation loop.
2. **OpenAI API Key**: Generate one via the [OpenAI Platform Dashboard](https://platform.openai.com/api-keys).
3. **System Dependencies**: Ensure `libgbm-dev` and `libnss3` are installed on your Linux host.

---

## 🏗️ Setup & Deployment

**1. Environment Setup**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m playwright install chromium
```

**2. Configure Secrets**
```bash
cp .env.example .env
# Enter your OPENAI_API_KEY in the .env file
```

**3. Execution & Testing**
The master orchestrator allows for dual-mode testing depending on your debugging requirements:
```bash
python run.py
```

---

## 💡 Usage Guide

* **Terminal CLI:** Optimized for high-speed data extraction and automated cron-job workflows. 
* **Streamlit UI:** Provides a "Headed" toggle to watch the browser actions in real-time. Use the text area to define natural language instructions.

**Example Tasks:**
* *"Go to Amazon, search for 'RTX 5090', and give me the price of the first result that is in stock."*
* *"Navigate to the GitHub trending page and summarize the top 3 Python repositories today."*
* *"Search for the latest stock price of NVIDIA and tell me the daily change percentage."*

---

## 📚 Official Documentation & References

* [Browser-Use Github Repository](https://github.com/browser-use/browser-use)
* [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
* [Saturn Cloud Help Center](https://saturncloud.io/docs/)
