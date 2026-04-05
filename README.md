# EduBench-RU

**The first comprehensive benchmark for evaluating Large Language Models in Russian K-12 education.**

EduBench-RU tests LLMs on real-world Russian pedagogical tasks: ФГОС-aligned lesson planning, student explanations, assessment design, teacher copilot scenarios, and — uniquely — endangered Chuvash language education (ChuvashBench).

## Why EduBench-RU?

Existing benchmarks don't cover Russian education:

| Benchmark | Russian Education? | Pedagogy Tasks? | Minority Languages? |
|-----------|-------------------|-----------------|---------------------|
| [EduBench](https://github.com/ybai-nlp/EduBench) | No (English/Chinese) | Yes | No |
| [MERA](https://github.com/ai-forever/MERA) | Has 1 exam task (USE) | No | No |
| [KazMMLU](https://arxiv.org/abs/2502.12829) | Partial (Kazakhstan) | No | No |
| **EduBench-RU** | **Yes (ФГОС, ОГЭ, ЕГЭ)** | **Yes (50 prompts)** | **Yes (Chuvash)** |

## Benchmark Structure

**50 prompts** across 4 modules:

| Module | Prompts | Focus |
|--------|---------|-------|
| **A. Russian Pedagogy** | 15 | Lesson planning (технологическая карта), student explanations, assessment analysis |
| **B. Subject Knowledge** | 10 | Mathematics, Russian language, physics, history, biology, literature |
| **C. Teacher Copilot** | 10 | КТП, characterizations, parent meetings, rubrics, inclusion |
| **D. ChuvashBench** | 15 | Chuvash↔Russian translation, language teaching, cultural context, bilingual education |

## Evaluation

**5-dimension rubric** (1-4 scale per dimension):

1. **Pedagogical Quality** — ФГОС alignment, structure, grade-appropriateness
2. **Language Quality** — Russian fluency, teacher register, natural tone
3. **Factual Accuracy** — Subject matter correctness
4. **Actionability** — Concrete steps, timelines, differentiation
5. **Cultural/Regional Context** — Russian educational standards awareness

Module D adds a 6th dimension: **Chuvash Accuracy** (validated by native speakers).

**Scoring:** LLM-as-judge (automated) + human validation on test set.

## Quick Start

```bash
# Clone
git clone https://github.com/csylabs-org/edubench-ru.git
cd edubench-ru

# Install dependencies
pip install -r requirements.txt

# Run benchmark (requires OpenRouter API key)
export OPENROUTER_API_KEY=your_key
python code/run_benchmark.py --batch=frontier

# Results saved to data/results/
```

## Leaderboard (March 2026)

**30 models** tested. **3-judge panel:** GPT-5.4 + Claude Sonnet 4.6 + Gemini 3.1 Pro. Scores: 1-4 scale (average of 5 dimensions, consensus across judges).

**EduRU** = Modules A+B+C (35 education prompts). **ChvBn** = Module D ChuvashBench (15 prompts, 6th dimension: Chuvash accuracy).

| # | Model | AVG | EduRU | ChvBn | Type |
|:--:|-------|:---:|:-----:|:-----:|------|
| 1 | Gemini 3.1 Pro | 3.61 | 3.64 | 3.43 | Cloud |
| 2 | Gemini 3.1 Flash Lite | 3.40 | 3.51 | 3.02 | Cloud |
| 3 | Claude Opus 4.6 | 3.36 | 3.46 | 3.00 | Cloud |
| 4 | Gemini 2.5 Pro | 3.34 | 3.38 | 3.16 | Cloud |
| 5 | Claude Sonnet 4.6 | 3.33 | 3.43 | 3.00 | Cloud |
| 6 | DeepSeek V3.2 | 3.24 | 3.37 | 2.77 | Cloud |
| 7 | Mistral Large 3 | 3.24 | 3.35 | 2.82 | Open |
| 8 | Kimi K2.5 | 3.22 | 3.35 | 2.51 | Cloud |
| 9 | **EduLLM-RU 27B Q6_K (ours)** | **3.21** | **3.35** | **2.64** | **Self-hosted** |
| 10 | GLM 5 | 3.20 | 3.34 | 2.77 | Cloud |
| 11 | GPT-5.4 | 3.20 | 3.33 | 2.82 | Cloud |
| 12 | GPT-5.4 Mini | 3.07 | 3.26 | 2.50 | Cloud |
| 13 | Gemini 2.5 Flash | 3.01 | 3.03 | 2.86 | Cloud |
| 14 | Qwen3.5 27B (base) | 3.00 | 3.13 | 2.47 | Open |
| 15 | Grok 4.1 Fast | 2.94 | 3.15 | 2.22 | Cloud |
| 16 | Qwen3 235B A22B | 2.83 | 3.12 | 1.96 | Open |
| 17 | EduLLM-RU 32B Q6_K (ours) | 2.69 | 2.88 | 2.04 | Self-hosted |
| 18 | GLM 4.7 Flash | 2.68 | 2.79 | 2.14 | Cloud |
| 19 | Qwen3 32B | 2.61 | 2.90 | 1.77 | Open |
| 20 | Llama 4 Maverick | 2.58 | 2.68 | 2.30 | Open |
| 21 | **YandexGPT 5.1 Pro** | 2.51 | 2.71 | 1.89 | **Russian cloud** |
| 22 | Qwen3 14B | 2.41 | 2.68 | 1.67 | Open |
| 23 | **GigaChat-2 Max** | 2.39 | 2.59 | 1.81 | **Russian cloud** |
| 24 | **GigaChat-2 Pro** | 2.36 | 2.57 | 1.76 | **Russian cloud** |
| 25 | Qwen3 8B | 2.34 | 2.56 | 1.69 | Open |
| 26 | **YandexGPT 5 Lite** | 2.27 | 2.45 | 1.78 | **Russian cloud** |
| 27 | Command A | 2.23 | 2.39 | 1.74 | Cloud |
| 28 | **GigaChat-2 Lite** | 2.16 | 2.30 | 1.73 | **Russian cloud** |
| 29 | Phi-4 14B | 1.57 | 1.60 | 1.44 | Open |

See [data/scores/](data/scores/) for per-dimension breakdowns by judge. See [CHANGELOG.md](CHANGELOG.md) for scoring methodology changes.

## Key Findings

1. **No existing benchmark** covers Russian K-12 education — EduBench-RU fills this gap
2. **A $300 fine-tuned 27B model (#9) beats GPT-5.4 and all Russian cloud LLMs** on education tasks
3. **Russian cloud LLMs (GigaChat, YandexGPT) rank #21-28** — optimized for general chat, not structured pedagogy
4. **Architecture > parameters:** Qwen3.5-27B fine-tuned (#9, 3.21) dramatically outperforms Qwen3-32B fine-tuned (#17, 2.69) despite fewer parameters
5. **ФГОС awareness varies dramatically** — frontier models produce proper технологические карты; smaller models produce generic lesson outlines
6. **All models struggle with Chuvash** — ChuvashBench scores 1.4-3.4 across all 30 models
7. **Self-hosted models** are viable for 152-ФЗ compliant school deployment

## ChuvashBench

Module D is the first benchmark for evaluating LLMs on an endangered Turkic language in educational contexts. Chuvash (чӑваш чĕлхи) is spoken by ~1.1 million people in the Chuvash Republic, Russia, and is classified as "definitely endangered" by UNESCO.

ChuvashBench evaluation requires native speaker validation. See [docs/chuvash-evaluation.md](docs/chuvash-evaluation.md).

## Citation

```bibtex
@misc{ivanov2026edubenchru,
  title={EduBench-RU: A Comprehensive Benchmark for Evaluating Large Language Models in Russian K-12 Education},
  author={Ivanov, Daniel and Antonov, Alexander},
  year={2026},
  howpublished={\url{https://github.com/csylabs-org/edubench-ru}}
}
```

## License

MIT — see [LICENSE](LICENSE).

## Related Work

- [EduBench](https://github.com/ybai-nlp/EduBench) — English/Chinese education benchmark
- [MERA](https://github.com/ai-forever/MERA) — Russian LLM evaluation (general)
- [Chuvash Datasets](https://huggingface.co/datasets/alexantonov/chuvash_russian_parallel) — CC0 Chuvash-Russian parallel corpus

## Contact

Daniel Ivanov — ООО "ЛИИ" (Лаборатория инновационных инициатив), Cheboksary, Russia
