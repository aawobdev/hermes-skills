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
   knowledge base source lists, any `*.json` agent configs (opencode.json etc.).

5. **Leave alone:** gitignored machine-specific configs (`.claude/settings.local.json`,
   `.mcp.json`) — these are agent-specific by design and not tracked.

6. **Verify:** `grep -r "CLAUDE.md\|Claude Code\|claude.ai/code" .` should only return
   the one-line CLAUDE.md stubs themselves.

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
