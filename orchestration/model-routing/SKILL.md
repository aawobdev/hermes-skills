---
name: model-routing
description: >
  Current model roster, routing tiers, and role assignments for Alistair's homelab
  AI setup: RTX 3090 Ti 24GB, LM Studio + Ollama on 192.168.1.123, OpenRouter fallback.
metadata:
  author: Alistair
  version: "1.0.0"
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
> To load into context — Windows: `read_file(path='C:/Users/alistair/Documents/Dev/homelab/scripts/tools/owi/models.yaml')` · Linux: `read_file(path='/opt/homelab/scripts/tools/owi/models.yaml')`

### LM Studio models (192.168.1.123:1234)

| Model | Size | tok/s | Context | Role fit |
|-------|------|-------|---------|----------|
| `qwen/qwen3-coder-30b` | ~18.6GB MoE | ~148 | 256k | Developer primary |
| `qwen/qwen3.6-35b-a3b` | ~22.1GB MoE | ~135 | 256k | Architect, Security — thinking model |
| `qwen/qwen3.6-27b` | ~17.5GB dense | ~38 | 256k | Architect fallback — thinking model, slow (dense) |
| `mistralai/devstral-small-2-2512` | ~15.2GB | ~46 | 384k | Developer fallback (long context) |
| `google/gemma-4-26b-a4b` | ~18GB MoE | ~113 | 256k | Vision, Tester, End-User |
| `google/gemma-4-e4b` | ~6.3GB | ~108 | 128k | Fast tasks, End-User |
| `google/gemma-4-31b` | ~19.9GB dense | ~22 | 256k | Avoid for interactive use — too slow |

**Architecture note — 35B-A3B vs 27B**: The 35B-A3B runs at ~135 tok/s and the 27B at ~38 tok/s despite being larger.
Both have thinking mode. The 35B-A3B is MoE (~3B active params/token); the 27B is dense (all 27B active every token).
Prefer 35B-A3B unless VRAM is critically constrained (35B needs ~22.1GB vs 27B's ~17.5GB).

**Thinking models** (qwen3.6-35b-a3b, qwen3.6-27b):
- Set `max_tokens ≥ 4000` — models use ~1700 reasoning tokens before output
- Use `/no_think` prefix for simple/mechanical tasks to skip reasoning overhead
- Expect 80-120s response time for complex tasks on 27B; 35B-A3B is faster (~5s/700tok)
- LM Studio has `separateReasoningContentInAPI: true` — reasoning in `reasoning_content`, answer in `content`

**KV cache**: All LM Studio models configured with `q8_0` KV cache (K + V) via per-model load config.
`useFp16ForKVCache` disabled. Reduces VRAM by ~10-15% vs fp16 default.

### Ollama models (192.168.1.123:11434)

| Model | Size | Quant | tok/s | Context | Role fit |
|-------|------|-------|-------|---------|----------|
| `qwen3-coder:30b` | ~18.6GB | Q4_K_M | ~135 | 64k | Developer (Ollama-side) |
| `gemma4:26b` | ~18GB | Q4_K_M | ~113 | 32k | Tester, End-User, Vision |
| `gpt-oss:20b` | ~13.8GB | MXFP4 | ~127 | 64k | General fallback (TTFT spikes noted) |
| `devstral-small-2:24b` | ~15.2GB | Q4_K_M | ~47 | 64k | Developer fallback |
| `phi4:14b` | ~9.1GB | Q4_K_M | ~72 | 16k | Quick tasks, math/STEM |

**KV cache**: `OLLAMA_KV_CACHE_TYPE=q8_0` set in User environment.

---

## Routing Tiers

```
TIER 1 — LM Studio (reasoning AND code execution)
  qwen3.6-35b-a3b → Architect, Security (thinking mode, ~135 tok/s)
  qwen3-coder-30b → Developer primary (~148 tok/s, fastest local coder)
  ↓ when: LM Studio unavailable, or VRAM needed for other model

TIER 2 — Ollama (fallback for code; primary for Tester/End-User)
  qwen3-coder:30b → Developer fallback (~135 tok/s)
  gemma4:26b     → Tester, End-User (~113 tok/s)
  ↓ when: both local options exhausted

TIER 3 — OpenRouter / Cloud (fallback, cost-controlled)
  deepseek/deepseek-v4-flash → cheap cloud inference
  ↓ when: deeper capability needed
  claude-sonnet or gpt-4o → frontier tasks
```

---

## Role-to-Model Assignment

| Role | Primary | tok/s | Fallback 1 | Fallback 2 |
|------|---------|-------|-----------|-----------|
| Architect | `qwen3.6-35b-a3b` (LMS) | ~135 | `qwen3.6-27b` (LMS, ~38) | Claude Sonnet (cloud) |
| Designer | `qwen3.6-35b-a3b` (LMS) | ~135 | `qwen3.6-27b` (LMS, ~38) | `gemma4:26b` (Ollama, ~113) |
| Developer | `qwen3-coder-30b` (LMS) | ~148 | `qwen3-coder:30b` (Ollama, ~135) | `devstral-small-2:24b` (Ollama, ~47) |
| Tester | `gemma4:26b` (Ollama) | ~113 | `qwen3-coder:30b` (Ollama, ~135) | `qwen3.6-35b-a3b` (LMS, ~135) |
| DevOps | `qwen3-coder-30b` (LMS) | ~148 | `qwen3-coder:30b` (Ollama, ~135) | `qwen3.6-35b-a3b` (LMS, ~135) for release-risk reasoning |
| Security | `qwen3.6-35b-a3b` (LMS) | ~135 | `qwen3.6-27b` (LMS, ~38) | Claude Sonnet (cloud) |
| End-User | `gemma4:26b` (Ollama) | ~113 | `gemma-4-e4b` (LMS, ~108) | `qwen3.6-27b` (LMS, /no_think, ~38) |

**Developer note**: `qwen3-coder-30b` (LMS) is now the fastest local coder at ~148 tok/s — faster than
the Ollama version of the same weights (~135 tok/s) due to LM Studio's q8_0 KV cache + backend differences.
Devstral is the last resort; it's dense and runs at only ~47 tok/s.

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

## Sampling / Generation Parameters

Set generation parameters to match the task type (see `prompting-standards` A13/B8):

| Task type | Temperature | Examples |
|-----------|-------------|----------|
| Deterministic | ~0 | code generation, refactors, config, data extraction, pipelines |
| Balanced | ~0.3–0.7 | prose, docs, test-case ideation |
| Divergent | ~0.7–1.0 | brainstorming, naming, design exploration |

Code and structured output should almost never run hot. For thinking models, also set
`max_tokens ≥ 4000` so reasoning (~1700 tokens) plus the answer both fit.

## Cost Guardrails

- Crons and scheduled tasks → always use cheapest model (`deepseek-v4-flash` via OpenRouter)
- Try local model twice before escalating to cloud
- OpenRouter spend is the signal for "local inference is failing" — monitor it
- `OPENROUTER_API_KEY` must be set in Hermes `.env` on the ollama VM

---

## VRAM Management

Loading order when VRAM is constrained (24GB total, ~0.5GB idle baseline):

1. Unload LM Studio model first if switching to Ollama (LM Studio UI → unload, or via v1 API)
2. Or unload Ollama model: `ollama stop [model-name]`

Measured VRAM above idle baseline (q8_0 KV cache, 65k context):

| Model | VRAM above baseline | Headroom left |
|-------|-------------------|---------------|
| `qwen3.6-35b-a3b` (LMS) | ~21.6 GB | ~2 GB — tight |
| `gemma-4-31b` (LMS) | ~21.5 GB | ~2 GB — tight, slow (22 tok/s) |
| `qwen3-coder-30b` (LMS) | ~20.9 GB | ~3 GB |
| `devstral-small-2` (LMS/Ollama) | ~19.8–20 GB | ~4 GB |
| `gemma-4-26b-a4b` / `gemma4:26b` | ~18.8–19 GB | ~5 GB |
| `qwen3.6-27b` (LMS) | ~19.3 GB | ~5 GB |
| `gpt-oss:20b` (Ollama) | ~13.5 GB | ~10 GB |
| `phi4:14b` (Ollama) | ~11.0 GB | ~13 GB |
| `gemma-4-e4b` (LMS) | ~5.4 GB | ~18 GB |
