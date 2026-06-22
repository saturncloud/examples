# 🏭 MetaGPT Software Factory

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** 4+ vCPU / 8GB+ RAM | **Resource:** Python Server | **Tech Stack:** MetaGPT, Docker, Python


<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-00A2FF?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-MetaGPT-6D28D9?style=for-the-badge" alt="MetaGPT">
  <img src="https://img.shields.io/badge/Container-Docker-003B57?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

The **MetaGPT Software Factory** is a production-grade multi-agent framework that simulates an entire software company. By assigning specialized roles—Product Manager, Architect, and Engineer—the system transforms a single natural language requirement into a comprehensive repository including PRDs, system designs, and executable code.

### Infrastructure Deployment
* **Environment Isolation:** Containerized via **Docker** using a Python 3.11-slim base and 2026 dependency anchors to prevent conflicts and ensure a "clean room" execution environment.
* **Persistent Workspace:** Uses Docker volume mounting to map internal agent outputs to the local `./workspace` directory, ensuring all generated assets remain persistent.
* **Headless Research:** Integrated with **Playwright** to allow the Product Manager agent to perform real-time market research via an automated Chromium browser.

---

## ✅ Prerequisites

1. **OpenAI API Key**: Required for the agentic reasoning engine (`gpt-4o`). [Get Key](https://platform.openai.com/)
2. **Docker & Docker Compose**: Mandatory for environment orchestration and isolation.
3. **Kali Linux Users**: Run `export DOCKER_HOST=unix:///var/run/docker.sock` to ensure Docker takes priority over Podman.
4. **Hardware Context**: Minimum 8GB RAM recommended for parallel agent processing.

---

## 🏗️ Setup & Deployment

**1. Secret Configuration**
```bash
cat << 'EOF' > config2.yaml
llm:
  api_type: "openai"
  api_key: "sk-YOUR_KEY_HERE"
  model: "gpt-4o"
  base_url: "https://api.openai.com/v1"
EOF
```

**2. Launching the Factory**
```bash
docker-compose up --build
```

---

## 💡 Usage Guide

### Mode 1: Streamlit Dashboard (Visual SOP)
1. Run `docker-compose up` and navigate to `http://localhost:8501`.
2. Input your software project idea.
3. Click **"Start Production"** to trigger the waterfall process.

### Mode 2: CLI Power-User
```bash
docker-compose run factory python run.py "Create a secure Flask API with JWT authentication"
```

## 📚 Official Documentation & References

* [MetaGPT Official Documentation](https://docs.deepwisdom.ai/main/en/)
* [Docker Compose Specification](https://docs.docker.com/compose/)
* [Playwright Python SDK](https://playwright.dev/python/docs/intro)
