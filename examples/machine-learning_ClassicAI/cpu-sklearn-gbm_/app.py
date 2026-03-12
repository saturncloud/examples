from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# 1. Initialize API
app = FastAPI(title="Iris Baseline API")

# 2. Define Input Schema (Sepal/Petal dimensions)
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# 3. Load Model Global Variable
model = None
MODEL_PATH = "iris_model.pkl"

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✅ Loaded model from {MODEL_PATH}")
    else:
        print(f"⚠️ Error: {MODEL_PATH} not found. Did you run baseline_demo.py?")

# 4. Prediction Endpoint
@app.post("/predict")
def predict(data: IrisData):
    if not model:
        return {"error": "Model not trained yet."}
    
    # Convert input JSON to model-ready array
    features = np.array([[
        data.sepal_length, 
        data.sepal_width, 
        data.petal_length, 
        data.petal_width
    ]])
    
    # Predict Class (0, 1, or 2)
    prediction = int(model.predict(features)[0])
    
    # Map to String Name
    classes = {0: "setosa", 1: "versicolor", 2: "virginica"}
    return {
        "class_id": prediction,
        "class_name": classes.get(prediction, "unknown")
    }

# 5. Run Server (If executed directly)
if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 is crucial for cloud servers to be accessible
    uvicorn.run(app, host="0.0.0.0", port=8000)