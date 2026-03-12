from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI(title="Titanic Survival Predictor")
model = joblib.load("model.joblib")

class Passenger(BaseModel):
    features: list[float] # [Pclass, Sex, Age, SibSp, Parch, Fare]

@app.post("/predict")
def predict(data: Passenger):
    features = np.array(data.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    
    status = "SURVIVED" if prediction == 1 else "DID NOT SURVIVE"
    
    return {
        "result": status,
        "probability": f"{round(np.max(prob) * 100, 2)}%",
        "data_source": "Existing Titanic Dataset"
    }