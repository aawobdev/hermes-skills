### User
Named Alistair. Runs a homelab with Docker Compose in /opt/homelab (8 VMs: pve, games, nas, media, ollama, services, server, pihole) with SSH host aliases.
Technically competent - git, Docker, SSH, self-hosting.
Prefers brief direct commands with no explanations or asking permission - try things yourself first, only ask as last resort.
Prefers Slack-friendly formatting for cron/automated reports: emoji status indicators (✅⚠️❌) in headers, bold for section headers (no markdown headers), bullet lists not paragraphs, sections 2-4 lines, inline code for names, compact inline commit links, reports under 6 lines when nothing changed.
Responds well to actionable follow-up suggestions - prefer offering concrete next steps over just answering.
GitHub username: aawobdev. Google accounts: al.ouma666@gmail.com, alistair@wobdev.co.uk.
Uses Bitwarden Secrets Manager (BWS) for credentials. UDM/Unifi SSH: BWS keys UNIFI_SSH_PASSWORD and UNIFI_USERNAME (value "copilot", but actual SSH user is root); UNIFI_PASSWORD for controller web UI.

### Projects
Personal projects live under ~/projects/ (e.g. hermes-skills, car-sync, life-tracker, recipe-site), auto-synced via repo-sync cron job.
Ollama and LM Studio both run on 192.168.1.123 (ollama VM). Ollama API at 192.168.1.123:11434 - query /api/tags for live installed-model list; never rely on memory for installed models.
Graylog on services VM (192.168.1.124:9009): MongoDB session auth - `docker exec graylog-mongodb mongosh --quiet graylog --eval 'print(JSON.stringify(db.sessions.findOne({authenticated:true})))'` then extract session_id; use as Cookie `authentication=<session_id>`. Search API uses GET with query/range/limit/fields, returns CSV.
Google Drive MCP server at ~/.hermes/scripts/gdrive-mcp-server.py uses service account amex-reconcile@hermes-499012.iam.gserviceaccount.com, key at ~/.gdrive-mcp/amex-service-account.json. Tools: list/search/read/get_file/move/create_folder/copy/trash. Service-account auth, no token expiry. Registered in both Hermes config (venv Python path to avoid ModuleNotFoundError) and Claude Code.
Amex-reconcile: reads Emma auto-export Google Sheet (gid=1) via the service account; 90-day rolling window including today; subset-sum DP matching. Marks paid only when Notes field starts with capital "P" - ignore Tags column. Slack output uses code-block tables (Date/Amount/Category/Merchant) with uppercase shortened merchants (M&S, BA, DELIVEROO). Cron defined in config.yaml, not the cron directory.
memory-sync cron (every 2h) syncs MEMORY.md → hermes-skills/shared/learnings.md via ~/.hermes/scripts/sync-memory.sh using `claude -p` (Opus 4.8) to avoid hermes -z Bitwarden startup overhead.
model-lineup cron (3AM daily) uses qwen3-coder:30b via Ollama.
Plex library shared only with UK and South Africa users.

### Conventions
Strip em dashes from curated/automated output (repo convention).
Personal projects kept consistent across machines (ollama server + laptop): same MCP serv
