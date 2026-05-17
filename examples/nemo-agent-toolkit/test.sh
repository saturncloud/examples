#!/usr/bin/env bash
# Smoke-tests the NeMo Agent Toolkit setup before running the demo
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASS=0; FAIL=0

ok()     { echo "  [PASS] $*"; PASS=$((PASS + 1)); }
fail()   { echo "  [FAIL] $*"; FAIL=$((FAIL + 1)); }
header() { echo; echo "── $* ──────────────────────────────────"; }

# Load env
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    set -o allexport; source "$SCRIPT_DIR/.env"; set +o allexport
fi

# ─── Python ───────────────────────────────────────────────────────────────────
header "Python"

PYTHON_CMD=""
for cmd in python3.13 python3.12 python3.11 python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [[ "$major" -eq 3 && "$minor" -ge 11 ]]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

[[ -n "$PYTHON_CMD" ]] \
    && ok "Python $("$PYTHON_CMD" --version) found" \
    || fail "Python 3.11, 3.12, or 3.13 not found — install one first"

# ─── nvidia-nat ───────────────────────────────────────────────────────────────
header "nvidia-nat"

VENV_NAT=".venv/bin/nat"
if [[ -f "$SCRIPT_DIR/$VENV_NAT" ]]; then
    ok "nat CLI found in .venv"
    "$SCRIPT_DIR/$VENV_NAT" --version &>/dev/null \
        && ok "nat --version OK" \
        || fail "nat --version failed"
else
    fail "nat CLI not found — run ./start.sh first to install"
fi

# ─── Workflow config ──────────────────────────────────────────────────────────
header "Workflow config"

[[ -f "$SCRIPT_DIR/workflow.yml" ]] \
    && ok "workflow.yml present" \
    || fail "workflow.yml missing"

# ─── Environment variables ────────────────────────────────────────────────────
header "Environment variables"

[[ -n "${NVIDIA_API_KEY:-}" ]] \
    && ok "NVIDIA_API_KEY is set" \
    || fail "NVIDIA_API_KEY not set — copy .env.example to .env and fill it in"

[[ "${NVIDIA_API_KEY:-}" == nvapi-* ]] \
    && ok "NVIDIA_API_KEY format looks correct (nvapi-...)" \
    || fail "NVIDIA_API_KEY doesn't start with 'nvapi-' — check your key"

# ─── NVIDIA API connectivity ──────────────────────────────────────────────────
header "NVIDIA API connectivity"

if [[ -n "${NVIDIA_API_KEY:-}" ]]; then
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $NVIDIA_API_KEY" \
        "https://integrate.api.nvidia.com/v1/models")

    case "$http_code" in
        200) ok "NVIDIA API reachable and key is valid (HTTP 200)" ;;
        401) fail "NVIDIA API key invalid or expired (HTTP 401)" ;;
        403) fail "NVIDIA API key lacks permissions (HTTP 403)" ;;
        *)   fail "NVIDIA API returned unexpected status: HTTP $http_code" ;;
    esac
else
    fail "Skipping API test — NVIDIA_API_KEY not set"
fi

# ─── Summary ──────────────────────────────────────────────────────────────────
echo
echo "══════════════════════════════════════"
echo "  Results: $PASS passed, $FAIL failed"
echo "══════════════════════════════════════"

[[ $FAIL -eq 0 ]] && echo "  Ready to run: ./start.sh" || echo "  Fix the failures above, then re-run test.sh"
echo
[[ $FAIL -eq 0 ]]
