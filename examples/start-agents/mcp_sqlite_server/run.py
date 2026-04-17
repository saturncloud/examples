import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("==================================================")
    print("🗄️ MCP SQLite Server Orchestrator")
    print("==================================================")

    db_path = os.getenv("SQLITE_DB_PATH")
    if not os.path.exists(db_path):
        print(f"⚠️ Warning: Database '{db_path}' not found. Creating a sample DB...")
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
        conn.execute("INSERT INTO users (name, role) VALUES ('Admin', 'Superuser'), ('Dev', 'Engineer')")
        conn.commit()
        conn.close()

    print("\nSelect Mode:")
    print("1. Run MCP Server (Standard Stdio)")
    print("2. Run MCP Inspector (Web UI for Testing Tools)")
    
    choice = input("\n> ")

    try:
        if choice == '1':
            print("🚀 Server starting... (Connect your MCP client to this process)")
            subprocess.run([sys.executable, "server.py"])
        elif choice == '2':
            print("🔍 Launching MCP Inspector...")
            # This requires the mcp[cli] extra
            subprocess.run(["npx", "@modelcontextprotocol/inspector", "python3", "server.py"])
        else:
            print("Invalid choice.")
    except KeyboardInterrupt:
        print("\n👋 Shutdown complete.")

if __name__ == "__main__":
    main()
