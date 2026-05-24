#!/usr/bin/env bash
# NeMo Text Processing — install dependencies on Saturn Cloud workspace startup
set -euo pipefail

LOG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/startup.log"
log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "Starting NeMo Text Processing setup..."

# ─── Check if already installed ───────────────────────────────────────────────
if python -c "import nemo_text_processing" &>/dev/null 2>&1; then
    log "nemo_text_processing already installed — OK"
    log "Open nemo_text_processing_demo.ipynb in JupyterLab to get started."
    exit 0
fi

# ─── Install ──────────────────────────────────────────────────────────────────
log "Installing nemo_text_processing (this takes 3-5 minutes on first run)..."
pip install --quiet nemo_text_processing &>>"$LOG" \
    || { log "ERROR: installation failed — check startup.log"; exit 1; }

log "Installation complete."
log "Open nemo_text_processing_demo.ipynb in JupyterLab to get started."
