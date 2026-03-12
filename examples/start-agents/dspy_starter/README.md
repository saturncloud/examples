# 🧠 DSPy Starter: AI System Optimizer & UI

**Hardware:** CPU/GPU | **Resource:** Jupyter Notebook & Web App | **Tech Stack:** DSPy, Streamlit, Python, OpenAI

<p align="left">
  <img src="https://img.shields.io/badge/Resource-Jupyter_Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter Notebook">
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Framework-DSPy-31A8FF?style=for-the-badge" alt="DSPy">
</p>

## 📖 Overview

This template provides a robust introduction to **DSPy** (Declarative Self-Improving Language Programs), a framework that replaces manual "prompt engineering" with algorithmic optimization.

It features a **Dual-Entrypoint Architecture**:
1. **Interactive Jupyter Notebook (`dspy_starter.ipynb`):** For defining your signatures, providing training datasets, and compiling/optimizing your agent using the `BootstrapFewShot` optimizer.
2. **Streamlit Testing Dashboard (`app.py`):** A production-grade web interface to interactively test your agent, explicitly visualizing the AI's hidden "Chain of Thought" reasoning alongside its final output.



---

## 🏗️ Setup & Installation

**1. Create Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment Variables**
Create an environment file to securely store your OpenAI credentials.

```bash
cp .env.example .env
nano .env
# Input your OpenAI API key. Save and exit.

```

---

## 💻 Method 1: Interactive Dashboard (Testing)

Use the Streamlit UI to quickly test the capacity of your DSPy module. This dashboard explicitly separates the internal reasoning monologue from the formatted output.

```bash
streamlit run app.py

```

*The dashboard will automatically open in your browser (usually at `http://localhost:8501`).*

---

## 🔬 Method 2: Jupyter Notebook (Compilation & Optimization)

Use the notebook to learn how DSPy compiles algorithms and optimizes prompts under the hood.

```bash
jupyter notebook

```

*Open `dspy_starter.ipynb` and execute the cells sequentially to watch DSPy mathematically rewrite your prompts to maximize accuracy.*

---

## 📚 Official Documentation & References

* **DSPy Repository:** [Stanford NLP DSPy GitHub](https://github.com/stanfordnlp/dspy)
* **DSPy Documentation:** [DSPy Official Docs](https://dspy-docs.vercel.app/)
* **UI Framework:** [Streamlit Documentation](https://docs.streamlit.io/)

```

### How to test your new UI:
1. Run `pip install -r requirements.txt` to grab Streamlit.
2. Save the `app.py` file in your project folder.
3. In your terminal, run `streamlit run app.py`.

Type in a your question and watch how the UI beautifully isolates the reasoning trace from the final answer! Would you like me to help you build the architecture for the next agent template on your list now?

```