# EduBench-RU: Benchmarking Large Language Models for Russian K-12 Education

**Daniel Ivanov**
ООО "ЛИИ" (Laboratory of Innovative Initiatives), Cheboksary, Russia

## Abstract

We present EduBench-RU, the first comprehensive benchmark for evaluating Large Language Models (LLMs) on Russian K-12 education tasks. Despite the rapid deployment of AI in education worldwide, no benchmark exists for evaluating LLM capabilities in the context of Russian federal educational standards (ФГОС), exam preparation (ОГЭ/ЕГЭ), or teacher support workflows. EduBench-RU addresses this gap with 50 structured prompts across four modules: Russian Pedagogy (15 prompts), Subject Knowledge (10), Teacher Copilot (10), and ChuvashBench (15) — the first evaluation suite for endangered Chuvash language education. We evaluate 22 models spanning frontier closed-source (Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro), mid-tier (GPT-5.4 Mini, Gemini 2.5 Flash, Grok 4.1), and open-source systems (Qwen3-32B, DeepSeek V3.2, Llama 4 Maverick). Using a dual-judge consensus scoring methodology (GPT-5.4 and Claude Sonnet 4.6), we find that: (1) frontier models achieve adequate quality on Russian education tasks (3.0-3.5/4.0) but none excel on ФГОС-specific pedagogy; (2) all 22 models fail on Chuvash language tasks (max 2.1/4.0 on Chuvash accuracy), revealing a critical gap for the 1.1 million speakers of this UNESCO-classified endangered language; and (3) open-source models suitable for self-hosted school deployment (Qwen3-32B, Qwen3-14B) score 35-40% below frontier models, highlighting the quality-compliance tradeoff for 152-ФЗ data sovereignty requirements. EduBench-RU and all evaluation data are publicly available under MIT license.

## 1. Introduction

The integration of artificial intelligence into education is accelerating globally, with national mandates in China (2024), the United States (2025), and Russia (2025-2026). In December 2025, President Putin signed a directive requiring AI integration across all Russian schools and universities, with implementation reports due in Spring 2026. The Russian Ministry of Digital Development (Минцифры) has introduced legislation (effective September 2027) that will exclude foreign AI systems from government procurement, creating urgency for domestic and self-hosted solutions.

Despite this momentum, the evaluation infrastructure for educational AI in Russia is notably absent. The dominant Russian LLM benchmark, MERA (Fenogenova et al., 2024), includes 23 tasks (v1.2.0, March 2025) across 11 skill domains. Two tasks touch education: USE (900 ЕГЭ Russian language exam items) and MaMuRAMu (4,248 expert-level questions across 29 domains). Both measure whether a model can *answer* exam questions — not whether it can *teach*, *plan lessons*, or *support pedagogical workflows*. These are categorically different capabilities: a model that scores well on USE can solve ЕГЭ problems but may fail to generate a ФГОС-aligned lesson plan or explain fractions to a 9-year-old. The international EduBench (Xu et al., 2025) covers English and Chinese educational scenarios but includes no Russian content, no ФГОС alignment, and no minority language support.

Russia presents a unique challenge for educational AI. The federal educational standard (ФГОС) prescribes specific lesson structures, competency frameworks, and assessment criteria that differ substantially from Western pedagogical traditions. Additionally, Russia's 35+ constitutionally recognized regional languages — many classified as endangered by UNESCO — receive no support from any existing AI system. The Chuvash language (чӑваш чĕлхи), spoken by approximately 1.1 million people in the Chuvash Republic, is representative of this gap: it belongs to the Oghur branch of Turkic languages, possesses a developed literary tradition and educational curriculum, yet receives zero coverage in any LLM benchmark.

We introduce **EduBench-RU**, a benchmark designed to evaluate LLMs on the tasks that Russian teachers and students actually need:

1. **Module A: Russian Pedagogy** (15 prompts) — ФГОС-aligned lesson planning (технологическая карта), grade-appropriate student explanations, and assessment analysis (ОГЭ/ЕГЭ)
2. **Module B: Subject Knowledge** (10 prompts) — Mathematics, Russian language, physics, biology, history, and literature at K-12 levels
3. **Module C: Teacher Copilot** (10 prompts) — Calendar planning (КТП), student characterizations, parent communication, inclusion strategies, and rubric design
4. **Module D: ChuvashBench** (15 prompts) — The first evaluation suite for Chuvash language education, covering translation, language teaching, cultural context, and bilingual education scenarios

We evaluate 22 models from 10 providers across three tiers: frontier closed-source, mid-tier efficient, and open-source self-hostable. Our dual-judge consensus methodology (GPT-5.4 + Claude Sonnet 4.6) provides cross-provider validation while measuring inter-judge agreement.

## 2. Related Work

### 2.1 Education-Focused LLM Benchmarks

EduBench (Xu et al., 2025) is the closest existing work: a benchmark with 9 educational scenarios and 4,000+ contexts, evaluated across 12 dimensions. However, it supports only English and Chinese, uses Western pedagogical frameworks, and includes no minority language component. MathTutorBench (Macina et al., 2025) evaluates mathematical tutoring quality but is limited to English and a single subject domain.

### 2.2 Russian LLM Evaluation

MERA (Fenogenova et al., 2024; v1.2.0, March 2025) provides comprehensive Russian language evaluation across 23 tasks in 11 skill domains. Its education-adjacent tasks — USE (ЕГЭ exam solving, 900 items) and MaMuRAMu (expert knowledge across 29 domains, 4,248 items) — treat education as content knowledge (exam answering) rather than pedagogical capability. The benchmark is maintained by a consortium of Sber, Yandex, and MTS AI, with private answer scoring to prevent data leakage. Russian SuperGLUE (Shavrina et al., 2020) evaluates general language understanding. POLLUX (2025) and LIBRA (2024) address dialogue and long-context evaluation respectively, with no education domain coverage. LLM Arena RU provides crowd-sourced comparative evaluation without structured educational assessment.

### 2.3 Minority Language AI

KazMMLU (Zhumazhanov et al., 2025) benchmarks LLMs on Kazakh and Russian university-level knowledge, representing the closest CIS-region educational evaluation. No benchmark exists for any Russian regional language. The Chuvash NLP landscape is limited to mGPT-1.3B-chuvash (ai-forever, 2024), a 1.3B-parameter base model with no instruction-following capability, and parallel corpus resources by Antonov (2024). The synthesis work on Bashkir/Chuvash translation (2025) demonstrated that traditional fine-tuning on parallel data alone proves ineffective without continued pretraining — an important finding for future Chuvash model development.

## 3. EduBench-RU Design

### 3.1 Prompt Design

EduBench-RU consists of 50 prompts organized into four modules. Prompts were designed by educational practitioners with experience in Russian K-12 schools, aligned with current ФГОС requirements (2022 revision), and validated for grade-level appropriateness.

**Module A: Russian Pedagogy (15 prompts)** covers three categories:
- *Lesson Planning* (5 prompts): Generation of технологическая карта (technology map) for lessons across subjects (Russian language, mathematics, environmental science, English, history) and grade levels (2-7). Each prompt requires ФГОС-aligned goals (educational, developmental, formative), lesson stages, planned outcomes (personal, meta-subject, subject-specific), and homework.
- *Student Explanations* (5 prompts): Age-appropriate explanations of concepts ranging from fractions (grade 3) to covalent bonds (grade 9), requiring vocabulary calibration and real-world analogies.
- *Assessment Analysis* (5 prompts): Data-driven analysis of student performance (ОГЭ results, error pattern identification, exam comparison), requiring actionable corrective plans with timelines.

**Module B: Subject Knowledge (10 prompts)** spans six subjects: mathematics (quadratic equations, geometry), Russian language (morphological analysis, dictation), physics (energy conservation, Ohm's law), biology (mitosis/meiosis), history (Peter I reforms), literature (Pushkin analysis), and geography (Volga essay).

**Module C: Teacher Copilot (10 prompts)** addresses practical teacher workflows: calendar-thematic planning (КТП), student characterizations, methodological comparison (Montessori vs. traditional), inclusion strategies (СДВГ, dyslexia), parent meeting scenarios, formative assessment design, rubric creation, recommendation letters, and extracurricular activity planning.

**Module D: ChuvashBench (15 prompts)** is organized into four categories:
- *Translation* (5 prompts): Russian↔Chuvash translation including simple sentences, contextual paragraphs, school vocabulary, and creative adaptation (nursery rhyme translation preserving rhythm).
- *Language Teaching* (5 prompts): Exercise creation, grammar explanation, bilingual lesson planning, morphological analysis, and assessment generation for Chuvash language classes.
- *Cultural Context* (3 prompts): Chuvash cultural knowledge (Акатуй celebration, national ornament symbolism, notable Chuvash figures) formatted as educational materials.
- *Bilingual Education* (2 prompts): Bilingual lesson planning (Chuvash + Russian) and Chuvash language olympiad material preparation.

### 3.2 Evaluation Methodology

#### Scoring Rubric

Responses are evaluated on five dimensions using a 1-4 scale:

1. **Pedagogical Quality**: Structure, ФГОС alignment, grade-appropriateness (1=unusable, 4=publication-quality methodology)
2. **Language Quality**: Russian fluency, register appropriateness, natural teacher tone (1=errors, 4=native методист level)
3. **Factual Accuracy**: Subject matter correctness, appropriate depth (1=errors present, 4=enriched with nuance)
4. **Actionability**: Concreteness of recommendations, implementability (1=abstract advice, 4=structured plan with timeline)
5. **Cultural/Regional Context**: ФГОС awareness, Russian educational system knowledge (1=ignores Russian context, 4=correct regulatory references)

Module D adds a sixth dimension:
6. **Chuvash Accuracy**: Correctness of Chuvash language content (1=hallucinated, 4=verified by native speaker)

#### Dual-Judge Consensus

Following the LLM-as-judge paradigm established by EduBench (Xu et al., 2025), we employ two independent evaluator models from different providers:
- **GPT-5.4** (OpenAI) — primary judge
- **Claude Sonnet 4.6** (Anthropic) — secondary judge

Each judge receives the original prompt, the model's response, and the scoring rubric, producing per-dimension scores (1-4) and a written justification. The **consensus score** is the arithmetic mean of both judges' scores.

We attempted Gemini 3.1 Pro and Gemini 2.5 Pro as a third judge but excluded both due to systematic JSON formatting failures in structured output (>50% error rate).

#### Inter-Judge Agreement

We report inter-judge agreement as the mean absolute difference between judges' scores. Across all models and prompts:
- Mean bias: Claude Sonnet scores +0.49 points higher than GPT-5.4 (σ=0.26)
- This bias is consistent across models, suggesting a systematic calibration difference rather than per-model favoritism
- Agreement is highest on bottom-tier models (±0.05-0.10) and lowest on top-tier (±0.7-0.9)

### 3.3 Models Evaluated

We evaluate 22 models across three tiers:

**Frontier closed-source (5):** Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.4, Gemini 3.1 Pro, Gemini 2.5 Pro

**Mid-tier (7):** GPT-5.4 Mini, Gemini 2.5 Flash, Gemini 3.1 Flash Lite, Grok 4.1 Fast, Kimi K2.5, GLM 5, DeepSeek V3.2

**Open-source (10):** Qwen3 235B-A22B, Qwen3.5 27B, Qwen3 32B, Qwen3 14B, Qwen3 8B, Mistral Large 3, Llama 4 Maverick, GLM 4.7 Flash, Phi-4 14B, Command A

All models were accessed via OpenRouter API with consistent parameters: max_tokens=8192, temperature=0.7, identical system prompt in Russian. Total benchmark cost: $18.69 for 2,421,700 output tokens across 1,100 API calls.

### 3.4 Technical Parameters

| Parameter | Value |
|-----------|-------|
| Total prompts | 50 |
| Models evaluated | 22 |
| Judges | 2 (GPT-5.4, Claude Sonnet 4.6) |
| Total output tokens | 2,421,700 |
| Total scoring evaluations | 2,093 |
| System prompt language | Russian |
| max_tokens | 8,192 |
| Temperature | 0.7 |
| API | OpenRouter |
| Benchmark cost | $18.69 |
| Scoring cost | ~$35 |

## 4. Results

### 4.1 Overall Rankings

Table 1 presents the consensus scores across all 22 models, ranked by overall average.

**Table 1: EduBench-RU Consensus Scores (22 models, dual-judge average)**

| Rank | Model | Overall | EduRU (A-C) | ChuvashBench (D) | Type | VRAM (Q4) |
|------|-------|---------|-------------|-------------------|------|-----------|
| 1 | Gemini 3.1 Pro | 3.42 | 3.51 | 3.19 | Closed | — |
| 2 | Claude Opus 4.6 | 3.24 | 3.36 | 2.98 | Closed | — |
| 3 | Claude Sonnet 4.6 | 3.22 | 3.34 | 2.95 | Closed | — |
| 4 | Gemini 3.1 Flash Lite | 3.22 | 3.33 | 2.94 | Closed | — |
| 5 | Gemini 2.5 Pro | 3.21 | 3.31 | 2.98 | Closed | — |
| 6 | DeepSeek V3.2 | 3.15 | 3.28 | 2.85 | Open | — |
| 7 | GLM 5 | 3.15 | 3.28 | 2.84 | Closed | — |
| 8 | Mistral Large 3 | 3.14 | 3.28 | 2.81 | Open | 72GB |
| 9 | GPT-5.4 | 3.09 | 3.23 | 2.78 | Closed | — |
| 10 | GPT-5.4 Mini | 2.99 | 3.19 | 2.51 | Closed | — |
| 11 | Gemini 2.5 Flash | 2.99 | 3.03 | 2.88 | Closed | — |
| 12 | Qwen3.5 27B | 2.93 | 3.09 | 2.54 | Open | 18GB |
| 13 | Grok 4.1 Fast | 2.87 | 3.14 | 2.21 | Closed | — |
| 14 | Qwen3 235B-A22B | 2.72 | 3.04 | 1.97 | Open | 128GB |
| 15 | GLM 4.7 Flash | 2.70 | 2.82 | 2.17 | Open | 20GB |
| 16 | Qwen3 32B | 2.58 | 2.91 | 1.81 | Open | 20GB |
| 17 | Llama 4 Maverick | 2.55 | 2.64 | 2.33 | Open | 64GB |
| 18 | Qwen3 14B | 2.42 | 2.73 | 1.70 | Open | 10GB |
| 19 | Qwen3 8B | 2.36 | 2.63 | 1.72 | Open | 6GB |
| 20 | Command A | 2.25 | 2.44 | 1.79 | Open | — |
| 21 | Phi-4 14B | 1.63 | 1.68 | 1.51 | Open | 10GB |

*Kimi K2.5 excluded from overall ranking due to incomplete Module D scoring (no Chuvash accuracy dimension).*

### 4.2 Module-Level Analysis

**Module A (Russian Pedagogy):** Frontier models score 3.3-3.8 on pedagogical quality, demonstrating awareness of ФГОС structure (образовательные/развивающие/воспитательные goals). However, specific ФГОС regulatory references (e.g., citing particular standards by number) are rare. Gemini 3.1 Pro and Kimi K2.5 produce the most structured lesson plans. Open-source models below 14B parameters consistently fail to generate proper технологическая карта format.

**Module B (Subject Knowledge):** Factual accuracy is the weakest dimension across all models (consensus average 2.5/4.0). Mathematics and physics prompts reveal calculation errors even in frontier models. Russian literature analysis (Pushkin) is handled competently by most models, while Chuvash-adjacent cultural knowledge is uniformly poor.

**Module C (Teacher Copilot):** This module shows the widest quality spread. Frontier models generate usable КТП, characterizations, and rubrics. Parent meeting scenarios and inclusion strategies require cultural sensitivity that smaller models lack. Qwen3.5 27B is notably verbose (114,313 tokens on Module C alone — 2× the next highest) but not proportionally higher quality.

**Module D (ChuvashBench):** The central finding. See Section 4.3.

### 4.3 ChuvashBench: The Endangered Language Gap

ChuvashBench reveals a systematic failure across all 22 models. Using the GPT-5.4 judge's Chuvash accuracy scores:

**Table 2: Chuvash Accuracy Distribution (GPT-5.4 judge, Module D, n=15 per model)**

| Chuvash Score | Meaning | Models |
|---------------|---------|--------|
| >3.0 (mostly correct) | 0 models | — |
| 2.0-3.0 (mixed) | 3 models | Claude Opus (2.1), GPT-5.4 (2.1), Gemini 3.1 Pro (2.1) |
| 1.0-2.0 (mostly hallucinated) | 14 models | Gemini 2.5 Flash (2.0), Sonnet (2.0), GLM 5 (2.0), Mistral (2.0), ... |
| =1.0 (fully hallucinated) | 5 models | Qwen3 8B, 14B, 32B, 235B, Phi-4 |

No model achieves "mostly correct" Chuvash language output. The best models (Claude Opus, GPT-5.4, Gemini 3.1 Pro) score 2.1/4.0 — a mix of correct and fabricated Chuvash words. Five models, all from the Qwen3 family and Phi-4, score exactly 1.0 on every Chuvash prompt, indicating complete hallucination of Chuvash content.

Qualitative analysis of high-scoring responses reveals that even models scoring 2.0+ produce unreliable Chuvash: correct greetings ("Салам" — hello) alongside fabricated vocabulary, grammatically impossible constructions, and invented grammar rules attributed to Chuvash. The Chuvash accuracy dimension in our automated evaluation is itself limited (see Section 6), as the judge models that score it also lack Chuvash competence.

### 4.4 Self-Hosting Feasibility

For Russian schools subject to 152-ФЗ data protection requirements, self-hosted deployment is a regulatory necessity. We annotate each open-source model with minimum VRAM requirements for local Q4 quantized deployment:

| Model | EduRU Score | VRAM (Q4) | Suitable Hardware |
|-------|------------|-----------|-------------------|
| Qwen3.5 27B | 3.09 | 18GB | RTX 4090 / Mac Mini M4 Pro |
| Qwen3 32B | 2.91 | 20GB | RTX 4090 / Mac Mini M4 Pro |
| Qwen3 14B | 2.73 | 10GB | RTX 4060 / Any 16GB GPU |
| Qwen3 8B | 2.63 | 6GB | RTX 3060 / Any 8GB GPU |

The quality gap between the best self-hostable model (Qwen3.5 27B at 3.09) and the frontier leader (Gemini 3.1 Pro at 3.51) is 12% — significant but potentially acceptable for schools where data sovereignty is mandatory.

### 4.5 Cost-Efficiency Analysis

| Model | EduRU Score | Output Cost ($/M tok) | Score/$ |
|-------|------------|----------------------|---------|
| Gemini 3.1 Flash Lite | 3.33 | $1.50 | 2.22 |
| Gemini 2.5 Flash | 3.03 | $2.50 | 1.21 |
| GPT-5.4 Mini | 3.19 | $4.50 | 0.71 |
| Qwen3 32B | 2.91 | $0.24 | 12.13 |
| Claude Opus 4.6 | 3.36 | $75.00 | 0.04 |

For deployment at scale, Gemini 3.1 Flash Lite offers the best cost-quality ratio among closed-source models, while Qwen3 32B (at $0.24/M output tokens or self-hosted at $0) provides the most economical path for quality-tolerant deployments.

## 5. Analysis

### 5.1 Closed-Source vs. Open-Source Gap

The average EduRU score (Modules A-C) for closed-source models is 3.30 versus 2.80 for open-source — an 18% gap. This gap narrows for larger open-source models: DeepSeek V3.2 (3.28) and Qwen3.5 27B (3.09) approach mid-tier closed-source performance. The gap widens dramatically on ChuvashBench (2.76 closed vs. 1.94 open), suggesting that minority language knowledge is concentrated in larger training corpora accessible only to frontier providers.

### 5.2 The Chuvash Problem

The ChuvashBench results demonstrate a structural failure in current LLM capabilities for endangered languages. With 1.1 million speakers and a developed educational curriculum in the Chuvash Republic, the Chuvash language is not obscure — yet the best model achieves only 2.1/4.0 on Chuvash accuracy. This finding has implications beyond Chuvash: Russia's 35+ regional languages, many with larger speaker populations (Tatar: 5.3M, Bashkir: 1.2M), likely face similar coverage gaps.

The availability of high-quality Chuvash training data — 2.92 million monolingual sentences and 1.46 million manually collected Russian-Chuvash parallel pairs (Antonov, 2024), released under CC0 — suggests that the gap is not due to data scarcity but to training prioritization. No model provider has invested in Chuvash language coverage despite the existence of sufficient data.

### 5.3 ФГОС Awareness

A notable finding is that ФГОС awareness correlates with overall model size but not perfectly with recency. Gemini 3.1 Pro demonstrates the strongest ФГОС alignment (cultural context score: 3.35 consensus), likely due to extensive Russian-language training data. Smaller open-source models (Qwen3 8B, Phi-4) consistently fail to generate ФГОС-compliant lesson structures, suggesting that Russian pedagogical knowledge requires a minimum model capacity threshold.

## 6. Limitations

1. **LLM-as-judge limitations for Chuvash**: Our automated Chuvash accuracy scores are produced by models that themselves score 2.0-2.1 on Chuvash tasks. While both judges consistently identify hallucinated content (convergent validity), the exact accuracy of Chuvash linguistic judgments requires validation by native speakers. We plan to conduct this validation in a follow-up study.

2. **Two judges, not three**: The exclusion of Gemini as a third judge due to JSON formatting failures reduces our inter-judge agreement analysis. The systematic +0.49 bias of Claude Sonnet relative to GPT-5.4 is measurable and consistent but would benefit from a third independent perspective.

3. **No human evaluation baseline**: Unlike EduBench (Xu et al., 2025), which validated LLM-judge scores against 198 human-annotated samples, our current evaluation relies entirely on automated scoring. Human validation — particularly from practicing Russian teachers — is needed to establish the correlation between our rubric scores and actual pedagogical utility.

4. **Single evaluation run**: Due to temperature=0.7, model outputs are non-deterministic. Our results represent a single evaluation pass. Repeated evaluations could yield different outputs and scores.

5. **API routing**: All models were accessed via OpenRouter, which may route requests to different provider endpoints based on load. This introduces a potential reproducibility concern for exact output matching.

6. **Prompt coverage**: 50 prompts across 13 subjects and 4 modules cannot comprehensively cover Russian K-12 education (grades 1-11, 15+ subjects). Our prompts emphasize commonly tested subjects and pedagogical scenarios.

## 7. Conclusion

EduBench-RU fills a critical gap in LLM evaluation infrastructure for Russian education. Our evaluation of 22 models reveals three key findings:

1. **Frontier models are adequate but not excellent** for Russian K-12 education, with consensus scores of 3.0-3.5/4.0. No model consistently produces publication-quality ФГОС-aligned pedagogy.

2. **All models fail on Chuvash**, with maximum accuracy scores of 2.1/4.0. This gap affects an endangered language spoken by 1.1 million people and likely extends to Russia's 35+ other regional languages.

3. **Self-hostable models** suitable for 152-ФЗ compliance (Qwen3-32B, Qwen3-14B) score 12-18% below frontier models, presenting a quantified quality-compliance tradeoff for school deployment decisions.

We release EduBench-RU, all evaluation data, scoring scripts, and model outputs under MIT license at [https://github.com/csylabs-org/edubench-ru](https://github.com/csylabs-org/edubench-ru). We welcome contributions of additional prompts, particularly for underrepresented subjects and regional languages.

Future work includes: (1) human evaluation validation with practicing Russian teachers; (2) development of ChuvashLM, a fine-tuned Qwen3-32B model trained on Chuvash parallel corpora, evaluated against ChuvashBench; and (3) extension to other CIS education systems (EduBench-KG for Kyrgyzstan, EduBench-KZ for Kazakhstan).

## References

Antonov, A. (2024). Open the Data! Chuvash Datasets. *arXiv preprint arXiv:2407.11982*.

Fenogenova, A., et al. (2024). MERA: A Comprehensive LLM Evaluation in Russian. *Proceedings of ACL 2024*.

Macina, J., et al. (2025). MathTutorBench: A Benchmark for Measuring Open-ended Pedagogical Capabilities of LLM Tutors. *Proceedings of EMNLP 2025*.

Shavrina, T., et al. (2020). RussianSuperGLUE: A Russian Language Understanding Evaluation Benchmark. *Proceedings of EMNLP 2020*.

Xu, Y., et al. (2025). EduBench: A Comprehensive Benchmarking Dataset for Evaluating Large Language Models in Diverse Educational Scenarios. *arXiv preprint arXiv:2505.16160*.

Zhumazhanov, B., et al. (2025). KazMMLU: Measuring Multitask Language Understanding in Kazakh. *arXiv preprint arXiv:2502.12829*.

## Appendix A: System Prompt

The following system prompt (in Russian) was used for all model evaluations:

> "Ты — опытный российский педагог и методист с высшей квалификационной категорией. Отвечай на русском языке. Давай конкретные, практичные ответы, соответствующие ФГОС."

(*Translation: "You are an experienced Russian educator and methodologist with the highest qualification category. Respond in Russian. Give concrete, practical answers aligned with ФГОС."*)

## Appendix B: Full Prompt List

Available at: [https://github.com/csylabs-org/edubench-ru/blob/main/data/prompts.json](https://github.com/csylabs-org/edubench-ru/blob/main/data/prompts.json)

## Appendix C: Scoring Rubric Details

Available at: [https://github.com/csylabs-org/edubench-ru/blob/main/docs/rubric.md](https://github.com/csylabs-org/edubench-ru/blob/main/docs/rubric.md)
