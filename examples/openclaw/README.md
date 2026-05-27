# OpenClaw Beta on Saturn Cloud

[OpenClaw](https://docs.openclaw.ai/) is an AI agent gateway that connects any major AI model to a browser-based Control UI and optional messaging channels (Telegram, WhatsApp). This template deploys OpenClaw as a long-running **Deployment** on Saturn Cloud — it installs, configures, and starts the gateway automatically every time it boots.

For the full guide, see:
[https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)

---

## What You'll End Up With

A live OpenClaw gateway running on Saturn Cloud, accessible at your deployment URL, protected by your own token, connected to the AI provider of your choice. Total setup time: **under 10 minutes** (plus 3–5 minutes for the deployment to boot).

---

## Step 1 — Create the Deployment from the Template

Click **Use Template** on the OpenClaw Beta card. Saturn Cloud pre-fills the deployment form with everything already configured:

- Instance type, image, and command are set
- Environment variables are pre-filled with sensible defaults
- Secret slots for your gateway token and all supported AI providers are already defined with descriptions

You can rename the deployment if you like. Click **Create** — the deployment is created but not started yet. You'll set up your secrets first.

---

## Step 2 — Create Your Secrets

Go to **Settings → Secrets** in the left sidebar. You need to create **two secrets**: one gateway token and one AI provider key.

### Gateway token (required)

This is the password that protects access to your OpenClaw Control UI. Generate a secure random one:

```bash
openssl rand -hex 32
```

Copy the output. In **Settings → Secrets**, click **New Secret**:
- **Name**: `OPENCLAW_GATEWAY_TOKEN`
- **Value**: the output from the command above

Save it somewhere safe — you'll need it every time you open the Control UI.

### AI provider key (pick one)

Create a secret for whichever AI provider you have an account with. Only one is needed.

| Secret name | Provider | Default model used |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic | `anthropic/claude-sonnet-4-5` |
| `OPENAI_API_KEY` | OpenAI | `openai/gpt-5.5` |
| `GEMINI_API_KEY` | Google Gemini | `google/gemini-3.1-pro-preview` |
| `MISTRAL_API_KEY` | Mistral | `mistral/mistral-large-latest` |
| `OPENROUTER_API_KEY` | OpenRouter | `openrouter/auto` |

If you set more than one, OpenClaw picks the first it detects in the order above (Anthropic → OpenAI → Gemini → Mistral → OpenRouter).

---

## Step 3 — Link Your Secrets to the Deployment

Go back to your deployment and open the **Details** tab. Scroll to the **Secrets** section — you'll see a slot for each provider and for the gateway token.

- Find the `OPENCLAW_GATEWAY_TOKEN` slot → click its dropdown → select the `OPENCLAW_GATEWAY_TOKEN` secret you just created
- Find the slot matching your AI provider (e.g. `ANTHROPIC_API_KEY`) → link your API key secret to it
- Leave all other provider slots **unlinked** — that's fine, the unused ones are just ignored

---

## Step 4 — Optional Configuration

Most users can skip this step entirely and go straight to Start. The defaults work out of the box.

If you want to customise:

| Environment variable | Default | When to change |
|---|---|---|
| `OPENCLAW_MODEL` | *(auto, based on provider)* | Set a specific model ID, e.g. `anthropic/claude-opus-4-7` or `openai/gpt-4o` |
| `OPENCLAW_PUBLIC_ORIGIN` | *(auto-detected)* | Leave blank — the deployment detects its own public URL at startup. Only set this if you're using a custom domain in front of the deployment. |
| `ENABLE_TELEGRAM` | `false` | Set to `true` to connect a Telegram bot |
| `ENABLE_WHATSAPP` | `false` | Set to `true` to connect WhatsApp |
| `TELEGRAM_ALLOW_FROM` | `["123456789"]` | Replace with your actual Telegram user ID(s) |
| `WHATSAPP_ALLOW_FROM` | `["+1234567890"]` | Replace with your actual phone number(s) in E.164 format |

---

## Step 5 — Start the Deployment

Click **Start**. The status changes from `stopped` → `pending` → `running`.

During startup (3–5 minutes), the bootstrap script runs automatically. You can watch its progress in the **Logs** section of the deployment page:

```
[openclaw] starting setup...
[openclaw] auto-detected public origin: https://your-deployment-url.community.saturnenterprise.io
[openclaw] selected auth provider: anthropic-api-key
[openclaw] selected model: anthropic/claude-sonnet-4-5
[openclaw] installing OpenClaw...
[openclaw] running onboarding...
[openclaw] setting default model...
[openclaw] starting gateway on port 8000...
[gateway] ready
```

If the status changes to `error`, check the logs — the most common cause is a missing or unlinked secret.

---

## Step 6 — Open the Control UI

Once the status shows **Running**, click the deployment URL (shown on the deployment detail page). The OpenClaw Control UI opens in your browser.

When prompted for a token, enter the value of `OPENCLAW_GATEWAY_TOKEN` — the one you generated with `openssl rand -hex 32` in Step 2. You're in.

---

## Step 7 — Use OpenClaw

Inside the Control UI you can:

- **Chat** with your AI model directly from the browser
- **View conversation history** across sessions
- **Configure tools and plugins** (web search, memory, and more)
- **Connect Telegram** (if enabled) — message your bot from Telegram and it replies via your AI model
- **Connect WhatsApp** (if enabled) — go to Channels → WhatsApp and scan the QR code

---

## 🔌 Enabling Telegram

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram — it gives you a bot token
2. Create a secret named `TELEGRAM_BOT_TOKEN` in **Settings → Secrets** with that token
3. Link it to the `TELEGRAM_BOT_TOKEN` slot on your deployment
4. Get your Telegram user ID by messaging [@userinfobot](https://t.me/userinfobot)
5. Set `ENABLE_TELEGRAM=true` and update `TELEGRAM_ALLOW_FROM` with your user ID: `["your_id"]`
6. Restart the deployment

---

## 🔌 Enabling WhatsApp

1. Set `ENABLE_WHATSAPP=true` and update `WHATSAPP_ALLOW_FROM` with your phone number in E.164 format: `["+1234567890"]`
2. Restart the deployment
3. Once running, open the Control UI → go to **Channels → WhatsApp** → scan the QR code with your phone

---

## ⚙️ How It Works

Every time the deployment starts, `bash .saturn/bootstrap-openclaw.sh` runs and does the following in order:

| Step | What happens |
|---|---|
| **Validate** | Fails immediately with a clear error if `OPENCLAW_GATEWAY_TOKEN` is not set |
| **Auto-detect origin** | Reads `SATURN_JUPYTER_BASE_DOMAIN` (injected by Saturn Cloud into every container) and sets the Control UI allowed origin automatically — no manual URL needed |
| **Detect provider** | Checks which API key env var is set and picks the matching provider and default model |
| **Install** | Downloads and installs OpenClaw via the official installer |
| **Onboard** | Runs `openclaw onboard --non-interactive` — configures port 8000, LAN binding, token auth |
| **Configure** | Sets the default model, allowed origins, and disables device pairing (required for Saturn's proxy environment) |
| **Channels** | Configures Telegram and/or WhatsApp if enabled |
| **Start** | Runs `exec openclaw gateway` — replaces the shell with the gateway process |

---

## 🛠️ Tech Stack

| Component | Role |
|---|---|
| **OpenClaw** | AI agent gateway — Control UI, channels, tool use |
| **Saturn Cloud Deployment** | Hosts the gateway as a long-running service on port 8000 |
| **`saturn-python:2025.05.01`** | Base image (includes Node.js, required by OpenClaw) |
| **`large` instance** | AWS r5.large — 2 vCPU, 16 GB RAM |

---

## ❓ Troubleshooting

**Deployment goes to `error` on startup**
→ Open the **Logs** section. Look for `is required` in the output — this means a required secret is missing or unlinked. Check that `OPENCLAW_GATEWAY_TOKEN` and your AI provider key are both linked in the Secrets section.

**Control UI loads but token is rejected**
→ Make sure you're entering the exact value you set for `OPENCLAW_GATEWAY_TOKEN`, not the secret name. Copy it directly from where you saved it.

**`origin not allowed` error in logs**
→ `OPENCLAW_PUBLIC_ORIGIN` was set to an incorrect value. Clear it (set to blank) and restart — auto-detection will handle it correctly.

**No AI provider found error in logs**
→ None of the AI provider keys are linked. Go to the deployment's Secrets section and link your API key to the correct slot.

---

## 🔗 Resources

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Saturn Cloud Deployment Guide](https://saturncloud.io/docs/)
- [Full Tutorial: OpenClaw on Saturn Cloud](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)
