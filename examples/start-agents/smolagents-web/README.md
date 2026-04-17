# 🤗 Hugging Face smolagents

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Script & Web App | **Tech Stack:** smolagents, Hugging Face, Streamlit

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Framework-smolagents-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="smolagents">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

This template provides a minimalist, production-ready implementation of Hugging Face's lightweight **smolagents** framework. 

Unlike traditional LLM agents that rely on rigid JSON tool-calling and often hallucinate logic, `smolagents` utilizes **Code Agents**. When faced with a problem, the agent dynamically writes Python code, executes it in a secure local sandbox, and uses the exact output to formulate its final, factual response.

### 🧩 Key Features
1. **CodeAgent Engine:** Powered by `Qwen2.5-Coder-32B-Instruct` via Hugging Face's Serverless Inference API for state-of-the-art Python generation.
2. **Web Surfing Engine:** Equipped with `DuckDuckGoSearchTool` (`ddgs`) to pull real-time data and news from the internet.
3. **Native Python Execution:** Authorized to import standard libraries (`math`, `datetime`) to solve complex geometric, mathematical, and temporal problems on the fly.
4. **Transparent UI Processing:** The Streamlit dashboard intercepts the agent's hidden terminal outputs, allowing you to read the exact Python scripts it writes in the background!

---

## 🏗️ Local Setup & Installation

**1. Create the Environment & Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
*(Note for Kali Linux / strict Debian users: If you hit a PEP 668 environment error, use `python3 -m pip install -r requirements.txt` to install safely into the venv).*

---

## 🔐 Environment Configuration

**1. Create your `.env` file:**
```bash
cp .env.example .env
```

**2. Add your Provider Keys:**
Open the `.env` file and insert your active Hugging Face token. *(You can generate a free "Fine-grained" token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens). Ensure it has **Serverless Inference API** permissions).*
```text
HF_TOKEN="hf_your_token_here"
```

---

## 🚀 Execution & Testing

This repository includes both a terminal script and a highly interactive Web Dashboard.

### Phase 1: The Terminal CLI
Watch the agent output its coding process directly in your terminal:
```bash
python smolagents_cli.py
```

### Phase 2: The Streamlit Web Dashboard
Launch the visual interface to see the intercepted Python sandbox logs directly in your browser:
```bash
streamlit run app.py
```

**🧪 Recommended Testing Flow:**
To see the true power of a Code Agent, test its ability to dynamically write Python scripts for different scenarios:

**1. The Pure Logic & Math Test:**
> *"Using the math library, calculate the volume of a sphere with a radius of 42.7 inches. Show me the exact Python code you used to figure it out."*

**2. The Live Web & Parsing Test:**
> *"Search the web and tell me the current stock price of NVIDIA (NVDA) right now. Also, summarize the top two most recent news headlines about the company."*

**3. The Multi-Step Hybrid Test (The Ultimate Stress Test):**
> *"Search the web for the current population of Tokyo, Japan. Once you find it, assume the average human weighs 62 kg. Calculate the total combined weight of Tokyo's entire population in pounds (1 kg = 2.204 lbs)."*

*(In the Streamlit UI, click the expandable **"Agent is writing Python code..."** box to literally read the code it wrote to solve these prompts!)*

---

## ☁️ Cloud Deployment

To deploy this minimalist agent to production on [Saturn Cloud](https://saturncloud.io/):

**Deployment Specifications:**

1. **Resource Type:** Streamlit Deployment / Python Server.
2. **Hardware:** CPU instance.
3. **Environment Variables:** Inject your `HF_TOKEN` directly into the Saturn Cloud secrets manager.
4. **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Agent Framework:** [smolagents GitHub](https://github.com/huggingface/smolagents)

