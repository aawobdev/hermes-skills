# Shared Learnings

Curated durable facts useful to any AI coding agent working in Alistair's projects.

## User

- Alistair. SA dev. Homelab: 8 Proxmox VMs, Docker Compose in /opt/homelab, SSH host aliases. Comfortable with git, Docker, system admin.
- GitHub: aawobdev. SSH remotes (git@github.com:aawobdev/*.git). Projects under ~/projects/.
- Google account: al.ouma666@gmail.com.
- Terse, direct, terminal-native. Automated reports: emoji status in headers, bold section headers, bullet lists, inline code, compact, under 6 lines when nothing changed.
- Infrastructure spans ollama server + laptop. Prefers consistent tooling setup across all instances.
- Local LLMs on ollama VM (192.168.1.123): Ollama and LM Studio both local. Live model list at http://192.168.1.123:11434/api/tags — always query rather than caching. Local: qwen3-coder:30b, gpt-oss:20b, devstral:24b, gemma4:26b, phi4:14b, deepseek-r1:8b. Cloud (OpenRouter): deepseek-v4-flash (default), qwen3-coder-next, devstral-small-2, gemma3, qwen3.5. qwen3-coder:30b preferred for agent work (faster MoE).
- Interested in AI features: audio/video transcription for recipe extraction (Whisper on 3090).
- Google Drive/Sheets accessible via service account amex-reconcile@hermes-499012.iam.gserviceaccount.com, key at ~/.gdrive-mcp/amex-service-account.json. Service account = no token expiry. Share Drive files/folders with this account for agent access. Python FastMCP server at ~/.hermes/scripts/gdrive-mcp-server.py — tools for list, search, read, upload, move, copy, trash, create folders. Also registered in ~/.claude.json for cross-agent availability.

## Projects

- Fold It In (recipe-site): Next.js/Prisma/PG on :3000. Docker PG on :5432. Instagram scraping via page HTML OG meta-tags. Apify fallback needs IG creds. AI extract chain: /api/v1/ai/extract-instagram + /api/v1/ai/extract-recipe.
- Crawford Measure: Next.js/Prisma on :5000. SA tax brackets (year 2027, rebate R17,820, conv rate 4.5%). Auth.js v5 — production next start needs AUTH_TRUST_HOST env var. Deployed to crawford.citium.space via PVE LXC 131.
- Life Tracker: Expo SDK 54, port 8089. Personal health tracking (cancer/chemo/surgery). Privacy paramount. EAS: aacodemode/life-tracker. AI: OpenRouter deepseek-v4-flash.
- CarSync: Android native, WSL. JDK 17 (~/jdk17), Android SDK (~/Android/sdk). Phone: Samsung SM_S921B, 192.168.1.243, adb wireless.
- hermes-skills: AI agent skill collection at ~/projects/hermes-skills/.
- Homelab: Docker Compose across Proxmox VMs. Repo at ~/projects/homelab (WSL) / /opt/homelab (VMs). Infra reference: AGENTS.md in repo.
- Amex reconciliation: reads credit card statements via Google Sheets service account.
- Projects under ~/projects/ auto-synced across machines.

## Conventions

- AGENTS.md is canonical for all repos. Agent-specific files (CLAUDE.md, .cursorrules, copilot-instructions.md, opencode.json) are one-line pointers — not verbose stubs.
- WSL dev servers: recipe-site :3000, crawford-measure 
