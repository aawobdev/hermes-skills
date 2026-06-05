---
name: model-routing
description: >
  Current model roster, routing tiers, and role assignments for Alistair's homelab
  AI setup: RTX 3090 Ti 24GB, Ollama on 192.168.1.123, OpenRouter fallback.
metadata:
  author: Alistair
  version: "2.0.0"
  category: orchestration
  hermes:
    tags: [orchestration, models, routing, ollama, openrouter]
---

# Model Routing

Current AI model roster and routing for Alistair's homelab.

**Hardware**: RTX 3090 Ti 24GB VRAM (desktop at 192.168.1.123)
**Inference**: Ollama only (port 11434) — all models loaded via Modelfile with 64K context
**KV cache**: `OLLAMA_KV_CACHE_TYPE=q8_0` set in User environment on desktop

---

## Model Roster

> Full registry with sizes, quantization, system prompts, and tags: `scripts/tools/owi/models.yaml` in the homelab repo.
> To load into context — Windows: `read_file(path='C:/Users/alistair/Documents/Development/homelab/scripts/tools/owi/models.yaml')` · Linux: `read_file(path='/opt/homelab/scripts/tools/owi/models.yaml')`

### Ollama models (192.168.1.123:11434)

| Model | Size | Quant | tok/s | Context | Role fit |
|-------|------|-------|-------|---------|----------|
| `qwen3.6:35b-a3b-q4_K_M` | ~23GB | Q4_K_M | ~104 | 64k | Architect, Security, **Hermes default** — thinking model, ~10% CPU offload |
| `qwen3.6:27b-q4_K_M` | ~17GB | Q4_K_M | ~38 | 64k | Architect fallback — thinking model, 2.7× slower (dense), use only if 35b unavailable |
| `qwen3-coder:30b` | ~18.6GB | Q4_K_M | ~135 | 64k | Developer primary |
| `gemma4:26b` | ~18GB | Q4_K_M | ~113 | 64k | Tester, End-User, Vision |
| `gemma4:e4b-it-q4_K_M` | ~9.6GB | Q4_K_M | ~108 | 64k | Fast tasks, End-User |
| `devstral-small-2:24b` | ~15.2GB | Q4_K_M | ~47 | 64k | Developer fallback — agentic (SWE-bench 68%) |
| `gpt-oss:20b` | ~13.8GB | MXFP4 | ~127 | 64k | General fallback |
| `phi4:14b` | ~9.1GB | Q4_K_M | ~72 | 16k | Quick tasks, math/STEM |

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
TIER 1 -- Ollama (all roles)
  qwen3.6:35b-a3b-q4_K_M --> Architect, Security, Hermes default (thinking mode, ~104 tok/s)
  qwen3-coder:30b         --> Developer primary (~135 tok/s)
  gemma4:26b              --> Tester, End-User, Vision (~113 tok/s)
  when: local inference exhausted

TIER 2 -- OpenRouter / Cloud (fallback, cost-controlled)
  deepseek/deepseek-v4-flash --> cheap cloud inference
  when: deeper capability needed
  claude-sonnet or gpt-4o --> frontier tasks
```

### Role-to-model assignment

| Role | Primary | tok/s | Fallback 1 | Fallback 2 |
|------|---------|-------|-----------|-----------|
| Orchestrator | `qwen3.6:35b-a3b-q4_K_M` | ~104 | Claude Sonnet (cloud) | — |
| Architect | `qwen3.6:35b-a3b-q4_K_M` | ~104 | `qwen3.6:27b-q4_K_M` (~38, 2.7× slower — last resort) | Claude Sonnet (cloud) |
| Designer | `qwen3.6:35b-a3b-q4_K_M` | ~104 | `qwen3.6:27b-q4_K_M` (~38, 2.7× slower — last resort) | Claude Sonnet (cloud -- blank canvas only) |
| Developer | `qwen3-coder:30b` | ~135 | `devstral-small-2:24b` (~47) | `qwen3.6:35b-a3b-q4_K_M` (~135) |
| Tester | `gemma4:26b` | ~113 | `qwen3-coder:30b` (~135) | `qwen3.6:35b-a3b-q4_K_M` (~135) for complex testing |
| DevOps | `qwen3-coder:30b` | ~135 | `devstral-small-2:24b` (~47) | `qwen3.6:35b-a3b-q4_K_M` (~135) for release-risk reasoning |
| Security | `qwen3.6:35b-a3b-q4_K_M` | ~104 | `qwen3.6:27b-q4_K_M` (~38, 2.7× slower — last resort) | Claude Sonnet (cloud) |
| End-User | `gemma4:26b` | ~113 | `gemma4:e4b-it-q4_K_M` (~108) | `qwen3.6:27b-q4_K_M` (/no_think, ~38) |

**Developer note**: `qwen3-coder:30b` is the primary coder at ~135 tok/s. Devstral is the fallback for multi-file
agentic work (SWE-bench 68%) but runs at only ~47 tok/s -- use it when qwen3-coder struggles with complex multi-step tasks.

---

## Hermes Configuration

Three instances, all using Ollama (192.168.1.123:11434) as primary backend:

| Instance | Host | Model endpoint | Skills path |
|----------|------|---------------|-------------|
| Desktop | al.desk.local (Windows) | localhost:11434 | `C:\Users\Alistair\Documents\Development\hermes-skills\orchestration` |
| Laptop | Windows laptop | 192.168.1.123:11434 | `C:\Users\Alistair\Documents\Development\hermes-skills\orchestration` |
| VM | ollama.citium.space (Linux) | 192.168.1.123:11434 | `/home/alistair/hermes-skills/orchestration` |

Config source: `opt/config/hermes/` in `aawobdev/homelab`:
- `config.yaml` → VM (sync: `git pull` on the VM)
- `config.laptop.yaml` → Laptop (copy to `%LOCALAPPDATA%\hermes\config.yaml`)
- Desktop config lives at `%LOCALAPPDATA%\hermes\config.yaml` (not tracked, uses localhost)

**Desktop Hermes** (`%LOCALAPPDATA%\hermes\config.yaml`):
```yaml
model:
  provider: custom
  default: qwen3.6:35b-a3b-q4_K_M
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
  - C:\Users\alistair\hermes-skills\orchestration
custom_providers:
- name: Ollama-Desktop
  base_url: http://localhost:11434/v1
  model: qwen3-coder:30b
```

**Laptop Hermes** (`~\.hermes\config.yaml`, tracked in `opt/config/hermes/config.laptop.yaml`):
```yaml
model:
  provider: custom
  default: qwen3.6:35b-a3b-q4_K_M
  base_url: http://192.168.1.123:11434/v1
auxiliary:
  vision:
    provider: custom
    model: gemma4:26b
    base_url: http://192.168.1.123:11434/v1
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash
skills:
  external_dirs:
  - C:\Users\alistair\hermes-skills\orchestration
custom_providers:
- name: Ollama-Desktop
  base_url: http://192.168.1.123:11434/v1
  model: qwen3-coder:30b
```

**VM Hermes** (`~/.hermes/config.yaml`, tracked in `opt/config/hermes/config.yaml`):
```yaml
model:
  provider: custom
  default: qwen3.6:35b-a3b-q4_K_M
  base_url: http://192.168.1.123:11434/v1
auxiliary:
  vision:
    provider: custom
    model: gemma4:26b
    base_url: http://192.168.1.123:11434/v1
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash
skills:
  external_dirs:
  - /home/alistair/hermes-skills/orchestration
custom_providers:
- name: Ollama-Desktop
  base_url: http://192.168.1.123:11434/v1
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

Daily cron (job id `7eddc85c`, schedule `0 3 * * *`) runs on the **ollama VM** (`ollama.citium.space`) and researches, syncs, and reports the model lineup.

**Prompt source**: `scripts/cron/model-lineup-prompt.txt` in the homelab repo (committed, branch `main`).
**Also on VM at**: `/opt/homelab/scripts/cron/model-lineup-prompt.txt` (copied from repo).
**Runtime prompt stored in**: `~/.hermes/cron/jobs.json` (in-memory copy used by the scheduler).

**Three-place sync when editing the prompt**:
1. Edit the file on the VM (`/opt/homelab/scripts/cron/model-lineup-prompt.txt`)
2. Copy back to Windows repo via `scp` and commit/push to `aawobdev/homelab` branch `main`
3. Update `jobs.json` on the VM (Python: patch the `prompt` field of job id `7eddc85c`)

**Delivery**: `deliver: ['all']` — sends final report to Slack automatically.
**Toolsets**: `['web', 'terminal', 'file', 'search']`.
**Workdir**: `/opt/homelab`.
**Model override**: `devstral-small-2:24b` via `Ollama-Desktop` provider (set in `jobs.json` under `model` key — does NOT change the Hermes default).
**Why devstral**: reasoning-heavy cron (8 phases, web research, API calls, Git ops) needs agentic capability. `devstral-small-2:24b` is slow for interactive use (~47 tok/s) but its SWE-bench 68% score makes it the right pick for multi-step agentic work.

**Phases**: Research new models → evaluate fit → update OWI presets → sync OWI → update hermes-skills model-routing skill → sync hermes-skills repo (git pull/commit/push) → report.

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
- `OPENROUTER_API_KEY` must be set in Hermes `.env` on the ollama VM

---

## VRAM Management

Loading order when VRAM is constrained (24GB total, ~0.5GB idle baseline):

1. Unload LM Studio model first if switching to Ollama (LM Studio UI → unload, or via v1 API)
2. Or unload Ollama model: `ollama stop [model-name]`

Measured VRAM above idle baseline (q8_0 KV cache, 64k context):

| Model | VRAM above baseline | Headroom left |
|-------|-------------------|---------------|
| `qwen3.6:35b-a3b-q4_K_M` | ~23 GB | ~1 GB — tight |
| `qwen3-coder:30b` | ~18.6 GB | ~5 GB |
| `devstral-small-2:24b` | ~15.2 GB | ~8 GB |
| `gemma4:26b` | ~18 GB | ~5 GB |
| `qwen3.6:27b-q4_K_M` | ~17 GB | ~7 GB |
| `gpt-oss:20b` | ~13.5 GB | ~10 GB |
| `gemma4:e4b-it-q4_K_M` | ~9.6 GB | ~14 GB |
| `phi4:14b` | ~9.1 GB | ~14 GB |
