### User
Alistair - Siemens £91k (~£4,775 net/mo) +10% bonus; engaged to Jamie (medical ~£400/mo, full £55k Oct 2026); Merton rent £2,200; target £650k house 2028; SMP25/SMP26 shares vest Feb27/Feb28; Startline w/ Tim ~£1,750/mo.
Finance tracked in Emma (Monzo, Barclays, BA Amex, PayPal, Lloyds). Notes: P=budget, "P Taken from Rainy"=Rainy fund, K=pending, "NOT PAID AMEX YET"=unsettled. Rainy Day Saver: Barclays savings→current→Amex; Rainy covers Deliveroo, Uber Eats, B&Q, attractions, hotels.
AI Enablement business: strategist+builder+trainer; tiers: Course (fixed, per-role), Implementation (fixed, scoped), MVP Build (fixed, 30-day, with client's vibe coder), Support £75-100/hr; targets privacy-conscious SMBs.
Personal projects under ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site, lifetap).
Media taste: rare 90s cartoons, obscure UK shows, niche anime, pre-2000 films; avoids animal-suffering content; prefers justice/triumph documentaries.

### Projects
Project hub ~/projects/.hub/ (git@github.com:aawobdev/project-hub): 20 projects, catalog.yaml; dashboard uses data.js for file:// CORS, or python3 serve.py :8080; click tasks to complete/block/comment/create. Kanban board 'projects' at ~/.hermes/kanban/boards/projects/; scripts: scan-projects.sh, claude-lane.sh <task-id> (claude -p, Max sub), kanban-snapshot.sh (30m cron).
Claude Code v2.1.220 + Max authed on ollama VM.
Ollama at 192.168.1.123:11434 - query /api/tags for live model list; never rely on memory.
Media VM 192.168.1.206: Plex native (user alis719; Preferences.xml plex:plex 0600, root-only) + Jellyfin Docker; 540GB/17.5k-track music at /pool/Music; Sonarr+Radarr on server VM. Jellyfin API keys via DB insert into ApiKeys table; auth header X-MediaBrowser-Token. Lidarr API key is literally "CHANGE_ME" and works - not unconfigured.
Emma transactions Google Sheet 1Y75QTjUjwBMGobWpsDlE2yNoZFVeYnPNtSjpQW3k9l8 (Primary sheet, US m/d/Y dates); service account ~/.gdrive-mcp/amex-service-account.json.
Amex cron ~/.hermes/scripts/amex-subset-sum.py daily 08:05: PAYMENT RECEIVED=card funding (excluded from matching), other positives=refunds (negative offsets); "NOT PAID AMEX YET" auto-pending; gap analysis flags P-marked-but-unpaid items.
Flutter SDK 3.27.4 at ~/flutter (in .bashrc PATH). LifeTap MTG app ~/projects/lifetap - user builds, Dom publishes.
BWS vault: UNIFI_SSH_PASSWORD, UNIFI_USERNAME=copilot (SSH root), UNIFI_PASSWORD.

### Conventions
Brief, direct, data-driven; tables > prose; budgets iterative - present options, user picks. Slack-compatible output: code-block tables, monospace, emoji headers, bold *sections*, actionable lists. On correction: adjust, don't defend.
Media cleanup: keep S1 + current Plex season + next; delete rest. Full-keep exceptions: Bluey, Ramsay's Kitchen Nightmares, Reacher, Sex and the City. Rick and Morty: latest season only.
