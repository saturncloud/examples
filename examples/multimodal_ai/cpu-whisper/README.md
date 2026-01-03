# 🎙️ Whisper Speech-to-Text: Saturn Cloud Template

This template provides a production-ready environment for deploying **OpenAI Whisper** for high-accuracy speech-to-text tasks. It is optimized for **Saturn Cloud** GPU/CPU resources, allowing for seamless scaling from single-file transcription to large-scale batch processing.

## 📋 Overview

* **Title**: cpu-whisperSpeech-to-Text
* **Tech Stack**: Whisper AI, PyTorch, FFmpeg, Librosa, Matplotlib
* **Resource Type**: Saturn Cloud Deployment / Jupyter Server
* **Description**: Whisper, Torch Transcribe sample audio, Waveform + transcript, Back logs.

---

## 🚀 Environment Setup

The environment configuration is automated via a dedicated setup script designed for the Saturn Cloud file system.

### 1. Initialize the Environment

Run the custom setup script to install system dependencies (FFmpeg), configure your Python environment, and install the Whisper library.

```bash
# Execute your pre-configured setup script
bash setup_saturn.sh

```

### 2. Activate the Environment

Once the script completes, ensure you are working within the correct virtual environment:

```bash
source whisper_env/bin/activate

```

---

## 🧪 Testing & Verification

Your environment contains two primary test scripts to verify the full functionality of the pipeline.

### 1. Running `test.py` (Audio Acquisition)

This script verifies the network connectivity and hardware detection. It automatically downloads a high-quality sample audio file from Hugging Face and transcribe it (output on terminal).

**Command:**

```bash
python test.py

```

**Terminal Output (Back Logs):**

* **Device Detection**: Shows `Testing on Device: CUDA` (or CPU).
* **Download Log**: Displays `Downloading sample audio...` followed by `Download complete.`.
* **Model Loading**: Shows a progress bar for the Whisper `base` model (139MB).
* **Transcription**: Prints a raw text block of the transcribed audio to the terminal.

### 2. Running `test2.py` (Visualization & Export)

This script tests the advanced features of the template, including waveform generation and local file processing.

**Command:**

```bash
python test2.py

```

**Terminal Output (Back Logs):**

* **Status**: `Loading model and transcribing...`.
* **Visualization Log**: `Generating waveform...` using Librosa and Matplotlib.
* **Success Message**: `Verification Complete: Check transcript.txt and waveform.png`.

---

## 📂 Expected Output Files

After running the tests, verify the presence of these files in your **Explorer**:

* **`sample1.flac`**: The downloaded test audio.
* **`transcript.txt`**: The saved text version of the transcription.
* **`waveform.png`**: The visual representation of the audio waves.

---

## 📊 Model Selection Guide

Choose the model size that best fits your hardware constraints on Saturn Cloud.

| Model | Parameters | Required VRAM | Relative Speed |
| --- | --- | --- | --- |
| **Tiny** | 39 M | ~1 GB | ~10x |
| **Base** | 74 M | ~1 GB | ~7x |
| **Small** | 244 M | ~2 GB | ~4x |
| **Medium** | 769 M | ~5 GB | ~2x |
| **Large** | 1550 M | ~10 GB | 1x |

---

## 🔗 Reference Links

* **Platform**: [Saturn Cloud Dashboard](https://saturncloud.io/)
* **Support**: [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Community**: [Whisper AI Discussions](https://github.com/openai/whisper/discussions)
