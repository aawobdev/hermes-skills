# Cross-Machine Memory Sync

Share Hermes learnings across multiple machines and with Claude Code via a shared git repo
+ LLM-curated cron. Each Hermes instance has its own local memory; this pattern converges
them into a single curated file any agent can read.

## Architecture

```
hermes-skills repo (git)          ← transport layer (already cloned everywhere)
├── shared/learnings.md           ← curated durable facts, useful to any agent
└── scripts/sync-memory.sh        ← cron: git pull → read local memory → LLM curate → commit + push
```

Each Hermes instance runs `sync-memory.sh` as a `--no-agent` cron job. Claude Code reads
`learnings.md` via a pointer in `~/.claude/CLAUDE.md`.

## How it works

1. Each Hermes instance runs `sync-memory.sh` as a `--no-agent` cron job (every 2h)
2. Script does `git pull`, reads local `~/.hermes/memories/MEMORY.md` + `USER.md`
3. Calls `hermes -z` with a curation prompt — LLM merges durable facts into `learnings.md`,
   drops Hermes-specific operational details and stale session state
4. Commits + pushes if content changed
5. Claude Code reads `learnings.md` via a pointer in `~/.claude/CLAUDE.md`

## Why `--no-agent` cron + script (not LLM-driven cron)

The script IS the job. The only LLM call is the `hermes -z` curation inside the script.
An LLM-driven cron that just runs the script would double the token cost for no benefit —
the outer LLM call would just be "run this script and report output" which is pure waste.

## Script location pitfall

Must be copied to `~/.hermes/scripts/` — **not symlinked**. The cron path resolver rejects
symlinks that traverse outside the scripts dir. Re-copy after updating the script in the repo:

```bash
cp ~/projects/hermes-skills/scripts/sync-memory.sh ~/.hermes/scripts/sync-memory.sh
```

## Curation prompt rules (embedded in script)

- Max 2500 chars, one fact per line, grouped by User/Projects/Conventions
- Keep only durable facts useful to ANY agent (ports, known issues, conventions, preferences)
- Drop Hermes-specific details (delegation syntax, tool quirks)
- Drop task progress, commit SHAs, PR numbers — anything stale in a week
- Don't remove existing facts unless clearly contradicted

## Collision avoidance

Stagger cron times by a few minutes across machines. If git push fails (conflict), the
script commits locally and retries next run — non-critical.

## Slack delivery

Set cron `deliver` to `slack:<channel_id>` so sync outcomes appear in the team channel.
The `--no-agent` pattern delivers script stdout as the message — non-empty stdout = message,
empty stdout = silent. The script always echoes a status line, so you get a message every run.

## Setting up on a new Hermes instance

1. Ensure `~/projects/hermes-skills` is cloned and up to date
2. Copy the script: `cp ~/projects/hermes-skills/scripts/sync-memory.sh ~/.hermes/scripts/`
3. Create the cron job:
   ```
   hermes cron create --name memory-sync --no-agent --script sync-memory.sh "every 2h"
   ```
4. Set delivery to Slack: `hermes cron edit --deliver "slack:<channel_id>" memory-sync`
5. Verify on next tick: check `shared/learnings.md` in the repo for a commit from this host

## Claude Code pointer

Add to `~/.claude/CLAUDE.md`:

```
For cross-project learnings (project ports, known issues, conventions, user preferences),
read `~/projects/hermes-skills/shared/learnings.md` — synced from Hermes memory across machines.
```
