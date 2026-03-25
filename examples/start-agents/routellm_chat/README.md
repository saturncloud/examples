# 🚦 RouteLLM Chat (Intelligent Model Routing)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** RouteLLM, Nebius AI, OpenAI, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-RouteLLM-FF4B4B?style=for-the-badge" alt="RouteLLM">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
</p>

## 📖 Overview

This template demonstrates how to implement intelligent model routing using **RouteLLM** to dramatically optimize enterprise inference costs. 

Instead of sending every user query to a massive, expensive model, this architecture uses a highly calibrated router to analyze the complexity of an incoming prompt. It routes trivial requests to the fast, low-cost **GPT-4o-mini**, while seamlessly routing complex reasoning tasks to the heavy-weight **Nebius Llama 3.3 70B**.

### 🧩 Key Features
1. **Matrix Factorization (MF) Router:** Utilizes the lightweight `mf` routing model trained on Chatbot Arena preference data.
2. **Cost-to-Quality Optimization:** Sets a specific routing threshold (`0.11593`) to optimally balance API costs against response intelligence.
3. **Multi-Provider Workaround:** Implements a LiteLLM workaround (`hosted_vllm`) to allow two distinct OpenAI-compatible base URLs to operate simultaneously within the same application.

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
Open the `.env` file and insert both of your active API keys.
```text
OPENAI_API_KEY="sk-your-openai-key"
NEBIUS_API_KEY="your-nebius-token-factory-key"
```

---

## 🚀 Execution & Testing

This repository includes both a CLI terminal script and a full interactive Web Dashboard.

### Phase 1: The Terminal CLI
Launch the lightweight routing interface in your terminal:
```bash
python routellm_chat.py
```

### Phase 2: The Streamlit Web Dashboard
Launch the interactive web UI to visually see the routing decisions:
```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow:**
Try giving the router a trivial task versus a highly complex reasoning task to see how it dynamically switches the target model in real time!

1. **The Simple Test (Should route to GPT-4o-mini):**
> *"What is the capital of France?"*

2. **The Complex Test (Should route to Llama 3.3 70B):**
> *"Write a Python script that implements a custom memory allocator in C using `mmap`, and explain the pointer arithmetic involved."*

---

## ☁️ Cloud Deployment

To deploy this intelligent routing gateway to production as a Web App on [Saturn Cloud](https://saturncloud.io/):

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance.
3. **Environment Variables:** Inject your `OPENAI_API_KEY` and `NEBIUS_API_KEY` directly into the Saturn Cloud secrets manager.
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Router Framework:** [RouteLLM GitHub](https://github.com/lm-sys/RouteLLM)
* **UI Framework:** [Streamlit Docs](https://docs.streamlit.io/)