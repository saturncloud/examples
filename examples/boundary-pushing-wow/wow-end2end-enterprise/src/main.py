import os
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from feast import FeatureStore

# Initialize FastAPI app
app = FastAPI(title="Enterprise ML Serving API")

# Initialize Feast Feature Store
store = FeatureStore(repo_path="feature_repo")

def get_latest_model_uri():
    """
    Uses the MLflow API to find the most recent successful run 
    across all experiments.
    """
    try:
        # Search all experiments and order by start_time descending
        runs = mlflow.search_runs(
            search_all_experiments=True, 
            order_by=["start_time DESC"], 
            max_results=1
        )
        
        if not runs.empty:
            run_id = runs.iloc[0].run_id
            # Construct the URI using the standard MLflow format
            model_uri = f"runs:/{run_id}/model"
            print(f"✅ Found latest model from Run ID: {run_id}")
            return model_uri
    except Exception as e:
        print(f"⚠️ Error searching for latest model: {e}")
    return None

# Load the model during startup
MODEL_URI = get_latest_model_uri()

if MODEL_URI:
    try:
        # Load as a generic Python function for easy inference
        model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)
        print(f"✅ Successfully loaded model from: {MODEL_URI}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None
else:
    model = None
    print("❌ Model not found. Run 'python src/training.py' first.")

class UserRequest(BaseModel):
    user_id: int

@app.get("/")
def health_check():
    return {
        "status": "Enterprise API is Online",
        "model_loaded": model is not None,
        "model_uri": MODEL_URI
    }

@app.post("/predict")
def predict(request: UserRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded on server.")

    try:
        # 1. Fetch Online Features from Feast
        feature_vector = store.get_online_features(
            features=["user_stats:total_spend"],
            entity_rows=[{"user_id": request.user_id}]
        ).to_dict()

        # 2. Convert to DataFrame
        features_df = pd.DataFrame.from_dict(feature_vector)

        prediction_df = features_df[["total_spend"]] 
        
        # 3. Generate Prediction using only the required features
        prediction = model.predict(prediction_df)
        
        return {
            "user_id": request.user_id,
            "prediction": float(prediction[0]),
            "features_retrieved": feature_vector
        }
    except Exception as e:
        # Logging the error helps debugging
        print(f"❌ Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)