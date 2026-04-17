# 📊 TaskWeaver Data Analyst (Code-First Intelligence)

*Cloud deployment architecture verified for [Saturn Cloud](https://saturncloud.io/). Optimized for **Python 3.13** and **Microsoft TaskWeaver**.*

**Hardware:** CPU/GPU | **Resource:** Python Project & Web App | **Tech Stack:** TaskWeaver, Pandas, Streamlit, OpenAI

\<p align="left"\>
\<img src="[https://img.shields.io/badge/Deployed\_on-Saturn\_Cloud-blue?style=for-the-badge\&logo=cloud](https://img.shields.io/badge/Deployed_on-Saturn_Cloud-blue?style=for-the-badge&logo=cloud)" alt="Saturn Cloud"\>
\<img src="[https://img.shields.io/badge/Framework-TaskWeaver-0078D4?style=for-the-badge\&logo=microsoft](https://www.google.com/search?q=https://img.shields.io/badge/Framework-TaskWeaver-0078D4%3Fstyle%3Dfor-the-badge%26logo%3Dmicrosoft)" alt="TaskWeaver"\>
\<img src="[https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)" alt="Streamlit"\>
\<img src="[https://img.shields.io/badge/Analytics-Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white](https://www.google.com/search?q=https://img.shields.io/badge/Analytics-Pandas-150458%3Fstyle%3Dfor-the-badge%26logo%3Dpandas%26logoColor%3Dwhite)" alt="Pandas"\>
\</p\>

## 📖 Overview

This template provides a production-grade **Data Analytics Agent** powered by Microsoft TaskWeaver. Unlike traditional agents that simply predict text, TaskWeaver is a **Code-First framework** that autonomously generates and executes Python code to manipulate DataFrames, perform statistical analysis, and create visualizations.

### 🧩 Key Features

1.  **Planner-Interpreter-Executor Loop:** The agent decomposes complex requests into discrete sub-tasks, writes Python code, executes it in a secure sandbox, and self-corrects if it encounters errors.
2.  **Native Pandas Integration:** Optimized for large-scale CSV/Excel manipulation. The agent "thinks" in DataFrames.
3.  **Stateful Session Management:** Maintain context across complex, multi-step data science workflows.

-----

## 🏗️ Local Setup & Installation

Due to the evolving nature of the TaskWeaver framework, we utilize a direct source-installation to ensure compatibility with Python 3.13.

```bash
# 1. Create and Activate Environment
python3 -m venv venv
source venv/bin/activate

# 2. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

*If you encounter visualization issues on Linux, ensure system headers are present:* `sudo apt update && sudo apt install python3-tk -y`

-----

## ⚙️ Infrastructure Configuration

**1. Environment Variables:**
Create a `.env` file in the root directory:

  * `OPENAI_API_KEY`: Your OpenAI Secret Key.
  * `LLM_MODEL`: Set to `gpt-4o` for optimal performance.

**2. TaskWeaver Project Config:**
The `project/taskweaver_config.json` is pre-configured to disable external example dependencies for a lightweight cloud start.

-----

## 🚀 Execution & Testing

### Phase 1: The Terminal CLI

Run the CLI to watch the agent's internal "thought process" and code generation.

```bash
python cli.py
```

### Phase 2: The Streamlit Data Dashboard

Launch the web interface to upload datasets and interact visually.

```bash
streamlit run app.py
```

-----

## 💪 Stress Testing (Limit Verification)

To verify the agent's reasoning and self-correction capabilities, try these **Boss Level** queries in either the CLI or UI:

### 🛠️ Test 1: The "Dirty Data" Challenge

*Tests data engineering and imputation logic.*

> "Generate a DataFrame with 50 rows of sales data. Include 5 rows with NaN values in 'Revenue' and 5 rows where the 'Date' is 'ERROR'. Then, clean the data by removing 'ERROR' dates, fill missing 'Revenue' with the median, and show the top 5 cleaned rows."

### 📊 Test 2: Multi-Step Statistical Correlation

*Tests mathematical reasoning and visualization.*

> "Create a dataset with 100 entries for 'Temperature', 'Ice\_Cream\_Sales', and 'Rainfall'. Make sales highly correlated with temperature but negatively with rainfall. Calculate the correlation matrix and generate a Seaborn heatmap."

### 🧠 Test 3: Predictive Modeling

*Tests Scikit-Learn integration and ML workflow.*

> "Generate a dataset of 200 'House\_Size' and 'House\_Price' entries. Split into training/testing sets, train a Linear Regression model, report the R-squared score, and predict the price for a 2500 sq ft house."

-----

## ☁️ Cloud Deployment (Saturn Cloud)

1.  **Resource:** Streamlit Deployment.
2.  **Secrets:** Inject `OPENAI_API_KEY` via Saturn Cloud Secrets.
3.  **Start Command:** `streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

-----

## 📚 References

  * [TaskWeaver Documentation](https://microsoft.github.io/TaskWeaver/)
  * [Saturn Cloud Guides](https://saturncloud.io/docs/)
  * [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)
