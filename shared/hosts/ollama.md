### User
Alistair - brief, direct, data-driven; tables > prose; Slack-compatible output (code-block tables, monospace, emoji headers, bold *sections*, actionable lists).
Iterative budgeting: present options, let him choose. Corrects openly - don't defend, adjust.
Wants interim check-ins during long tasks; investigative silence feels unresponsive.
Finances: Siemens £91k+10% bonus; Startline w/ Tim ~£1,750/mo; Merton rent £2,200; Jamie's cancer ~£400/mo (full £55k Oct 2026). Accounts: Monzo, Barclays, BA Amex; Rainy Day Saver = Barclays savings→current→Amex.
Emma transactions Google Sheet ID 1Y75QTjUjwBMGobWpsDlE2yNoZFVeYnPNtSjpQW3k9l8 (Primary sheet, US m/d/Y dates); service account ~/.gdrive-mcp/amex-service-account.json.
Media taste: rare 90s cartoons, obscure UK shows, niche anime, pre-2000 films. Avoids animal suffering/cruelty; prefers justice/triumph documentaries.

### Projects
Personal projects under ~/projects/. Project hub ~/projects/.hub/ with catalog.yaml + kanban board 'projects'; Slack routing via catalog.yaml → generate-slack-config.py.
Hardware: 192.168.1.153 (this host, Quadro P2000 5GB, Docker); 192.168.1.123 GPU inference (3090 Ti, Ollama); 192.168.1.206 media VM; 192.168.1.124 services.
Ollama at 192.168.1.123:11434 - query /api/tags for live model list; never rely on memory for installed models.
Media VM 192.168.1.206: Plex + Jellyfin Docker, 540GB music lib. Plex prefs 0600 root-only; Plex DB /var/lib/plexmediaserver, user alis719. Sonarr+Radarr on server VM.
Jellyfin API keys: create via DB insert into ApiKeys table; auth header X-MediaBrowser-Token.
Lidarr API key is literally "CHANGE_ME" and works as-is - not unconfigured.
Amex subset-sum cron: ~/.hermes/scripts/amex-subset-sum.py, daily 08:05.
AI Enablement business: strategist+builder+trainer; tiers: Course (fixed/role), Implementation (fixed scoped), MVP Build (fixed 30d w/ client's vibe coder), Support £75-100/hr. Target: privacy-conscious SMBs.
Customer tiers (Budget×Privacy): T1 Budget Cloud £500+£50/mo; T2 Budget Private Docker/Ollama £750+£75/mo; T3 Premium Cloud £1500+£150/mo; T4 Premium Private GPU+32B local £3000+£250/mo.
Productising isolated Hermes profiles as managed SMB AI service; LifeTap (client Dom, free) is isolation test case: ~/.hermes/profiles/lifetap/, Docker, local Qwen 32B via llm-api proxy. Docs: hub docs/multi-profile-architecture.md.
APK publishing: apk.citium.space = dufs container on 192.168.1.124, data /opt/homelab/opt/data/apk-repo/ (subdir per project), Cloudflare tunnel; SCP file → live immediately, no restart.
BWS vault holds UNIFI_SSH_PASSWORD, UNIFI_USERNAME=copilot (SSH root), UNIFI_PASSWORD.

### Conventions
Budget notes: P=budget, K=pending, "NOT PAID AMEX YET"=unsettled/auto-pending. Amex positives: "PAYMENT RECEIVED"=funding (excluded); other positives=refunds (negative offsets).
Local model calls go direct to Ollama :11434.
