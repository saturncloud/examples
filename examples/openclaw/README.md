# OpenClaw on Saturn Cloud

This example deploys [OpenClaw](https://docs.openclaw.ai/) as a **Saturn Cloud deployment**: the start script installs Node.js 22 and OpenClaw, then runs `openclaw gateway --headless` bound to **port 8000** and **0.0.0.0** so the dashboard is reachable via Saturn’s external URL.

## Before you start

- Saturn Cloud account  
- LLM credentials via resource **environment variables** (do not commit secrets), for example `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` / `OPENAI_BASE_URL`  
- A messaging integration configured inside OpenClaw (for example Discord); see OpenClaw docs  

## Configure secrets

In the resource UI, add your provider keys under **Environment Variables**. They are injected at runtime and should not appear in this repository.

## Optional: existing OpenClaw config

If you already have `config.json` (and optional skills) from a local install:

1. Upload them under `/home/jovyan/workspace/.openclaw/` on the resource **or** place `.openclaw/` next to this example in the cloned repo path.  
2. The start script sets `OPENCLAW_HOME` automatically when one of those directories exists.

## Enable the dashboard URL

Turn on the deployment **external URL** in Saturn Cloud so you can open the OpenClaw dashboard in a browser and finish onboarding if you are not using an uploaded `config.json`.

## Custom skills

See `skills/README.md`. Restart the deployment after changing skills or config.

## References

- OpenClaw documentation: https://docs.openclaw.ai/  
- Saturn Cloud deployments: https://saturncloud.io/docs/

## Maintainer note (gallery thumbnail)

The default template entry uses the shared deployment thumbnail (`api-icon.png`) until `example-thumbnails/openclaw.png` (500×250) is published under `saturn-public-assets`, then update `.saturn/templates-*.json` to point at that URL.
