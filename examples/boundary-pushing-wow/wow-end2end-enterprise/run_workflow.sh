#!/bin/bash
# 1. Clean previous runs
rm -rf data/*.db data/*.parquet mlruns/

# 2. Source environment
source virt-env/bin/activate

# 3. Ingest: Raw Data -> Spark -> Parquet
echo "--- Phase 1: Ingesting Data with Spark ---"
python src/ingestion.py

# 4. Feature: Register with Feast
echo "--- Phase 2: Registering Features with Feast ---"
cd feature_repo
feast apply
# Materialize data into the Online Store (SQLite) for FastAPI
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental $CURRENT_TIME
cd ..

# 5. Train: Feast -> MLflow
echo "--- Phase 3: Training Model with MLflow ---"
python src/training.py

# 6. Serve: MLflow + Feast -> FastAPI
echo "--- Phase 4: Launching FastAPI Serving Layer ---"
echo "API will be available at http://localhost:8000"
echo "Check Swagger Docs at http://localhost:8000/docs"
python src/main.py