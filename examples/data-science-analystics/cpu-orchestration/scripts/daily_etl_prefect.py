from prefect import flow, task
import random
import os
import time
from datetime import datetime

# Define absolute paths so it works from anywhere
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "data", "pipeline_logs.csv")

@task(name="Extract & Transform", retries=2)
def run_etl():
    print("🚀 [Prefect] Starting Extraction...")
    time.sleep(1) # Simulate CPU work
    
    # 90% Success Rate Simulation
    duration = random.randint(45, 120)
    status = "Success" if random.random() > 0.1 else "Failure"
    return duration, status

@task(name="Log Results")
def log_data(etl_data):
    duration, status = etl_data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create CSV header if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("Date,Duration_Seconds,Status,Orchestrator\n")
            
    # Append the run data
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp},{duration},{status},Prefect\n")
    
    print(f"✅ [Prefect] Logged: {status} in {duration}s")

@flow(name="Daily ETL + Model Run")
def main_flow():
    data = run_etl()
    log_data(data)

if __name__ == "__main__":
    main_flow()