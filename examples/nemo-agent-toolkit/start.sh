#!/usr/bin/env bash
# NeMo Agent Toolkit — Research Assistant demo
# Runs locally and as a Saturn Cloud start_script
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/nat-start.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
die() { log "ERROR: $*"; exit 1; }

# ─── 1. Load environment ─────────────────────────────────────────────────────
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    set -o allexport
    source "$SCRIPT_DIR/.env"
    set +o allexport
    log "Loaded .env"
fi

# Disable telemetry in non-interactive environments
export NAT_TELEMETRY_ENABLED="${NAT_TELEMETRY_ENABLED:-false}"

# ─── 2. Validate required vars ───────────────────────────────────────────────
[[ -z "${NVIDIA_API_KEY:-}" ]] && die "NVIDIA_API_KEY is not set. Copy .env.example to .env and fill it in."
export NVIDIA_API_KEY

# ─── 3. Check Python 3.11+ ───────────────────────────────────────────────────
PYTHON_CMD=""
check_python() {
    local python_cmd=""
    for cmd in python3.13 python3.12 python3.11 python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
            local major minor
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            if [[ "$major" -eq 3 && "$minor" -ge 11 ]]; then
                python_cmd="$cmd"
                break
            fi
        fi
    done
    [[ -z "$python_cmd" ]] && die "Python 3.11, 3.12, or 3.13 is required. Install one and re-run."
    log "Python $("$python_cmd" --version) — OK"
    PYTHON_CMD="$python_cmd"
}

# ─── 4. Set up virtual environment ───────────────────────────────────────────
setup_venv() {
    local python_cmd="$1"
    local venv_dir="$SCRIPT_DIR/.venv"

    if [[ ! -d "$venv_dir" ]]; then
        log "Creating virtual environment..."
        "$python_cmd" -m venv "$venv_dir" &>>"$LOG_FILE"
    fi

    # Activate
    source "$venv_dir/bin/activate"
    log "Virtual environment active"
}

# ─── 5. Install nvidia-nat ───────────────────────────────────────────────────
install_nat() {
    if python -c "import nemo_agent_toolkit; import langchain_core; import langchain_nvidia_ai_endpoints; import nat.plugins.langchain; import nat.plugins.eval; import nat.plugins.opentelemetry" &>/dev/null 2>&1; then
        log "nvidia-nat and integrations already installed — OK"
        apply_wikipedia_patch
        apply_loader_patch
        return
    fi
    log "Installing nvidia-nat..."
    python -m pip install --quiet --upgrade nvidia-nat &>>"$LOG_FILE" \
        || die "nvidia-nat install failed — check $LOG_FILE"

    log "Installing langchain integrations..."
    python -m pip install --quiet --upgrade langchain langchain-core langchain-community langchain-nvidia-ai-endpoints &>>"$LOG_FILE" \
        || die "langchain integrations install failed — check $LOG_FILE"

    log "Registering integration plugins..."
    python -m pip install --quiet --upgrade --no-deps nvidia-nat-langchain nvidia-nat-eval nvidia-nat-opentelemetry &>>"$LOG_FILE" \
        || die "plugin registration failed — check $LOG_FILE"

    log "Installing telemetry dependencies..."
    python -m pip install --quiet --upgrade opentelemetry-api opentelemetry-sdk "opentelemetry-exporter-otlp~=1.3" &>>"$LOG_FILE" \
        || die "telemetry dependencies install failed — check $LOG_FILE"

    log "nvidia-nat and integrations installed successfully"
    apply_wikipedia_patch
    apply_loader_patch
}

apply_wikipedia_patch() {
    log "Applying Wikipedia API User-Agent patch..."
    python -c "
import nat.plugins.langchain.tools.wikipedia_search as ws
path = ws.__file__
with open(path, 'r') as f:
    content = f.read()
if 'wikipedia.set_user_agent' not in content:
    patched = content.replace(
        'async def _wiki_search(question: str) -> str:',
        'async def _wiki_search(question: str) -> str:\n        import wikipedia\n        wikipedia.set_user_agent(\"SaturnCloudResearchBot/1.0 (contact@saturncloud.io)\")'
    )
    with open(path, 'w') as f:
        f.write(patched)
" &>>"$LOG_FILE" || log "WARNING: Failed to apply Wikipedia User-Agent patch"
}

apply_loader_patch() {
    log "Applying plugin loader traceback suppression patch..."
    python -c "
import nat.runtime.loader as nl
path = nl.__file__
with open(path, 'r') as f:
    content = f.read()
target = '            except ImportError:\n                logger.warning(\"Failed to import plugin \\'%s\\'\", entry_point.name, exc_info=True)'
replacement = '            except ImportError:\n                logger.debug(\"Failed to import plugin \\'%s\\'\", entry_point.name, exc_info=True)\n                logger.warning(\"Failed to import plugin \\'%s\\' (optional integration dependencies not installed)\", entry_point.name)'
if target in content:
    patched = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(patched)
" &>>"$LOG_FILE" || log "WARNING: Failed to apply loader patch"
}

# ─── 6. Run the demo ─────────────────────────────────────────────────────────
run_demo() {
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "Running Research Assistant demo..."
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    nat run \
        --config_file "$SCRIPT_DIR/workflow.yml" \
        --input "Research large language models and provide a timeline of five key milestones in their development, from early transformer models to recent advances."

    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "Demo complete. To run your own query:"
    log "  nat run --config_file workflow.yml --input \"your question here\""
    log ""
    log "To launch the chat UI:"
    log "  nat serve --config_file workflow.yml"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ─── Main ────────────────────────────────────────────────────────────────────
log "Starting NeMo Agent Toolkit — Research Assistant"
check_python
setup_venv "$PYTHON_CMD"
install_nat
run_demo
