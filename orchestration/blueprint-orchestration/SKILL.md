---
name: blueprint-orchestration
description: >
  Multi-agent orchestration methodology: interview → blueprint → role-specific execution.
  The expensive model thinks. The cheap models do. You supervise.
metadata:
  author: Alistair
  version: "1.0.1"
  category: orchestration
  hermes:
    tags: [orchestration, blueprint, multi-agent, workflow, planning]
---

# Blueprint Orchestration

## HOW THIS WORKS

Split AI-assisted work into specialised roles. Each role has its own system prompt,
its own model assignment, and its own phase in the workflow. You paste the relevant
role card into a fresh session with the assigned model when that phase begins.

Not every project needs every role. The interview determines which roles activate.

> **Prompt quality is load-bearing.** This whole method depends on the blueprint being
> well-written enough that a cheap model executes it reliably. Everything the Architect
> authors here, and everything the orchestrator runs, follows the `prompting-standards`
> skill — Part A (authoring) for the blueprint, Part B (execution) for running tasks.
> Read it before producing or executing a blueprint.

### Available roles

| Role | Skill | Purpose | Default |
|------|-------|---------|---------|
| Architect | `role-architect` | System design, planning, blueprint production | Always active |
| Designer | `role-designer` | UI/UX, visual design, user flows | Optional (any UI) |
| Developer | `role-developer` | Code, config, file creation, command execution | Active unless plan-only |
| Tester | `role-tester` | Validation, verification, drift detection | Recommended |
| Security Auditor | `role-security-auditor` | Credential review, permissions, attack surface | Recommended for any app |
| DevOps / Release | `role-devops` | CI/CD, environments, release, rollback, observability | Recommended for anything deployed |
| End-User | `role-end-user` | Role-play the finished product, find UX gaps | Optional (user-facing) |

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
│ PHASE 5: Deploy (devops wires CI/CD, release, observ.)   │
│                         ↓                                │
│ PHASE 6: Security audit (auditor reviews everything)     │
│                         ↓                                │
│ PHASE 7: End-user review (simulated usage, if activated) │
│                         ↓                                │
│ PHASE 8: Closeout (architect reviews, you sign off)      │
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

**2b. Platforms & targets** → drives the support matrix and Designer/Tester scope
- Which surfaces: desktop app, mobile app (iOS/Android, native/cross-platform), responsive
  website, CLI, API/service? More than one?
- For web: which browsers and minimum versions? Which breakpoints (mobile/tablet/desktop)?
- For mobile/desktop: which OS versions, screen sizes, offline behaviour?

**3. Technical environment**
- What infrastructure exists? Languages, frameworks, tools already in use?
- APIs, services, or external systems? Deployment target? Credential constraints?

**3b. Stack & hosting selection** → drives §3b of the blueprint
- Is the software stack already decided, or does it need choosing? Same for hosting.
- If choosing: what are the selection criteria and their weight — team skills, budget
  (one-off + recurring), time-to-market, expected scale, compliance/data-residency,
  ops burden for a small team, tolerance for vendor lock-in?
- Any hard mandates or exclusions (must use X / cannot use Y)?

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
- Test expectations: unit/integration/end-to-end? Coverage target? Cross-device/browser?

**7b. Non-functional requirements (NFRs)**
- Performance budgets (load time, response time, bundle size, memory)?
- Accessibility target (WCAG A / AA / AA+)? Legal obligation?
- Expected scale/load? Availability expectation?

**8. Design requirements** → determines if Designer activates
- UI needed? Visual design, branding, responsive requirements? Existing design system?

**9. Security posture (shift-left)** → determines if Security Auditor activates
- Handles credentials or sensitive data? Internet-exposed? Touches production?
- Authentication/authorisation model? Untrusted input? Relevant compliance (e.g. PCI)?
- Capture security *requirements* now — they shape the design, not just the later audit.

**9b. Data & privacy**
- Does it collect/store personal data (PII)? What, why, for how long?
- Privacy obligations (GDPR/CCPA)? Where is data stored, and is it encrypted?

**10. User-facing surface** → determines if End-User activates
- Real humans interact with it? User journey to simulate? Accessibility requirements?

**10b. Deployment & operations** → determines if DevOps activates
- Where does it run? Environments (dev/staging/prod)? CI/CD expectations?
- Release + rollback approach? What must be observable in production (logs, metrics, alerts)?

**11. Patterns & preferences**
- Existing conventions, naming style, anti-patterns? Source-of-truth policy when
  sources disagree?

---

## PHASE 1 — THE BLUEPRINT

After the interview, produce the blueprint. Every section is mandatory. If not
applicable, write "N/A — [reason]."

Write the blueprint to the `prompting-standards` skill, Part A: be explicit, frame
positively, say *why*, define output contracts with examples, ground every task ("don't
invent — escalate"), and keep tasks atomic and verifiable. The blueprint is a set of prompts;
its quality is what lets a cheap model execute it.

The blueprint must be **self-contained**. Each role receives ONLY its relevant sections
plus the role card. Nothing from the interview carries over unless it's in the blueprint.

```
================================================================
PROJECT BLUEPRINT
================================================================
Generated: [date]
Architect: [model name/version]
Project:   [name]
Platforms: [desktop / mobile / responsive web / CLI / API — list all]

ACTIVE ROLES:
  [✓] Architect
  [✓/✗] Designer      — [reason if skipped]
  [✓/✗] Developer     — [reason if skipped]
  [✓/✗] Tester        — [reason if skipped]
  [✓/✗] DevOps        — [reason if skipped]
  [✓/✗] Security      — [reason if skipped]
  [✓/✗] End-User      — [reason if skipped]
================================================================
```

### 0. COVERAGE MATRIX

Fill this in before writing the rest. It is the guarantee that nothing falls through the
cracks. For every concern × every target platform, name the role(s) and blueprint section(s)
that cover it, or write "N/A — [reason]". An empty cell is a gap to close, not to ignore.

| Concern | Desktop | Mobile | Responsive web | Covered by |
|---------|---------|--------|----------------|------------|
| Design / UX | | | | Designer · §5 |
| System design & architecture | | | | Architect · §3 |
| Stack & hosting selection | | | | Architect · §3b |
| Development | | | | Developer · §6 |
| Functional testing | | | | Tester · §6 |
| Non-functional (perf, a11y) | | | | §4c |
| Security (design + audit) | | | | §4d · Security |
| Data & privacy | | | | §4e |
| Deployment & release | | | | DevOps · §10b |
| Observability | | | | DevOps · §10c |
| End-user validation | | | | End-User · §6 |
| Documentation | | | | §10d |

(Use only the platform columns that apply — delete the rest.)

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

### 3b. STACK & HOSTING SELECTION *(skip if both are mandated — record the mandate and why)*
The decision class with the largest cost and lock-in consequences. Don't silently pick —
evaluate and justify, per Architect rule #4. For greenfield this is mandatory; for brownfield,
justify staying on (or migrating off) the existing stack/host.

State the decision driver (decided / to-select) and the weighted criteria from the interview,
then evaluate **2–3 candidate options** for each of software stack and hosting:

| Option | Fit for requirements | Cost (setup + recurring) | Ops burden (small team) | Lock-in | Team familiarity |
|--------|---------------------|--------------------------|-------------------------|---------|------------------|
| A | | | | | |
| B | | | | | |

Cover the choices that actually matter for the target platforms (§4c), e.g.:
- **Software**: language & framework; desktop delivery (native / Electron / Tauri); mobile
  (native / React Native / Flutter / PWA); web rendering (SSR / SPA / static); datastore.
- **Hosting**: VPS vs managed PaaS vs serverless vs on-prem/homelab; app-store vs web
  distribution; CDN; data residency / compliance constraints.

End with:
- **Decision**: chosen stack + hosting, stated plainly.
- **Why this and not the others**: the trade-off that decided it.
- **Reversibility**: how hard is it to change later, and what would force a re-decision.

The chosen versions/runtimes then flow into §4 (Technical Spec) and the hosting choice into
§10b (Deployment & Release).

### 4. TECHNICAL SPEC
- Language / framework / runtime (with versions)
- File structure with every file named and explained
- Key interfaces, dependencies, environment variables, config files

### 4b. CONTENT INVENTORY *(skip for greenfield)*
- Sources, format, volume, extraction approach, mapping old→new, discard list
- Content acquisition tasks MUST be early in the build plan (Task 1 or 2)

### 4c. NON-FUNCTIONAL REQUIREMENTS
Concrete, testable targets — not adjectives. These become Tester and DevOps verification checks.
- **Performance budgets**: e.g. page load < 2s on 4G, API p95 < 300ms, bundle < 250KB gzipped, memory ceiling.
- **Accessibility target**: WCAG level (AA default), keyboard-navigable, screen-reader support. State the obligation.
- **Platform / device support matrix** — what must work where:

  | Surface | Targets | Min versions / breakpoints | Notes |
  |---------|---------|----------------------------|-------|
  | Responsive web | Chrome, Safari, Firefox, Edge | mobile 360px / tablet 768px / desktop 1280px | |
  | Mobile app | iOS, Android | iOS 16+, Android 11+ | offline behaviour? |
  | Desktop app | Win/macOS/Linux | versions | window sizes |

- **Scale & availability**: expected load, concurrency, uptime expectation (if any).

### 4d. SECURITY REQUIREMENTS *(shift-left — define here even if Security Auditor runs later)*
Security is a design input, not only a post-build audit. Capture requirements now so the
Developer builds them in and the Auditor has a spec to verify against.
- **AuthN / AuthZ**: who can do what; session/token model; password/secret policy.
- **Input handling**: every untrusted input validated/sanitised; injection (SQL/command),
  XSS, CSRF defences for the relevant platform.
- **Secrets**: sourced from env/secret store, never committed; `.gitignore` covers them.
- **Transport & storage**: TLS in transit; encryption at rest for sensitive data.
- **Relevant threat classes** for this app (OWASP Top 10 web / Mobile Top 10 as applicable).
- **Compliance constraints** (PCI, HIPAA, etc.) if any.

### 4e. DATA & PRIVACY *(skip if no personal/sensitive data)*
- **PII inventory**: what personal data is collected, why, and the lawful basis.
- **Retention & deletion**: how long, how deleted, user data-export/erasure path if required.
- **Storage & access**: where it lives, who/what can read it, encryption.
- **Privacy obligations**: GDPR/CCPA or equivalent; consent and disclosure requirements.

### 5. DESIGN SPEC *(skip if Designer inactive)*
- Visual language, layout, colour, typography, components, responsive, accessibility
- Concrete values, not vague guidance

### 6. BUILD PLAN
Atomic tasks. Each small enough for one focused session.

Write each task to `prompting-standards` Part A. The fields below operationalise it:

```
TASK [N]: [short name]
─────────────────────────────────────────────
Role:        [Architect/Designer/Developer/Tester/DevOps/Security/End-User]
Model:       [which model — from model strategy]
Description: [what to do — explicit, positive framing, and WHY it matters]
Input:       [what must exist before starting]
Output contract: [exact shape of the result — file(s)/signature/schema/format]
Example:     [one worked example of correct output; add an anti-example if subtle]
Verify:      [exact check to confirm success — a command or concrete inspection]
Reasoning:   [think | no_think — and why (complex reasoning vs mechanical)]
Sampling:    [temp ≈ 0 for code/extraction · 0.3–0.7 prose · 0.7+ ideation]
Notes:       [gotchas; "use ONLY the names below — invent nothing, escalate instead"]
Escalate if: [the specific ambiguity or blocker that should stop the task]
```

Task design rules:
- Each task produces a verifiable output with an explicit output contract
- Each task is independent enough to restart without losing prior work (idempotent)
- Each task is grounded: it names everything the executor needs, and tells it to escalate
  rather than invent anything missing
- No task requires the executor to make design decisions
- No task assumes knowledge from the interview
- Designer tasks before dependent Developer tasks
- Tester tasks follow the Developer tasks they validate
- DevOps tasks after the build is functionally complete and Tester-passed
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
| DevOps | [local code model] | 1 | Config/pipeline execution; escalate release-risk reasoning |
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

### 10b. DEPLOYMENT & RELEASE *(skip if nothing is deployed)*
Owned by the DevOps role. Cross-references the Rollback Plan (§10).
- **Environments**: dev / staging / production — what differs between them.
- **Pipeline**: build → test → release steps; what triggers each; reproducibility (pinned
  versions, pinned images, no `latest` in prod).
- **Secret injection**: how each environment's secrets are provided (env/secret store), never
  committed.
- **Release procedure**: exact steps to ship a version.
- **Post-deploy smoke tests**: the concrete checks that prove the release actually works
  (health endpoint, one critical user path, key metric emitting).

### 10c. OBSERVABILITY *(skip if N/A)*
What must be visible in production so failures are caught early. Owned by DevOps; informed by NFRs (§4c).
- **Logging**: structured logs, levels, what is and isn't logged (no secrets/PII in logs).
- **Metrics**: the handful that matter (latency, error rate, key business metric).
- **Error tracking**: where uncaught errors surface.
- **Alerts**: what condition pages someone, and the threshold.

### 10d. DOCUMENTATION
Deliverables, each assigned as a task to the role that owns it.
- **README**: what it is, how to run/build/deploy it.
- **User-facing docs**: if there's a user surface (informs the End-User walkthrough).
- **API docs**: if it exposes an API.
- **Runbook / operations notes**: how to deploy, roll back, and respond to common failures.

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
- [ ] Coverage Matrix (§0): every cell satisfied or explicitly N/A
- [ ] No hardcoded secrets or credentials
- [ ] File structure matches technical spec
- [ ] Design matches design spec (if Designer was active)
- [ ] Edge cases from user stories are handled
- [ ] NFRs met: performance budgets and accessibility target verified (§4c)
- [ ] Support matrix verified: works on every listed platform/browser/breakpoint (§4c)
- [ ] Security requirements implemented (§4d) and Security audit passed (if Security was active)
- [ ] Data & privacy handling matches §4e (if applicable)
- [ ] Deployment pipeline + smoke tests pass; rollback verified (§10, §10b)
- [ ] Observability live: logging, error tracking, key metrics/alerts (§10c)
- [ ] End-user simulation completed (if End-User was active)
- [ ] Documentation deliverables produced and accurate (§10d)
- [ ] STATUS.md reflects all tasks complete

### 13. PROGRESS TRACKING
The Architect produces `STATUS.md` at blueprint finalisation. Every role updates it.

> **Note:** STATUS.md is read independently — do not use §-notation cross-references
> (e.g. `§4e`) in it. Write plain English instead (e.g. "GDPR requirement").

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

> **Note:** DECISIONS.md is read independently of the blueprint — do not use §-notation
> shorthand in the `Affects` field. Write plain English section names instead.
> Good: `"Architecture, all build tasks, model assignments"`
> Bad: `"§3, §3b, §6 (all tasks), §7"`

```
# Decisions & Changes — [project name]

## [YYYY-MM-DD] — [short title]
**Trigger**: [what prompted this]
**Decision**: [what was decided]
**Why**: [reasoning]
**Affects**: [plain English — e.g. "Architecture and all build tasks", not §-notation]
**Decided by**: [role / human / model]
```

---

## PHASE 2-8 — EXECUTION

Execution follows `prompting-standards` Part B: fresh session per role, stable prompt prefix,
verify side effects on disk, validate structured output, re-prompt with new signal rather
than identical retry, and check for drift at every task boundary.

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

**Critical rules** (these are `prompting-standards` Part B applied to Hermes profiles):
- The orchestrator MUST NOT do a role's work itself. Route it.
- After each task, verify side effects on disk — files actually written, not just shown
  (local models via `-q` often output code as text instead of calling write_file). B3.
- After each task, verify the output against its contract — e.g. CSS class names match the
  actual stylesheet; structured output parses. B4.
- On failure, re-prompt with added signal (constraint/example); don't retry identically. B5.
- Bulk mechanical transformations go via `execute_code` scripts, not model prompts. B7.

### Phase execution order

```
PHASE 1: Architect    → always runs (produces the blueprint)
PHASE 2: Designer     → if active: before Developer
PHASE 3: Developer    → if active: bulk of the work
PHASE 4: Tester       → if active: after each Developer phase
PHASE 5: DevOps       → if active: after build is functionally complete + Tester-passed
PHASE 6: Security     → if active: after Developer is functionally complete (reviews deploy too)
PHASE 7: End-User     → if active: last, after everything else passes
PHASE 8: Closeout     → architect reviews against the Coverage Matrix, human signs off
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
