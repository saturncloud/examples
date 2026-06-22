import subprocess
import sys
import os

def main():
    print("==================================================")
    print("🚀 Letta (MemGPT) Frontend Launcher")
    print("==================================================")

    # Check if running in a Cloud environment
    is_cloud = os.getenv("CLOUD_ENV", "false").lower() == "true"

    try:
        if is_cloud:
            print("\n☁️ Cloud environment detected. Auto-launching Streamlit...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"])
        else:
            print("\nWhich interface would you like to run?")
            print("1. Streamlit Web Dashboard (UI Testing)")
            print("2. Terminal CLI (Headless Testing)")
            
            choice = input("\n> ")

            if choice == '1':
                print("\n🌐 Launching Streamlit Dashboard...")
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
            elif choice == '2':
                print("\n🖥️ Launching Terminal CLI...")
                subprocess.run([sys.executable, "letta_cli.py"])
            else:
                print("Invalid choice. Shutting down.")
            
    except KeyboardInterrupt:
        print("\n✅ Exiting frontend launcher...")

if __name__ == "__main__":
    main()
