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

**28 models** tested. Scores: GPT-5.4 judge, 1-4 scale (average of 5 dimensions).

**EduRU** = Modules A+B+C (35 education prompts). **ChuvashBench** = Module D (15 prompts, reported separately).

| # | Model | EduRU | Type |
|:--:|-------|:---:|------|
| 1 | Gemini 3.1 Pro | 3.24 | Cloud |
| 2 | Gemini 3.1 Flash Lite | 3.12 | Cloud |
| 3 | Kimi K2.5 | 3.09 | Cloud |
| 4 | Claude Sonnet 4.6 | 2.99 | Cloud |
| 5 | Mistral Large 3 | 2.99 | Open |
| 6 | Claude Opus 4.6 | 2.98 | Cloud |
| 7 | GPT-5.4 Mini | 2.98 | Cloud |
| 8 | GLM 5 | 2.95 | Cloud |
| 9 | GPT-5.4 | 2.91 | Cloud |
| 10 | Gemini 2.5 Pro | 2.89 | Cloud |
| 11 | EduLLM-RU (ours, fine-tuned 27B) | 2.88 | Self-hosted |
| 12 | DeepSeek V3.2 | 2.87 | Cloud |
| 13 | Qwen3 235B A22B | 2.85 | Open |
| 14 | Grok 4.1 Fast | 2.84 | Cloud |
| 15 | Qwen3.5 27B | 2.77 | Open |
| 16 | Qwen3 32B | 2.73 | Open |
| 17 | Gemini 2.5 Flash | 2.67 | Cloud |
| 18 | Llama 4 Maverick | 2.67 | Open |
| 19 | **YandexGPT 5.1 Pro** | 2.66 | **Russian cloud** |
| 20 | GLM 4.7 Flash | 2.63 | Cloud |
| 21 | Qwen3 14B | 2.59 | Open |
| 22 | Qwen3 8B | 2.58 | Open |
| 23 | **GigaChat-2-Pro** | 2.58 | **Russian cloud** |
| 24 | **GigaChat-2-Max** | 2.56 | **Russian cloud** |
| 25 | **YandexGPT 5 Lite** | 2.47 | **Russian cloud** |
| 26 | Command A | 2.38 | Cloud |
| 27 | **GigaChat-2-Lite** | 2.33 | **Russian cloud** |
| 28 | Phi-4 14B | 1.69 | Open |

See [data/scores/](data/scores/) for per-dimension breakdowns by judge.

## Key Findings

1. **No existing benchmark** covers Russian K-12 education — EduBench-RU fills this gap
2. **Russian cloud LLMs (GigaChat, YandexGPT) rank #19-27** — optimized for general chat, not structured pedagogy
3. **A $300 fine-tuned 27B model (#11) beats all Russian cloud LLMs** on education tasks
4. **ФГОС awareness varies dramatically** — frontier models produce proper технологические карты; smaller models produce generic lesson outlines
5. **All models struggle with Chuvash** — ChuvashBench scores 1.4-2.8 across all 28 models (reported separately)
6. **Self-hosted models** are viable for 152-ФЗ compliant school deployment

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
