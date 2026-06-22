# 📈 Agno UI (Finance & Web Agent Dashboard)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Web Application | **Tech Stack:** Agno (v2.5+), Streamlit, Yahoo Finance, DuckDuckGo

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-Agno-F2E222?style=for-the-badge&logoColor=black" alt="Agno">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Data-Yahoo_Finance-7303c0?style=for-the-badge" alt="YFinance">
</p>

## 📖 Overview

This template provides a production-grade interactive Web UI for financial and research agents. It utilizes **Agno** to seamlessly bind Large Language Models to external tool APIs, and wraps the logic in a dynamic **Streamlit** dashboard.

### 🧩 The Agent Dashboard
The application features a sidebar that allows users to seamlessly switch between different specialized AI modes:
1. **🌐 Web Researcher:** Queries DuckDuckGo for live internet news and context.
2. **📈 Finance Analyst:** Queries the Yahoo Finance API for live ticker prices, company fundamentals, and analyst ratings.
3. **👔 Finance Swarm:** A multi-agent `Team` that coordinates the web and finance agents to synthesize comprehensive investment reports.

---

## 🏗️ Local Setup & Installation

This web application runs entirely within a standard Python virtual environment, requiring no heavy containerization for local development.

**1. Create the Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Agno securely loads your API keys via the `python-dotenv` library.

**1. Create your `.env` file:**
```bash
cp .env.example .env
```

**2. Add your Provider Keys:**
Open the `.env` file and insert your active API key.
```text
OPENAI_API_KEY="sk-your-actual-api-key-goes-here"
```

---

## 🚀 Execution & Testing

Launch the interactive Streamlit UI directly from your terminal:

```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow:**
Once the UI opens in your browser (default `http://localhost:8501`), use the sidebar to switch between agents and paste these exact prompts to verify their tool connectivity:

**1. Test the Web Researcher**
> *"What are the top 3 biggest AI or tech news stories from this week? Please summarize each one briefly and cite the source."*
*(Verifies the DuckDuckGo standard web search API is connected and formatting properly).*

**2. Test the Finance Analyst**
> *"Pull the current stock price, market cap, and the latest analyst consensus recommendation for Tesla (TSLA)."*
*(Verifies the Yahoo Finance API is successfully pulling live market data and analyst ratings).*

**3. Test the Finance Swarm (The Ultimate Test)**
> *"Write a comprehensive investment report on NVIDIA (NVDA). I need you to pull the latest stock data and analyst recommendations, then search the web for recent news about their upcoming AI chips. Synthesize everything into a final verdict."*
*(Verifies multi-agent orchestration. Watch as the Swarm Leader delegates tasks to the Analyst and Researcher before writing the final report).*

---

## ☁️ Cloud Deployment

To deploy this multi-agent web application to production, you can provision a resource on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance (financial APIs and web searches are extremely lightweight).
3. **Environment Variables:** Inject your `OPENAI_API_KEY` directly into the Saturn Cloud secrets manager (do not commit your `.env` file to version control).
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Agent Framework:** [Agno Official Docs](https://docs.agno.com/)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)
