# hermes-skills

Global [Hermes](https://hermes-agent.nousresearch.com) agent skills for multi-agent project orchestration.

Follows the [agentskills.io](https://agentskills.io) open standard — compatible with any skills-compliant agent.

## Skills

### `orchestration/`

A complete multi-agent project workflow: an expensive thinking model interviews you and produces a blueprint, cheap local models execute it role by role, you supervise.

| Skill | What it does |
|-------|-------------|
| [`blueprint-orchestration`](orchestration/blueprint-orchestration/SKILL.md) | Full workflow: interview → blueprint → execution. Start here. |
| [`role-architect`](orchestration/role-architect/SKILL.md) | System prompt: interviews, designs, produces the blueprint |
| [`role-designer`](orchestration/role-designer/SKILL.md) | System prompt: visual decisions, UI layouts, interaction patterns |
| [`role-developer`](orchestration/role-developer/SKILL.md) | System prompt: executes build tasks, writes code, never decides |
| [`role-tester`](orchestration/role-tester/SKILL.md) | System prompt: adversarially verifies output against the spec |
| [`role-security-auditor`](orchestration/role-security-auditor/SKILL.md) | System prompt: vulnerability review, credentials, attack surface |
| [`role-end-user`](orchestration/role-end-user/SKILL.md) | System prompt: simulates real user to find UX gaps |
| [`model-routing`](orchestration/model-routing/SKILL.md) | Model roster, VRAM constraints, role-to-model assignments |

## Setup

Clone and point your Hermes config at the skill directory:

```bash
git clone https://github.com/aawobdev/hermes-skills ~/hermes-skills
```

```yaml
# hermes config.yaml
skills:
  external_dirs:
    - ~/hermes-skills/orchestration
```

## Usage

In Hermes, load the orchestration skill and describe your project:

```
/skill blueprint-orchestration

My project: I want to build a monitoring dashboard for my homelab.
```

The Architect interviews you, determines which roles activate, and produces a blueprint. You execute each phase with the assigned model. See [`orchestration/README.md`](orchestration/README.md) for the full guide.
