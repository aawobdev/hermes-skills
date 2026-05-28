# Hermes Orchestration Skills

Global Hermes skills for AI-assisted project work. These live in the homelab repo
and are loaded by both Hermes instances (local and VM) via `skills.external_dirs`.

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
| `role-security-auditor` | System prompt for the Security Auditor. Reviews for vulnerabilities. |
| `role-end-user` | System prompt for the End-User. Simulates real user interaction. |
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

1. Start a session with a strong thinking model (qwen3.6-35b-a3b via LM Studio, or Claude)
2. Paste the content of `role-architect/SKILL.md`
3. Tell it your project in one sentence
4. Answer the interview questions
5. Wait for the blueprint
6. Execute each phase with the assigned model

---

## The workflow

```
You → Architect (thinking model) → Blueprint
                                      ↓
                         ┌─────────────────────────┐
                         │ Developer (cheap model)  │ ← executes tasks
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

| Role | Use this model | Where |
|------|---------------|-------|
| Architect | `qwen3.6-35b-a3b` | LM Studio |
| Designer | `qwen3.6-35b-a3b` | LM Studio |
| Developer | `devstral-small-2:24b` | Ollama |
| Tester | `gemma4:26b` | Ollama |
| Security | `qwen3.6-35b-a3b` | LM Studio |
| End-User | `gemma4:26b` | Ollama |

Full details including fallbacks and VRAM notes: see `model-routing/SKILL.md`.

---

## Adding a new role or updating models

- Role skills are in `role-*/SKILL.md` — edit in place, changes are picked up immediately
  (no Hermes restart needed as long as the directory is in `skills.external_dirs`)
- Model changes go in `model-routing/SKILL.md`
- Changes are picked up by Hermes immediately — no restart needed

---

## Hermes config (for reference)

Both Hermes instances load these skills via `skills.external_dirs`:

```yaml
# In hermes config.yaml
skills:
  external_dirs:
    - C:\Users\alistair\Documents\Dev\hermes-skills\orchestration  # Windows (local Hermes)
    # OR on the VM (clone this repo to ~/hermes-skills/):
    - /home/hermes/hermes-skills/orchestration
```

Repo: https://github.com/aawobdev/hermes-skills

Clone on any new Hermes instance, then add the path to `skills.external_dirs`:
```bash
git clone https://github.com/aawobdev/hermes-skills ~/hermes-skills
```
Pull to get skill updates.
