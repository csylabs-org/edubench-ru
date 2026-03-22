#!/usr/bin/env python3
"""
EduBench-RU LLM-as-Judge Scorer

Scores benchmark outputs using a strong evaluator model (GPT-5.4 by default).
Applies the 5-dimension rubric (6 for Module D) and outputs scores + justifications.

Usage:
  export OPENROUTER_API_KEY=your_key
  python code/scoring/llm_judge.py                    # Score all models
  python code/scoring/llm_judge.py --model="Claude Opus 4.6"  # Score one model
  python code/scoring/llm_judge.py --summary           # Print score summary

Saves scores to data/scores/<model-name>.json
"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = DATA_DIR / "results"
SCORES_DIR = DATA_DIR / "scores"
SCORES_DIR.mkdir(parents=True, exist_ok=True)

OPENROUTER_URL = "https://openrouter.ai/api/v1"

# Judge panel — 3 providers for consensus scoring
JUDGE_PANEL = [
    {"model": "openai/gpt-5.4", "label": "GPT-5.4"},
    {"model": "anthropic/claude-sonnet-4.6", "label": "Claude Sonnet 4.6"},
    {"model": "google/gemini-2.5-pro", "label": "Gemini 2.5 Pro"},
]

# Default single judge (overridden by --panel flag)
JUDGE_MODEL = JUDGE_PANEL[0]["model"]
JUDGE_LABEL = JUDGE_PANEL[0]["label"]

# Load prompts for context
with open(DATA_DIR / "prompts.json") as f:
    BENCHMARK = json.load(f)
PROMPTS_BY_ID = {p["id"]: p for p in BENCHMARK["prompts"]}

RUBRIC_BASE = """Score this response on 5 dimensions using a 1-4 scale.

## Dimensions:

1. PEDAGOGICAL QUALITY (педагогическое качество)
   1 = No structure, not usable
   2 = Some structure but generic, not ФГОС-aligned
   3 = ФГОС-aligned, clear goals, proper lesson stages, grade-appropriate
   4 = Publication-quality, innovative, differentiation included

2. LANGUAGE QUALITY (качество языка)
   1 = Grammatical errors, unnatural
   2 = Correct but stiff
   3 = Natural teacher register, fluent Russian
   4 = Native методист level, perfect register

3. FACTUAL ACCURACY (фактическая точность)
   1 = Contains factual errors
   2 = Mostly correct, minor inaccuracies
   3 = Accurate, appropriate depth
   4 = Accurate and enriched with nuance

4. ACTIONABILITY (практичность)
   1 = Abstract advice, no concrete steps
   2 = Some suggestions but unstructured
   3 = Clear action plan with specific steps
   4 = Structured plan with timeline, differentiation, ready to implement

5. CULTURAL/REGIONAL CONTEXT (культурный контекст)
   1 = Ignores Russian educational context
   2 = Generic, no ФГОС/ОГЭ/ЕГЭ references
   3 = Russian-specific, mentions ФГОС and relevant standards
   4 = Deep ФГОС integration, correct regulatory references"""

RUBRIC_CHUVASH = """
6. CHUVASH ACCURACY (точность чувашского языка)
   1 = Hallucinated/fabricated Chuvash words or grammar
   2 = Mix of correct and incorrect Chuvash
   3 = Mostly correct, minor errors a native speaker would catch
   4 = Verified correct use of Chuvash with proper special characters (ă, ĕ, ç, ÿ)"""

JUDGE_PROMPT_TEMPLATE = """You are an expert evaluator of educational AI responses for Russian K-12 education.

{rubric}

## Task

Score the following response to an education prompt.

### Original Prompt:
{prompt_text}

### Model Response:
{response_text}

## Output Format

Return ONLY a JSON object with this exact structure (no markdown, no explanation outside JSON):
{{
  "scores": {{
    "pedagogical_quality": <1-4>,
    "language_quality": <1-4>,
    "factual_accuracy": <1-4>,
    "actionability": <1-4>,
    "cultural_context": <1-4>{chuvash_field}
  }},
  "justification": "<2-3 sentences explaining the key strengths and weaknesses>"
}}"""


def score_response(api_key: str, prompt_id: str, response_text: str) -> dict:
    """Score a single response using the judge model."""
    prompt_info = PROMPTS_BY_ID.get(prompt_id, {})
    prompt_text = prompt_info.get("text", "")
    module = prompt_info.get("module", "")

    is_chuvash = module == "D"
    rubric = RUBRIC_BASE + (RUBRIC_CHUVASH if is_chuvash else "")
    chuvash_field = ',\n    "chuvash_accuracy": <1-4>' if is_chuvash else ""

    judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
        rubric=rubric,
        prompt_text=prompt_text,
        response_text=response_text[:6000],  # Truncate very long responses for judge context
        chuvash_field=chuvash_field,
    )

    start = time.time()
    try:
        resp = requests.post(
            f"{OPENROUTER_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": JUDGE_MODEL,
                "messages": [{"role": "user", "content": judge_prompt}],
                "max_tokens": 512,
                "temperature": 0.0,  # Deterministic scoring
            },
            timeout=60,
        )
        elapsed = time.time() - start
        data = resp.json()

        if "error" in data:
            return {"success": False, "error": str(data["error"]), "elapsed": round(elapsed, 1)}

        content = data["choices"][0]["message"]["content"]

        # Parse JSON from response (handle markdown wrapping)
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content
            content = content.rsplit("```", 1)[0] if "```" in content else content
            content = content.strip()
        if content.startswith("json"):
            content = content[4:].strip()

        scores_data = json.loads(content)
        return {
            "success": True,
            "scores": scores_data.get("scores", {}),
            "justification": scores_data.get("justification", ""),
            "elapsed": round(elapsed, 1),
        }
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse error: {e}. Raw: {content[:200]}", "elapsed": round(time.time() - start, 1)}
    except Exception as e:
        return {"success": False, "error": str(e), "elapsed": round(time.time() - start, 1)}


def safe_filename(label: str) -> str:
    return label.lower().replace(" ", "-").replace(".", "").replace("/", "-")


def score_model(api_key: str, result_file: Path, judge_suffix: str = "") -> dict:
    """Score all responses from a single model."""
    data = json.loads(result_file.read_text())
    label = data["model"]["label"]
    suffix = f"-{judge_suffix}" if judge_suffix else ""
    score_file = SCORES_DIR / f"{safe_filename(label)}{suffix}.json"

    # Check if already scored
    if score_file.exists():
        existing = json.loads(score_file.read_text())
        scored = sum(1 for s in existing.get("scores", []) if s.get("success"))
        total = len(data.get("results", []))
        if scored >= total:
            print(f"\n  {label}: Already scored ({scored}/{total}). Skipping.")
            return existing

    print(f"\n{'='*60}")
    print(f"  Scoring: {label} (judge: {JUDGE_LABEL})")
    print(f"{'='*60}")

    results = data.get("results", [])
    scores = []

    for i, result in enumerate(results):
        if not result.get("success"):
            scores.append({"prompt_id": result.get("prompt_id", "?"), "success": False, "error": "Original response failed"})
            continue

        prompt_id = result["prompt_id"]
        print(f"  [{i+1}/{len(results)}] {prompt_id}...", end=" ", flush=True)

        score = score_response(api_key, prompt_id, result["content"])
        score["prompt_id"] = prompt_id
        score["module"] = result.get("module", "")
        score["category"] = result.get("category", "")
        scores.append(score)

        if score["success"]:
            s = score["scores"]
            dims = [s.get("pedagogical_quality", 0), s.get("language_quality", 0),
                    s.get("factual_accuracy", 0), s.get("actionability", 0),
                    s.get("cultural_context", 0)]
            if "chuvash_accuracy" in s:
                dims.append(s["chuvash_accuracy"])
            avg = sum(dims) / len(dims)
            print(f"avg={avg:.1f} [{'/'.join(str(d) for d in dims)}]")
        else:
            print(f"FAILED: {score.get('error', '')[:60]}")

        # Save incrementally
        output = {
            "model": data["model"],
            "judge": {"model": JUDGE_MODEL, "label": JUDGE_LABEL},
            "scores": scores,
        }
        score_file.write_text(json.dumps(output, ensure_ascii=False, indent=2))

    # Print model summary
    successful = [s for s in scores if s.get("success")]
    if successful:
        all_dims = {
            "pedagogical_quality": [],
            "language_quality": [],
            "factual_accuracy": [],
            "actionability": [],
            "cultural_context": [],
            "chuvash_accuracy": [],
        }
        for s in successful:
            for dim, vals in all_dims.items():
                if dim in s.get("scores", {}):
                    vals.append(s["scores"][dim])

        print(f"\n  {'Dimension':<25} | {'Avg':>4} | {'Count':>5}")
        print(f"  {'-'*25}-+-{'-'*4}-+-{'-'*5}")
        total_avg = []
        for dim, vals in all_dims.items():
            if vals:
                avg = sum(vals) / len(vals)
                total_avg.append(avg)
                print(f"  {dim:<25} | {avg:>4.2f} | {len(vals):>5}")
        if total_avg:
            print(f"  {'OVERALL':<25} | {sum(total_avg)/len(total_avg):>4.2f} |")

    return output


def print_summary():
    """Print summary of all scores, grouped by judge."""
    dims = ["pedagogical_quality", "language_quality", "factual_accuracy", "actionability", "cultural_context"]

    # Group score files by judge
    judges_data = {}
    for f in sorted(SCORES_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        judge_label = data.get("judge", {}).get("label", "unknown")
        model_label = data["model"]["label"]
        if judge_label not in judges_data:
            judges_data[judge_label] = {}
        judges_data[judge_label][model_label] = data

    if not judges_data:
        print("  No scores found. Run scoring first.")
        return

    # Print per-judge tables
    for judge_label, models in judges_data.items():
        print(f"\n{'='*100}")
        print(f"  Judge: {judge_label}")
        print(f"{'='*100}")

        header = f"  {'Model':<30} | {'Ped':>4} | {'Lng':>4} | {'Fct':>4} | {'Act':>4} | {'Ctx':>4} | {'Chv':>4} | {'AVG':>5} | {'EduRU':>5} | {'ChvBn':>5}"
        print(header)
        print(f"  {'-'*len(header.strip())}")

        rows = []
        for model_label, data in models.items():
            successful = [s for s in data.get("scores", []) if s.get("success")]

            dim_avgs = {}
            for dim in dims + ["chuvash_accuracy"]:
                vals = [s["scores"][dim] for s in successful if dim in s.get("scores", {})]
                dim_avgs[dim] = sum(vals) / len(vals) if vals else 0

            edu_scores = [s for s in successful if s.get("module") in ("A", "B", "C")]
            edu_avg = 0
            if edu_scores:
                edu_vals = [sum(s["scores"].get(d, 0) for d in dims) / len(dims) for s in edu_scores]
                edu_avg = sum(edu_vals) / len(edu_vals)

            chv_scores = [s for s in successful if s.get("module") == "D"]
            chv_avg = 0
            if chv_scores:
                chv_vals = [sum([s["scores"].get(d, 0) for d in dims] + [s["scores"].get("chuvash_accuracy", 0)]) / 6 for s in chv_scores]
                chv_avg = sum(chv_vals) / len(chv_vals)

            active_dims = [v for v in dim_avgs.values() if v > 0]
            overall = sum(active_dims) / len(active_dims) if active_dims else 0
            rows.append((model_label, dim_avgs, overall, edu_avg, chv_avg))

        for label, da, overall, edu, chv in sorted(rows, key=lambda x: -x[2]):
            chv_str = f"{da['chuvash_accuracy']:>4.1f}" if da["chuvash_accuracy"] > 0 else "  - "
            print(f"  {label:<30} | {da['pedagogical_quality']:>4.1f} | {da['language_quality']:>4.1f} | {da['factual_accuracy']:>4.1f} | {da['actionability']:>4.1f} | {da['cultural_context']:>4.1f} | {chv_str} | {overall:>5.2f} | {edu:>5.2f} | {chv:>5.2f}")

    # Consensus table (if multiple judges)
    if len(judges_data) > 1:
        print(f"\n{'='*100}")
        print(f"  CONSENSUS (average across {len(judges_data)} judges: {', '.join(judges_data.keys())})")
        print(f"{'='*100}")

        all_models = set()
        for models in judges_data.values():
            all_models.update(models.keys())

        header = f"  {'Model':<30} | {'AVG':>5} | {'EduRU':>5} | {'ChvBn':>5} | {'Agreement':>9}"
        print(header)
        print(f"  {'-'*len(header.strip())}")

        consensus_rows = []
        for model_label in sorted(all_models):
            judge_overalls = []
            judge_edus = []
            judge_chvs = []
            for judge_label, models in judges_data.items():
                if model_label not in models:
                    continue
                data = models[model_label]
                successful = [s for s in data.get("scores", []) if s.get("success")]
                if not successful:
                    continue

                all_vals = []
                for s in successful:
                    sc = s["scores"]
                    v = [sc.get(d, 0) for d in dims]
                    if "chuvash_accuracy" in sc:
                        v.append(sc["chuvash_accuracy"])
                    all_vals.append(sum(v) / len(v))
                judge_overalls.append(sum(all_vals) / len(all_vals))

                edu_s = [s for s in successful if s.get("module") in ("A", "B", "C")]
                if edu_s:
                    judge_edus.append(sum(sum(s["scores"].get(d, 0) for d in dims) / len(dims) for s in edu_s) / len(edu_s))

                chv_s = [s for s in successful if s.get("module") == "D"]
                if chv_s:
                    judge_chvs.append(sum(sum([s["scores"].get(d, 0) for d in dims] + [s["scores"].get("chuvash_accuracy", 0)]) / 6 for s in chv_s) / len(chv_s))

            if judge_overalls:
                avg_overall = sum(judge_overalls) / len(judge_overalls)
                avg_edu = sum(judge_edus) / len(judge_edus) if judge_edus else 0
                avg_chv = sum(judge_chvs) / len(judge_chvs) if judge_chvs else 0
                spread = max(judge_overalls) - min(judge_overalls) if len(judge_overalls) > 1 else 0
                agreement = "High" if spread < 0.3 else "Medium" if spread < 0.6 else "Low"
                consensus_rows.append((model_label, avg_overall, avg_edu, avg_chv, agreement, spread))

        for label, overall, edu, chv, agreement, spread in sorted(consensus_rows, key=lambda x: -x[1]):
            print(f"  {label:<30} | {overall:>5.2f} | {edu:>5.2f} | {chv:>5.2f} | {agreement:>5} (±{spread:.2f})")


def main():
    parser = argparse.ArgumentParser(description="EduBench-RU LLM-as-Judge Scorer")
    parser.add_argument("--model", type=str, help="Score a single model by label")
    parser.add_argument("--summary", action="store_true", help="Print score summary")
    parser.add_argument("--judge", type=str, default=None, help="Override judge model (OpenRouter ID)")
    parser.add_argument("--panel", action="store_true", help="Use all 3 judges (GPT-5.4, Claude Sonnet, Gemini 2.5 Pro)")
    args = parser.parse_args()

    global JUDGE_MODEL, JUDGE_LABEL

    if args.summary:
        print_summary()
        return

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        sys.exit(1)

    result_files = sorted(RESULTS_DIR.glob("*.json"))

    if args.model:
        result_files = [f for f in result_files if args.model.lower() in f.stem.replace("-", " ")]
        if not result_files:
            print(f"No results found for: {args.model}")
            sys.exit(1)

    # Determine which judges to run
    if args.panel:
        judges = JUDGE_PANEL
    elif args.judge:
        judges = [{"model": args.judge, "label": args.judge.split("/")[-1]}]
    else:
        judges = [JUDGE_PANEL[0]]  # Default: GPT-5.4

    for judge in judges:
        JUDGE_MODEL = judge["model"]
        JUDGE_LABEL = judge["label"]
        judge_suffix = safe_filename(JUDGE_LABEL)

        print(f"\n{'#'*70}")
        print(f"  JUDGE: {JUDGE_LABEL} ({JUDGE_MODEL})")
        print(f"  Models to score: {len(result_files)}")
        print(f"{'#'*70}")

        for result_file in result_files:
            try:
                score_model(api_key, result_file, judge_suffix=judge_suffix)
            except KeyboardInterrupt:
                print("\n\nInterrupted. Partial scores saved.")
                return
            except Exception as e:
                print(f"\n  ERROR scoring {result_file.stem}: {e}")
                continue

    print_summary()


if __name__ == "__main__":
    main()
