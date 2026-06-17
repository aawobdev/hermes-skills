# Shared Learnings

Curated durable facts useful to any AI coding agent working in Alistair's projects.
Synced across Hermes instances via this repo. Each instance merges its local memory here.

## User

- Alistair. SA dev, cancer treatment. Homelab: Proxmox + Ollama + RTX 3090 Ti. Claude Pro.
- CSS Modules, build-must-pass, no port-hopping. Function-first, polish-later.
- Terse, direct, terminal-native. Lead with answer, no choices. Wants fixes not explanations.
- One-at-a-time delegation preferred; verify each task before next.
- Cares about test coverage and seed data.
- Interested in AI features: audio/video transcription for recipe extraction (Whisper on 3090).

## Projects

- Fold It In (recipe-site): Next.js/Prisma/PG on :3000. Docker PG on :5432. Instagram scraping via page HTML OG meta-tags. Apify fallback needs IG creds. AI extract chain: /api/v1/ai/extract-instagram + /api/v1/ai/extract-recipe.
- Crawford Measure: Next.js/Prisma on :5000. SA tax brackets (year 2027, rebate R17,820, conv rate 4.5%). Auth.js v5 — `next start` needs AUTH_TRUST_HOST; `npm run dev` works fine. Deployed to crawford.citium.space via PVE LXC 131.
- Life Tracker: Expo SDK 54, port 8089. Personal health tracking (cancer/chemo/surgery). Privacy paramount. EAS: aacodemode/life-tracker. AI: OpenRouter deepseek-v4-flash.
- CarSync: Android native, WSL. JDK 17 (~/jdk17), Android SDK (~/Android/sdk). Phone: Samsung SM_S921B, 192.168.1.243, adb wireless. Onboarding crash on "Get Started" — need crash logs.
- Homelab: Docker Compose across Proxmox VMs. Repo at ~/projects/homelab (WSL) / /opt/homelab (VMs). Infra reference: AGENTS.md in repo. Delegation: hermes -z (qwen3-coder:30b routine), claude -p (CC-class).

## Conventions

- AGENTS.md is canonical for all repos. Agent-specific files (CLAUDE.md, .cursorrules, copilot-instructions.md, opencode.json) are one-line pointers — not verbose stubs.
- WSL dev servers: recipe-site :3000, crawford-measure :5000. Node v24 via nvm.
- Resend: verified domain folditin.co.uk, shared across projects. FROM: 'Project Name <noreply@folditin.co.uk>'. Env var: AUTH_RESEND_KEY or RESEND_API_KEY.
- Auth.js v5: dev mode (npm run dev) works fine, production (next start) needs AUTH_TRUST_HOST. Port confusion causes false negatives — check actual port.
- Hermes skills repo: ~/projects/hermes-skills (WSL + ollama VM). VM config skills.external_dirs → ~/projects/hermes-skills/skills.
