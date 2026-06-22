# Cross-Machine Memory Sync

Share Hermes learnings across multiple machines and with Claude Code via a shared git repo
plus an LLM-curated cron. Each Hermes instance has its own local memory; this pattern
collects every machine's durable facts into a single file any agent can read, without the
machines clobbering each other.

## Architecture

```
hermes-skills repo (git)          # transport layer (already cloned everywhere)
├── shared/hosts/<host>.md        # per-machine curated facts (each host owns exactly one)
├── shared/learnings.md           # AUTO-GENERATED: concatenation of all host files
└── scripts/sync-memory.sh        # cron: curate this host -> regenerate combined -> push
```

Each Hermes instance runs `sync-memory.sh` as a `--no-agent` cron job. Agents (and Claude
Code) read the combined `shared/learnings.md`; it is regenerated, never hand-edited.

## Why per-host files (the important bit)

A Hermes instance can only read its OWN `~/.hermes/memories/MEMORY.md`. The earlier design
had every host LLM-curate its own memory into the SAME `shared/learnings.md`, so each run
overwrote the other machines' facts. The result was constant churn (a commit every run),
push conflicts, and silent loss of whichever host pushed first.

Now each host writes only `shared/hosts/<host>.md`. The combined `learnings.md` is rebuilt by
deterministically concatenating every host file (sorted), so the output is identical no
matter which host builds it. Hosts edit disjoint files, so rebases never conflict and the
combined file converges instead of churning.

## How it works

1. Each Hermes instance runs `sync-memory.sh` as a `--no-agent` cron job (every 2h).
2. Script rebases onto the remote (`--autostash`, self-healing).
3. Hash guard: if this host's `MEMORY.md` + `USER.md` are unchanged since the last run,
   curation is skipped entirely (no LLM call, no commit). A stable machine is silent.
4. Otherwise it curates this host's memory into `shared/hosts/<host>.md` via `claude -p`
   (falls back to `hermes -z` if `claude` is absent; override with `MEMORY_SYNC_CURATOR`).
5. Regenerates `shared/learnings.md` from all `shared/hosts/*.md`.
6. Commits if anything changed, then pushes (rebase + one retry on contention).

The host hash marker lives outside the repo at `~/.hermes/cache/memory-sync-<host>.sha`.

## Why `--no-agent` cron + script (not LLM-driven cron)

The script IS the job. The only LLM call is the curation step inside the script. An
LLM-driven cron that just runs the script would double the token cost for no benefit.

## Script location pitfall

Must be copied to `~/.hermes/scripts/`, not symlinked. The cron path resolver rejects
symlinks that traverse outside the scripts dir. Re-copy after updating the script in the repo:

```bash
cp ~/projects/hermes-skills/scripts/sync-memory.sh ~/.hermes/scripts/sync-memory.sh
```

## Curation prompt rules (embedded in script)

- Max 2500 chars, one fact per line, grouped under `### User`, `### Projects`, `### Conventions`.
- Keep only durable facts useful to ANY agent (ports, known issues, conventions, preferences).
- Drop Hermes-specific details (delegation syntax, tool quirks).
- Drop task progress, commit SHAs, PR numbers, anything stale in a week.
- Do not remove existing facts unless clearly contradicted.
- Em dashes are stripped from curated output (repo convention: no em dashes in notes/docs).

## Setting up on a new Hermes instance

1. Ensure `~/projects/hermes-skills` is cloned and up to date.
2. Copy the script: `cp ~/projects/hermes-skills/scripts/sync-memory.sh ~/.hermes/scripts/`
3. Create the cron job:
   ```
   hermes cron create --name memory-sync --no-agent --script sync-memory.sh "every 2h"
   ```
4. Set delivery to Slack: `hermes cron edit --deliver "slack:<channel_id>" memory-sync`
5. Run once to seed: `bash ~/.hermes/scripts/sync-memory.sh`. Verify a `shared/hosts/<host>.md`
   appears and `learnings.md` gains a `## host: <host>` section.

Each machine needs exactly one memory-sync job. Two jobs writing the same host file would
race; the per-host design assumes one writer per host file.

## Slack delivery

Set cron `deliver` to `slack:<channel_id>` so sync outcomes appear in the channel. The
`--no-agent` pattern delivers script stdout as the message: non-empty stdout = message,
empty stdout = silent. The script always echoes a status line, so you get a message every run.

## Claude Code pointer

Add to `~/.claude/CLAUDE.md`:

```
For cross-project learnings (project ports, known issues, conventions, user preferences),
read ~/projects/hermes-skills/shared/learnings.md, synced from Hermes memory across machines.
```
