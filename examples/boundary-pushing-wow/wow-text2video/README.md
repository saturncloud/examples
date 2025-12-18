# 🎬 Text→Video Diffusion Dashboard

A high-performance **Generative AI** template designed to transform textual descriptions into cinematic short videos. Utilizing the **ModelScope (DAMO-VILAB)** 1.7-billion parameter diffusion model, this dashboard provides a user-friendly interface for generating high-quality visual content directly on GPU infrastructure.

---

## 🚀 Overview

This template provides a streamlined pipeline for **Latent Video Diffusion**. It utilizes a **UNet3D structure** to iteratively denoise pure Gaussian noise into coherent video sequences based on your English text prompts. Optimized for memory-efficient inference, it features 8-bit quantization and VAE slicing to run effectively on standard cloud GPUs.

### Key Features

* **Prompt-to-Video**: Generate realistic or stylized motion sequences from simple text descriptions.
* **Optimized Inference**: Powered by the `diffusers` library with **DPMSolverMultistepScheduler** for faster, high-quality denoising.
* **VRAM Efficiency**: Integrated **VAE slicing** and **CPU offloading** to prevent Out-of-Memory (OOM) errors during high-resolution generation.
* **Interactive Dashboard**: A polished **Streamlit** interface featuring adjustable inference steps and frame counts for creative control.

---

## 📂 Project Structure

```text
├── app.py              # Main Streamlit Dashboard & Diffusion logic
├── requirements.txt    # Python dependencies (Diffusers, Torch, etc.)
└── env/                # Local virtual environment (User created)

```

---

## ⚙️ Setting Up on [Saturn Cloud](https://saturncloud.io/)

[Saturn Cloud](https://saturncloud.io/) offers the high-performance NVIDIA GPUs (like T4, L4, or A10G) required to run large diffusion models. Follow these steps to deploy:

### 1. Create a Project

Start a new [Saturn Cloud project](https://saturncloud.io/docs/getting-started/) and select a resource with at least **16GB of VRAM** and **40GB of disk space** to store the model weights.

### 2. Initialize the Environment

Open a terminal in your Saturn Cloud resource and follow these steps to prepare your workspace:

**Create and Activate a Virtual Environment:**

```bash
# Create a virtual environment named 'env'
python3 -m venv env

# Activate the environment
source env/bin/activate

# Upgrade pip
pip install --upgrade pip

```

**Install Dependencies:**
Install the core diffusion and dashboard libraries from the provided `requirements.txt`:

```bash
pip install -r requirements.txt

```

> **Note**: This includes `diffusers`, `accelerate`, and `bitsandbytes` for quantized model loading.

### 3. Launch the Dashboard

Run the following command to start the interactive generator:

```bash
python -m streamlit run app.py

```

---

## 🖥️ Accessing the Dashboard

Saturn Cloud users can view their application via the **"Dashboard"** link on the project resource page. For remote access or SSH users:

```bash
# Launch with broad address binding
python -m streamlit run app.py --server.address 0.0.0.0

```

Then, establish an SSH tunnel on your **local host machine**:

```bash
ssh -L 8501:localhost:8501 root@<YOUR_SATURN_IP> -p <PORT>

```

Visit `http://localhost:8501` in your browser to begin prompting.

---

## 🛠️ How it Works

1. **Stage 1 (Encoding)**: The user prompt is converted into a latent representation using a text encoder.
2. **Stage 2 (Denoising)**: The **UNet3D model** performs iterative denoising over 20-50 steps to create a sequence of latent frames.
3. **Stage 3 (Decoding)**: The VAE decoder transforms these latents back into a standard RGB video format.
4. **Stage 4 (Post-Processing)**: Frames are converted to NumPy arrays and exported as an MP4 file for playback.

---

## 📚 Reference & Community

* **Saturn Cloud Documentation**: [Resources and Dashboards](https://saturncloud.io/docs/design-principles/concepts/resources/)
* **Hugging Face**: [Text-to-Video-MS-1.7B Model Card](https://huggingface.co/ali-vilab/text-to-video-ms-1.7b)
* **Diffusers Library**: [Video Generation Guide](https://huggingface.co/docs/diffusers/api/pipelines/text_to_video)

For more deep learning templates, visit the [Saturn Cloud Examples Gallery](https://saturncloud.io/docs/user-guide/examples/).

---