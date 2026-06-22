# 🎙️ Sayna Voice Agent Starter

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Server & Web Frontend | **Tech Stack:** Deepgram Agent API, WebSocket, Python, HTML5/JS

<p align="left">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Infrastructure-WebSocket-000000?style=for-the-badge&logo=socketdotio&logoColor=white" alt="WebSocket">
  <img src="https://img.shields.io/badge/Provider-Deepgram-111111?style=for-the-badge&logo=deepgram&logoColor=white" alt="Deepgram">
</p>

## 📖 Overview

The **Sayna Voice Agent** is a production-ready, ultra-low latency voice infrastructure template. 

It utilizes **Deepgram's End-to-End Voice Agent API**, which dramatically reduces latency by handling the Speech-to-Text (STT), Large Language Model (LLM) routing, and Text-to-Speech (TTS) entirely on their edge servers. 

### ✨ Key Capabilities
* **Managed LLM Orchestration:** Deepgram acts as a centralized orchestrator. By passing a JSON configuration to the WebSocket, Deepgram natively routes the transcript to third-party LLMs (like Google Gemini, OpenAI, or Anthropic) on their backend. You only need a single Deepgram API key to power the entire pipeline.
* **Cross-Browser Audio Streaming:** The `index.html` frontend features a custom Web Audio API downsampler, ensuring strict browsers (like Firefox) can capture 48kHz hardware microphones and stream them at the required 16kHz without throwing `DOMExceptions`.
* **Real-Time Visualizer:** Includes a live-rendering `<canvas>` audio visualizer so users know their microphone is actively capturing sound.

---

## 📁 Project Structure

```text
sayna_voice_agent/
├── .env.example             # Template for API keys
├── requirements.txt         # Python dependencies (websockets, python-dotenv)
├── server.py                # Python WebSocket proxy server
├── index.html               # Frontend UI with mic capture and audio playback
└── README.md                # Documentation

```

---

## 🏗️ Local Setup & Execution

**1. Install Dependencies**
Ensure you have Python installed, then create your virtual environment.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**2. Configure Environment**
Because Deepgram manages the LLM connection internally, you only need one API key for the entire application.

```bash
cp .env.example .env
# Edit .env and add: DEEPGRAM_API_KEY="your-key-here"

```

**3. Launch the Application**
This architecture requires two local servers running simultaneously: one for the WebSocket backend, and one to serve the secure HTML frontend.

*Open Terminal 1 (The Backend):*

```bash
python server.py
# Listens on ws://localhost:8000

```

*Open Terminal 2 (The Frontend):*

```bash
python -m http.server 3000
# Serves the UI on http://localhost:3000

```

**4. Talk to the Agent**
Open your web browser and navigate to `http://localhost:3000`. Click **Start Conversation**, allow microphone permissions, and speak!

---

## ☁️ Cloud Deployment

To deploy this low-latency voice infrastructure to a production environment, provision an instance on [Saturn Cloud](https://saturncloud.io/).

**Deployment Specifications:**

1. **Resource Type:** Python Server / Background Job.
2. **Environment Variables:** Inject `DEEPGRAM_API_KEY` securely into the Saturn Cloud secrets manager.
3. **Network Routing:** Ensure the deployment exposes port `8000` (for the WebSocket) and port `3000` (if serving the static HTML from the same instance). The load balancer must be configured to allow upgraded WebSocket (`ws://` or `wss://`) connections.
4. **Execution:** Run the deployment with standard Python execution: `python server.py`.

---

## 📚 Official Documentation & References

* **Deployment Infrastructure:** [Saturn Cloud Documentation](https://saturncloud.io/docs/)
* **Voice Engine:** [Deepgram Agent API Docs](https://developers.deepgram.com/docs/flux/agent)
* **Server Protocol:** [Python WebSockets](https://websockets.readthedocs.io/)