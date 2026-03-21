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

## Models Tested

See [results/](data/results/) for full outputs. Initial evaluation covers 24+ models including:

**Closed-source:** Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, Grok 4.1, Kimi K2.5, GLM 5

**Open-source:** Qwen3-32B, Qwen3-235B, DeepSeek V3.2, Llama 4 Maverick, Mistral Large 3, GigaChat-20B

**Local (consumer hardware):** Qwen3-14B (16GB), Qwen3-32B Q4 (24GB), GigaChat-20B (16GB)

## Key Findings

1. **No existing benchmark** covers Russian K-12 education — EduBench-RU fills this gap
2. **All models struggle with Chuvash** — only Claude Opus/Sonnet produce verifiably correct phrases
3. **ФГОС awareness varies dramatically** — frontier models outperform open-source on pedagogical structure
4. **Self-hostable models** (Qwen3-32B, GigaChat-20B) are viable for school deployment at reduced quality

## ChuvashBench

Module D is the first benchmark for evaluating LLMs on an endangered Turkic language in educational contexts. Chuvash (чӑваш чĕлхи) is spoken by ~1.1 million people in the Chuvash Republic, Russia, and is classified as "definitely endangered" by UNESCO.

ChuvashBench evaluation requires native speaker validation. See [docs/chuvash-evaluation.md](docs/chuvash-evaluation.md).

## Citation

```bibtex
@misc{ivanov2026edubenchru,
  title={EduBench-RU: A Comprehensive Benchmark for Evaluating Large Language Models in Russian K-12 Education},
  author={Ivanov, Daniel},
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
