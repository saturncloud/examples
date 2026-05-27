# OpenClaw Beta on Saturn Cloud

[OpenClaw](https://docs.openclaw.ai/) is an AI agent gateway that connects any major AI model to a browser-based Control UI and optional messaging channels (Telegram, WhatsApp). This template deploys OpenClaw as a long-running **Deployment** on Saturn Cloud — install, onboard, and start the gateway automatically on every boot.

For the full guide, see:
[https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)

---

## 🚀 Getting Started

### Step 1 — Create your secrets

Go to **Settings → Secrets** in Saturn Cloud and create the following secrets. Secret names must match exactly (case-sensitive).

**Required:**

| Secret name | What to put in it |
|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | A secure random token — run `openssl rand -hex 32` to generate one. This is the password to access your OpenClaw Control UI. |

**AI provider — create exactly one:**

| Secret name | Provider | Default model (if `OPENCLAW_MODEL` is blank) |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic | `anthropic/claude-sonnet-4-5` |
| `OPENAI_API_KEY` | OpenAI | `openai/gpt-5.5` |
| `GEMINI_API_KEY` | Google Gemini | `google/gemini-3.1-pro-preview` |
| `MISTRAL_API_KEY` | Mistral | `mistral/mistral-large-latest` |
| `OPENROUTER_API_KEY` | OpenRouter | `openrouter/auto` |

Only **one** provider key is needed. If you set more than one, OpenClaw uses the first it detects in the order listed above (Anthropic → OpenAI → Gemini → Mistral → OpenRouter).

---

### Step 2 — Link your secrets to the deployment

On the deployment detail page, scroll to the **Secrets** section. You'll see a slot for each provider. Link the secrets you created in Step 1 to their matching slots. Leave the other provider slots unlinked.

---

### Step 3 — Configure optional settings

In the **Environment Variables** section:

| Variable | Default | When to change it |
|---|---|---|
| `OPENCLAW_MODEL` | *(auto, based on provider)* | Set a specific model ID to override the default, e.g. `anthropic/claude-opus-4-7` |
| `OPENCLAW_PUBLIC_ORIGIN` | *(auto-detected)* | Leave blank — the deployment auto-detects its own public URL at startup |
| `ENABLE_TELEGRAM` | `false` | Set to `true` to enable Telegram channel |
| `ENABLE_WHATSAPP` | `false` | Set to `true` to enable WhatsApp channel |

---

### Step 4 — Start the deployment

Hit **Start**. The bootstrap script will:
1. Install OpenClaw
2. Run non-interactive onboarding (configures gateway port, token auth, allowed origin)
3. Set the default model
4. Start the gateway on port 8000

Startup takes **3–5 minutes** on first boot.

---

### Step 5 — Open the Control UI

Once the status shows **Running**, click the deployment URL. You'll be prompted for your `OPENCLAW_GATEWAY_TOKEN`. Enter the token you generated in Step 1.

---

## 🔌 Optional Channels

### Telegram

Set `ENABLE_TELEGRAM=true` and create + link a `TELEGRAM_BOT_TOKEN` secret (token from [@BotFather](https://t.me/BotFather)).

Update `TELEGRAM_ALLOW_FROM` with the Telegram user ID(s) allowed to message the bot:
```
["your_telegram_user_id"]
```
Get your Telegram user ID by messaging [@userinfobot](https://t.me/userinfobot).

### WhatsApp

Set `ENABLE_WHATSAPP=true`.

Update `WHATSAPP_ALLOW_FROM` with the phone number(s) in E.164 format:
```
["+1234567890"]
```
After the gateway starts, go to **Channels → WhatsApp** in the Control UI and scan the QR code.

---

## ⚙️ How It Works

The deployment command runs `bash .saturn/bootstrap-openclaw.sh`, which:

1. **Validates** that `OPENCLAW_GATEWAY_TOKEN` is set — fails immediately with a clear error if not
2. **Auto-detects the public origin** from `SATURN_JUPYTER_BASE_DOMAIN` (injected by Saturn Cloud) — no manual URL needed
3. **Detects the AI provider** from whichever API key env var is set
4. **Installs OpenClaw** via the official installer
5. **Runs onboarding** non-interactively — configures port 8000, LAN binding, token auth
6. **Applies config** — sets model, allowed origins, disables device pairing for proxy environments
7. **Configures channels** if enabled (Telegram / WhatsApp)
8. **Starts the gateway** via `exec openclaw gateway`

---

## 🛠️ Tech Stack

| Component | Role |
|---|---|
| **OpenClaw** | AI agent gateway — Control UI, channels, tool use |
| **Saturn Cloud Deployment** | Hosts the gateway as a long-running service on port 8000 |
| **`saturn-python:2025.05.01`** | Base image (includes Node.js, required by OpenClaw) |
| **`large` instance** | AWS r5.large — 2 vCPU, 16 GB RAM |

---

## 🔗 Resources

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Saturn Cloud Deployment Guide](https://saturncloud.io/docs/)
- [Full Tutorial: OpenClaw on Saturn Cloud](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)
