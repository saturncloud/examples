# XGBoost Serving API

This template implements a **maintenance-free** Model Serving workflow for a **Regression** problem. It uses the **California Housing dataset** (~20,000 samples) to train an XGBoost model that predicts house prices, deployed via a schema-agnostic FastAPI service.

**Infrastructure:** [Saturn Cloud](https://saturncloud.io/)
**Resource:** Jupyter Notebook
**Hardware:** CPU
**Tech Stack:** XGBoost (Regression), FastAPI, Pandas, Scikit-Learn

---

## 📖 Overview

In traditional model serving, changing the model's features (e.g., adding "zip_code" or removing "age") often requires rewriting the API code. This template demonstrates a **"Model-First"** architecture where the API is generic and adapts to the model artifact automatically.

This is deployed as a **Jupyter Notebook** resource on [Saturn Cloud](https://saturncloud.io/), allowing you to develop, train, and serve from a single environment.

---

## 🚀 Quick Start

### 1. Workflow

1. Open **`xgboost_serving.ipynb`** in the Jupyter interface.
2. **Run All Cells**:
* **Install:** Installs dependencies (`xgboost`, `fastapi`, `uvicorn`) directly in the kernel.
* **Train:** Trains an `XGBRegressor` on the California Housing dataset (20,640 samples).
* **Generate:** Writes the `app.py` server file to disk.



### 2. Launch the Server

The notebook generates the API code for you. To run it, open a **Terminal** in Jupyter (File -> New -> Terminal) and execute:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000

```
We can run it from the next code cell in the jupyter notebook.
---

## 🧠 Architecture: Schema-Agnostic Design

This template uses a **"Model-First"** approach where the API code is decoupled from the specific features of the model. This allows the API to serve the regression model dynamically.

* **Inputs:** A generic list of numerical values (representing the 8 housing features like `MedInc`, `HouseAge`, etc.).
* **Outputs:** A continuous float value (Estimated House Value).
* **Maintenance:** To update the model features (e.g., adding "Zip Code" or removing "Rooms"), you simply retrain and replace `model.json`. The Python API code remains untouched.

### Dataset Details

* **Source:** California Housing Dataset (1990 Census).
* **Target:** Median House Value in units of **$100,000**.
* **Features:** 8 numerical features including Median Income, House Age, Average Rooms, Latitude, and Longitude.

---

## 🧪 Testing

The API using the built-in Swagger UI or via the terminal.

### Method 1: Web Interface

Visit `http://localhost:8000/docs`. Click **POST /predict** -> **Try it out** and paste the JSON below.

```json
{
  "features": [
    8.32,
    41.0,
    6.98,
    1.02,
    322.0,
    2.55,
    37.88,
    -122.23
  ]
}

```

### Method 2: Terminal (CURL)

Run this command in a separate terminal window to send a sample request:

```bash
# Features: [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Lat, Long]
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [8.32, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]}'

```

**Expected Output:**

```json
{"estimated_value": 4.526}

```

*Interpretation: The model predicts a median house value of roughly **$452,600**.*

---

Note: you can use whatever values for the parameters and get predicted results

## 🏁 Conclusion

For scaling this workflow—such as deploying this API to a Kubernetes cluster or scheduling the training job—consider moving this pipeline to [Saturn Cloud](https://saturncloud.io/).

```