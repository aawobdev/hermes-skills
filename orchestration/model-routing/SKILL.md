---
name: model-routing
description: >
  Current model roster, routing tiers, and role assignments for Alistair's homelab
  AI setup: RTX 3090 Ti 24GB, LM Studio + Ollama on 192.168.1.123, OpenRouter fallback.
metadata:
  author: Alistair
  version: "1.1.0"
  category: orchestration
  hermes:
    tags: [orchestration, models, routing, lm-studio, ollama, openrouter]
---

# Model Routing

Current AI model roster and routing for Alistair's homelab.

**Hardware**: RTX 3090 Ti 24GB VRAM (desktop at 192.168.1.123)
**Inference**: LM Studio (port 1234) + Ollama (port 11434)
**VRAM note**: LM Studio and Ollama share the GPU. Only one model loaded at a time.
  If LM Studio has a model loaded, Ollama cannot load another.

---

## Model Roster

> Full registry with sizes, quantization, system prompts, and tags: `scripts/tools/owi/models.yaml` in the homelab repo.
> To load into context — Windows: `read_file(path='C:/Users/alistair/Documents/Development/homelab/scripts/tools/owi/models.yaml')` · Linux: `read_file(path='/opt/homelab/scripts/tools/owi/models.yaml')`

### LM Studio models (192.168.1.123:1234)

Context window: **64K for all models** (LM Studio global default — no per-model overrides configured).

| Model | Size | Context | Role fit |
|-------|------|---------|----------|
| `qwen/qwen3.6-35b-a3b` | ~22.1GB MoE | 64k | Architect, Security — thinking model |
| `qwen/qwen3.6-27b` | ~17.5GB dense | 64k | Architect, orchestration — thinking model, Hermes primary |
| `qwen/qwen3-coder-30b` | ~18.6GB MoE | 64k | Developer (same context as Ollama version) |
| `mistralai/devstral-small-2-2512` | ~15.2GB dense | 64k | Developer (same context as Ollama version) |
| `google/gemma-4-31b` | ~19.9GB dense | 64k | General — dense, thorough (no Ollama equivalent) |
| `google/gemma-4-26b-a4b` | ~18GB MoE | 64k | Vision, Tester (same context as Ollama version) |
| `google/gemma-4-e4b` | ~6.3GB | 64k | Fast tasks, End-User (no Ollama equivalent) |

**Thinking models** (qwen3.6-35b-a3b, qwen3.6-27b):
- Set `max_tokens ≥ 4000` — models use ~1700 reasoning tokens before output
- Use `/no_think` prefix for simple/mechanical tasks to skip reasoning overhead
- Expect 80-120s response time for complex tasks
- LM Studio has `separateReasoningContentInAPI: true` — reasoning in `reasoning_content`, answer in `content`

**LMS coder/vision variants** (qwen3-coder-30b, devstral-small-2-2512, gemma-4-26b-a4b):
- Same weights and now same context window as Ollama equivalents
- Only reason to prefer these over Ollama: LM Studio is already loaded and switching would evict the current model

### Ollama models (192.168.1.123:11434)

Context from modelfile (`/api/show`). KV cache: `OLLAMA_KV_CACHE_TYPE=q8_0` (halves KV memory usage).
OWI overrides num_ctx at inference time via parameters.yaml — values below are modelfile defaults (what Hermes sees).

| Model | Size | Quant | Context | Role fit |
|-------|------|-------|---------|----------|
| `devstral-small-2:24b` | ~15.2GB | Q4_K_M | 64k | Developer primary — SWE-bench 68%, agentic |
| `qwen3-coder:30b` | ~18.6GB | Q4_K_M | 64k | Developer — fast MoE coder |
| `gpt-oss:20b` | ~13.8GB | MXFP4 | 64k | General fallback — OpenAI open-weight MoE |
| `gemma4:26b` | ~18GB | Q4_K_M | 32k | Vision + general — multimodal, fast MoE |
| `phi4:14b` | ~9.1GB | Q4_K_M | 16k | Quick STEM/math — model max is 16K |

Note: phi4 modelfile incorrectly specifies 65536 — the model's actual maximum is 16K and OWI enforces this.

---

## Routing

### Backend selection

The context window is now equal across both backends (64K). Backend choice is based on capability, not context:

- **Use LM Studio** when thinking mode matters: architecture decisions, security review, complex multi-step reasoning. The `separateReasoningContentInAPI` output is only available here.
- **Use Ollama** for everything else: coding, vision, quick tasks, math/STEM. Better for multi-model workflows since models can be hot-swapped within Ollama without touching LM Studio.
- **Use Cloud** when local is unavailable or the task requires frontier capability.

```
TIER 1 — Ollama (default for most tasks)
  devstral-small-2:24b → coding, multi-file edits, agentic tasks
  qwen3-coder:30b       → fast coding iteration
  gemma4:26b            → vision tasks, end-user, general
  phi4:14b              → quick STEM, math, routing
  ↓ when: task requires deep reasoning or security analysis

TIER 1 — LM Studio (for thinking-mode tasks, runs alongside Ollama only if VRAM permits)
  qwen3.6-35b-a3b       → best local reasoning, architecture, security
  qwen3.6-27b           → lighter reasoning, Hermes orchestration
  gemma-4-31b           → thorough dense analysis (LMS-exclusive)
  gemma-4-e4b           → fast edge tasks (LMS-exclusive)
  ↓ when: both tiers unavailable

TIER 2 — OpenRouter / Cloud (fallback, cost-controlled)
  deepseek/deepseek-v4-flash → cheap cloud inference (crons, scheduled tasks)
  claude-sonnet              → frontier capability
```

### Role-to-model assignment

| Role | Primary | Fallback 1 | Fallback 2 |
|------|---------|-----------|-----------|
| Architect | `qwen3.6-35b-a3b` (LMS) | `qwen3.6-27b` (LMS) | Claude Sonnet (cloud) |
| Designer | `qwen3.6-27b` (LMS) | `gemma-4-31b` (LMS) | `gpt-oss:20b` (Ollama) |
| Developer | `devstral-small-2:24b` (Ollama) | `qwen3-coder:30b` (Ollama) | Claude Sonnet (cloud) |
| Tester | `gemma4:26b` (Ollama) | `qwen3-coder:30b` (Ollama) | `qwen3.6-27b` (LMS, /no_think) |
| Security | `qwen3.6-35b-a3b` (LMS) | `qwen3.6-27b` (LMS) | Claude Sonnet (cloud) |
| End-User | `gemma4:26b` (Ollama) | `gemma-4-e4b` (LMS) | `qwen3.6-27b` (LMS, /no_think) |

**Backend-aware override**: if LM Studio is already loaded and the task is coding/vision, prefer the LMS equivalent (`qwen3-coder-30b`, `devstral-small-2-2512`, `gemma-4-26b-a4b`) rather than switching backends.

---

## Hermes Configuration

Three instances, all using LM Studio (192.168.1.123:1234) as primary backend:

| Instance | Host | Model endpoint | Skills path |
|----------|------|---------------|-------------|
| Desktop | al.desk.local (Windows) | localhost:1234 | `C:\Users\alistair\hermes-skills\orchestration` |
| Laptop | Windows laptop | 192.168.1.123:1234 | `C:\Users\alistair\hermes-skills\orchestration` |
| VM | ollama.citium.space (Linux) | 192.168.1.123:1234 | `/home/alistair/hermes-skills/orchestration` |

Config source: `opt/config/hermes/` in `aawobdev/homelab`:
- `config.yaml` → VM (sync: `git pull` on the VM)
- `config.laptop.yaml` → Laptop (copy to `%LOCALAPPDATA%\hermes\config.yaml`)
- Desktop config lives at `%LOCALAPPDATA%\hermes\config.yaml` (not tracked, uses localhost)

**Desktop Hermes** (`%LOCALAPPDATA%\hermes\config.yaml`):
```yaml
model:
  provider: custom
  default: qwen/qwen3.6-27b
  base_url: http://localhost:1234/v1
auxiliary:
  vision:
    provider: custom
    model: google/gemma-4-26b-a4b
    base_url: http://localhost:1234/v1
  compression:
    provider: openrouter
    model: deepseek/deepseek-v4-flash
skills:
  external_dirs:
  - C:\Users\alistair\hermes-skills\orchestration
```

**Laptop Hermes** (from `opt/config/hermes/config.laptop.yaml`):
```yaml
model:
  provider: custom
  default: qwen/qwen3.6-27b
  base_url: http://192.168.1.123:1234/v1
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
```

**VM Hermes** (`opt/config/hermes/config.yaml`):
```yaml
model:
  provider: custom
  default: qwen/qwen3.6-27b
  base_url: http://192.168.1.123:1234/v1
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
- name: LM Studio
  base_url: http://192.168.1.123:1234/v1
  model: qwen/qwen3.6-27b
- name: Ollama-Desktop
  base_url: http://192.168.1.123:11434/v1
  model: qwen3-coder:30b
```

---

## Model Lineup Cron Job

Daily cron (job id `7eddc85c`, schedule `0 3 * * *`) on the ollama VM researches, syncs, and reports the model lineup.

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
**Why devstral**: reasoning-heavy cron (8 phases, web research, API calls, Git ops) needs agentic capability beyond cheap cloud models. `devstral-small-2:24b` is the agentic primary (SWE-bench 68%).

**Phases**: Research new models → evaluate fit → update OWI presets → sync OWI → update hermes-skills model-routing skill → sync hermes-skills repo (git pull/commit/push) → report.

---

## Per-Job Model Overrides

To assign a specific model to a cron job without changing the Hermes default:

1. Edit `~/.hermes/cron/jobs.json` on the VM
2. Add `"model": {"provider": "<provider-name>", "model": "<model-name>"}` to the job entry
3. Provider name must match a `custom_providers` entry in `config.yaml` (e.g. `Ollama-Desktop`, `LM Studio`)
4. Restart `hermes-gateway.service` to apply

**When to use**: reasoning-heavy crons (multi-phase research, analysis, Git ops) that need more capability than cheap cloud models. Example: `devstral-small-2:24b` for agentic tasks, `qwen/qwen3.6-27b` for deep reasoning.

---

## Cost Guardrails

- Simple/mechanical crons → cheapest model (`deepseek-v4-flash` via OpenRouter)
- Reasoning-heavy crons → capable local model with per-job override (see above)
- Try local model twice before escalating to cloud
- OpenRouter spend is the signal for "local inference is failing" — monitor it
- `OPENROUTER_API_KEY` must be set in Hermes `.env` on the ollama VM

---

## VRAM Management

Loading order when VRAM is constrained (24GB total):

1. Unload LM Studio model first if switching to Ollama (LM Studio UI → unload button)
2. Or unload Ollama model: `ollama stop [model-name]`
3. Largest models that fit alone: `qwen3.6-35b-a3b` (~22.1GB), `gemma-4-31b` (~19.9GB), `qwen3-coder-30b`/`qwen3-coder:30b` (~18.6GB)
4. Models that allow headroom for 64K KV cache: `qwen3.6-27b` (~17.5GB), `gemma-4-26b-a4b`/`gemma4:26b` (~18GB), `devstral-small-2` (~15.2GB)
5. `gpt-oss:20b` (~13.8GB) and `phi4:14b` (~9.1GB) leave the most headroom
