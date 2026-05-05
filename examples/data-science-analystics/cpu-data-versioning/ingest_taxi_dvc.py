#!/usr/bin/env python
"""Ingest a month of NYC TLC taxi data and version it with DVC.

One invocation = one new dataset version. Designed to run as a Saturn
job (HTTP-triggerable) with the repo and DVC remote on networked storage.

Layout (defaults under $SHARED_STORAGE, /home/jovyan/shared):
    {base}/nyc-taxi/        git + dvc repo; holds cleaned/taxi.parquet
    {base}/nyc-taxi/raw/    intermediate downloads (gitignored)
    {base}/dvc-storage/     dvc remote (object-store equivalent)

Differentiate v1 vs v2 across runs by changing --year/--month or
--min-fare; each run produces a new git commit + dvc push.
"""
import argparse
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import pandas as pd

NYC_TLC_BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DEFAULT_BASE = os.environ.get("SHARED_STORAGE", "/home/jovyan/shared")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year", type=int, default=2024)
    p.add_argument("--month", type=int, default=1)
    p.add_argument("--taxi-type", choices=["yellow", "green", "fhv"], default="yellow")
    p.add_argument("--min-fare", type=float, default=0.0,
                   help="Drop trips with fare_amount below this. v1=0.0, v2=2.5 makes a clear demo diff.")
    p.add_argument("--repo-dir", default=f"{DEFAULT_BASE}/nyc-taxi")
    p.add_argument("--dvc-remote", default=f"{DEFAULT_BASE}/dvc-storage")
    p.add_argument("--message", default=None)
    return p.parse_args()


def run(cmd, cwd=None):
    print(f"$ {' '.join(str(c) for c in cmd)}", flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_repo(repo_dir: Path, dvc_remote: Path):
    repo_dir.mkdir(parents=True, exist_ok=True)
    if not (repo_dir / ".git").exists():
        run(["git", "init", "-q"], cwd=repo_dir)
        run(["git", "config", "user.email", "ingest@saturncloud.io"], cwd=repo_dir)
        run(["git", "config", "user.name", "ingest-job"], cwd=repo_dir)
        (repo_dir / ".gitignore").write_text("raw/\n")
        run(["git", "add", ".gitignore"], cwd=repo_dir)
        run(["git", "commit", "-q", "-m", "init repo"], cwd=repo_dir)
    if not (repo_dir / ".dvc").exists():
        run(["dvc", "init", "-q"], cwd=repo_dir)
        run(["dvc", "config", "core.autostage", "true"], cwd=repo_dir)
        dvc_remote.mkdir(parents=True, exist_ok=True)
        run(["dvc", "remote", "add", "-d", "shared", str(dvc_remote)], cwd=repo_dir)
        run(["git", "add", ".dvc", ".dvcignore"], cwd=repo_dir)
        run(["git", "commit", "-q", "-m", "init dvc"], cwd=repo_dir)


def download(year: int, month: int, taxi_type: str, dest: Path) -> dict:
    url = f"{NYC_TLC_BASE}/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"⬇️  {url}", flush=True)
    t0 = time.time()
    urllib.request.urlretrieve(url, dest)
    elapsed = time.time() - t0
    size_mb = dest.stat().st_size / 1e6
    rate = size_mb / elapsed if elapsed else 0
    print(f"   {size_mb:.1f} MB in {elapsed:.1f}s ({rate:.1f} MB/s, ≈{rate * 3.6:.1f} GB/hr)", flush=True)
    return {"bytes": dest.stat().st_size, "seconds": elapsed, "mb_per_sec": rate}


def clean(src: Path, dst: Path, min_fare: float) -> dict:
    df = pd.read_parquet(src)
    n_in = len(df)
    if min_fare > 0 and "fare_amount" in df.columns:
        df = df[df["fare_amount"] >= min_fare]
    dst.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(dst, index=False)
    print(f"   cleaned {n_in:,} → {len(df):,} rows (min_fare={min_fare})", flush=True)
    return {"rows_in": n_in, "rows_out": len(df)}


def commit_version(repo_dir: Path, tracked: Path, message: str) -> str:
    rel = tracked.relative_to(repo_dir)
    run(["dvc", "add", str(rel)], cwd=repo_dir)
    status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo_dir).returncode
    if status == 0:
        print("   no change vs HEAD; skipping commit", flush=True)
    else:
        run(["git", "commit", "-q", "-m", message], cwd=repo_dir)
    run(["dvc", "push", "-q"], cwd=repo_dir)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_dir, text=True).strip()


def main():
    args = parse_args()
    repo_dir = Path(args.repo_dir).resolve()
    dvc_remote = Path(args.dvc_remote).resolve()

    ensure_repo(repo_dir, dvc_remote)

    raw = repo_dir / "raw" / f"{args.taxi_type}_{args.year}-{args.month:02d}.parquet"
    cleaned = repo_dir / "cleaned" / "taxi.parquet"

    dl = download(args.year, args.month, args.taxi_type, raw)
    cl = clean(raw, cleaned, args.min_fare)

    msg = args.message or (
        f"{args.taxi_type} {args.year}-{args.month:02d} min_fare={args.min_fare}"
    )
    sha = commit_version(repo_dir, cleaned, msg)

    lineage = {
        "dvc_commit": sha,
        "dataset_path": str(cleaned),
        "source": f"{args.taxi_type}_tripdata_{args.year}-{args.month:02d}",
        "min_fare": args.min_fare,
        "ingest": dl,
        "clean": cl,
    }
    print("LINEAGE:", json.dumps(lineage), flush=True)


if __name__ == "__main__":
    main()
