### User
Alistair. South African developer, undergoing cancer treatment (chemo/surgery). Claude Pro subscriber.
Terse, direct, terminal-native. Lead with the answer, no menus of choices. Wants fixes, not explanations.
Swearing means stop and fix fast. Don't debate fault — verify scope first, report pre-existing issues.
Visually oriented: proactively spot design issues. Clean/minimalist taste — muted palette, tight spacing.
Function-first, polish-later. One task at a time; verify each before starting the next.
Cares about test coverage and seed data. Frustrated by persistent config/auth errors that block testing.
Homelab: Proxmox + Ollama + RTX 3090 Ti. Interested in AI features — e.g. Whisper transcription on the 3090 to extract recipes from Instagram Reels.

### Projects
Fold It In (recipe-site): Next.js/Prisma/Postgres, dev on :3000.
Crawford Measure (crawford-measure): SA tax tool, dev on :5000, deployed to crawford.citium.space (PVE LXC 131, rsync + docker compose rebuild + seed). Seed uses 2026/2027 tax brackets (year 2027, rebate R17,820, adequacy conversion rate 4.5%). Auth.js on Node v24 ESM: `next start` needs AUTH_TRUST_HOST set in env; `npm run dev` (Turbopack) auto-trusts host.
Life Tracker (life-tracker): Expo SDK 54, personal health tracking (cancer/chemo/surgery) — symptoms, food triggers, side effects, peri-event nutrition. Privacy paramount. Port 8089, never hop. 3 tabs (Home/Insights/More). Edit mode on all log screens via ?id param. SeveritySlider uses PanResponder + haptics. Timeline refreshes on focus (useFocusEffect). EAS: aacodemode/life-tracker. AI via OpenRouter deepseek-v4-flash.
gdrive-organisation: Python, OAuth to Google Drive. ~118K items / 378GB. inventory_parallel.py (10 threads). generate_mapping.py is folder-first, 100% mapping. Person split: 01-personal (Alistair), 05-family/jamie (Jamie); Emma transactions → 02-finance/budget.
CarSync (car-sync): WSL Android toolchain works. Test device Samsung SM-S921B at 192.168.1.243 via adb wireless. Known issue: onboarding crash after "Get Started".
Resend: verified domain folditin.co.uk, shared across recipe-site and crawford-measure. FROM format `Project Name <noreply@folditin.co.uk>`. Env var AUTH_RESEND_KEY or RESEND_API_KEY.
WSL dev: Node v24 via nvm, npm. recipe-site :3000, crawford-measure :5000.

### Conventions
One task at a time. Never port-hop — each project has a fixed port.
Build must pass. CSS Modules for styling.
AGENTS.md is canonical for every repo; other agent files (CLAUDE.md etc.) are one-line pointers to it. Shared infra notes in ~/projects/homelab/AGENTS.md.
Folder names: lowercase-hyphenated. No PascalCase, underscores, or spaces.
For visual inspection of deployed sites use browser_navigate + browser_vision — not curl/grep.
