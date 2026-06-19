# Agent-Agnostic Repos: Migration & Multi-Agent Memory Harmonisation

## Why AGENTS.md over CLAUDE.md

`AGENTS.md` is agent-agnostic — any AI coding agent (Claude Code, Hermes, Codex, OpenCode,
Cursor) can read it. `CLAUDE.md` is Claude-specific. Using AGENTS.md as canonical means
one file serves all agents, and you stop maintaining duplicate guidance across
CLAUDE.md, .cursorrules, .github/copilot-instructions.md, etc.

## Migrating an existing repo from CLAUDE.md to AGENTS.md

1. **Create AGENTS.md** at repo root (and in subdirectories that had their own CLAUDE.md).
   Copy the CLAUDE.md content, de-Claude it:
   - "This file provides guidance to Claude Code (claude.ai/code)" → "guidance to AI coding agents"
   - "Claude Code" → "AI coding agents" or "your agent"
   - Agent-specific setup steps → generic ("Register the MCP server with your agent's config")
   - Suggested usernames like `claude-readonly` → `agent-readonly`

2. **Replace each CLAUDE.md with a one-line pointer:**
   ```
   See [AGENTS.md](AGENTS.md).
   ```
   Do NOT write multi-line stubs with "do not edit" instructions. One line. The user
   finds verbose pointer files annoying.

3. **Add the "only guidance file" directive to AGENTS.md:**
   ```markdown
   > **This is the only agent guidance file.** Do not create `CLAUDE.md`, `.cursorrules`,
   > `.github/copilot-instructions.md`, or any other agent-specific config files.
   ```

4. **Search and update all in-repo references:**
   ```
   CLAUDE.md → AGENTS.md
   Claude Code → AI coding agent(s)
   claude.ai/code → (remove)
   ```
   Check: Python docstrings/comments, YAML configs, markdown links, cron prompts,
   knowledge base source lists, any `*.json` agent configs (opencode.json etc.),

   **Also check these file types (often missed):**
   - `.kt` / `.java` / `.swift` comments referencing safety/privacy constraints from CLAUDE.md
   - `.gitignore` comments mentioning "Claude Code agent state"
   - `.toml` / `.yml` / `.yaml` build configs with CLAUDE.md in inline comments
   - `DECISIONS.md` — update historical CLAUDE.md file references to AGENTS.md,
     but leave product-name "Claude Code" references (e.g. in delegation commands)
     as-is. Those name the tool being used, not the agent identity.

5. **Preserve project tracking files.** Do NOT delete `BLUEPRINT.md`, `STATUS.md`,
  `DECISIONS.md`, or `HANDOVER.md` during migration — they are living documents used by
  the blueprint-orchestration workflow. Instead, reference them from AGENTS.md's project
  tracking section. If a blueprint file is a stale fragment (not a real blueprint), delete
  it but add a note in AGENTS.md: "No active blueprint. To generate one, use the
  `blueprint-orchestration` Hermes skill."

6. **Leave alone:** gitignored machine-specific configs (`.claude/settings.local.json`,
   `.mcp.json`) — these are agent-specific by design and not tracked.

7. **Keep "Claude Code CLI" as a product name.** When "Claude Code" appears in delegation
   commands (e.g. `claude -p "task" --max-turns 10`), it refers to the actual CLI tool,
   not the agent identity. Don't de-Claude these — just the guidance/identity references.

8. **Scan source code comments too.** Check `.kt`, `.ts`, `.py`, `.java`, `.swift` files
   for comments referencing `CLAUDE.md` (e.g. `// SAFETY (CLAUDE.md): ...`). These are
   safety/privacy constraint references that must point to `AGENTS.md`. Use:
   ```bash
   grep -rn "CLAUDE\.md" --include="*.kt" --include="*.ts" --include="*.py" --include="*.java" .
   ```

9. **Handle HERMES.md.** Some repos have both `CLAUDE.md` and `HERMES.md`. Both become
   one-line pointers to `AGENTS.md`.

10. **Verify:** `grep -r "CLAUDE.md\|Claude Code\|claude.ai/code" .` should only return
    the one-line CLAUDE.md stubs themselves, references to "Claude Code CLI" as a product
    name in delegation commands, and historical/factual mentions (e.g. "handover from
    claude.ai session").

## Multi-agent memory harmonisation

When running both Claude Code and Hermes on the same projects, their global memory stores
overlap and drift. The pattern that works:

```
┌─────────────────────────────────────────────────────┐
│ REPO AGENTS.md          ← shared infra reference    │
│ (host tables, deploy commands, delegation tiers,    │
│  architecture, conventions — both agents read this)  │
├─────────────────────────────────────────────────────┤
│ ~/.claude/CLAUDE.md     ← thin, Claude-specific     │
│ (PowerShell tool usage, Invoke-HL, DPAPI secrets —  │
│  things only Claude Code needs operationally)        │
├─────────────────────────────────────────────────────┤
│ ~/.hermes/memories/     ← thin, Hermes-specific     │
│ (project state, user preferences — managed by the   │
│  memory tool, not infrastructure reference)          │
└─────────────────────────────────────────────────────┘
```

Principles:
- **Repo AGENTS.md is the shared layer.** Both agents can read files from the repo when
  working in it. Put shared knowledge here.
- **Global stores stay thin and agent-specific.** Claude's global CLAUDE.md has PowerShell
  tool quirks. Hermes memory has project state. Neither duplicates the other.
- **No symlinks or include hacks.** Both agents can read files from the repo.
- **Point the global stores at the repo.** Claude's global says "read the repo's AGENTS.md
  for infra details." Hermes memory says "infra details in ~/projects/homelab/AGENTS.md."
- **When shared knowledge changes, update AGENTS.md** (one place), not both global stores.

## AGENTS.md template for new projects

When the blueprint's build plan includes a task to create AGENTS.md, use this structure
as the starting point. Adapt to the project — remove sections that don't apply.

```markdown
# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

> **This is the only agent guidance file.** Do not create `CLAUDE.md`, `.cursorrules`,
> `.github/copilot-instructions.md`, or any other agent-specific config files. If you
> need to add or correct guidance, edit `AGENTS.md` (or the nearest `AGENTS.md` in a
> subdirectory).

## What This Repo Is

[1-2 sentences: what the project is, what it does]

## Common Commands

```bash
# Build
[npm run build / cargo build / docker compose up -d / etc.]

# Test
[npm test / pytest / etc.]

# Lint
[npm run lint / ruff check / etc.]

# Dev server
[npm run dev / etc.]
```

## Architecture

[Key directories, data flow, frameworks, patterns. Enough for an agent to navigate
without guessing. Don't repeat what's obvious from package.json / Cargo.toml.]

## Conventions

[Naming, file organisation, CSS approach, state management patterns, anything an
agent would get wrong by default.]

## Environment

[Required env vars, where secrets live, how to get a local dev environment running.
Never hardcode secrets — reference .env.example.]
```

Keep it concise — under 150 lines. An agent reads this on every session; verbose
guidance wastes context. Add subdirectory `AGENTS.md` files only where a subsystem
has its own distinct workflow (e.g. a sub-project with a different build system).

## Deleting stale duplicates of hermes-skills content

Some repos have a local `blueprint/` directory with `ORCHESTRATOR.md` and `roles/*.md`
that are earlier versions of what's now in the hermes-skills repo. These are stale
duplicates — the hermes-skills repo is the canonical source for the orchestration
methodology and role cards.

- **Delete** `blueprint/ORCHESTRATOR.md` if it's an old version of the blueprint-orchestration skill.
- **Delete** `blueprint/roles/` if they're old local role cards (the hermes-skills versions are canonical).
- **Keep** `blueprint/STATUS.md`, `blueprint/DECISIONS.md`, and `blueprint/<project>-blueprint.md` — these are project-specific tracking documents, not methodology.
- If a `HERMES.md` file says "do not maintain local copies" of role cards, that's the signal to delete them.

## Consolidation decision framework

When migrating a repo with many .md files, decide per file:

| File type | Action |
|-----------|--------|
| `CLAUDE.md`, `HERMES.md` | One-line pointer to AGENTS.md |
| `.github/copilot-instructions.md`, `opencode.json`, `.cursorrules` | One-line pointer to AGENTS.md |
| `docs/LOCAL-DEV.md`, `docs/DEPLOY.md`, `docs/SETUP.md` (operational) | Merge into AGENTS.md, delete original |
| `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/SECURITY-AUDIT.md` (reference) | Keep as-is, list in AGENTS.md project tracking |
| `BLUEPRINT.md` (complete) | Keep, update Claude references |
| `BLUEPRINT.md` (fragment/stale) | Delete, note in AGENTS.md |
| `STATUS.md`, `DECISIONS.md`, `HANDOVER.md` | Keep, update Claude references |
| `blueprint/ORCHESTRATOR.md` + `blueprint/roles/` (stale dups of hermes-skills) | Delete |
| `README.md` | Keep (public-facing docs) |

## Migrating repos with no CLAUDE.md

Some repos never had a CLAUDE.md. Create AGENTS.md from scratch using:
- `README.md` — feature docs, setup, project structure
- `docs/LOCAL-DEV.md`, `docs/DEPLOY.md` — operational setup (merge into AGENTS.md, then delete the docs)
- `package.json` scripts block — build/test/lint commands
- `STATUS.md` — secrets setup, deploy automation, environment details
- `BLUEPRINT.md` header — project brief, architecture

Consolidation opportunity: if `docs/` contains small operational .md files (local-dev,
deploy, setup), merge their content into AGENTS.md and delete them. Keep `docs/` only
if it has non-operational content (design briefs, security audits, mockups).

## Stale BLUEPRINT.md handling

If a repo has a BLUEPRINT.md that is a fragment (missing header, just sections 14-15
ripped from context) or is completely stale:

- **Don't keep the fragment** — it looks broken and a future blueprint-orchestration run
  will produce a fresh full blueprint anyway.
- **Delete it** and add this line to AGENTS.md project tracking section:
  `No active blueprint. To generate one, use the \`blueprint-orchestration\` Hermes skill.`
- If BLUEPRINT.md is a real, complete blueprint (has header, tasks, architecture), keep it.
  Just update any "Claude Code" identity references to "AI coding agent(s)".

## Cross-machine memory sync

When Hermes runs on multiple machines and Claude Code also needs the learnings, use a
shared git repo as the transport layer with LLM-curated cron sync. See
`references/cross-machine-memory-sync.md` for the full setup (script pattern, symlink
pitfall, curation rules, Claude Code pointer).
