# OpenClaw on Saturn Cloud

This example runs [OpenClaw](https://docs.openclaw.ai/) as a **Deployment**: on start it installs OpenClaw (once), applies onboarding and configuration from environment variables, then runs `openclaw gateway` on port **8000**. The recipe uses **`saturn-python:2025.05.01`** and instance size **`large`** (AWS **r5.large**: 2 vCPU, 16 GB RAM).

For the full guide (resource options, QR flows, troubleshooting), see:

[https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)

## Startup

`deployment.command`: **`bash .saturn/bootstrap-openclaw.sh`** (runs from **`working_directory`**).

## Environment variables

Set values in the deployment **Details** (never commit secrets).

### Required

| Variable | Description |
|----------|-------------|
| `OPENCLAW_GATEWAY_TOKEN` | Gateway authentication token (`--gateway-token-ref-env`). |
| `OPENCLAW_PUBLIC_ORIGIN` | Control UI allowed origin, e.g. `https://your-subdomain.community.saturnenterprise.io`. |

### AI provider

Set **one** API key; that determines the provider. Optional model override: **`OPENCLAW_MODEL`**.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI (`openai-api-key`). |
| `ANTHROPIC_API_KEY` | Anthropic (`anthropic-api-key`). |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Gemini (`gemini-api-key`). |
| `MISTRAL_API_KEY` | Mistral (`mistral-api-key`). |
| `OPENROUTER_API_KEY` | OpenRouter (`openrouter-api-key`). |
| `OPENCLAW_MODEL` | Primary model id (defaults depend on provider if unset). |

### WhatsApp (optional)

When **`ENABLE_WHATSAPP=true`**:

| Variable | Description |
|----------|-------------|
| `ENABLE_WHATSAPP` | `true` / `false`. |
| `WHATSAPP_ALLOW_FROM` | JSON array string, e.g. `["+1234567890"]`. |

### Telegram (optional)

When **`ENABLE_TELEGRAM=true`**:

| Variable | Description |
|----------|-------------|
| `ENABLE_TELEGRAM` | `true` / `false`. |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather. |
| `TELEGRAM_ALLOW_FROM` | JSON array string, e.g. `["123456789"]`. |
