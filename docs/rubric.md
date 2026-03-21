# EduBench-RU Scoring Rubric

## Overview

Each response is scored on 5 dimensions using a 1-4 scale.
Module D (ChuvashBench) adds a 6th dimension: Chuvash Accuracy.

**Max score per prompt:** 20 points (Modules A-C), 24 points (Module D)

---

## Dimension 1: Pedagogical Quality

| Score | Criteria |
|-------|----------|
| **1** | No structure. Not usable in a classroom. Missing key components. |
| **2** | Some structure but generic. Not aligned with ФГОС. Missing goals or stages. |
| **3** | ФГОС-aligned. Clear goals (образовательные, развивающие, воспитательные). Proper lesson stages. Grade-appropriate. |
| **4** | Publication-quality methodology. Innovative approaches. Differentiation included. Reflects current pedagogical best practices. Could be used as a model lesson. |

## Dimension 2: Language Quality

| Score | Criteria |
|-------|----------|
| **1** | Grammatical errors. Unnatural phrasing. Not appropriate register for education. |
| **2** | Correct but stiff. Reads like a translation. Overly formal or overly casual. |
| **3** | Natural teacher register. Fluent Russian. Appropriate tone for the audience (students vs. teachers vs. parents). |
| **4** | Native методист level. Perfect register switching. Warm but professional. Age-appropriate vocabulary. |

## Dimension 3: Factual Accuracy

| Score | Criteria |
|-------|----------|
| **1** | Contains factual errors (wrong formulas, incorrect historical dates, scientific inaccuracies). |
| **2** | Mostly correct but with minor inaccuracies or oversimplifications that could mislead. |
| **3** | Accurate. No errors in subject matter. Appropriate depth for the grade level. |
| **4** | Accurate and enriched. Includes nuance, edge cases, or connections to related topics. Sources or references mentioned where appropriate. |

## Dimension 4: Actionability

| Score | Criteria |
|-------|----------|
| **1** | Abstract advice. "Consider the student's needs." No concrete steps. |
| **2** | Some concrete suggestions but no structure. List of ideas without prioritization. |
| **3** | Clear action plan with specific steps. Includes examples or templates. |
| **4** | Structured plan with timeline, differentiation by student level, success criteria, and follow-up. Ready to implement immediately. |

## Dimension 5: Cultural/Regional Context

| Score | Criteria |
|-------|----------|
| **1** | Ignores Russian educational context. Uses international examples that don't apply. |
| **2** | Generic advice that could apply anywhere. No ФГОС, ОГЭ, or ЕГЭ references. |
| **3** | Russian-specific references. Mentions ФГОС, relevant exam formats, Russian school structure. |
| **4** | Deep ФГОС integration. Correct regulatory references. Awareness of Russian school realities (class sizes, resources, региональный компонент). |

## Dimension 6: Chuvash Accuracy (Module D only)

| Score | Criteria |
|-------|----------|
| **1** | Hallucinated Chuvash words/phrases. Fabricated grammar rules. No real Chuvash content. |
| **2** | Mix of correct and incorrect. Some real Chuvash words but with errors in grammar, spelling, or meaning. |
| **3** | Mostly correct. Real Chuvash vocabulary and grammar. Minor errors that a native speaker would catch. |
| **4** | Verified correct by native speaker. Proper use of special characters (ă, ĕ, ç, ÿ). Culturally appropriate. |

---

## Scoring Procedure

### Automated (LLM-as-Judge)
1. A strong evaluator model (Claude Opus 4.6 or DeepSeek V3) scores each response
2. Evaluator receives: the prompt, the response, and the rubric above
3. Evaluator outputs: score per dimension + brief justification

### Human Validation
1. A subset of responses (10% minimum) is scored by human annotators
2. Module D responses require Chuvash native speaker validation
3. Inter-annotator agreement measured via Kendall's W
4. Automated scores calibrated against human scores

### Aggregation
- **EduBench-RU Score:** Average across Modules A+B+C (35 prompts × 20 points = 700 max)
- **ChuvashBench Score:** Average across Module D (15 prompts × 24 points = 360 max)
- **Combined Score:** Weighted average (70% EduBench-RU + 30% ChuvashBench), normalized to 100
