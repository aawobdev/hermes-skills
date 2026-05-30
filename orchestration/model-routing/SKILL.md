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

### LM Studio models (192.168.1.123:1234)

| Model | Size | Context | Role fit |
|-------|------|---------|----------|
| `qwen/qwen3.6-35b-a3b` | ~22.1GB MoE | 256k | Architect, Security — thinking model |
| `qwen/qwen3.6-27b` | ~17.5GB | 256k | Architect, orchestration — thinking model |
| `qwen/qwen3-coder-30b` | ~18.6GB MoE | 256k | Developer (long context) |
| `mistralai/devstral-small-2-2512` | ~15.2GB | 384k | Developer (long context) |
| `google/gemma-4-31b` | ~19.9GB | 256k | General (dense, thorough) |
| `google/gemma-4-26b-a4b` | ~18GB MoE | 256k | Vision, Tester, End-User |
| `google/gemma-4-e4b` | ~6.3GB | 128k | Fast tasks, End-User |

**Thinking models** (qwen3.6-35b-a3b, qwen3.6-27b):
- Set `max_tokens ≥ 4000` — models use ~1700 reasoning tokens before output
- Use `/no_think` prefix for simple/mechanical tasks to skip reasoning overhead
- Expect 80-120s response time for complex tasks
- LM Studio has `separateReasoningContentInAPI: true` — reasoning in `reasoning_content`, answer in `content`

### Ollama models (192.168.1.123:11434)

| Model | Size | Context | Role fit |
|-------|------|---------|----------|
| `devstral-small-2:24b` | ~15.2GB Q4 | 128k | Developer primary |
| `qwen3-coder:30b` | ~18.6GB | 64k | Developer fallback |
| `gpt-oss:20b` | ~13.8GB MXFP4 | 64k | General fallback |
| `gemma4:26b` | ~18GB | 32k | Tester, End-User, Vision |
| `phi4:14b` | ~9.1GB | 16k | Quick tasks, routing, math/STEM |

**KV cache**: `OLLAMA_KV_CACHE_TYPE=q8_0` set in User environment (restart Ollama to activate)

---

## Routing Tiers

```
TIER 1 — LM Studio (default for reasoning tasks)
  qwen3.6-35b-a3b → best local reasoning, thinking mode
  ↓ when: model too large for current VRAM state, or Ollama needed

TIER 2 — Ollama (default for code execution tasks)
  devstral-small-2:24b → code-focused, fast
  ↓ when: VRAM conflict with LM Studio, or task needs pure speed

TIER 3 — OpenRouter / Cloud (fallback, cost-controlled)
  deepseek/deepseek-v4-flash → cheap cloud inference
  ↓ when: both local options unavailable
  claude-sonnet or gpt-4o → for tasks requiring frontier capability
```

---

## Role-to-Model Assignment

| Role | Primary | Fallback 1 | Fallback 2 |
|------|---------|-----------|-----------|
| Architect | `qwen3.6-35b-a3b` (LMS) | `qwen3.6-27b` (LMS) | Claude Sonnet (cloud) |
| Designer | `qwen3.6-35b-a3b` (LMS) | `qwen3.6-27b` (LMS) | `gemma4:26b` (Ollama) |
| Developer | `devstral-small-2:24b` (Ollama) | `qwen3-coder:30b` (Ollama) | `qwen3-coder-30b` (LMS, 256k) |
| Tester | `gemma4:26b` (Ollama) | `qwen3-coder:30b` (Ollama) | `qwen3.6-35b-a3b` (LMS) |
| Security | `qwen3.6-35b-a3b` (LMS) | `qwen3.6-27b` (LMS) | Claude Sonnet (cloud) |
| End-User | `gemma4:26b` (Ollama) | `gemma-4-e4b` (LMS) | `qwen3.6-27b` (LMS, /no_think) |

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

## Cost Guardrails

- Crons and scheduled tasks → always use cheapest model (`deepseek-v4-flash` via OpenRouter)
- Try local model twice before escalating to cloud
- OpenRouter spend is the signal for "local inference is failing" — monitor it
- `OPENROUTER_API_KEY` must be set in Hermes `.env` on the ollama VM

---

## VRAM Management

Loading order when VRAM is constrained (24GB total):

1. Unload LM Studio model first if switching to Ollama (LM Studio UI → unload button)
2. Or unload Ollama model: `ollama stop [model-name]`
3. Largest models that fit alone: `qwen3.6-35b-a3b` (~22.1GB), `gemma-4-31b` (~19.9GB), `qwen3-coder-30b`/`qwen3-coder:30b` (~18.6GB)
4. Models that allow headroom for system: `qwen3.6-27b` (~17.5GB), `gemma-4-26b-a4b`/`gemma4:26b` (~18GB), `devstral-small-2` (~15.2GB)
5. `gpt-oss:20b` (~13.8GB) and `phi4:14b` (~9.1GB) leave the most headroom
