# Shared Learnings

Curated durable facts useful to any AI coding agent working in Alistair's projects.

## User

- Alistair. SA dev. Homelab: 8 Proxmox VMs (pve, games, nas, media, ollama, services, server, pihole), Docker Compose in /opt/homelab, SSH host aliases. Comfortable with git, Docker, system admin.
- GitHub: aawobdev. SSH remotes (git@github.com:aawobdev/*.git). Projects under ~/projects/ (auto-synced across machines).
- Google account: al.ouma666@gmail.com.
- Terse, direct, terminal-native. Tries things first, only asks as last resort. Automated reports: emoji status (✅⚠️❌) in headers, bold section headers (no md headers), bullet lists, inline code for names, compact, under 6 lines when nothing changed.
- Infrastructure spans ollama VM (192.168.1.123, hostname `ollama`) + laptop. Consistent tooling/setup across instances.
- Credentials: Bitwarden Secrets Manager (BWS): UNIFI_SSH_PASSWORD, UNIFI_USERNAME, UNIFI_PASSWORD. Google service account key: ~/.gdrive-mcp/amex-service-account.json (amex-reconcile@hermes-499012.iam.gserviceaccount.com, service account — no token expiry).
- Plex library: shared with UK and South Africa users only.
- Responsive to actionable follow-up suggestions — prefer concrete next steps over answers alone.
- Ollama (192.168.1.123:11434): query /api/tags endpoint for live model list — always query live, never rely on memory.

## Projects

- Fold It In (recipe-site): Next.js/Prisma/PG on :3000. Docker PG on :5432. Instagram scraping via page HTML OG meta-tags. Apify fallback needs IG creds. AI extract chain: /api/v1/ai/extract-instagram + /api/v1/ai/extract-recipe.
- Crawford Measure: Next.js/Prisma on :5000. SA tax brackets (year 2027, rebate R17,820, conv rate 4.5%). Auth.js v5 — production next start needs AUTH_TRUST_HOST env var. Deployed to crawford.citium.space via PVE LXC 131.
- Life Tracker: Expo SDK 54, port 8089. Personal health tracking (cancer/chemo/surgery). Privacy paramount. EAS: aacodemode/life-tracker. AI: OpenRouter deepseek-v4-flash.
- CarSync: Android native, WSL. JDK 17 (~/jdk17), Android SDK (~/Android/sdk). Phone: Samsung SM_S921B, 192.168.1.243, adb wireless.
- hermes-skills: AI agent skill collection at ~/projects/hermes-skills/.
- Homelab: Docker Compose across Proxmox VMs. Repo at ~/projects/homelab (WSL) / /opt/homelab (VMs). Infra reference: AGENTS.md in repo.
- Amex reconciliation: Google Sheets via service account amex-reconcile@hermes-499012.iam.gserviceaccount.com (key: ~/.gdrive-mcp/amex-service-account.json). Google Drive MCP tools: list/search/read/get_file/move/create_folder/copy/trash.
- Graylog (192.168.1.124:9009): MongoDB session auth — `docker exec graylog-mongodb mongosh --quiet graylog --eval 'print(JSON.stringify(db.sessions.findOne({authenticated:true})))' | python3 -c "import json,sys; print(json.load(sys.stdin)['session_id'])"` — use as `Cookie: authentication=<session_id>`. Search API: GET with query/range/limit/fields params, returns CSV.
