from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import os
import time

# Handle paths relative to AIRFLOW_HOME
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", os.getcwd())
# Go up one level from airflow_home to find the 'data' folder
BASE_DIR = os.path.dirname(AIRFLOW_HOME)
LOG_FILE = os.path.join(BASE_DIR, "data", "pipeline_logs.csv")

def airflow_etl():
    print("🚀 [Airflow] Starting Extraction...")
    time.sleep(1)
    return random.randint(50, 130), "Success" if random.random() > 0.1 else "Failure"

def airflow_log(ti):
    # Get data from previous task
    duration, status = ti.xcom_pull(task_ids='run_etl_task')
    
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("Date,Duration_Seconds,Status,Orchestrator\n")
            
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()},{duration},{status},Airflow\n")
    print(f"✅ [Airflow] Logged: {status}")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'daily_etl_airflow',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='run_etl_task',
        python_callable=airflow_etl
    )

    t2 = PythonOperator(
        task_id='log_status_task',
        python_callable=airflow_log
    )

    t1 >> t2