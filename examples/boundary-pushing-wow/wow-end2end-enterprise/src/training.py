import mlflow
import mlflow.sklearn
import pandas as pd
from feast import FeatureStore
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
import os

def train_model():
    # 1. Connect to the Feast Feature Store
    store = FeatureStore(repo_path="feature_repo")

    # 2. Define the 'Entity DataFrame'
    # In a real enterprise app, these IDs and timestamps come from your target labels
    entity_df = pd.DataFrame.from_dict({
        "user_id": [101, 102],
        "event_timestamp": [
            datetime.now() - timedelta(minutes=10),
            datetime.now() - timedelta(minutes=5)
        ],
        "target": [150.0, 20.0]  # The 'labels' the model tries to predict
    })

    # 3. Fetch Historical Features from Feast
    # This retrieves 'total_spend' for those users at those specific timestamps
    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=["user_stats:total_spend"]
    ).to_df()

    # 4. MLflow Experiment Tracking
    mlflow.set_experiment("Enterprise_Workflow_Training")
    
    with mlflow.start_run() as run:
        # Prepare Features (X) and Target (y)
        X = training_df[["total_spend"]]
        y = training_df["target"]

        # Train the Model
        # (Change to XGBoost or PyTorch here for GPU support)
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X, y)

        # Log Parameters and Metrics to MLflow
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("feature_count", len(X.columns))
        
        # Log the Model Artifact
        # This creates the folder inside 'mlruns' that FastAPI looks for
        mlflow.sklearn.log_model(model, "model")
        
        print(f"✅ Training Complete. Run ID: {run.info.run_id}")
        print(f"✅ Model saved to: mlruns/0/{run.info.run_id}/artifacts/model")

if __name__ == "__main__":
    train_model()