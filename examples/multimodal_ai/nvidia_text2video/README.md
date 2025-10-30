# 🎬 Gradio Text→Video Demo

Generate 5-second AI-generated video clips from text prompts using state-of-the-art diffusion models — all inside a GPU-powered Jupyter Notebook.

![Video Demo](https://cdn-icons-png.flaticon.com/512/3447/3447651.png)

---

## 🧠 Model Used

- [`cerspense/zeroscope_v2_576w`](https://huggingface.co/cerspense/zeroscope_v2_576w)  
  A powerful text-to-video diffusion model capable of producing smooth and realistic short clips at **576×320 resolution**.

---

## ⚙️ Tech Stack

- **Diffusers** – For loading and running the diffusion pipeline
- **Gradio** – To build an interactive UI for prompt-based video generation
- **PyTorch** – For GPU acceleration
- **Saturn Cloud** – To run everything in a high-performance GPU notebook environment

---

## 🚀 Features

- Text prompt → 5-second video (~16 frames @ 3 fps)
- Clean and responsive Gradio interface
- Adjustable settings for inference steps, guidance scale, and frame count
- Inline preview inside Jupyter Notebook (with fallback display using `IPython.display.Video`)
- Works seamlessly on GPU inside [Saturn Cloud](https://saturncloud.io/)

---

## 🧪 Example Prompts

- `"Waves crashing on a beach at sunset"`
- `"A coffee cup steaming on a table, camera zoom in"`
- `"Fireworks exploding in the night sky"`
- `"A cat playing with a ball of yarn"`

---

## 💻 How to Run

1. Launch the notebook in [Saturn Cloud](https://saturncloud.io/).
2. Make sure your environment includes a **GPU** and **`diffusers`, `gradio`, `transformers`, `torch`, and `imageio`**.
3. Run all cells in sequence.
4. Type your prompt, hit **Generate**, and preview your video instantly!

---

## 📎 Useful Links

- [Saturn Cloud Templates](https://saturncloud.io/resources/templates/)
- [Diffusers Library (Hugging Face)](https://huggingface.co/docs/diffusers/index)
- [Zeroscope Model Card](https://huggingface.co/cerspense/zeroscope_v2_576w)
- [Gradio Documentation](https://www.gradio.app/)

---

## 📢 Note

This demo generates short, low-frame-rate videos. For longer or higher-quality clips, you may explore batch rendering or multi-GPU scaling in Saturn Cloud.

---

## 🛰️ Powered By

[![Saturn Cloud](https://saturncloud.io/images/logo/logo-light-mode.svg)](https://saturncloud.io/)

A fully managed data science platform with GPU notebooks, scalable compute, and collaborative workflows.

---
