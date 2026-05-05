#!/usr/bin/env python
"""Aggregate DVC-tracked NYC taxi trips into per-zone-hour features,
register them with Feast, and materialize to the online store.

Reads the parquet produced by ingest_taxi_dvc.py and writes a new
aggregated parquet (PULocationID × hour) that Feast points at via a
FileSource. Online store is SQLite on the shared FS — single-process
demo, so no server.

Lineage emitted: feast project + feature view + online store path +
dvc commit (read from the source repo's HEAD) for downstream MLflow
runs to consume.
"""
import argparse
import json
import os
import subprocess
from datetime import timedelta
from pathlib import Path

import pandas as pd

DEFAULT_BASE = os.environ.get("SHARED_STORAGE", "/home/jovyan/shared")

FEATURES_PY = '''from datetime import timedelta
from feast import Entity, Field, FeatureView, FileSource
from feast.types import Float32, Int64

zone = Entity(name="zone", join_keys=["PULocationID"])

zone_stats_source = FileSource(
    name="zone_stats_source",
    path="data/zone_hourly_stats.parquet",
    timestamp_field="event_timestamp",
)

zone_hourly_stats = FeatureView(
    name="zone_hourly_stats",
    entities=[zone],
    ttl=timedelta(days={ttl_days}),
    schema=[
        Field(name="avg_fare", dtype=Float32),
        Field(name="avg_distance", dtype=Float32),
        Field(name="avg_passengers", dtype=Float32),
        Field(name="trip_count", dtype=Int64),
    ],
    online=True,
    source=zone_stats_source,
)
'''

YAML = '''project: nyc_taxi_features
registry: data/registry.db
provider: local
online_store:
    type: sqlite
    path: data/online_store.db
entity_key_serialization_version: 3
'''


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-parquet",
                   default=f"{DEFAULT_BASE}/nyc-taxi/cleaned/taxi.parquet")
    p.add_argument("--source-repo",
                   default=f"{DEFAULT_BASE}/nyc-taxi",
                   help="DVC/git repo to read HEAD from for lineage")
    p.add_argument("--feast-repo",
                   default=f"{DEFAULT_BASE}/feast-repo")
    p.add_argument("--ttl-days", type=int, default=1825)
    return p.parse_args()


def run(cmd, cwd=None, capture=False):
    print(f"$ {' '.join(str(c) for c in cmd)}", flush=True)
    if capture:
        return subprocess.check_output(cmd, cwd=cwd, text=True).strip()
    subprocess.run(cmd, cwd=cwd, check=True)


def aggregate(src: Path, dst: Path) -> dict:
    df = pd.read_parquet(src, columns=[
        "tpep_pickup_datetime", "PULocationID",
        "fare_amount", "trip_distance", "passenger_count",
    ])
    df = df.dropna(subset=["tpep_pickup_datetime", "PULocationID"])
    df["event_timestamp"] = df["tpep_pickup_datetime"].dt.floor("h")

    agg = df.groupby(["PULocationID", "event_timestamp"], as_index=False).agg(
        avg_fare=("fare_amount", "mean"),
        avg_distance=("trip_distance", "mean"),
        avg_passengers=("passenger_count", "mean"),
        trip_count=("fare_amount", "size"),
    )
    agg["PULocationID"] = agg["PULocationID"].astype("int64")
    for col in ("avg_fare", "avg_distance", "avg_passengers"):
        agg[col] = agg[col].astype("float32")
    agg["trip_count"] = agg["trip_count"].astype("int64")

    dst.parent.mkdir(parents=True, exist_ok=True)
    agg.to_parquet(dst, index=False)
    return {
        "rows": len(agg),
        "min_ts": agg["event_timestamp"].min().isoformat(),
        "max_ts": agg["event_timestamp"].max().isoformat(),
        "unique_zones": int(agg["PULocationID"].nunique()),
    }


def write_repo(repo: Path, ttl_days: int):
    (repo / "data").mkdir(parents=True, exist_ok=True)
    (repo / "features.py").write_text(FEATURES_PY.format(ttl_days=ttl_days))
    (repo / "feature_store.yaml").write_text(YAML)


def dvc_head(repo: Path):
    if not (repo / ".git").exists():
        return None
    try:
        return run(["git", "rev-parse", "HEAD"], cwd=repo, capture=True)
    except subprocess.CalledProcessError:
        return None


def main():
    args = parse_args()
    src = Path(args.source_parquet)
    feast_repo = Path(args.feast_repo).resolve()

    if not src.exists():
        raise SystemExit(f"source parquet not found: {src}")

    write_repo(feast_repo, args.ttl_days)

    agg_path = feast_repo / "data" / "zone_hourly_stats.parquet"
    print(f"📊 aggregating {src} → {agg_path}", flush=True)
    info = aggregate(src, agg_path)
    print(f"   {info['rows']:,} rows across {info['unique_zones']} zones, "
          f"[{info['min_ts']}, {info['max_ts']}]", flush=True)

    run(["feast", "apply"], cwd=feast_repo)

    start = pd.Timestamp(info["min_ts"]).isoformat()
    end = (pd.Timestamp(info["max_ts"]) + timedelta(days=1)).isoformat()
    run(["feast", "materialize", start, end], cwd=feast_repo)

    lineage = {
        "feast_project": "nyc_taxi_features",
        "feast_repo": str(feast_repo),
        "feature_view": "zone_hourly_stats",
        "online_store": str(feast_repo / "data" / "online_store.db"),
        "registry": str(feast_repo / "data" / "registry.db"),
        "dvc_commit": dvc_head(Path(args.source_repo)),
        "source_parquet": str(src),
        "materialization_window": {"start": start, "end": end},
        "aggregated_rows": info["rows"],
        "unique_zones": info["unique_zones"],
    }
    print("LINEAGE:", json.dumps(lineage), flush=True)


if __name__ == "__main__":
    main()
