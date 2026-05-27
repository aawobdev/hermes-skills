---
name: blueprint-orchestration
description: >
  Multi-agent orchestration methodology: interview → blueprint → role-specific execution.
  The expensive model thinks. The cheap models do. You supervise.
platforms: [linux, macos, windows]
version: 1.0.0
author: Alistair
category: orchestration
metadata:
  hermes:
    tags: [orchestration, blueprint, multi-agent, workflow, planning]
---

# Blueprint Orchestration

## HOW THIS WORKS

Split AI-assisted work into specialised roles. Each role has its own system prompt,
its own model assignment, and its own phase in the workflow. You paste the relevant
role card into a fresh session with the assigned model when that phase begins.

Not every project needs every role. The interview determines which roles activate.

### Available roles

| Role | Skill | Purpose | Default |
|------|-------|---------|---------|
| Architect | `role-architect` | System design, planning, blueprint production | Always active |
| Designer | `role-designer` | UI/UX, visual design, user flows | Optional |
| Developer | `role-developer` | Code, config, file creation, command execution | Active unless plan-only |
| Tester | `role-tester` | Validation, verification, drift detection | Recommended |
| Security Auditor | `role-security-auditor` | Credential review, permissions, attack surface | Recommended for infra |
| End-User | `role-end-user` | Role-play the finished product, find UX gaps | Optional |

### The workflow

```
┌─────────────────────────────────────────────────────────┐
│ YOU start a session with the Architect role              │
│                         ↓                                │
│ PHASE 0: Interview (architect determines scope + roles)  │
│                         ↓                                │
│ PHASE 1: Blueprint (architect produces the full plan)    │
│                         ↓                                │
│ PHASE 2: Design (designer, if activated)                 │
│                         ↓                                │
│ PHASE 3: Build (developer executes tasks from blueprint) │
│              ↕                                           │
│ PHASE 4: Test (tester validates after each dev phase)    │
│                         ↓                                │
│ PHASE 5: Security audit (auditor reviews everything)     │
│                         ↓                                │
│ PHASE 6: End-user review (simulated usage, if activated) │
│                         ↓                                │
│ PHASE 7: Closeout (architect reviews, you sign off)      │
└─────────────────────────────────────────────────────────┘

Escalation at any phase → back to architect
You are the relay between all phases — roles never talk to each other directly
```

---

## PHASE 0 — THE INTERVIEW

The Architect interviews the human, determines which roles this project needs,
and produces a blueprint so thorough that each role can execute without ambiguity.

The Architect does not write code. Does not execute tasks. Does not design UI. Does not test.
Produces the plan. Others execute it.

### Interview areas

Ask about each area below. Combine related questions where natural.
Must explicitly cover every area before producing the blueprint.

**1. Vision & outcome**
- What is the end result? What does "done" look like?
- Who is this for? What's the single most important thing it must get right?

**2. Scope & boundaries**
- What's in scope / out of scope? Hard constraints?
- Greenfield (new) or brownfield (modifying existing)?
- If brownfield AND content-heavy: where does existing content live? Volume? Format?
  Content acquisition belongs in the build plan EARLY, not deferred as an afterthought.

**3. Technical environment**
- What infrastructure exists? Languages, frameworks, tools already in use?
- APIs, services, or external systems? Deployment target? Credential constraints?

**4. Execution context**
- What executes each phase? (local AI, Claude Code, Hermes, manual, team)
- Can executors access the internet, terminal, file system? Approval gates?

**5. Model inventory & routing**
- What AI models are available? (local and cloud)
- Hardware for local inference? Routing layer? Fallback when local is unavailable?
- Cloud accounts? Budget caps? Task types that must always/never go to a specific model?

**6. Risk & rollback**
- What happens if this goes wrong? Rollback plan? Destructive operations?

**7. Quality & verification**
- How will you know each step succeeded? Existing tests or linters?

**8. Design requirements** → determines if Designer activates
- UI needed? Visual design, branding, responsive requirements?

**9. Security posture** → determines if Security Auditor activates
- Handles credentials or sensitive data? Internet-exposed? Touches production?

**10. User-facing surface** → determines if End-User activates
- Real humans interact with it? User journey to simulate? Accessibility requirements?

**11. Patterns & preferences**
- Existing conventions, naming style, anti-patterns? Source-of-truth policy when
  sources disagree?

---

## PHASE 1 — THE BLUEPRINT

After the interview, produce the blueprint. Every section is mandatory. If not
applicable, write "N/A — [reason]."

The blueprint must be **self-contained**. Each role receives ONLY its relevant sections
plus the role card. Nothing from the interview carries over unless it's in the blueprint.

```
================================================================
PROJECT BLUEPRINT
================================================================
Generated: [date]
Architect: [model name/version]
Project:   [name]

ACTIVE ROLES:
  [✓] Architect
  [✓/✗] Designer      — [reason if skipped]
  [✓/✗] Developer     — [reason if skipped]
  [✓/✗] Tester        — [reason if skipped]
  [✓/✗] Security      — [reason if skipped]
  [✓/✗] End-User      — [reason if skipped]
================================================================
```

### 1. PRODUCT BRIEF
Plain-language summary. One paragraph. What it is, why it exists, who it's for,
what "done" looks like, what's out of scope.

### 2. USER STORIES / USE CASES
```
As a [role], I want to [action], so that [outcome].
Acceptance criteria:
  - [criterion]
```
Include: primary happy path, one edge case, one failure case.

### 3. ARCHITECTURE
- Components and responsibilities, data flow, external dependencies
- State management, diagram (ASCII or mermaid)

### 4. TECHNICAL SPEC
- Language / framework / runtime (with versions)
- File structure with every file named and explained
- Key interfaces, dependencies, environment variables, config files

### 4b. CONTENT INVENTORY *(skip for greenfield)*
- Sources, format, volume, extraction approach, mapping old→new, discard list
- Content acquisition tasks MUST be early in the build plan (Task 1 or 2)

### 5. DESIGN SPEC *(skip if Designer inactive)*
- Visual language, layout, colour, typography, components, responsive, accessibility
- Concrete values, not vague guidance

### 6. BUILD PLAN
Atomic tasks. Each small enough for one focused session.

```
TASK [N]: [short name]
─────────────────────────────────────────────
Role:        [Architect/Designer/Developer/Tester/Security/End-User]
Model:       [which model — from model strategy]
Description: [what to do]
Input:       [what must exist before starting]
Output:      [what this produces]
Verify:      [exact check to confirm success]
Notes:       [gotchas, things NOT to do]
Escalate if: [when to stop and ask the architect]
```

Task design rules:
- Each task produces a verifiable output
- Each task is independent enough to restart without losing prior work
- No task requires the executor to make design decisions
- No task assumes knowledge from the interview
- Designer tasks before dependent Developer tasks
- Tester tasks follow the Developer tasks they validate
- Security tasks after development is functionally complete

### 7. MODEL STRATEGY
See the `model-routing` Hermes skill for the current model roster and routing tiers.
This section documents project-specific overrides and task-to-model assignments.

#### 7.1 — Role-to-model assignment
| Role | Assigned model | Tier | Reasoning |
|------|---------------|------|-----------|
| Architect | [frontier model] | 3 | Requires complex reasoning |
| Developer | [local model] | 1 | Routine execution from clear spec |
| Tester | [mid-tier or local] | 1-2 | Methodical, not complex |
| Security | [frontier model] | 3 | Must not miss vulnerabilities |
| End-User | [any capable model] | 1 | Perspective > raw capability |

#### 7.2 — Task-to-model assignment
| Task | Role | Model | Tier | Escalate to |
|------|------|-------|------|-------------|

#### 7.3 — Model-specific prompting notes
For thinking models (qwen3.6-27b, qwen3.6-35b-a3b):
- Set `max_tokens ≥ 4000` — models use ~1700 reasoning tokens before output starts
- Use `/no_think` prefix for simple/mechanical tasks to skip reasoning overhead
- Expect 80-120s response time for complex reasoning tasks
- Output lives in `reasoning_content`, then `content` — don't mistake empty `content` for failure

#### 7.4 — Cost guardrails
- Crons and scheduled tasks always use cheapest model
- Try once more on cheap model before escalating to expensive
- Per-task ceiling before approval needed: [define per project]

### 8. DEPENDENCY GRAPH
```
Task 1 (no dependencies)
Task 2 → depends on: Task 1
Task 3 → depends on: Task 1   ← can run parallel with Task 2
Task 4 → depends on: Task 2, Task 3
```

### 9. RISK REGISTER
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

Must include: infrastructure risk, model drift risk, data/state risk,
model availability risk, cost escalation risk.

### 10. ROLLBACK PLAN
| After completing... | To rollback... |
|----|-----|
| Tasks 1-3 | [steps] |
| Full build | [nuclear option] |

### 11. ROLE HANDOFF PROMPTS
For each active role, the exact text to paste into that role's session.
Each handoff prompt includes: role card reference, relevant blueprint sections,
assigned tasks, verification criteria.

```
HANDOFF: [ROLE NAME]
═══════════════════════════════════════════
Paste the role card (from Hermes skill `role-[name]`) into a fresh session, then paste this:

[role-specific blueprint context]
[tasks assigned to this role]
```

### 12. POST-BUILD CHECKLIST
- [ ] All task verification checks pass
- [ ] No hardcoded secrets or credentials
- [ ] File structure matches technical spec
- [ ] Design matches design spec (if Designer was active)
- [ ] Edge cases from user stories are handled
- [ ] Security audit passed (if Security was active)
- [ ] End-user simulation completed (if End-User was active)
- [ ] Rollback plan confirmed viable
- [ ] Documentation / README accurate
- [ ] STATUS.md reflects all tasks complete

### 13. PROGRESS TRACKING
The Architect produces `STATUS.md` at blueprint finalisation. Every role updates it.

```
# Project Status — [project name]
Last updated: [date] by [role/model]

## Phase summary
| Phase | Role | Status | Notes |
|-------|------|--------|-------|

## Task status
| Task | Description | Status | Notes |
|------|-------------|--------|-------|

## Blockers
## Pending decisions
```

### 14. DECISIONS & CHANGE LOG
The Architect produces `DECISIONS.md` alongside `STATUS.md`. Append when:
- A blueprint section is patched, scope changes, source-of-truth conflict resolved,
  role added/removed, model swapped, interview assumption turns out wrong.

```
# Decisions & Changes — [project name]

## [YYYY-MM-DD] — [short title]
**Trigger**: [what prompted this]
**Decision**: [what was decided]
**Why**: [reasoning]
**Affects**: [blueprint sections / tasks]
**Decided by**: [role / human / model]
```

---

## PHASE 2-6 — EXECUTION

### Manual execution (paste-and-relay)

1. Open a fresh session with the model assigned to the next active role
2. Paste the role card (from Hermes via `/skill role-[name]`)
3. Paste the handoff prompt from the blueprint (section 11)
4. Supervise the work
5. Collect the output and update STATUS.md
6. Hand off to the next role

### Automated execution (Hermes profile orchestration)

Create a Hermes profile per role, each configured for the assigned model:

```bash
hermes profile create developer --clone
developer config set model.default devstral-small-2:24b-instruct-2512-q4_K_M
developer config set model.provider custom:Ollama-Desktop
developer config set model.base_url http://192.168.1.123:11434/v1

# Per-task execution from orchestrating agent's terminal
hermes -p developer chat -q "[role card + project context + task spec]"
```

**Critical rules:**
- The orchestrator MUST NOT do the developer's work itself. Route it.
- After each task, verify files were actually written (local models via `-q` often
  output code as text instead of calling write_file).
- After each task, verify CSS class names match the actual stylesheet.
- Bulk mechanical transformations go via `execute_code` scripts, not model prompts.

### Phase execution order

```
PHASE 1: Architect    → always runs (produces the blueprint)
PHASE 2: Designer     → if active: before Developer
PHASE 3: Developer    → if active: bulk of the work
PHASE 4: Tester       → if active: after each Developer phase
PHASE 5: Security     → if active: after Developer is functionally complete
PHASE 6: End-User     → if active: last, after everything else passes
PHASE 7: Closeout     → architect reviews, human signs off
```

### Escalation protocol

1. Copy the problem and the role's output
2. Paste into the Architect session
3. Architect produces a **patch** — revised task or clarification
4. Paste the patch back into the stuck role's session
5. Human is always the relay — roles never communicate directly

---

## QUICK START

```
Start a Hermes session. Run: /skill blueprint-orchestration

Tell the Architect: "My project: [one sentence]"

The Architect begins the interview → determines roles → produces blueprint.
Execute each phase with the assigned model and role card. Supervise.
```
