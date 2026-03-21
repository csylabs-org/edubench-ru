# EduBench-RU — Benchmark Results Summary

**Date:** March 21, 2026
**Models:** 22 API (via OpenRouter) + 3 local (LM Studio)
**Prompts:** 50 (Module A: 15, B: 10, C: 10, D: 15)
**max_tokens:** 8,192 | **temperature:** 0.7
**Total output tokens:** 2,421,700
**Total API cost:** $18.69

---

## Performance Overview

| Model                          |    Tokens |  tok/s | Avg Time |    Cost | Open |  VRAM |
|-------------------------------|----------|-------|---------|--------|-----|------|
| Qwen3.5 27B                    |   334,783 |   76.5 |   81.9s | $  0.52 |  Yes |  18GB |
| Gemini 2.5 Pro                 |   205,307 |  106.0 |   38.8s | $  2.05 |   No |   API |
| Kimi K2.5                      |   195,804 |   56.3 |  103.5s | $  0.43 |   No |   API |
| GLM 4.7 Flash                  |   164,416 |   78.8 |   45.0s | $  0.07 |  Yes |  20GB |
| Gemini 3.1 Pro                 |   150,307 |   76.7 |   45.3s | $  1.80 |   No |   API |
| Claude Sonnet 4.6              |   123,324 |   57.5 |   42.5s | $  1.85 |   No |   API |
| Claude Opus 4.6                |   121,848 |   55.3 |   43.4s | $  9.14 |   No |   API |
| Qwen3 32B                      |   105,695 |   60.1 |   44.3s | $  0.03 |  Yes |  20GB |
| Gemini 2.5 Flash               |   104,391 |  165.7 |   12.4s | $  0.26 |   No |   API |
| Grok 4.1 Fast                  |    98,618 |  102.0 |   19.5s | $  0.05 |   No |   API |
| Qwen3 235B A22B                |    94,519 |   57.6 |   34.7s | $  0.17 |  Yes | 128GB |
| Qwen3 8B                       |    94,150 |   64.9 |   30.1s | $  0.04 |  Yes |   6GB |
| Qwen3 14B                      |    93,526 |   42.2 |   61.2s | $  0.02 |  Yes |  10GB |
| GPT-5.4                        |    84,561 |   65.5 |   25.0s | $  1.27 |   No |   API |
| DeepSeek V3.2                  |    78,499 |   24.6 |  107.3s | $  0.03 |  Yes |   API |
| GLM 5                          |    76,535 |   46.9 |   48.6s | $  0.18 |   No |   API |
| Mistral Large 3                |    75,076 |   52.0 |   28.7s | $  0.11 |  Yes |  72GB |
| GPT-5.4 Mini                   |    61,667 |  165.8 |    6.9s | $  0.28 |   No |   API |
| Phi-4 14B                      |    58,700 |   77.0 |   16.7s | $  0.01 |  Yes |  10GB |
| Gemini 3.1 Flash Lite          |    43,518 |  155.1 |    5.8s | $  0.07 |   No |   API |
| Command A                      |    30,151 |   37.2 |   19.5s | $  0.30 |   No |   API |
| Llama 4 Maverick               |    26,305 |   67.5 |   12.6s | $  0.02 |  Yes |  64GB |

## Per-Module Token Distribution

| Model                          |  A: Pedagogy |  B: Subject |  C: Copilot |  D: Chuvash |
|-------------------------------|-------------|------------|------------|------------|
| Claude Opus 4.6                |       52,522 |      11,738 |      29,013 |      28,575 |
| Claude Sonnet 4.6              |       46,327 |      13,414 |      28,994 |      34,589 |
| Command A                      |       10,432 |       5,266 |       6,510 |       7,943 |
| DeepSeek V3.2                  |       27,000 |      12,348 |      19,717 |      19,434 |
| Gemini 2.5 Flash               |       38,524 |      14,705 |      25,343 |      25,819 |
| Gemini 2.5 Pro                 |       67,714 |      34,312 |      41,316 |      61,965 |
| Gemini 3.1 Flash Lite          |       14,630 |       7,557 |       9,259 |      12,072 |
| Gemini 3.1 Pro                 |       48,319 |      25,157 |      29,256 |      47,575 |
| GLM 4.7 Flash                  |       46,762 |      27,396 |      34,321 |      55,937 |
| GLM 5                          |       24,021 |      11,397 |      15,542 |      25,575 |
| GPT-5.4 Mini                   |       23,607 |       6,817 |      16,067 |      15,176 |
| GPT-5.4                        |       34,862 |       8,762 |      22,622 |      18,315 |
| Grok 4.1 Fast                  |       29,579 |      15,179 |      18,367 |      35,493 |
| Kimi K2.5                      |       62,149 |      30,558 |      46,661 |      56,436 |
| Llama 4 Maverick               |        8,312 |       4,519 |       6,240 |       7,234 |
| Mistral Large 3                |       25,592 |      11,303 |      20,381 |      17,800 |
| Phi-4 14B                      |       21,526 |       9,578 |      12,508 |      15,088 |
| Qwen3 14B                      |       28,651 |      14,486 |      19,542 |      30,847 |
| Qwen3 235B A22B                |       31,654 |      16,477 |      19,421 |      26,967 |
| Qwen3 32B                      |       32,320 |      17,730 |      24,971 |      30,674 |
| Qwen3 8B                       |       30,626 |      16,072 |      21,932 |      25,520 |
| Qwen3.5 27B                    |       62,319 |      63,705 |     114,313 |      94,446 |

## Speed Leaderboard

| Rank | Model                          |  tok/s | Avg Time |
|------|-------------------------------|-------|---------|
|    1 | GPT-5.4 Mini                   |  165.8 |    6.9s |
|    2 | Gemini 2.5 Flash               |  165.7 |   12.4s |
|    3 | Gemini 3.1 Flash Lite          |  155.1 |    5.8s |
|    4 | Gemini 2.5 Pro                 |  106.0 |   38.8s |
|    5 | Grok 4.1 Fast                  |  102.0 |   19.5s |
|    6 | GLM 4.7 Flash                  |   78.8 |   45.0s |
|    7 | Phi-4 14B                      |   77.0 |   16.7s |
|    8 | Gemini 3.1 Pro                 |   76.7 |   45.3s |
|    9 | Qwen3.5 27B                    |   76.5 |   81.9s |
|   10 | Llama 4 Maverick               |   67.5 |   12.6s |
|   11 | GPT-5.4                        |   65.5 |   25.0s |
|   12 | Qwen3 8B                       |   64.9 |   30.1s |
|   13 | Qwen3 32B                      |   60.1 |   44.3s |
|   14 | Qwen3 235B A22B                |   57.6 |   34.7s |
|   15 | Claude Sonnet 4.6              |   57.5 |   42.5s |
|   16 | Kimi K2.5                      |   56.3 |  103.5s |
|   17 | Claude Opus 4.6                |   55.3 |   43.4s |
|   18 | Mistral Large 3                |   52.0 |   28.7s |
|   19 | GLM 5                          |   46.9 |   48.6s |
|   20 | Qwen3 14B                      |   42.2 |   61.2s |
|   21 | Command A                      |   37.2 |   19.5s |
|   22 | DeepSeek V3.2                  |   24.6 |  107.3s |

## Verbosity Leaderboard

Average tokens per prompt (higher = more detailed responses):

  Qwen3.5 27B                      6696 tok/prompt █████████████████████████████████
  Gemini 2.5 Pro                   4106 tok/prompt ████████████████████
  Kimi K2.5                        3916 tok/prompt ███████████████████
  GLM 4.7 Flash                    3288 tok/prompt ████████████████
  Gemini 3.1 Pro                   3006 tok/prompt ███████████████
  Claude Sonnet 4.6                2466 tok/prompt ████████████
  Claude Opus 4.6                  2437 tok/prompt ████████████
  Qwen3 32B                        2114 tok/prompt ██████████
  Gemini 2.5 Flash                 2088 tok/prompt ██████████
  Grok 4.1 Fast                    1972 tok/prompt █████████
  Qwen3 235B A22B                  1890 tok/prompt █████████
  Qwen3 8B                         1883 tok/prompt █████████
  Qwen3 14B                        1871 tok/prompt █████████
  GPT-5.4                          1691 tok/prompt ████████
  DeepSeek V3.2                    1570 tok/prompt ███████
  GLM 5                            1531 tok/prompt ███████
  Mistral Large 3                  1502 tok/prompt ███████
  GPT-5.4 Mini                     1233 tok/prompt ██████
  Phi-4 14B                        1174 tok/prompt █████
  Gemini 3.1 Flash Lite             870 tok/prompt ████
  Command A                         603 tok/prompt ███
  Llama 4 Maverick                  526 tok/prompt ██

---

## Notes

- Quality scoring (LLM-as-judge + human evaluation) is pending
- Module D (ChuvashBench) requires native speaker validation
- Token count reflects response depth but not necessarily quality
- Local model results (GigaChat-20B, Qwen-Opus-Distilled, Qwen3.5-9B) from separate run with 5 prompts
