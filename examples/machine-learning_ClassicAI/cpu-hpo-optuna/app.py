from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Auto-Tuned Iris API")

# Define Input Schema
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Global Model Variable
model = None
MODEL_PATH = "best_model.pkl"

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✅ Loaded optimized model: {MODEL_PATH}")
    else:
        print(f"⚠️ Error: {MODEL_PATH} not found. Run 'python tune_hpo.py' first.")

@app.post("/predict")
def predict(data: IrisData):
    if not model:
        return {"error": "Model not loaded"}
    
    # Prepare features
    features = np.array([[
        data.sepal_length, 
        data.sepal_width, 
        data.petal_length, 
        data.petal_width
    ]])
    
    # Predict
    prediction = int(model.predict(features)[0])
    
    # Map to Class Name
    classes = {0: "setosa", 1: "versicolor", 2: "virginica"}
    
    return {
        "class_id": prediction,
        "class_name": classes.get(prediction, "unknown")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)