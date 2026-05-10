# OpenClaw on Saturn Cloud

This example matches the **setup-first** workflow from the Saturn Cloud blog: create a **Deployment** that keeps running with `sleep infinity`, then install and operate OpenClaw **over SSH** (official installer, onboarding, WhatsApp plugin, foreground gateway). The deployment command does **not** start OpenClaw automatically.

For the full walkthrough with screenshots, see the Saturn Cloud blog post **How to Deploy OpenClaw on Saturn Cloud** on https://saturncloud.io (same steps as this example).

## What this recipe provides

| In the template | You do manually (SSH / UI) |
|-----------------|----------------------------|
| `saturn-python` image, **medium** instance | Generate gateway token (`openssl rand -hex 32`) |
| **`sleep infinity`** so the deployment stays alive | Set env vars in Saturn deployment **Details** |
| Clone path under `working_directory` | Enable **SSH**, external URL on port **8000**, subdomain |
| | Install OpenClaw via **install.sh**, run **onboard**, configure WhatsApp |
| | Run **`openclaw gateway`** in a terminal session (foreground) |

## Deployment settings (summary)

Create a **Deployment** (not Jupyter) with:

- **Image:** `saturncloud/saturn-python` (this recipe uses the equivalent `public.ecr.aws/saturncloud/saturn-python` tag from examples).  
- **Command:** `sleep infinity` — keeps the container running while you configure OpenClaw in SSH (same as this repo’s `saturn.json`).  
- **External URL:** enabled, routed to container port **8000**.  
- **Allow SSH connections:** enabled.  
- **Custom subdomain:** set a unique value for your public URL.

## Environment variables

Add in the deployment **Details** (never commit secrets):

```bash
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENCLAW_GATEWAY_TOKEN=YOUR_GATEWAY_TOKEN   # from openssl rand -hex 32
OPENCLAW_PUBLIC_ORIGIN=https://your-subdomain.community.saturnenterprise.io
WHATSAPP_OWNER_E164=+1234567890
```

Use your real deployment URL for `OPENCLAW_PUBLIC_ORIGIN` (no trailing slash). `WHATSAPP_OWNER_E164` is the allowed sender number for WhatsApp DMs.

## After SSH connects

1. Check Node: `node -v` / `npm -v` (install Node only if missing).  
2. Install OpenClaw:

   ```bash
   curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --no-onboard
   ```

3. Run non-interactive onboarding (port **8000**, token from env), then set `gateway.controlUi.allowedOrigins` — exact flags are in the blog post.  
4. Install and configure **WhatsApp** (`plugins`, `channels login`, QR scan) per the blog.  
5. Start the gateway in **Terminal 1:** `openclaw gateway` (foreground). Use **Terminal 2** for `openclaw devices approve` when the browser asks.  
6. Do **not** rely on `openclaw gateway restart` for this setup (no systemd service).

## Persistence warning

Without persistent storage for `~/.openclaw`, redeploys can lose WhatsApp session, device approvals, and config. Plan storage before changing the deployment command away from `sleep infinity` after setup.

## Optional custom skills

See `skills/README.md` if you add OpenClaw skills under this clone path.

## References

- OpenClaw docs: https://openclaw.ai/docs  
- Saturn Cloud SSH: https://saturncloud.io/docs/user-guide/how-to/access/ide_ssh/

## Maintainer note (gallery thumbnail)

Template manifests use `example-thumbnails/api-icon.png` until `example-thumbnails/openclaw.png` (500×250) exists on `saturn-public-assets`; then update `.saturn/templates-*.json`.
