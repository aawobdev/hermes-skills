### User
- Alistair, UK-based; GitHub: aawobdev; Google account: al.ouma666@gmail.com.
- Competent with git/Docker/SSH/system admin. Prefers brief direct commands - try first, ask as last resort.
- Personal projects under ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site).
- Runs Hermes on multiple machines (ollama server + laptop); wants consistent MCP server, skill, and cron setup across instances.
- Avoids media depicting animal suffering/cruelty; prefers documentaries with justice/triumph themes and satisfying conclusions.

### Projects
- Homelab: Docker Compose in /opt/homelab; 8 VMs (pve, games, nas, media, ollama, services, server, pihole); SSH host aliases configured.
- Ollama and LM Studio both on 192.168.1.123 (ollama VM). Ollama at :11434 - query /api/tags for live model list; never rely on memory for installed models.
- Jellyfin on media VM (Docker): DB at /config/data/data/jellyfin.db (BaseItems table); 5 libraries; YouTube library lacks CollectionType.
- Keep in Touch: Flutter app (uk.co.wobdev.keep_in_touch), ADHD/neurodivergent focus, capybara mascot Bo. Local-first (Drift/SQLite), privacy-centric, tip-jar monetisation. Play Store prep (July 2026): V2-2 auto-detect stripped for Play Store; full version via Obtainium.
- AMEX subset-sum: ~/.hermes/scripts/amex-subset-sum.py, target from amex-target.txt. "P" notes = paid/excluded, "K" notes = keep pending. Service account ~/.gdrive-mcp/amex-service-account.json. Daily 08:05 cron to Slack (no_agent). Recency-ranked multi-solution DP; output single solution with budget/off-budget/pending tables.
- Cron jobs on this machine: model-lineup (3AM daily, qwen3-coder:30b via Ollama); memory-sync (every 2h, MEMORY.md → hermes-skills/shared/learnings.md, script ~/.hermes/scripts/sync-memory.sh, uses claude -p to avoid Bitwarden startup overhead).
- Home Assistant: HASS_TOKEN in BWS, not .env. Gateway restart needs separate SSH (sudo systemctl restart hermes-gateway.service) - blocked from within gateway. Entity registry ops need WebSocket API (pip websocket-client).

### Conventions
- Credentials in Bitwarden Secrets Manager (BWS). Real binary at ~/.hermes/bin/bws - pip `bws` is a different project; use full path. BWS_ACCESS_TOKEN from ~/.hermes/.env.
- UniFi: UDM SSH creds in BWS (UNIFI_SSH_PASSWORD, UNIFI_USERNAME - SSH user is actually root); UNIFI_PASSWORD is for controller web UI.
- Cron jobs: prefer no_agent mode - clean script stdout, scripts in ~/.hermes/scripts/, must exit 0 (non-zero suppresses delivery).
- Slack formatting: emoji headers, bold *text* sections, data tables as monospace code blocks with aligned columns (no markdown tables), inline code for filenames/commands.
