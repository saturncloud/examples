# 🗄️ MCP SQLite Agent

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/).*

**Hardware:** CPU/GPU | **Resource:** Python Server | **Tech Stack:** MCP, SQLite, Python

<p align="center">
  <img src="https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud" alt="Saturn Cloud">
  <img src="https://img.shields.io/badge/Protocol-MCP-6D28D9?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

## 📖 Overview

The **MCP SQLite Agent** is a production-grade Model Context Protocol server. It acts as a bridge between local SQLite databases and AI models, allowing agents to perform natural language data analysis via structured SQL execution and schema reflection.

### Infrastructure Deployment
* **Hybrid Interface:** Supports both **Stdio Transport** (for production AI connections) and **Web Inspector** (for developer testing).
* **Environment Isolation:** Uses a dedicated Python virtual environment to manage `aiosqlite` and the `mcp` SDK without system-level conflicts.
* **Auto-Provisioning:** The orchestrator automatically initializes a sample `users` table if no database is detected, ensuring immediate "plug-and-play" functionality.

---

## ✅ Prerequisites

1. **Python 3.10+**: Core runtime.
2. **Node.js & NPM**: Mandatory for the **MCP Inspector** UI.
3. **Claude Desktop**: (Optional) Recommended client for production testing.

---

## 🏗️ Setup & Deployment

**1. System & Python Setup**
```bash
sudo apt update && sudo apt install -y nodejs npm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Secret Configuration**
```bash
cp .env.example .env
# Ensure SQLITE_DB_PATH points to your desired .db file
```

**3. Launching the Orchestrator**
```bash
python run.py
```

---

## 💡 Usage Guide

### Mode 1: Testing with MCP Inspector (Web UI)
Use this mode to verify your tools are working before connecting to an AI.
1. Run `python run.py` and select **Option 2**.
2. In the browser, click the **Connect** button (ensure command is `python3` and args is `server.py`).
3. Navigate to the **Tools** tab.
4. Select `query_db` and enter `SELECT * FROM users;` to test data retrieval.

### Mode 2: Production (Claude Desktop)
To give Claude "eyes" on your local database:
1. Locate your Claude Desktop config (typically `~/Library/Application Support/Claude/claude_desktop_config.json`).
2. Add the following entry to the `mcpServers` object:
```json
"mcp-sqlite": {
  "command": "/path/to/your/venv/bin/python3",
  "args": ["/path/to/your/mcp_sqlite_server/server.py"],
  "env": { "SQLITE_DB_PATH": "/path/to/your/local_data.db" }
}
```
3. Restart Claude and look for the 🔨 icon.

**Example Prompts:**
* *"List the tables in my local database."*
* *"Who are the users registered as 'Engineer'?"*

---

## 📚 Official Documentation & References

* [MCP Documentation](https://modelcontextprotocol.io/)
* [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
* [aiosqlite Reference](https://aiosqlite.omnilib.dev/)
