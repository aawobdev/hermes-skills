## User

- **Name**: Alistair
- **GitHub**: aawobdev
- **Google account**: al.ouma666@gmail.com
- **Credentials storage**: Bitwarden Secrets Manager (BWS)
- **Preferences**: Direct commands, minimal explanation; try things first, ask only as last resort
- **Communication style**: Slack-friendly — emoji status (✅⚠️❌), bold headers, bullet lists, compact sections (2-4 lines), inline code for names; keep reports under 6 lines if nothing changed
- **Project locations**: ~/projects/ (hermes-skills, car-sync, life-tracker, recipe-site)
- **Engagement**: Responds well to actionable follow-up suggestions; prefer concrete next steps over just answering the question

## Projects & Environment

- **Homelab**: Docker Compose in /opt/homelab with 8 VMs (pve, games, nas, media, ollama, services, server, pihole); SSH host aliases configured
- **Ollama**: 192.168.1.123:11434 — **always query /api/tags for live model list; never assume models from memory**
- **LM Studio**: Also at 192.168.1.123
- **Google Drive MCP**: Service account `amex-reconcile@hermes-499012.iam.gserviceaccount.com`, key at `~/.gdrive-mcp/amex-service-account.json`; tools: list/search/read/get_file/move/create_folder/copy/trash
- **Graylog**: 192.168.1.124:9009 (services VM), requires MongoDB session auth
- **Plex**: Library shared only with UK and South Africa users
- **Multiple machines**: Runs on ollama server + laptop; prefers consistent MCP setup across instances

## Conventions

- Never rely on memory for Ollama installed models — query `/api/tags` endpoint to confirm
- Offer actionable follow-ups and concrete next steps, not just answers to questions
- Technically competent with git, Docker, SSH, self-hosting — skip basic explanations
