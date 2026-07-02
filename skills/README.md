# Hermes Orchestration Skills

Global Hermes skills for AI-assisted project work. Load them on any Hermes instance
via `skills.external_dirs` in your config.

---

## What this is

A multi-agent workflow where:

- An **expensive thinking model** (local or cloud) acts as the Architect — it interviews
  you, makes all design decisions, and produces a detailed blueprint
- **Cheap local models** execute the blueprint as Developer, Tester, etc. — they
  follow the plan without needing to reason about it
- **You** supervise and relay between roles

The key insight: if the blueprint is thorough enough, you don't need a frontier model
for every task. A blueprint that specifies exact file names, function signatures, and
verification commands turns a $0.001/task local model into a reliable executor.

---

## Skills in this directory

| Skill | What it does |
|-------|-------------|
| `blueprint-orchestration` | Full workflow: interview → blueprint → execution. Start here for any new project. |
| `role-architect` | System prompt for the Architect. Paste this + your project description to begin. |
| `role-designer` | System prompt for the Designer. Activates when UI/visual work is needed. |
| `role-developer` | System prompt for the Developer. Executes build tasks from the blueprint. |
| `role-tester` | System prompt for the Tester. Adversarially verifies Developer output. |
| `role-devops` | System prompt for the DevOps/Release role. CI/CD, release, rollback, observability. |
| `role-researcher` | System prompt for the Researcher. Gathers evidence, compares options, produces reports. |
| `role-security-auditor` | System prompt for the Security Auditor. Reviews for vulnerabilities. |
| `role-end-user` | System prompt for the End-User. Simulates real user interaction. |
| `role-orchestrator` | System prompt for the Orchestrator. Sequences tasks and delegates via one-shot commands (`hermes -z` / `claude -p`). |
| `prompting-standards` | LLM/prompt best practices: how blueprints are authored and executed. |
| `model-routing` | Current model roster, VRAM constraints, role-to-model assignments. |

---

## How to start a project

**Option A: In Hermes (ask it to run the skill)**

```
/skill blueprint-orchestration

My project: I want to [one sentence description]
```

Hermes loads the orchestration methodology and starts the Architect interview.

**Option B: Manual (paste and relay)**

1. Start a session with a strong thinking model (qwen3.6-35b-a3b via Ollama, or Claude)
2. Paste the content of `role-architect/SKILL.md`
3. Tell it your project in one sentence
4. Answer the interview questions
5. Wait for the blueprint
6. Execute each phase with the assigned model

---

## The workflow

```
You → Architect (thinking model) → Blueprint
         ↑                              ↓
    Researcher                ┌─────────────────────────┐
  (evidence reports)          │ Developer (cheap model)  │ ← executes tasks
                              │ Tester (mid model)       │ ← validates output
                              │ Security (thinking model)│ ← reviews for risks
                              │ End-User (any model)     │ ← simulates usage
                              └─────────────────────────┘
                                           ↓
                                   You sign off
```

You are the relay between all phases. Roles never talk to each other directly.
Escalations always go back through you to the Architect.

---

## Per-project setup

Each project needs a minimal entry point that references these global skills:

```markdown
# HERMES.md (in project root)

## Orchestration
Uses global Hermes skills. Run `/skill blueprint-orchestration` to start.
Blueprint is at: [path/to/blueprint.md]

## Project-specific model overrides
- [Any overrides from the global defaults in model-routing]

## Project context for Hermes
- [One paragraph: what this project is, its stack, key constraints]
```

The project blueprint (produced by the Architect) lives in the project repo,
not in this skills directory. Only reusable methodology lives here.

---

## Model quick reference

| Role | Primary | Where |
|------|---------|-------|
| Architect | `qwen3.6-35b-a3b` | Ollama |
| Designer | `qwen3.6-35b-a3b` | Ollama — spec/UX reasoning; `gemma4:12b` for vision review; Claude Sonnet for blank-canvas creative direction |
| Developer | `qwen3-coder-30b` | Ollama |
| Tester | `gemma4:26b` | Ollama |
| DevOps | `qwen3-coder-30b` | Ollama |
| Researcher | `qwen3.6-35b-a3b` or Claude Sonnet (web search) | Ollama / Claude |
| Security | `qwen3.6-35b-a3b` | Ollama |
| End-User | `gemma4:26b` | Ollama |

Full details including tok/s benchmarks, fallbacks, and VRAM notes: see `model-routing/SKILL.md`.

---

## Adding a new role or updating models

- Role skills are in `role-*/SKILL.md` — edit in place, changes are picked up immediately
  (no Hermes restart needed as long as the directory is in `skills.external_dirs`). They
  carry full Hermes frontmatter, so they're loadable as skills (`/skill role-architect`)
  AND usable paste-and-relay (copy the SKILL.md body into any session) — both are
  supported, pick whichever fits the moment.
- Model changes go in `model-routing/SKILL.md`
- Changes are picked up by Hermes immediately — no restart needed

---

## Hermes config (for reference)

### Via tap (recommended)

```bash
hermes skills tap add aawobdev/hermes-skills
hermes skills tap update aawobdev/hermes-skills  # to update
```

### Manual (external_dirs)

```bash
git clone https://github.com/aawobdev/hermes-skills ~/projects/hermes-skills
```

```yaml
# ~/.hermes/config.yaml (Linux/Mac) or %LOCALAPPDATA%\hermes\config.yaml (Windows)
skills:
  external_dirs:
    - ~/projects/hermes-skills/skills       # Linux/Mac
    # - C:\Users\<you>\projects\hermes-skills\skills  # Windows
```

For remote Ollama (e.g. a separate inference VM), set
`model.base_url` to the remote address:

```yaml
model:
  provider: custom
  base_url: http://<ollama-host>:11434/v1
```
