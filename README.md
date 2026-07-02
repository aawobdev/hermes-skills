# hermes-skills

Global [Hermes](https://hermes-agent.nousresearch.com) agent skills for multi-agent project orchestration.

Follows the [agentskills.io](https://agentskills.io) open standard — compatible with any skills-compliant agent.

## Skills

### `skills/`

A complete multi-agent project workflow: an expensive thinking model interviews you and produces a blueprint, cheap local models execute it role by role, you supervise.

| Skill | What it does |
|-------|-------------|
| [`blueprint-orchestration`](skills/blueprint-orchestration/SKILL.md) | Full workflow: interview → blueprint → one-shot execution. Start here. |
| [`role-architect`](skills/role-architect/SKILL.md) | System prompt: interviews, designs, produces the blueprint |
| [`role-designer`](skills/role-designer/SKILL.md) | System prompt: visual decisions, UI layouts, interaction patterns |
| [`role-developer`](skills/role-developer/SKILL.md) | System prompt: executes build tasks, writes code, never decides |
| [`role-tester`](skills/role-tester/SKILL.md) | System prompt: adversarially verifies output against the spec |
| [`role-devops`](skills/role-devops/SKILL.md) | System prompt: CI/CD, environments, release, rollback, observability |
| [`role-security-auditor`](skills/role-security-auditor/SKILL.md) | System prompt: vulnerability review, credentials, attack surface |
| [`role-end-user`](skills/role-end-user/SKILL.md) | System prompt: simulates real user to find UX gaps |
| [`role-orchestrator`](skills/role-orchestrator/SKILL.md) | System prompt: sequences tasks, delegates via one-shot commands (`hermes -z` / `claude -p`) |
| [`prompting-standards`](skills/prompting-standards/SKILL.md) | LLM/prompt best practices for authoring and executing blueprints |
| [`model-routing`](skills/model-routing/SKILL.md) | Model roster (local Ollama + OpenRouter free/paid + Claude Code CLI), VRAM constraints, role-to-model assignments |

## Setup

### Via tap (recommended)

```bash
hermes skills tap add aawobdev/hermes-skills
```

Skills are immediately available. Update anytime with:

```bash
hermes skills tap update aawobdev/hermes-skills
```

### Manual

Clone and point your Hermes config at the skill directory:

```bash
# Linux / Mac
git clone https://github.com/aawobdev/hermes-skills ~/projects/hermes-skills
```

```powershell
# Windows
git clone https://github.com/aawobdev/hermes-skills "$env:USERPROFILE\projects\hermes-skills"
```

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - ~/projects/hermes-skills/skills               # Linux/Mac
    # - C:\Users\YourName\projects\hermes-skills\skills  # Windows
```

## Usage

In Hermes, load the orchestration skill and describe your project:

```
/skill blueprint-orchestration

My project: I want to build a monitoring dashboard for my homelab.
```

The Architect interviews you, determines which roles activate, and produces a blueprint.

### Execution

Tasks are executed via two one-shot patterns:

**Routine tasks** (CRUD, config, scaffolding, tests):
```bash
hermes -z "TASK [N]: [fully self-contained task spec with output contract and verify command]"
```

**CC-class tasks** (complex logic, multi-file refactors, security):
```bash
claude -p "[task spec]" --allowedTools "Read,Write,Bash" --max-turns 15 --output-format json
```

See [`skills/README.md`](skills/README.md) for the full guide, or the `blueprint-orchestration`
skill for the detailed workflow.
