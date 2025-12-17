# 📹 Multimodal Video RAG Dashboard

An advanced **Retrieval-Augmented Generation (RAG)** template designed to transform video content into a searchable, interactive Q&A knowledge base. Leveraging state-of-the-art Visual Language Models (VLM) like **LLaVA v1.6** and **CLIP**, this dashboard allows users to ask natural language questions and receive precise visual context with high-fidelity answers.

---

## 🚀 Overview

Traditional RAG systems are limited to text. This template breaks that barrier by enabling **Video & Visual RAG**. It extracts semantic meaning from frames using multimodal embeddings, stores them in a **FAISS** vector database, and uses a quantized VLM to "see" and interpret the video content for precise answering.

### Key Features

* **Video Processing**: Automatic frame extraction at configurable intervals.
* **Multimodal Embeddings**: Uses CLIP (`vit-base-patch32`) for high-speed cross-modal retrieval.
* **Vector Search**: Efficient similarity searching via FAISS.
* **VLM Synthesis**: Powered by LLaVA v1.6 (Mistral-7B) with 8-bit quantization for high performance on standard GPUs.
* **Streamlit Dashboard**: A clean, interactive web interface built for AI experimentation.

---

## 📂 Project Structure

```text
├── data/               # Directory for video assets
│   └── input_video.mp4 # Target video for the RAG pipeline
├── env/                # Local virtual environment (ignored by Git)
├── app.py              # Main Streamlit Dashboard logic
└── requirements.txt    # Python dependencies


```
---

## ⚙️ Setting Up on [Saturn Cloud](https://saturncloud.io/)

[Saturn Cloud](https://saturncloud.io/) provides the scalable GPU infrastructure needed to run visual models like LLaVA efficiently. Follow these steps to deploy this template:

### 1. Create a Project

Start a new [Saturn Cloud project](https://saturncloud.io/docs/getting-started/) with the following hardware recommendations:

* **GPU**: NVIDIA T4, L4, or A10G (minimum 16GB VRAM recommended for LLaVA 8-bit).
* **Disk Space**: At least 50GB (to accommodate model weights).


### 2. Initialize the Environment

Open a terminal in your Saturn Cloud resource and follow these steps to prepare your workspace:

**Create and Activate a Virtual Environment:**

```bash
# Create a virtual environment named 'env'
python3 -m venv env

# Activate the environment
source env/bin/activate

# Upgrade pip for the latest package support
pip install --upgrade pip

```

**Install Dependencies:**
Install the multimodal and dashboard libraries from the provided `requirements.txt`:

```bash
pip install -r requirements.txt

```

> **Note**: This process will install specialized libraries like `bitsandbytes` and `faiss-cpu`, which are critical for running quantized VLMs on Saturn Cloud's GPU infrastructure.

### 3. Prepare Your Video

Upload your video to the `data/` folder in the project root.

> **Note**: The file **must** be renamed to `input_video.mp4` for the pipeline to detect it.

### 4. Launch the Dashboard

Run the following command to start the interactive app:

```bash
python -m streamlit run app.py

```
---

## 🖥️ Accessing the Dashboard

Saturn Cloud users can view their application by clicking the **"Dashboard"** link in the project resource page. If you are accessing via SSH or a remote terminal, use:

```bash
python -m streamlit run app.py --server.address 0.0.0.0

```

Then, ensure you have set up SSH tunneling to map port `8501` to your local machine:

```bash
ssh -L 8501:localhost:8501 <user>@<saturn-cloud-ip>

```
---

## 🛠️ How it Works

1. **Stage 1 (Frame Extraction)**: The system reads `input_video.mp4` and captures frames every 5 seconds.
2. **Stage 2 (Indexing)**: CLIP generates semantic vectors for every frame. These are indexed in a FAISS `IndexFlatL2` for sub-millisecond retrieval.
3. **Stage 3 (RAG Q&A)**: When you ask a question, the system finds the most similar frame and passes it—along with your prompt—to the LLaVA model for a human-like response.

---

## 📚 Reference & Community

* **Saturn Cloud Documentation**: [Getting Started with Python Dashboards](https://saturncloud.io/docs/user-guide/examples/python/production/qs-py-dashboard-streamlit/)
* **Streamlit**: [Building Interactive AI Apps](https://docs.streamlit.io/)
* **Hugging Face**: [LLaVA v1.6 Model Card](https://huggingface.co/llava-hf/llava-v1.6-mistral-7b-hf)

For more AI and Machine Learning templates, visit the [Saturn Cloud Examples Gallery](https://saturncloud.io/docs/user-guide/examples/).

---



