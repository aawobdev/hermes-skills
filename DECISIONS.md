# Decisions & Changes — hermes-skills

## Open backlog items

- **`scripts/` homelab security-investigation one-offs don't belong in a reusable-skills
  repo.** `geo_check.py`, `graylog_analysis.py`/`graylog_analysis2.py` (duplicate
  variants), `plex_crossref.py`/`plex_crossref_full.py` (duplicate variants),
  `plex_threats.py`, `check_unifi_policies.py`, `copy_key_to_udm.py`,
  `setup_udm_ssh.sh`, and `find_bws_secrets.py` are one-off scripts from ad-hoc homelab
  security investigations, not reusable skill logic, and several have superseded
  duplicate variants sitting alongside the current one. Proposed: move these to the
  `homelab` repo (or wherever one-off ops scripts live) and delete the superseded
  variants once the current ones are confirmed as the keepers. Not implemented as part
  of this doc-fix pass — flagging only.

## 2026-06-19 — 2-tier model routing (proposed, pending trial)

**Trigger**: Alistair frustrated by constant switching between Claude Max subscription and Hermes+OpenRouter/local Ollama. The 4-tier, ~15-model routing in `model-routing` and `blueprint-orchestration` causes decision fatigue on every task — two competing sunk-cost pressures ("use the Max sub I'm paying for" vs "save quota with free local models") stall projects.

**Decision**: Collapse routing to 2 tiers:
- **Tier 0 — Orchestrator**: GLM 5.2 (or deepseek-v4-flash) via OpenRouter. Cheap-ish reasoning, holds blueprint, sequences tasks, delegates, validates output. Better prompt quality here saves Claude retries downstream.
- **Tier 1 — Default executor**: Claude via `claude -p` (Max subscription). All dev/test/devops tasks route here by default. No per-task routine-vs-CC-class classification — just send it.
- **Overflow (explicit only)**: Local Ollama for privacy-sensitive work (Life Tracker health data), bulk parallel tasks, offline, or when Max quota is genuinely exhausted. Not a default routing tier.

**Why**: The switching is the problem, not the routing. Any single default beats a perfect multi-tier system you keep abandoning. Claude Max is a sunk cost; routing routine work to local models to "save" quota is false economy when local models need 2-3 retries or produce lower-quality output needing fixes. During cancer treatment, energy is the scarcer resource than API credits.

**Native subagent delegation**: `delegate_task` with ACP transport for Claude is NOT available (no paid GitHub Copilot account). Claude stays as `claude -p` shell-out. `delegate_task` is still worth using for local-model subagents (context isolation, parallel batch, structured summaries) — but Claude execution itself remains shell-out, optionally wrapped in a Hermes leaf for context hygiene.

**Affects**: model-routing (full rewrite of routing tiers), blueprint-orchestration (execution engine section, model strategy section), role-orchestrator (delegation protocol, model assignment table). Local model roster table kept as reference, not as routing tiers.

**Status**: PROPOSED — Alistair will trial the switching in practice before skills are rewritten. Do NOT rewrite the three skill files until Alistair confirms preference after real use.

**Decided by**: Alistair (decision), GLM 5.2 (analysis + recommendation)

**Note on GLM 5.2**: During this session, GLM 5.2 produced one severe output corruption (repeated token garbage mid-response). This is a reliability data point for the orchestrator-model question — worth monitoring if GLM 5.2 becomes the orchestrator.

**Needs resolution (flagged 2026-07-02)**: This entry is still marked PROPOSED two
weeks after the 2026-06-19 trigger date, with no trial outcome recorded. Do not assume
the trial happened or invent a result here — confirm with Alistair whether the 2-tier
switch was trialed and what was decided, then update the Status line.

This also needs reconciling against the tier counts actually in the skill files, which
disagree with each other: this proposal targets **2 tiers**, the trigger above describes
the current state as **4 tiers** (matching the "Four routing tiers" language in the
global CLAUDE.md Hermes Delegation section), but `skills/model-routing/SKILL.md` as it
stands today documents **5 tiers** (TIER 0 Orchestrator through TIER 4 OpenRouter Paid
fallback). Until this decision is resolved, treat `model-routing/SKILL.md` as the
current source of truth (per the "Status" line above — skills not yet rewritten to 2
tiers).
