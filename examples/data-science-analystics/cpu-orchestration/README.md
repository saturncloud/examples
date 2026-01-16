# 🚀 Prefect/Airflow Orchestration Template

### **Overview**



This template provides a robust, production-ready environment for orchestrating **Daily ETL and Machine Learning workflows** using **Python 3.11**. It demonstrates a dual-orchestrator pattern where the same logic can be executed instantly via **Prefect 2.x** or scheduled via **Apache Airflow 2.10**.

* **Hardware:** CPU
* **Tech Stack:** Prefect (v2.x), Apache Airflow (v2.10.4), Plotly, Pandas
* **Use Case:** Daily ETL + Model Run DAG

> **Ready to scale?** Deploy this template effortlessly on **[Saturn Cloud](https://saturncloud.io/)**, the easiest way to run data science and ML workloads in the cloud.

---

### **📂 Project Structure**

```text
cpu-orchestration/
├── setup.sh                # Master installer (Handles Miniconda, Venv, & Conflicts)
├── requirements.txt               
├── miniconda_dist/           # Self-contained Python 3.11 environment
├── airflow_home/             # Airflow config and database (SQLite)
│   └── dags/
│       └── daily_etl_airflow.py  # Airflow DAG definition
├── data/
│   └── pipeline_logs.csv     # Shared log file for both orchestrators
├── scripts/
│   ├── daily_etl_prefect.py  # Prefect Flow (Immediate execution)
│   └── dashboard.py          # Plotly visualization of run status
└── README.md

```

---

### **⚙️ Installation**

This template includes a custom `setup.sh` script that manages system dependencies, installs a local Miniconda distribution, and resolves dependency conflicts between Prefect and Airflow (specifically regarding `SQLAlchemy`).

1. **Run the Setup Script:**
```bash
chmod +x setup.sh
./setup.sh

```


*This will take 2-5 minutes to download Python 3.11 and compile Airflow dependencies.*
2. **Activate the Environment:**
*You must run this command every time you open a new terminal.*
```bash
source $(pwd)/miniconda_dist/bin/activate $(pwd)/miniconda_dist/envs/airflow_env

```



---

### **🏃 Quick Start**

#### **Option A: Run with Prefect (Fast & Immediate)**

Prefect is configured for immediate, ad-hoc execution of the pipeline.

```bash
python scripts/daily_etl_prefect.py

```

* **Output:** You will see logs in the terminal (`🚀 [Prefect] Starting Extraction...`) and a success message.
* **Data:** Logs are saved to `data/pipeline_logs.csv`.

#### **Option B: Run with Airflow (Scheduled & UI-Based)**

Airflow is configured as a standalone service with a web interface.

1. **Set Home & Start:**
```bash
export AIRFLOW_HOME=$(pwd)/airflow_home
airflow standalone

```


2. **Access the UI:**
* **URL:** [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)
* **Username:** `admin`
* **Password:** `admin`


3. **Trigger the DAG:**
* Search for `daily_etl_airflow`.
* **Unpause:** Click the toggle switch (gray → blue).
* **Trigger:** Click the **Play (▶)** button under "Actions" → "Trigger DAG".



---

### **📊 Visualization**

Monitor the performance of your pipeline across both tools using the included dashboard.

```bash
python scripts/dashboard.py

```

* **Yellow Dots:** Runs executed by Prefect.
* **Blue Dots:** Runs executed by Airflow.

---

### **🔧 Troubleshooting & Notes**

* **Version Pinning:** We explicitly pinned `prefect<3.0.0` and `sqlalchemy<2.0` in the setup. **Do not upgrade these** manually, or Airflow 2.10 will crash due to database driver incompatibility.
* **Environment Location:** If you see `EnvironmentLocationNotFound`, ensure you are using the full path provided in the activation command above.
* **Saturn Cloud Deployment:** When moving this to [Saturn Cloud](https://saturncloud.io/), you can skip the Miniconda installation steps and simply install the `requirements.txt` (generated via `pip freeze`) into the default Saturn image.

---

**Developed for Data Science & Analytics Templates.**
*Need more power? Upgrade to GPU resources on [Saturn Cloud](https://saturncloud.io/).*