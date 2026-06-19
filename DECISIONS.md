# Decisions & Changes — hermes-skills

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
