# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

> **This is the only agent guidance file.** Do not create `CLAUDE.md`, `.cursorrules`,
> `.github/copilot-instructions.md`, or any other agent-specific config files. If you
> need to add or correct guidance, edit `AGENTS.md` (or the nearest `AGENTS.md` in a
> subdirectory).

## What This Repo Is

Global Hermes agent skills for multi-agent project orchestration. Follows the
[agentskills.io](https://agentskills.io) open standard — compatible with any
skills-compliant agent. Cloned to `~/hermes-skills` (Linux) or
`C:\Users\<user>\hermes-skills` (Windows) and referenced via Hermes config
`skills.external_dirs`.

## Common Commands

```bash
# Validate skill structure (if hermes CLI available)
hermes skills list

# Preview a skill's content
cat skills/blueprint-orchestration/SKILL.md

# Test a skill in Hermes
hermes
> /skill blueprint-orchestration
```

No build system, test suite, or linter. Skills are markdown files (YAML frontmatter +
body). Validation is implicit — Hermes loads them or doesn't.

## Architecture

### Skill structure

Each skill lives in `skills/<skill-name>/`:

```
skills/<skill-name>/
├── SKILL.md              YAML frontmatter (name, description, metadata) + markdown body
└── references/           Optional supporting files (guides, templates, gotchas)
```

### Skills in this repo

| Skill | Purpose |
|-------|---------|
| `blueprint-orchestration` | Full workflow: interview → blueprint → execution. Start here. |
| `role-architect` | System prompt: interviews, designs, produces the blueprint |
| `role-designer` | System prompt: visual decisions, UI layouts, interaction patterns |
| `role-developer` | System prompt: executes build tasks, writes code, never decides |
| `role-tester` | System prompt: adversarially verifies output against the spec |
| `role-devops` | System prompt: CI/CD, environments, release, rollback, observability |
| `role-researcher` | System prompt: gathers evidence, compares options, produces reports |
| `role-security-auditor` | System prompt: vulnerability review, credentials, attack surface |
| `role-end-user` | System prompt: simulates real user to find UX gaps |
| `role-orchestrator` | System prompt: sequences tasks, delegates via one-shot commands |
| `prompting-standards` | LLM/prompt best practices for authoring and executing blueprints |
| `model-routing` | Model roster (local Ollama + OpenRouter + Claude Code CLI), VRAM constraints, role-to-model assignments |

### Key references

- `blueprint-orchestration/references/one-shot-execution.md` — Practical gotchas for `hermes -z` and `claude -p`
- `blueprint-orchestration/references/agent-agnostic-repos.md` — Migrating repos to AGENTS.md, memory harmonisation, AGENTS.md template

## Conventions

- **SKILL.md frontmatter**: `name`, `description`, `metadata` (author, version, category, hermes.tags). Always bump version on meaningful changes.
- **Role skills** (`role-*`) are system prompts — paste-and-relay, not loaded as Hermes skills. They contain no tool instructions, just the role's persona, rules, and output format.
- **Blueprint orchestration** is the master skill — it references all role skills and drives the workflow.
- **Model routing** is environment-specific — update `model-routing/SKILL.md` when hardware or installed models change.
- **One-line pointer files**: agent-specific config files (CLAUDE.md, .cursorrules, .github/copilot-instructions.md, opencode.json) in any repo using these skills should be one-line pointers to that repo's AGENTS.md. See `agent-agnostic-repos.md` reference.

## Setup

### Via tap (recommended)

```bash
hermes skills tap add aawobdev/hermes-skills
hermes skills tap update aawobdev/hermes-skills
```

### Manual

```bash
git clone https://github.com/aawobdev/hermes-skills ~/hermes-skills
```

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/hermes-skills/skills
```
