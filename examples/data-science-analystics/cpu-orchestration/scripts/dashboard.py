import plotly.express as px
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "data", "pipeline_logs.csv")

def show_dashboard():
    if not os.path.exists(LOG_FILE):
        print("⚠️ No logs found yet. Run the Prefect script first!")
        return

    df = pd.read_csv(LOG_FILE)
    
    fig = px.scatter(
        df, x='Date', y='Duration_Seconds',
        color='Orchestrator', symbol='Status',
        title="<b>🚀 Pipeline Status: Prefect vs Airflow</b>",
        color_discrete_map={'Prefect': '#f1c40f', 'Airflow': '#3498db'},
        template="plotly_dark"
    )
    fig.show()

if __name__ == "__main__":
    show_dashboard()