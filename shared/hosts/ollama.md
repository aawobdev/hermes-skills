### User
Alistair - Siemens £91k + 10% bonus; Startline Ltd side business w/ Tim (~£1,750/mo). Engaged to Jamie. Merton, rent £2,200/mo; target £650k house 2028.
Style: brief, direct, data-driven; tables > prose; present budget options iteratively. Slack-friendly output: code-block tables, monospace, emoji headers, *bold* sections, actionable lists. Corrects openly - adjust, don't defend.
Personal projects under ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site, lifetap).
Finance via Emma (Monzo, Barclays, BA Amex, PayPal, Lloyds). Note codes: P=budget, "P Taken from Rainy"=Rainy fund, K=pending, "NOT PAID AMEX YET"=unsettled. Rainy fund covers Deliveroo/Uber Eats/B&Q/attractions/hotels.
Media taste: rare 90s cartoons, obscure UK shows, niche anime, pre-2000 films. Avoids media depicting animal suffering; prefers justice/triumph documentaries.
AI Enablement business: strategist+builder+trainer; 4 tiers (Course fixed per-role, Implementation fixed, MVP Build fixed 30-day, Support £75-100/hr); target privacy-conscious SMBs.

### Projects
Ollama: 192.168.1.123:11434 - query /api/tags for live model list; never rely on memory.
Media VM 192.168.1.206: Plex native (user alis719) + Jellyfin Docker. Music lib 540GB/17.5k tracks at /pool/Music. Plex Preferences.xml owned plex:plex 0600 - root only.
Jellyfin: create API keys via DB insert into ApiKeys table; auth header X-MediaBrowser-Token.
Lidarr API key is literally "CHANGE_ME" and works - never assume unconfigured.
Sonarr + Radarr run on server VM.
Emma transactions Google Sheet ID 1Y75QTjUjwBMGobWpsDlE2yNoZFVeYnPNtSjpQW3k9l8 (Primary sheet); service account ~/.gdrive-mcp/amex-service-account.json; US date format (m/d/Y).
Amex cron: ~/.hermes/scripts/amex-subset-sum.py daily 08:05. PAYMENT RECEIVED = card funding (excluded from matching); other positives = refunds (negative offsets in subset-sum).
Project hub: ~/projects/.hub (git@github.com:aawobdev/project-hub); catalog.yaml + dashboard (python3 serve.py :8080); 22 projects; kanban snapshot cron 30min. Slack routing: add slack_channel to catalog.yaml, run generate-slack-config.py, add config.yaml channel_skill_binding.
Flutter SDK at ~/flutter (in .bashrc PATH). LifeTap MTG app at ~/projects/lifetap, Slack C0BNGLN33GD.
Startline Ltd Slack channel: C0BNK0V0RRU.
BWS vault: UNIFI_SSH_PASSWORD, UNIFI_USERNAME=copilot (SSH root), UNIFI_PASSWORD.

### Conventions
Media cleanup: keep S1 + current Plex season + next season, delete rest. Exceptions kept whole: Bluey, Ramsay's Kitchen Nightmares, Reacher, Sex and the City. Rick and Morty: latest season only.
