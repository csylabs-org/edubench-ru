# Changelog

## v0.3 — 3-Judge Panel + Qwen3-32B Comparison (March 25, 2026)

### Scoring Methodology Change: 2 → 3 Judges

**Previous (v0.2):** 2-judge panel — GPT-5.4 + Claude Sonnet 4.6 via OpenRouter.

**Current (v0.3):** 3-judge panel — GPT-5.4 + Claude Sonnet 4.6 + **Gemini 3.1 Pro** (direct Google API with structured output).

All 30 models rescored with all 3 judges for consistency. Final scores are consensus averages across the full judge panel.

**Why the change:**
- Reduces single-judge bias (GPT-5.4 tended to score higher on actionability, Gemini stricter on factual accuracy)
- Gemini 3.1 Pro added via official Google API with `responseMimeType: application/json` + `responseSchema` for reliable structured output
- OpenRouter `response_format` with `json_schema` also works for Gemini but requires `max_tokens >= 4096` (reasoning tokens consume budget)

**Impact on rankings:** Most models moved ±1-2 positions. EduLLM-RU 27B moved from #11 (2-judge) to #9 (3-judge, score 3.21). The Gemini judge generally scored Modules A-C higher and Module D lower than the other judges.

### New Models Added

- **EduLLM-RU 32B Q6_K** — Qwen3-32B + education LoRA, GGUF Q6_K via llama-server. Rank #17 (2.69). Training: 45.4h on RTX PRO 6000 Blackwell.
- **Qwen3 32B Base Q6_K** — Control run for the 32B comparison.

### Key Finding: Architecture > Parameters

| Model | Params | Score | Training Loss |
|-------|--------|:-----:|:------------:|
| EduLLM-RU 27B (Qwen3.5) | 27B | **3.21** | 0.51 |
| EduLLM-RU 32B (Qwen3) | 32B | 2.69 | 0.47 |

Despite lower training loss, the 32B scored 0.52 points lower. The Qwen3.5 architecture (newer generation) outperforms Qwen3 (older) regardless of parameter count. Same training data, same LoRA config, same hardware.

**Decision:** Ship Qwen3.5-27B as the production EduLLM-RU model.

### Technical Notes

- Gemini 3.1 Pro scoring via direct API: `generativelanguage.googleapis.com/v1beta` with `responseSchema` for guaranteed JSON
- `max_tokens: 512` causes truncated JSON with Gemini (reasoning tokens eat budget) — use `max_tokens: 4096`
- Parallelized scoring: 5 workers for 26 models completed in ~15 minutes
- `llm_judge.py` fixed: model name matching now normalizes dashes in both search term and filename

---

## v0.2 — 28-Model Leaderboard + Russian LLMs + EduLLM-RU (March 23, 2026)

### Models Added
- 5 Russian cloud LLMs: GigaChat-2 Pro/Max/Lite, YandexGPT 5.1 Pro, YandexGPT 5 Lite
- EduLLM-RU Q6_K (Qwen3.5-27B + education LoRA) — self-hosted via llama-server

### Scoring
- 2-judge panel: GPT-5.4 + Claude Sonnet 4.6 (via OpenRouter)
- 50 prompts × 28 models × 2 judges = 2,800 scoring calls

### Key Finding
- All Russian cloud LLMs ranked #19-27 — optimized for chat, not pedagogy
- EduLLM-RU (#11) beats all Russian cloud LLMs despite being a 27B self-hosted model

---

## v0.1 — Initial Release (March 21, 2026)

### Benchmark
- 50 prompts across 4 modules (A: Pedagogy, B: Subject Knowledge, C: Teacher Copilot, D: ChuvashBench)
- 5-dimension rubric (6 for Module D)

### Models
- 22 frontier + open-source models via OpenRouter
- Single judge: GPT-5.4

### Scoring
- LLM-as-judge with GPT-5.4
- Per-dimension scores saved to `data/scores/`
