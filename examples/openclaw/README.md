# OpenClaw on Saturn Cloud

This example is a **Deployment** with `sleep infinity` so you can install and run [OpenClaw](https://docs.openclaw.ai/) over SSH. The recipe uses **`saturn-python:2025.05.01`** and instance size **`large`** (AWS **r5.large**: 2 vCPU, 16 GB RAM). For the full guide (resource options, env vars, install, WhatsApp, gateway, and troubleshooting), see the blog:

[https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/](https://saturncloud.io/blog/how-to-deploy-openclaw-on-saturncloud/)

## Environment variables

Set these in the deployment **Details** (do not commit secrets). The blog explains each value and how to generate `OPENCLAW_GATEWAY_TOKEN`.

- `OPENAI_API_KEY`
- `OPENCLAW_GATEWAY_TOKEN`
- `OPENCLAW_PUBLIC_ORIGIN`
- `WHATSAPP_OWNER_E164`

Optional custom skills: see `skills/README.md`.
