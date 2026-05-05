"""FastAPI inference endpoint: tip-prediction model + Feast online features.

Loads at startup:
- The most recent MLflow run from experiment `nyc_taxi_tipping` (or the run
  pinned by $MLFLOW_RUN_ID), plus its sklearn model.
- The Feast feature store at $FEAST_REPO so we can fetch live zone features.

At request time:
- Caller supplies (PULocationID, trip_distance, fare_amount).
- We pull the live `zone_hourly_stats` row for that zone from Feast's online
  store, combine it with the request features, and call model.predict_proba.
- Lineage tags from the MLflow run are echoed back so any prediction can be
  traced to the exact dataset + feature view it was trained on.

Run locally:
    uvicorn serve:app --host 0.0.0.0 --port 8000

Saturn deployment command (same string in the Deployment "Command" field):
    python3 -m uvicorn serve:app --host 0.0.0.0 --port 8000
"""
import os
from pathlib import Path

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from feast import FeatureStore
from pydantic import BaseModel
from starlette.responses import Response

BASE = Path(os.environ.get("SHARED_STORAGE", "/home/jovyan/shared/demo/test-data"))
MLRUNS = Path(os.environ.get("MLFLOW_TRACKING_DIR", BASE / "mlruns"))
FEAST_REPO = Path(os.environ.get("FEAST_REPO", BASE / "feast-repo"))
EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT", "nyc_taxi_tipping")
PINNED_RUN = os.environ.get("MLFLOW_RUN_ID")

FEATURE_COLS = ["avg_fare", "avg_distance", "avg_passengers", "trip_count",
                "trip_distance", "fare_amount"]


def _resolve_run_id() -> str:
    if PINNED_RUN:
        return PINNED_RUN
    client = mlflow.tracking.MlflowClient()
    exp = client.get_experiment_by_name(EXPERIMENT)
    if exp is None:
        raise RuntimeError(f"experiment not found: {EXPERIMENT}")
    runs = client.search_runs([exp.experiment_id], order_by=["start_time DESC"], max_results=1)
    if not runs:
        raise RuntimeError(f"no runs in experiment: {EXPERIMENT}")
    return runs[0].info.run_id


LINEAGE_KEYS = {"dvc_commit", "feast_project", "feast_feature_view",
                "feast_registry_mtime", "source_parquet"}

mlflow.set_tracking_uri(f"file:{MLRUNS}")
RUN_ID = _resolve_run_id()
MODEL = mlflow.sklearn.load_model(f"runs:/{RUN_ID}/model")
_run_tags = mlflow.tracking.MlflowClient().get_run(RUN_ID).data.tags
LINEAGE = {k: v for k, v in _run_tags.items() if k in LINEAGE_KEYS}
LINEAGE["mlflow_run_id"] = RUN_ID
STORE = FeatureStore(repo_path=str(FEAST_REPO))

app = FastAPI(title="NYC taxi tip predictor", version="1.0")


class PredictRequest(BaseModel):
    PULocationID: int
    trip_distance: float
    fare_amount: float


@app.get("/")
async def root():
    return Response("Opening the docs UI", status_code=302, headers={"location": "/docs"})


@app.get("/health")
async def health():
    return {"status": "ok", "lineage": LINEAGE}


@app.post("/predict")
async def predict(req: PredictRequest):
    online = STORE.get_online_features(
        features=[
            "zone_hourly_stats:avg_fare",
            "zone_hourly_stats:avg_distance",
            "zone_hourly_stats:avg_passengers",
            "zone_hourly_stats:trip_count",
        ],
        entity_rows=[{"PULocationID": req.PULocationID}],
    ).to_dict()

    if online["avg_fare"][0] is None:
        raise HTTPException(404, f"no online features for PULocationID={req.PULocationID}")

    row = pd.DataFrame([{
        "avg_fare": online["avg_fare"][0],
        "avg_distance": online["avg_distance"][0],
        "avg_passengers": online["avg_passengers"][0],
        "trip_count": online["trip_count"][0],
        "trip_distance": req.trip_distance,
        "fare_amount": req.fare_amount,
    }])[FEATURE_COLS]

    proba = float(MODEL.predict_proba(row)[0, 1])
    return {
        "PULocationID": req.PULocationID,
        "high_tip_probability": round(proba, 4),
        "prediction": int(proba >= 0.5),
        "features_used": row.iloc[0].to_dict(),
        "lineage": LINEAGE,
    }
