import os
import sys
import subprocess

def main():
    print("==================================================")
    print("🧩 Semantic Kernel Copilot Orchestrator")
    print("==================================================")
    print("\nSelect Mode:")
    print("1. Terminal CLI (Rapid Testing)")
    print("2. Streamlit Web UI (Production View)")
    
    choice = input("\n> ")

    if choice == '1':
        print("📟 Launching CLI...")
        subprocess.run([sys.executable, "copilot.py"])
    elif choice == '2':
        print("🖥️ Launching Web UI...")
        subprocess.run(["streamlit", "run", "app.py"])
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
