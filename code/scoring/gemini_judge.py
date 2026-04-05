#!/usr/bin/env python3
"""
EduBench-RU Gemini 3.1 Pro Judge — Direct API
Scores all models using Gemini 3.1 Pro via the official Google API.
Uses structured output (responseSchema) for reliable JSON.

Usage:
  python code/scoring/gemini_judge.py                     # Score all unscored models
  python code/scoring/gemini_judge.py --model="claude-opus-46"  # Score one model
  python code/scoring/gemini_judge.py --summary            # Print leaderboard
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

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.1-pro-preview"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
JUDGE_LABEL = "gemini-31-pro"

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

Return scores and a 2-3 sentence justification."""


def make_schema(is_chuvash: bool) -> dict:
    props = {
        "pedagogical_quality": {"type": "INTEGER"},
        "language_quality": {"type": "INTEGER"},
        "factual_accuracy": {"type": "INTEGER"},
        "actionability": {"type": "INTEGER"},
        "cultural_context": {"type": "INTEGER"},
    }
    required = ["pedagogical_quality", "language_quality", "factual_accuracy", "actionability", "cultural_context"]
    if is_chuvash:
        props["chuvash_accuracy"] = {"type": "INTEGER"}
        required.append("chuvash_accuracy")
    return {
        "type": "OBJECT",
        "properties": {
            "scores": {"type": "OBJECT", "properties": props, "required": required},
            "justification": {"type": "STRING"},
        },
        "required": ["scores", "justification"],
    }


def score_response(prompt_id: str, response_text: str, retries: int = 3) -> dict:
    prompt_info = PROMPTS_BY_ID.get(prompt_id, {})
    prompt_text = prompt_info.get("text", "")
    module = prompt_info.get("module", "")
    is_chuvash = module == "D"

    rubric = RUBRIC_BASE + (RUBRIC_CHUVASH if is_chuvash else "")
    judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
        rubric=rubric,
        prompt_text=prompt_text,
        response_text=response_text[:6000],
    )

    for attempt in range(retries):
        start = time.time()
        try:
            resp = requests.post(
                f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": judge_prompt}]}],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "responseSchema": make_schema(is_chuvash),
                        "temperature": 0.0,
                    },
                },
                timeout=60,
            )
            elapsed = time.time() - start
            data = resp.json()

            if "error" in data:
                if attempt < retries - 1 and data["error"].get("code") == 429:
                    time.sleep(5 * (attempt + 1))
                    continue
                return {"success": False, "error": str(data["error"]), "elapsed": round(elapsed, 1)}

            content = data["candidates"][0]["content"]["parts"][0]["text"]
            scores_data = json.loads(content)
            usage = data.get("usageMetadata", {})

            return {
                "success": True,
                "scores": scores_data.get("scores", {}),
                "justification": scores_data.get("justification", ""),
                "elapsed": round(elapsed, 1),
                "thinking_tokens": usage.get("thoughtsTokenCount", 0),
            }
        except json.JSONDecodeError as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return {"success": False, "error": f"JSON parse: {e}", "elapsed": round(time.time() - start, 1)}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return {"success": False, "error": str(e), "elapsed": round(time.time() - start, 1)}

    return {"success": False, "error": "Max retries exceeded"}


def score_model(result_file: Path) -> None:
    model_name = result_file.stem
    score_file = SCORES_DIR / f"{model_name}-{JUDGE_LABEL}.json"

    if score_file.exists():
        print(f"  Already scored: {model_name} — skipping")
        return

    with open(result_file) as f:
        results = json.load(f)

    responses = results.get("responses", results.get("results", []))
    if not responses:
        print(f"  No responses in {result_file.name}")
        return

    print(f"\n{'='*60}")
    print(f"  Scoring: {model_name} (judge: {JUDGE_LABEL})")
    print(f"{'='*60}")

    scored = []
    failed = 0
    for i, item in enumerate(responses):
        pid = item.get("prompt_id", item.get("id", f"unknown-{i}"))
        response_text = item.get("response", item.get("content", "")) or ""

        result = score_response(pid, response_text)

        if result["success"]:
            scores = result["scores"]
            vals = list(scores.values())
            avg = sum(vals) / len(vals) if vals else 0
            scored.append({"prompt_id": pid, **result})
            print(f"  [{i+1}/{len(responses)}] {pid}... avg={avg:.1f} [{'/'.join(str(v) for v in vals)}]")
        else:
            failed += 1
            scored.append({"prompt_id": pid, **result})
            print(f"  [{i+1}/{len(responses)}] {pid}... FAILED: {result['error'][:80]}")

        # No sleep needed — API call itself takes 3-4s (thinking time)
        # Gemini paid tier: 1000 RPM limit, we do ~15 RPM max

    output = {
        "model": model_name,
        "judge": JUDGE_LABEL,
        "judge_model": f"google/{GEMINI_MODEL}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total": len(responses),
        "scored": len(responses) - failed,
        "failed": failed,
        "scores": scored,
    }

    with open(score_file, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved: {score_file.name} ({len(responses)-failed}/{len(responses)} scored)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    global GEMINI_API_KEY
    if not GEMINI_API_KEY:
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    if not GEMINI_API_KEY and not args.summary:
        print("ERROR: Set GEMINI_API_KEY environment variable")
        sys.exit(1)

    result_files = sorted(RESULTS_DIR.glob("*.json"))

    if args.model:
        search = args.model.lower().replace("-", " ")
        result_files = [f for f in result_files if search in f.stem.replace("-", " ")]
        if not result_files:
            print(f"No results found for: {args.model}")
            sys.exit(1)

    print(f"Gemini 3.1 Pro Judge — {len(result_files)} models to score")
    print(f"API: Direct Google (not OpenRouter)")

    for rf in result_files:
        score_model(rf)

    print("\n\nDone!")


if __name__ == "__main__":
    main()
