### User
Alistair; GitHub username aawobdev; email alistair@wobdev.co.uk.
Personal projects under ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site).
Brief, direct, data-driven; prefers tables over prose. Budgets: iterative - present options, let them choose. Corrects openly; don't defend, adjust.
Comfortable with git, Docker, and system admin.
Finances (Aug 2026): Siemens £91k (~£4,775 net/mo + 10% bonus); engaged to Jamie, combined finances (Jamie on statutory pay ~£400/mo, returns to ~£55k Oct 2026). Merton, rent £2,200/mo; target £650k house by 2028. Siemens share matching buy-1-get-3-free: SMP25 vests Feb 2027, SMP26 vests Feb 2028. Side project Startline with co-founder Tim (~£1,750/mo retainer after free MVP build).
Avoids media depicting animal suffering/cruelty; prefers documentaries with justice/triumph themes and satisfying conclusions.
Media taste values rare content: 90s cartoons, obscure UK shows, niche anime, pre-2000 films.

### Projects
Homelab: Docker Compose in /opt/homelab; 8 VMs (pve, games, nas, media, ollama, services, server, pihole) with SSH host aliases.
Ollama and LM Studio both on 192.168.1.123 (ollama VM). Ollama at :11434 - query /api/tags for live model list; never rely on memory for installed models.
Media VM (192.168.1.206): Plex native (user alis719, id=1) + Jellyfin Docker. Plex DB at /var/lib/plexmediaserver/.../com.plexapp.plugins.library.db - fetch via scp then query with local sqlite3.
Sonarr v3 + Radarr on server VM. Batch-fetch Sonarr episode files via a remote Python script on the server VM (not sequential SSH curl) to avoid auth issues.
Media cleanup rule: keep S1 + current Plex season + next season, delete rest. Exceptions kept in full: Bluey, Ramsay's Kitchen Nightmares, Reacher, Sex and the City. Rick and Morty: keep only latest season.
Emma transactions Google Sheet ID 1Y75QTjUjwBMGobWpsDlE2yNoZFVeYnPNtSjpQW3k9l8 (Primary sheet); service account ~/.gdrive-mcp/amex-service-account.json; US date format (m/d/Y).
BWS vault holds: GITHUB_TOKEN (write), GITHUB_READ, UNIFI_SSH_PASSWORD, UNIFI_USERNAME=copilot (SSH root), UNIFI_PASSWORD.
Keep-in-Touch app: Flutter, ADHD/neurodivergent focus, capybara mascot Bo. Local-first, tip-jar monetisation. Google Play prep (Jul 2026).
AI Enablement business (Aug 2026): user is strategist + builder + trainer. Pricing: (1) course - fixed, per role track; (2) implementation (llm-api deploy + workflow mapping + training + 30-day warranty) - fixed; (3) MVP build - fixed, 30-day go-live, hours cap, upsell; (4) ongoing support £75–100/hr. Target: privacy-conscious SMBs.

### Conventions
Slack messages: monospace tables, emoji headers, bold *sections*, inline code for filenames.
