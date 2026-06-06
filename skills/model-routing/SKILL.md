---
name: model-routing
description: >
  Model roster, routing tiers, and role assignments for a local Ollama + OpenRouter
  setup. Update to match your own hardware and installed models.
metadata:
  author: Alistair
  version: "2.0.0"
  category: orchestration
  hermes:
    tags: [orchestration, models, routing, ollama, openrouter]
---

# Model Routing

Current AI model roster and routing. Update this file to match your own hardware and installed models.

**Inference**: Ollama (port 11434) + OpenRouter (orchestrator only)
**KV cache**: `OLLAMA_KV_CACHE_TYPE=q8_0` recommended for quality/speed balance
**Context windows**: per-model via Modelfile — see registry. Not all models use 64K — see table below.
**Dynamic routing**: use the `model-registry` MCP tool (`list_available_models`, `get_loaded_models`, `get_model_for_role`) for runtime model selection. Prefer loaded (warm) models to avoid VRAM reload latency.

---

## Model Roster

### Ollama models

| Model | Size | Quant | tok/s | ctx | Role fit |
|-------|------|-------|-------|-----|----------|
| `qwen3.6:35b-a3b-q4_K_M` | ~23GB | Q4_K_M | ~104 | **16k** | Architect, Security — thinking model, ~10% CPU offload |
| `qwen3.6:27b-q4_K_M` | ~17GB | Q4_K_M | ~38 | 32k | Architect fallback — thinking model, 2.7× slower (dense) |
| `qwen3-coder:30b` | ~18.6GB | Q4_K_M | ~135 | **32k** | Developer primary |
| `devstral-small-2:24b` | ~15.2GB | Q4_K_M | ~47 | 64k | Developer long-ctx — agentic (SWE-bench 68%) |
| `qwen2.5-coder:32b-instruct` | ~19GB | Q4_K_M | ~tbd | 32k | Developer strong — complex coding |
| `qwen2.5-coder:14b` | ~9GB | Q4_K_M | ~tbd | 64k | Developer fast — single-file, high-volume |
| `glm-4.7-flash` | ~19GB | Q4_K_M | ~tbd | 32k | General fallback |
| `gemma4:26b` | ~18GB | Q4_K_M | ~113 | **32k** | Tester, End-User, Vision |
| `gemma4:e4b-it-q4_K_M` | ~9.6GB | Q4_K_M | ~108 | 64k | Fast tasks, End-User |
| `gpt-oss:20b` | ~13.8GB | MXFP4 | ~127 | 64k | General fallback |
| `phi4:14b` | ~9.1GB | Q4_K_M | ~72 | **16k** | Quick tasks, math/STEM |

**Cloud (OpenRouter)**:
| Model | Role fit |
|-------|----------|
| `deepseek/deepseek-v4-flash` | **Orchestrator** — task decomposition, dynamic model selection, cheap reasoning |

**Thinking models** (`qwen3.6:35b-a3b-q4_K_M`, `qwen3.6:27b-q4_K_M`):
- Set `max_tokens >= 4000` -- models use ~1700 reasoning tokens before output
- Use `/no_think` prefix for simple/mechanical tasks to skip reasoning overhead
- Expect 80-120s response time for complex tasks on 27B; 35B-A3B is faster (~5s/700tok)

**Architecture note -- 35B-A3B vs 27B**: Benchmarked 2026-06-05: 35B-A3B runs at ~104 tok/s; 27B at ~38 tok/s — 2.7× slower despite being smaller.
Both have thinking mode. The 35B-A3B is MoE (~3B active params/token); the 27B is dense (all 27B active every token).
The 35B has ~10% CPU offload (model weights fill 24GB VRAM; no q3 quant available) — this is minor compared to the 2.7× speed penalty of the 27B.
Use 27B only if the 35B is genuinely unavailable; it is slower *and* less capable.

---

## Routing

```
TIER 0 -- OpenRouter (orchestrator only)
  deepseek/deepseek-v4-flash --> Orchestrator (task decomposition, dynamic model selection)
  when: starting a blueprint execution session

TIER 1 -- Ollama (all worker roles)
  qwen3.6:35b-a3b-q4_K_M  --> Architect, Security (thinking mode, ~104 tok/s, 16k ctx)
  qwen3-coder:30b          --> Developer primary (~135 tok/s, 32k ctx)
  devstral-small-2:24b     --> Developer long-ctx (SWE-bench 68%, ~47 tok/s, 64k ctx)
  qwen2.5-coder:14b        --> Developer fast (high-volume, 64k ctx)
  gemma4:26b               --> Tester, End-User, Vision (~113 tok/s, 32k ctx)
  when: local inference exhausted

TIER 2 -- OpenRouter / Cloud (fallback, cost-controlled)
  deepseek/deepseek-v4-flash --> cheap cloud inference (also orchestrator)
  claude-sonnet or gpt-4o    --> frontier tasks (CC-class)
```

### Dynamic model selection (preferred)

Before delegating, the orchestrator should call `get_model_for_role(role)` via the
`model-registry` MCP tool. This returns:
- The canonical model for that role
- Whether it's currently loaded in VRAM (prefer warm models)
- The exact inference params to use

Call `get_loaded_models()` first to check what's warm. If a loaded model can handle the
task, use it rather than triggering a VRAM reload.

### Role-to-model assignment (static defaults)

Use these when the `model-registry` MCP tool is unavailable.

| Role | Primary | Provider | ctx | Fallback 1 | Fallback 2 |
|------|---------|----------|-----|-----------|-----------|
| **Orchestrator** | `deepseek/deepseek-v4-flash` | OpenRouter | — | Claude Sonnet (cloud) | — |
| Architect | `qwen3.6:35b-a3b-q4_K_M` | Ollama | 16k | `qwen3.6:27b-q4_K_M` (32k, 2.7× slower) | Claude Sonnet |
| Designer | `qwen3.6:35b-a3b-q4_K_M` | Ollama | 16k | `qwen3.6:27b-q4_K_M` | Claude Sonnet (blank canvas only) |
| Developer (default) | `qwen3-coder:30b` | Ollama | 32k | `devstral-small-2:24b` (64k) | `qwen2.5-coder:32b-instruct` (32k) |
| Developer (long-ctx) | `devstral-small-2:24b` | Ollama | 64k | `qwen3-coder:30b` | — |
| Developer (fast) | `qwen2.5-coder:14b` | Ollama | 64k | `qwen3-coder:30b` | — |
| Tester | `gemma4:26b` | Ollama | 32k | `qwen3-coder:30b` | `qwen3.6:35b-a3b-q4_K_M` |
| DevOps | `qwen3-coder:30b` | Ollama | 32k | `devstral-small-2:24b` | `qwen3.6:35b-a3b-q4_K_M` |
| Security | `qwen3.6:35b-a3b-q4_K_M` | Ollama | 16k | `qwen3.6:27b-q4_K_M` | Claude Sonnet |
| End-User | `gemma4:26b` | Ollama | 32k | `gemma4:e4b-it-q4_K_M` | `qwen3.6:27b-q4_K_M` |

**Developer model choice guide**:
- Single-file, high-volume, fast iteration → `qwen2.5-coder:14b` (64k, generous headroom)
- Standard multi-task blueprint work → `qwen3-coder:30b` (32k, ~135 tok/s)
- Multi-file agentic sessions hitting 32k+ context → `devstral-small-2:24b` (64k, dense)
- Complex reasoning + coding → `qwen2.5-coder:32b-instruct` (32k, deepest code quality)

---

## Hermes Configuration

Example config for a local Ollama setup. Adjust `base_url`, `default` model, and
`skills.external_dirs` to match your environment.

**Local Ollama** (add to your Hermes config):
```yaml
model:
  provider: custom
  default: qwen3.6:35b-a3b-q4_K_M   # change to your preferred default
  base_url: http://localhost:11434/v1
auxiliary:
  vision:
    provider: custom
    model: gemma4:26b
    base_url: http://localhost:11434/v1
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash
skills:
  external_dirs:
  - ~/hermes-skills/orchestration     # Linux/Mac
  # - C:\Users\<you>\hermes-skills\orchestration   # Windows
custom_providers:
- name: Ollama-Local
  base_url: http://localhost:11434/v1
  model: qwen3-coder:30b
```

**Remote Ollama** (Ollama on a separate machine):
```yaml
model:
  provider: custom
  default: qwen3.6:35b-a3b-q4_K_M
  base_url: http://<ollama-host>:11434/v1
auxiliary:
  vision:
    provider: custom
    model: gemma4:26b
    base_url: http://<ollama-host>:11434/v1
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash
skills:
  external_dirs:
  - ~/hermes-skills/orchestration
custom_providers:
- name: Ollama-Remote
  base_url: http://<ollama-host>:11434/v1
  model: qwen3-coder:30b
```

---

## Sampling / Generation Parameters

Set generation parameters to match the task type (see `prompting-standards` A13/B8):

| Task type | Temperature | Examples |
|-----------|-------------|----------|
| Deterministic | ~0 | code generation, refactors, config, data extraction, pipelines |
| Balanced | ~0.3–0.7 | prose, docs, test-case ideation |
| Divergent | ~0.7–1.0 | brainstorming, naming, design exploration |

Code and structured output should almost never run hot. For thinking models, also set
`max_tokens ≥ 4000` so reasoning (~1700 tokens) plus the answer both fit.

---

## Model Lineup Cron Job

A daily cron (`0 3 * * *`) can be set up to automatically research, evaluate, and sync
the model lineup — keeping this skill file up to date without manual effort.

**Typical phases**: Research new releases → evaluate fit for each role → update model
presets → sync repos (git pull/commit/push) → deliver report.

**Model override**: Use `devstral-small-2:24b` for reasoning-heavy crons (multi-phase
research, API calls, Git ops). It's slower for interactive use (~47 tok/s) but its
SWE-bench 68% score makes it the right pick for multi-step agentic work.

**Per-job model override** (in `~/.hermes/cron/jobs.json`):
```json
{
  "model": { "provider": "Ollama-Local", "model": "devstral-small-2:24b" }
}
```
This does NOT change the Hermes default — only the specific cron job uses it.

**Toolsets**: `['web', 'terminal', 'file', 'search']`.
**Delivery**: configure `deliver` in the job to send the report to your preferred channel.

---

## Per-Job Model Overrides

To assign a specific model to a cron job without changing the Hermes default:

1. Edit `~/.hermes/cron/jobs.json` on the VM
2. Add `"model": {"provider": "<provider-name>", "model": "<model-name>"}` to the job entry
3. Provider name must match a `custom_providers` entry in `config.yaml` (e.g. `Ollama-Desktop`)
4. Restart `hermes-gateway.service` to apply

**When to use**: reasoning-heavy crons (multi-phase research, analysis, Git ops) that need more capability than cheap cloud models. Example: `devstral-small-2:24b` for agentic tasks, `qwen3.6:27b-q4_K_M` for deep reasoning.

---

## Cost Guardrails

- Simple/mechanical crons → cheapest model (`deepseek-v4-flash` via OpenRouter)
- Reasoning-heavy crons → capable local model with per-job override (see above)
- Try local model twice before escalating to cloud
- OpenRouter spend is the signal for "local inference is failing" — monitor it
- `OPENROUTER_API_KEY` must be set in Hermes `.env` on the machine running the orchestrator

---

## VRAM Management

Loading order when VRAM is constrained (24GB total, ~0.5GB idle baseline):

1. Unload LM Studio model first if switching to Ollama (LM Studio UI → unload, or via v1 API)
2. Or unload Ollama model: `ollama stop [model-name]`

Measured VRAM above idle baseline (q8_0 KV cache at each model's capped context):

| Model | Weights | ctx cap | KV cache | Total | Headroom |
|-------|---------|---------|----------|-------|----------|
| `qwen3.6:35b-a3b-q4_K_M` | ~23 GB | **16k** | ~1.5 GB | ~24.5 GB | ~0 — 10% CPU offload |
| `qwen3-coder:30b` | ~18.6 GB | **32k** | ~3.0 GB | ~21.6 GB | ~2.4 GB |
| `devstral-small-2:24b` | ~15.2 GB | 64k | ~8.0 GB | ~23.2 GB | ~0.8 GB |
| `qwen2.5-coder:32b-instruct` | ~19 GB | **32k** | ~4.0 GB | ~23 GB | ~1 GB |
| `qwen2.5-coder:14b` | ~9 GB | 64k | ~4.0 GB | ~13 GB | ~11 GB |
| `glm-4.7-flash` | ~19 GB | **32k** | ~4.0 GB | ~23 GB | ~1 GB |
| `gemma4:26b` | ~18 GB | **32k** | ~3.0 GB | ~21 GB | ~3 GB |
| `qwen3.6:27b-q4_K_M` | ~17 GB | **32k** | ~4.0 GB | ~21 GB | ~3 GB |
| `gpt-oss:20b` | ~13.5 GB | 64k | ~4.0 GB | ~17.5 GB | ~6.5 GB |
| `gemma4:e4b-it-q4_K_M` | ~9.6 GB | 64k | ~2.0 GB | ~11.6 GB | ~12.4 GB |
| `phi4:14b` | ~9.1 GB | **16k** | ~1.0 GB | ~10.1 GB | ~13.9 GB |
