#!/usr/bin/env bash
set -eo pipefail

cat > "$HOME/start-openclaw.sh" <<'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

echo "[openclaw] starting setup..."

: "${OPENCLAW_GATEWAY_TOKEN:?OPENCLAW_GATEWAY_TOKEN is required}"
: "${OPENCLAW_PUBLIC_ORIGIN:?OPENCLAW_PUBLIC_ORIGIN is required}"

ENABLE_WHATSAPP="${ENABLE_WHATSAPP:-false}"
ENABLE_TELEGRAM="${ENABLE_TELEGRAM:-false}"

ENABLE_WHATSAPP="$(echo "$ENABLE_WHATSAPP" | tr '[:upper:]' '[:lower:]')"
ENABLE_TELEGRAM="$(echo "$ENABLE_TELEGRAM" | tr '[:upper:]' '[:lower:]')"

is_true() {
  case "$1" in
    true|1|yes|y|on) return 0 ;;
    false|0|no|n|off|"") return 1 ;;
    *)
      echo "[openclaw] invalid boolean value: $1"
      echo "[openclaw] use true or false"
      exit 1
      ;;
  esac
}

detect_ai_provider() {
  if [ -n "${OPENAI_API_KEY:-}" ]; then
    AI_AUTH_CHOICE="openai-api-key"
    AI_MODEL="${OPENCLAW_MODEL:-openai/gpt-5.5}"
  elif [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    AI_AUTH_CHOICE="anthropic-api-key"
    AI_MODEL="${OPENCLAW_MODEL:-anthropic/claude-sonnet-4-5}"
  elif [ -n "${GEMINI_API_KEY:-}" ] || [ -n "${GOOGLE_API_KEY:-}" ]; then
    AI_AUTH_CHOICE="gemini-api-key"
    AI_MODEL="${OPENCLAW_MODEL:-google/gemini-3.1-pro-preview}"
  elif [ -n "${MISTRAL_API_KEY:-}" ]; then
    AI_AUTH_CHOICE="mistral-api-key"
    AI_MODEL="${OPENCLAW_MODEL:-mistral/mistral-large-latest}"
  elif [ -n "${OPENROUTER_API_KEY:-}" ]; then
    AI_AUTH_CHOICE="openrouter-api-key"
    AI_MODEL="${OPENCLAW_MODEL:-openrouter/auto}"
  else
    echo "[openclaw] No AI provider API key found."
    echo "[openclaw] Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, MISTRAL_API_KEY, OPENROUTER_API_KEY."
    exit 1
  fi

  echo "[openclaw] selected auth provider: $AI_AUTH_CHOICE"
  echo "[openclaw] selected model: $AI_MODEL"
}

detect_ai_provider

echo "[openclaw] installing OpenClaw..."

curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard

echo "[openclaw] installed version:"
openclaw --version

echo "[openclaw] running onboarding..."

openclaw onboard --non-interactive \
  --mode local \
  --auth-choice "$AI_AUTH_CHOICE" \
  --secret-input-mode ref \
  --gateway-port 8000 \
  --gateway-bind lan \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk \
  --skip-health

echo "[openclaw] setting default model..."

openclaw config set agents.defaults.model.primary "$AI_MODEL"

echo "[openclaw] setting allowed origin..."

openclaw config set gateway.controlUi.allowedOrigins "[\"$OPENCLAW_PUBLIC_ORIGIN\"]" --strict-json

echo "[openclaw] disabling Control UI device pairing for template mode..."

openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true --strict-json

if is_true "$ENABLE_WHATSAPP"; then
  echo "[openclaw] configuring WhatsApp..."

  : "${WHATSAPP_ALLOW_FROM:?WHATSAPP_ALLOW_FROM is required when ENABLE_WHATSAPP=true}"

  openclaw plugins install @openclaw/whatsapp

  openclaw config set channels.whatsapp.dmPolicy allowlist
  openclaw config set channels.whatsapp.allowFrom "$WHATSAPP_ALLOW_FROM" --strict-json
  openclaw config set channels.whatsapp.groupPolicy disabled

  echo "[openclaw] WhatsApp configured."
  echo "[openclaw] After the UI opens, go to Channels and scan the WhatsApp QR code."
else
  echo "[openclaw] WhatsApp disabled."
fi

if is_true "$ENABLE_TELEGRAM"; then
  echo "[openclaw] configuring Telegram..."

  : "${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN is required when ENABLE_TELEGRAM=true}"
  : "${TELEGRAM_ALLOW_FROM:?TELEGRAM_ALLOW_FROM is required when ENABLE_TELEGRAM=true}"

  openclaw config set channels.telegram.enabled true
  openclaw config set channels.telegram.botToken "$TELEGRAM_BOT_TOKEN"

  openclaw config set channels.telegram.dmPolicy allowlist
  openclaw config set channels.telegram.allowFrom "$TELEGRAM_ALLOW_FROM" --strict-json
  openclaw config set channels.telegram.groupPolicy disabled

  echo "[openclaw] Telegram configured."
  echo "[openclaw] Message your Telegram bot from the allowlisted Telegram user ID."
else
  echo "[openclaw] Telegram disabled."
fi

echo "[openclaw] starting gateway on port 8000..."

exec openclaw gateway
SCRIPT

chmod +x "$HOME/start-openclaw.sh"

echo "Created $HOME/start-openclaw.sh"

exec "$HOME/start-openclaw.sh"
