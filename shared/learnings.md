# Shared Learnings

Curated durable facts useful to any AI coding agent working in Alistair's projects.

## User

- Alistair. SA dev. Homelab: 8 Proxmox VMs (pve, games, nas, media, ollama, services, server, pihole). Docker Compose in /opt/homelab.
- GitHub: aawobdev. All git repos use SSH remotes (git@github.com:aawobdev/*.git) — HTTPS fails (no credential helper). Personal projects under ~/projects/.
- Comfortable with git, Docker, system administration.
- Terse, direct, terminal-native. Lead with answer, no choices. Wants fixes not explanations.
- Prefers Slack-friendly formatting for automated reports: emoji status indicators in headers, bold section headers, bullet lists, inline code, compact, under 6 lines when nothing changed.
- Cares about test coverage and seed data. CSS Modules, build-must-pass, no port-hopping. Function-first, polish-later.
- Local LLMs on ollama VM (192.168.1.123): Ollama + LM Studio ("custom" provider). Live model list at http://192.168.1.123:11434/api/tags. Local: qwen3-coder:30b (primary, MoE), gpt-oss:20b (MoE, MXFP4), devstral:24b (agentic, vision), gemma4:26b (vision, MoE), phi4:14b (STEM/math), deepseek-r1:8b (fast reasoning). Cloud (OpenRouter): deepseek-v4-flash (default), qwen3-coder-next, devstral-small-2, gemma3, qwen3.5 (397B-A17B, vision).
- Interested in AI features: audio/video transcription for recipe extraction (Whisper on 3090).

## Projects

- Fold It In (recipe-site): Next.js/Prisma/PG on :3000. Docker PG on :5432. Instagram scraping via page HTML OG meta-tags. Apify fallback needs IG creds. AI extract chain: /api/v1/ai/extract-instagram + /api/v1/ai/extract-recipe.
- Crawford Measure: Next.js/Prisma on :5000. SA tax brackets (year 2027, rebate R17,820, conv rate 4.5%). Auth.js v5 — production `next start` needs AUTH_TRUST_HOST env var. Deployed to crawford.citium.space via PVE LXC 131.
- Life Tracker: Expo SDK 54, port 8089. Personal health tracking (cancer/chemo/surgery). Privacy paramount. EAS: aacodemode/life-tracker. AI: OpenRouter deepseek-v4-flash.
- CarSync: Android native, WSL. JDK 17 (~/jdk17), Android SDK (~/Android/sdk). Phone: Samsung SM_S921B, 192.168.1.243, adb wireless. Onboarding crash on "Get Started" — need crash logs.
- Homelab: Docker Compose across Proxmox VMs. Repo at ~/projects/homelab (WSL) / /opt/homelab (VMs). Infra reference: AGENTS.md in repo.

## Conventions

- AGENTS.md is canonical for all repos. Agent-specific files (CLAUDE.md, .cursorrules, copilot-instructions.md, opencode.json) are one-line pointers — not verbose stubs.
- WSL dev servers: recipe-site :3000, crawford-measure :5000. Node v24 via nvm.
- Resend: verified domain folditin.co.uk, shared across projects. FROM: 'Project Name <noreply@folditin.co.uk>'. Env var: AUTH_RESEND_KEY or RESEND_API_KEY.
- Auth.js v5: dev mode (`npm run dev`) works fine, production (`next start`) needs `AUTH_TRUST_HOST`. Port confusion causes false negatives — check actual port.
