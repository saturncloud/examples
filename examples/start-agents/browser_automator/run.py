import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("==================================================")
    print("🌐 Browser-Use Automator Launcher")
    print("==================================================")

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env")
        sys.exit(1)

    print("\nSelect Testing Mode:")
    print("1. Streamlit Web UI (Visual Debugging)")
    print("2. Terminal CLI (Headless Extraction)")
    
    choice = input("\n> ")

    try:
        if choice == '1':
            print("\n🖥️ Launching Streamlit...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        elif choice == '2':
            print("\n📟 Launching CLI...")
            subprocess.run([sys.executable, "automator_cli.py"])
        else:
            print("Invalid choice. Exiting.")
    except KeyboardInterrupt:
        print("\n👋 Shutdown complete.")

if __name__ == "__main__":
    main()
