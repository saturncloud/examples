# Hyperparameter Tuning & Serving (Optuna + Ray Tune)

This template implements an end-to-end **Auto-ML workflow** on a **Python Server**. It automates the lifecycle of a machine learning model, combining the intelligent search of Optuna with the scalable execution of Ray Tune.

**Infrastructure:** [Saturn Cloud](https://saturncloud.io/)
**Resource:** Python Server
**Hardware:** CPU
**Tech Stack:** Optuna, Ray Tune, FastAPI, Scikit-Learn

---

## 📖 Overview

Standard hyperparameter tuning scripts often stop at printing the best parameters. This template goes further by **operationalizing** the result. It solves two key problems:

1.  **Efficient Search:** It uses **Optuna's** Tree-Parzen Estimator (TPE) algorithm to intelligently select hyperparameters, wrapped in **Ray Tune** to run multiple trials in parallel.
2.  **Instant Deployment:** The workflow automatically retrains the model with the best parameters, saves the artifact, and serves it via a production-ready **FastAPI** server.

---

## 🚀 Quick Start

### 1. Environment Setup
Run the setup script to create a virtual environment and install all dependencies (Ray, Optuna, FastAPI, Uvicorn, Scikit-Learn).
```bash
# 1. Make executable
chmod +x setup.sh

# 2. Run setup
bash setup.sh

```

### 2. Run the Tuning Job (Batch)

Execute the tuning script. This will:

* Launch 20 concurrent trials using Ray Tune.
* Identify the best configuration (e.g., `n_estimators`, `max_depth`).
* **Retrain** the model on the full dataset using those winning parameters.
* **Save** the final model to `best_model.pkl`.

```bash
# Activate environment
source venv/bin/activate

# Start tuning
python tune_hpo.py

```

### 3. Start the API Server

Once `tune_hpo.py` finishes and generates `best_model.pkl`, start the server to accept real-time requests.

```bash
python app.py

```

---

## 🧠 Architecture: "Tune & Serve"

The workflow consists of two distinct stages designed to bridge the gap between experimentation and production.

### Stage 1: Optimization (`tune_hpo.py`)

* **Search Algorithm:** We use `OptunaSearch`, which leverages Bayesian optimization to learn from previous trials and find optimal parameters faster.
* **Execution Engine:** Ray Tune manages the resources. It uses a `ConcurrencyLimiter` to run 4 trials simultaneously on the CPU, significantly reducing total wait time.

### Stage 2: Inference (`app.py`)

* **Loader:** On startup, the API loads the optimized `best_model.pkl` artifact.
* **Endpoint:** Exposes a `/predict` route that accepts Iris flower features and returns the classified species (Setosa, Versicolor, or Virginica).

---

## 🧪 Testing

You can test the API using the built-in Swagger UI or via the terminal.

### Method 1: Web Interface

Visit `http://localhost:8000/docs`. Click **POST /predict** -> **Try it out**.

**Test Case A: Setosa (Small Petals)**
Paste this JSON:

```json
{
  "sepal_length": 5.1, "sepal_width": 3.5,
  "petal_length": 1.4, "petal_width": 0.2
}

```

*Expected Result:* `{"class_name": "setosa"}`

**Test Case B: Virginica (Large Petals)**
Paste this JSON:

```json
{
  "sepal_length": 6.5, "sepal_width": 3.0,
  "petal_length": 5.2, "petal_width": 2.0
}

```

*Expected Result:* `{"class_name": "virginica"}`

### Method 2: Terminal (CURL)

Run this command in a new terminal window to test the Virginica prediction:

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length": 6.5,
  "sepal_width": 3.0,
  "petal_length": 5.2,
  "petal_width": 2.0
}'

```

---

## 🏁 Conclusion

This template demonstrates a "Best of Both Worlds" approach: using Optuna for search intelligence and Ray Tune for scaling. By automating the retraining and serving steps, you create a pipeline where model improvements can be deployed rapidly.

To scale the tuning phase—running hundreds of parallel trials across a distributed cluster of machines—consider deploying this workflow on [Saturn Cloud](https://saturncloud.io/).

```

```