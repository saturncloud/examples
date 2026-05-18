# 🤖 NVIDIA NeMo Agent Toolkit — Research Assistant

### **Overview**

This template deploys an AI research agent powered by the [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit). Given any question or topic, the agent searches Wikipedia, reasons step-by-step using a **ReAct loop** (Reason + Act), and returns a structured answer — all backed by **NVIDIA NIM cloud inference**. No GPU required.

* **Hardware:** CPU Large (2 cores, 16 GB RAM)
* **Runtime:** NVIDIA NIM cloud API — bring your own `nvapi-...` key
* **Use Case:** Research automation, knowledge summarization, agentic reasoning demos

---

### **Tech Stack**

* **NVIDIA NeMo Agent Toolkit (`nvidia-nat`):** Orchestrates the ReAct agent loop, tool dispatch, and LLM calls.
* **NVIDIA NIM (`nvidia/nemotron-3-nano-30b-a3b`):** Cloud-hosted inference — no local GPU needed.
* **Wikipedia Search (`wiki_search`):** Built-in tool; no extra API key required.
* **LangChain:** Provides the tool and chain integration layer used by `nvidia-nat`.

---

## 🪐 Using on Saturn Cloud

### 1. Get an NVIDIA API key

Get a free key at [build.nvidia.com](https://build.nvidia.com) → sign up → **API Keys** → **Generate Key**. Your key will start with `nvapi-`.

### 2. Create the workspace from the template

In Saturn Cloud, go to **New Resource → Workspace → Templates** and select **NeMo Agent Toolkit — Research Assistant**. Before clicking Start, open **Settings → Environment Variables**, find `NVIDIA_API_KEY`, and paste your key in.

### 3. Start the workspace

Click **Start**. Saturn Cloud will clone the repo and run `start.sh` automatically — this installs all dependencies and runs a demo query. The process takes about 3–4 minutes. You can watch it complete by opening **Logs** from the workspace panel.

### 4. Open JupyterLab

Once the workspace status shows **Running**, click the **JupyterLab** button to open the IDE. Open a terminal from **File → New → Terminal**.

### 5. Run a query from the terminal

```bash
cd /home/jovyan/examples/examples/nemo-agent-toolkit
source .venv/bin/activate
nat run --config_file workflow.yml --input "your question here"
```

You will see the agent's full reasoning — each Wikipedia search and every reasoning step — printed live in the terminal.

### 6. Launch the Gradio chat UI

```bash
source .venv/bin/activate
python app.py
```

Then go to **Settings → Routes** on the workspace and open the URL listed next to port **8000**. This opens the chat interface in your browser where you can have a full conversation with the agent.

To stop the UI:

```bash
pkill -f "app.py"
```

---

## 🛠️ Local Setup

### 1. Set your NVIDIA API key

```bash
cp .env.example .env
# Edit .env and set NVIDIA_API_KEY=nvapi-...
```

Get a free key at [build.nvidia.com](https://build.nvidia.com) → API Keys.

### 2. Run the demo

```bash
chmod +x start.sh test.sh
./start.sh
```

`start.sh` creates a `.venv`, installs `nvidia-nat` and its integrations, then runs a pre-set research query so you can see the agent working immediately.

### 3. Verify your setup (optional)

```bash
./test.sh
```

Checks Python version, `nat` CLI availability, `workflow.yml`, API key format, and live NVIDIA API connectivity.

---

## 🏃 Run a custom query

```bash
source .venv/bin/activate
nat run --config_file workflow.yml --input "your question here"
```

Examples:

```bash
nat run --config_file workflow.yml --input "What is NVIDIA Hopper architecture and how does it differ from Ampere?"
nat run --config_file workflow.yml --input "Explain how transformer models work and list three key papers"
nat run --config_file workflow.yml --input "Research the history of autonomous vehicles and list 5 major milestones"
```

---

## 💬 Launch the chat UI

```bash
source .venv/bin/activate
python app.py
```

Opens a Gradio chat interface on port 8000. Type questions and the agent will search Wikipedia and reason step-by-step in the background.

**On Saturn Cloud** — the port 8000 route is pre-configured on the workspace. Once `app.py` is running, open the port 8000 URL from your workspace settings.

To stop:

```bash
pkill -f "app.py"
```

---

## ⚙️ Customise the workflow

All configuration lives in `workflow.yml` — no Python required.

**Change the model:**

```yaml
llms:
  nim_llm:
    model_name: nvidia/llama-3.1-nemotron-70b-instruct   # higher quality
    # model_name: nvidia/llama-3.1-nemotron-nano-8b-v1    # faster / cheaper
    # model_name: meta/llama-3.1-8b-instruct              # widely available
```

**Get more search results:**

```yaml
functions:
  wikipedia_search:
    max_results: 5   # default is 3
```

**Reduce verbosity:**

```yaml
workflow:
  verbose: false
```

Browse all available NIM models at [build.nvidia.com](https://build.nvidia.com).

---

## 🔧 Troubleshooting

**`NVIDIA_API_KEY is not set`**

```bash
cp .env.example .env   # then paste your key
```

**`nat: command not found`**

```bash
source .venv/bin/activate   # activate the venv first
```

**`HTTP 401` from NVIDIA API** — key is invalid or expired; generate a new one at [build.nvidia.com](https://build.nvidia.com).

**Agent loops without answering** — increase retries or switch to a more capable model:

```yaml
workflow:
  parse_agent_response_max_retries: 5
```

**Model not available** — try `meta/llama-3.1-8b-instruct`, which is broadly available on free-tier keys.

---

## 🔗 Resources

* **NeMo Agent Toolkit docs:** [docs.nvidia.com/nemo/agent-toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)
* **NVIDIA NIM models:** [build.nvidia.com](https://build.nvidia.com)
* **Saturn Cloud:** [saturncloud.io](https://saturncloud.io/)
