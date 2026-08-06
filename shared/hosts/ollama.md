### User
Alistair (GitHub: aawobdev). Personal projects under ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site).
Style: brief, direct, data-driven. Tables > prose. For budgets/decisions, present options and let them choose. Corrects openly - don't defend, adjust.
Slack formatting: monospace tables, emoji headers, bold *sections*, inline code for filenames.
Comfortable with git, Docker, system admin.
Finances: Siemens £91k (~£4,775 net/mo + 10% bonus). Engaged to Jamie (combined finances; Jamie on statutory pay ~£400/mo, returns to ~£55k Oct 2026). Rent £2,200 (Merton). Target: £650k house by 2028. Siemens share matching buy-1-get-3: SMP25 vests Feb 2027, SMP26 Feb 2028.
Media taste: rare 90s cartoons, obscure UK shows, niche anime, pre-2000 films. Avoids media depicting animal suffering/cruelty; prefers documentaries with justice/triumph endings.

### Projects
Homelab: Docker Compose in /opt/homelab; 8 VMs (pve, games, nas, media, ollama, services, server, pihole); SSH host aliases configured.
Ollama VM (192.168.1.123): Ollama on :11434 and LM Studio both here. Query /api/tags for live model list - never rely on memory for installed models. Claude Code (Max plan) authed here.
Project hub ~/projects/.hub/: git repo ignoring project dirs; dashboard uses data.js for file:// CORS. Kanban board 'projects' at ~/.hermes/kanban/boards/projects/; scripts scan-projects.sh, claude-lane.sh <task-id>, kanban-snapshot.sh (cron 30m).
Media VM (192.168.1.206): Plex native + Jellyfin Docker. Music lib 540GB / 17.5k tracks at /pool/Music. Plex Preferences.xml is plex:plex 0600 - needs root. Plex DB under /var/lib/plexmediaserver, user alis719.
Sonarr + Radarr on server VM.
Jellyfin API: create keys via DB insert into ApiKeys table; auth with X-MediaBrowser-Token header.
Lidarr API key is literally "CHANGE_ME" and works as-is - don't assume it's unconfigured.
Media cleanup: keep S1 + current Plex season + next; delete rest. Keep fully: Bluey, Ramsay's Kitchen Nightmares, Reacher, Sex and the City. Rick and Morty: latest season only.
Emma transactions Sheet ID 1Y75QTjUjwBMGobWpsDlE2yNoZFVeYnPNtSjpQW3k9l8 (Primary). Service account ~/.gdrive-mcp/amex-service-account.json. US dates (m/d/Y).
Amex cron ~/.hermes/scripts/amex-subset-sum.py (daily 08:05): PAYMENT RECEIVED = card funding (excluded from matching); other credits = refunds (negative offsets). "NOT PAID AMEX YET" notes auto-pending; gap analysis flags P-marked but unpaid items.
Keep-in-Touch app: Flutter, ADHD/neurodivergent focus, capybara mascot Bo. Local-first, tip-jar monetisation. Google Play prep since Jul 2026.
Startline: side project with co-founder Tim; contracting ~£1,750/mo retainer after free MVP build.
AI Enablement business (Aug 2026): fixed-price course (per role), implementation, MVP build (30-day, built with client's vibe coder); support £75-100/hr. Target: privacy-conscious SMBs.
BWS vault secrets: UNIFI_SSH_PASSWORD, UNIFI_USERNAME=copilot (SSH root), UNIFI_PASSWORD.
