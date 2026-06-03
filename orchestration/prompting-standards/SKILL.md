---
name: prompting-standards
description: >
  LLM and prompt-engineering best practices for this orchestration system. Two halves:
  (A) how the Architect writes blueprints and task specs, (B) how the orchestrator and
  roles execute those prompts against an LLM. Referenced by every other skill.
metadata:
  author: Alistair
  version: "1.0.0"
  category: orchestration
  hermes:
    tags: [orchestration, prompting, llm, best-practices, reference]
---

# Prompting Standards

The single source of truth for how prompts are **written** and **executed** in this
orchestration system. The blueprint methodology and every role card defer to this file.

Why this exists: the whole premise is that a thorough blueprint lets a cheap model execute
reliably. That only holds if the blueprint and the task prompts follow prompt-engineering
best practice. A weak prompt makes a capable model look stupid; a strong prompt makes a
cheap model look capable.

There are two audiences:

- **Part A — Authoring.** The Architect writes the blueprint and task specs. The quality of
  the *content* it produces is governed here.
- **Part B — Execution.** The orchestrator (human or agent) and each role run those prompts
  against an LLM. How the prompt is *delivered and validated* is governed here.

---

## PART A — AUTHORING PROMPTS & BLUEPRINTS

These rules apply to anything the Architect writes that another model will later act on:
task descriptions, handoff prompts, acceptance criteria, output contracts.

### A1. Be explicit and specific

Vague prompts force the model to guess, and a cheap model guesses badly.

- State the exact thing you want, with names, paths, versions, counts, and limits.
- ❌ "Make the dashboard load fast." ✅ "First contentful paint < 1.5s on a 4G connection;
  lazy-load images below the fold."
- ❌ "Handle errors." ✅ "On a 4xx, show the server's `message` field; on a 5xx or network
  failure, show 'Something went wrong — try again' and log the status code to console."

### A2. Prefer positive instructions over prohibitions

Tell the model what to do, not only what to avoid. Models follow "do X" far more reliably
than "don't do Y." Keep a short list of hard prohibitions for known failure modes, but lead
with the positive instruction.

- ❌ "Don't use inline styles." ✅ "Put all styling in `styles.css`; reference classes by name."

### A3. Give the *why*, not just the *what*

A one-line rationale measurably improves instruction-following and lets the model make
sensible micro-decisions inside the task without escalating.

- "Pin every dependency version **because** an unpinned minor bump silently broke the build
  last time."

### A4. Structure the prompt

- Use headings, numbered lists, and delimiters so sections are unambiguous.
- Put reference material (existing code, schemas, file listings) in clearly fenced blocks or
  tagged sections (e.g. `<spec>…</spec>`, `<existing_code>…</existing_code>`) so the model
  can tell *instructions* from *data*.
- Keep one task = one prompt. Don't bundle unrelated work.

### A5. Define an output contract

Every task that produces structured output must specify the exact shape and a worked example.

- State the format (JSON schema, file with named sections, exact function signature, a table
  with named columns).
- Give **one worked example** of a correct output. For anything subtle, also give **one
  anti-example** ("not like this — here's why").
- For free-form output, specify length, audience, and tone.
- If the output is parsed downstream, demand *only* the artifact with no prose wrapper, or
  specify an exact delimiter the orchestrator can extract between.

### A6. Use few-shot examples for non-trivial tasks

If the task has any ambiguity in *form*, show 1–3 input→output examples. Examples constrain
behaviour more reliably than description. Make examples cover the tricky case, not the easy
one. Keep them consistent with each other — contradictory examples are worse than none.

### A7. Direct the model's reasoning deliberately

Match thinking to the task:

- **Complex/ambiguous reasoning** (architecture, security analysis, tricky logic): let the
  model reason step by step before answering. Ask it to "think through X, then output Y."
- **Mechanical/deterministic work** (rename, reformat, fill a template): suppress reasoning
  for speed (`/no_think` on thinking models). Reasoning adds latency and can introduce drift
  on tasks that need none.
- Each blueprint task carries a `Reasoning:` directive (think / no_think) saying which and why.

### A8. Ground the model; license it to say "I don't know"

The most damaging failure for a cheap executor is confident invention.

- "Use **only** the names, paths, and APIs given in the spec below. If something you need
  isn't there, **stop and escalate** — do not invent a name, endpoint, CSS class, or column."
- Explicitly permit "I can't determine X from the spec" as a valid, expected answer. This is
  what the escalation protocol depends on.

### A9. Decompose into atomic, verifiable, restartable tasks

- One focused outcome per task; small enough for a single session.
- Each task names a concrete, checkable `Verify:` step.
- Each task is restartable without losing prior work (idempotent where possible) — a worker
  that crashes mid-task should be safe to re-run.
- No task should require the executor to make a design or visual decision (those belong to
  the Architect/Designer).

### A10. Build in self-verification

Ask the executor to check its own work before reporting done: "After writing the file,
re-read it and confirm every class referenced exists in the stylesheet." Self-checks catch a
large share of cheap-model errors before they reach the Tester.

### A11. Write for long context: instructions at the top *and* the bottom

Models attend most strongly to the start and end of a long prompt and can lose material in
the middle ("lost in the middle"). Put the core instruction first; restate the key
constraint and the required output format again at the end. Keep large reference dumps in the
middle, not wrapped around the instruction.

### A12. Budget tokens and design for prompt caching

- Keep a **stable prefix**: role card → durable project context → task-specific content, in
  that order. A constant prefix lets the runtime cache it across tasks; reordering it on
  every call defeats caching.
- Pass only the blueprint sections a role actually needs — not the whole document.
- Strip irrelevant history from a role's session; long stale context degrades quality and
  costs tokens.

### A13. Specify sampling per task type

The Architect records a `Sampling:` hint per task:

- **Deterministic** (code generation, refactors, data extraction, config): temperature ≈ 0.
- **Balanced** (prose, docs, test-case ideas): ~0.3–0.7.
- **Divergent** (brainstorming options, naming, design exploration): ~0.7–1.0.
  Code and structured output should almost never run hot.

---

## PART B — EXECUTING PROMPTS AGAINST AN LLM

These rules apply to the orchestrator (human or agent) and every role when actually running
a task against a model.

### B1. Fresh session, minimal context

Start each role/task in a clean session. Paste the role card, then the durable project
context, then the task. Don't carry another role's transcript in — it pollutes context and
invites drift.

### B2. Preserve the stable prefix for cache hits

Send the same prefix (role card + project context) in the same order every time so the
runtime can reuse a cached prefix. Only the task tail should change between calls.

### B3. Verify tool calls actually happened — don't trust the transcript

Local models invoked one-shot frequently *describe* an action instead of *performing* it —
e.g. printing code as text rather than calling `write_file`. After every task that should
have produced a side effect:

- Confirm the file was actually created/modified on disk (not just shown in the reply).
- If the model emitted the artifact as text but didn't write it, the orchestrator extracts
  and writes it directly rather than re-prompting blindly.

### B4. Validate structured output before accepting it

If a task has an output contract (A5), parse/schema-check the result before passing it on.
Reject and re-prompt on malformed output; never hand a downstream role output you haven't
validated.

### B5. Re-prompt smarter, don't retry identical

If a task fails, an identical retry usually fails identically. On retry, *add* signal: a
clarifying constraint, a worked example, or a pointer to exactly what was wrong. Two failed
attempts → stop and escalate (per the role rules), don't loop.

### B6. Try cheap first, escalate by capability tier

Run the assigned (cheapest viable) model first. Escalate to a stronger tier only on genuine
failure or ambiguity — not pre-emptively. Track escalations; a task that always escalates is
a sign the blueprint task spec (Part A) is too weak and should be patched, not the model
upgraded.

### B7. Do bulk mechanical transforms in code, not in prompts

A 200-file find-and-replace is a script, not an LLM task. Use a model to *write* the
transform script (a reasoning task), then run the script deterministically. This is cheaper,
faster, and exact — and avoids the model silently skipping or altering items.

### B8. Set generation parameters to match the task

- Apply the task's `Sampling:` hint (B/A13). Default code and extraction to temperature 0.
- For thinking models, set `max_tokens` high enough to cover reasoning **plus** output
  (reasoning alone can consume well over a thousand tokens before any answer appears). An
  empty `content` field with populated `reasoning_content` is reasoning-in-progress, not
  failure — see `model-routing` for model-specific token/latency figures.

### B9. Guard against drift at execution time

Executors add unrequested features, rename things, "improve" structure. After each task the
orchestrator checks: only the specified files changed, interfaces/schemas/contracts are
unchanged, nothing was added that the task didn't ask for. Drift is the most common and most
expensive failure mode — catch it at the task boundary, not at closeout.

### B10. Keep the human as the relay

Roles never call each other. Output, escalations, and patches flow through the orchestrator.
This keeps each session's context clean (B1) and makes every handoff inspectable.

---

## Quick checklist

**Authoring a task (Architect):** explicit · positive framing · says *why* · structured ·
output contract + example · few-shot if subtle · reasoning directive · grounded ("don't
invent — escalate") · atomic & verifiable · self-check · sampling hint.

**Executing a task (orchestrator/role):** fresh session · stable prefix · verify side effects
on disk · validate structured output · re-prompt with new signal not identical retry · cheap
first then escalate · scripts for bulk transforms · params match task · drift check · human
relays.
