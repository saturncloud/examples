# 🧠 LangGraph Agent Sandbox

This sample notebook demonstrates how to build a **local multi-agent coding assistant** using **LangGraph**, **Transformers**, and **LangChain Sandbox** — fully compatible with [Saturn Cloud](https://saturncloud.io/).

The system allows you to:
- Generate clean Python code from natural-language prompts.
- Check the code for syntax and structure validity.
- Execute the generated code safely in an isolated sandbox.
- Interactively explore different code generation tasks — all locally, with **no API keys required**.

---

## ⚙️ What You’ll Learn
- How to design an **agentic workflow** using LangGraph.
- How to use **local transformer models (Phi-3 Mini)** for reasoning.
- How to integrate a **safe execution sandbox** (with local fallback).
- How to run multi-stage LLM pipelines entirely within Saturn Cloud.

---

## 🧩 Notebook Structure

| Stage | Description |
|--------|--------------|
| **1. Install Dependencies** | Installs LangGraph, LangChain, and related libraries. |
| **2. Load Model & Sandbox** | Loads the local Hugging Face model and initializes a secure sandbox (with fallback). |
| **3. Define Workflow Agents** | Builds LangGraph nodes for Code Generation, Syntax Checking, and Execution. |
| **4. Batch Testing** | Runs several example coding tasks through the full pipeline. |
| **5. Interactive Mode** | Launches an interactive terminal to test your own code prompts. |

---

## 🚀 How to Run on Saturn Cloud

1. **Open this template** in your Saturn Cloud environment.  
2. Run all cells sequentially from top to bottom.  
3. The local model (`Phi-3-mini`) will load automatically.  
4. Explore the pre-loaded test prompts or use the **interactive assistant** in Stage 5.  
5. All runs execute securely inside your Saturn Cloud instance — no external API calls.

---

## ☁️ About Saturn Cloud

[Saturn Cloud](https://saturncloud.io/) provides powerful GPU-accelerated Jupyter environments that make it easy to run, scale, and share AI and data-science projects.  
This template is part of Saturn Cloud’s **open-source educational catalog**, showcasing safe, local AI workflows.

---

### 🧠 Built With

- 🤗 **Transformers**
- 🧮 **LangGraph**
- ⚡ **LangChain Sandbox**
- ☁️ **Saturn Cloud**

