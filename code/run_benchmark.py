#!/usr/bin/env python3
"""
EduBench-RU: Benchmark runner for evaluating LLMs in Russian K-12 Education.

Usage:
  export OPENROUTER_API_KEY=your_key
  python code/run_benchmark.py                    # Run all models
  python code/run_benchmark.py --batch=frontier    # Run only frontier models
  python code/run_benchmark.py --model="Claude Opus 4.6"  # Run single model

Results are saved incrementally to data/results/<model-name>.json
Already-completed models are skipped automatically (delete the JSON to re-run).
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OPENROUTER_URL = "https://openrouter.ai/api/v1"

# --- Load prompts from data/prompts.json ---
with open(DATA_DIR / "prompts.json") as f:
    BENCHMARK = json.load(f)

PROMPTS = BENCHMARK["prompts"]
SYSTEM_PROMPT = BENCHMARK["system_prompt"]
SYSTEM_PROMPT_CHUVASH = BENCHMARK.get("system_prompt_chuvash", SYSTEM_PROMPT)
MAX_TOKENS = BENCHMARK["max_tokens"]
TEMPERATURE = BENCHMARK["temperature"]

# --- Model Registry ---
MODELS = {
    "frontier": [
        {"id": "anthropic/claude-opus-4.6", "label": "Claude Opus 4.6", "vram": None, "open": False},
        {"id": "anthropic/claude-sonnet-4.6", "label": "Claude Sonnet 4.6", "vram": None, "open": False},
        {"id": "openai/gpt-5.4", "label": "GPT-5.4", "vram": None, "open": False},
        {"id": "google/gemini-3.1-pro-preview", "label": "Gemini 3.1 Pro", "vram": None, "open": False},
        {"id": "google/gemini-2.5-pro", "label": "Gemini 2.5 Pro", "vram": None, "open": False},
    ],
    "midtier": [
        {"id": "openai/gpt-5.4-mini", "label": "GPT-5.4 Mini", "vram": None, "open": False},
        {"id": "google/gemini-2.5-flash", "label": "Gemini 2.5 Flash", "vram": None, "open": False},
        {"id": "google/gemini-3.1-flash-lite-preview", "label": "Gemini 3.1 Flash Lite", "vram": None, "open": False},
        {"id": "x-ai/grok-4.1-fast", "label": "Grok 4.1 Fast", "vram": None, "open": False},
        {"id": "moonshotai/kimi-k2.5", "label": "Kimi K2.5", "vram": None, "open": False},
        {"id": "z-ai/glm-5", "label": "GLM 5", "vram": None, "open": False},
        {"id": "deepseek/deepseek-v3.2", "label": "DeepSeek V3.2", "vram": None, "open": True},
    ],
    "opensource": [
        {"id": "qwen/qwen3-235b-a22b", "label": "Qwen3 235B A22B", "vram": 128, "open": True},
        {"id": "qwen/qwen3.5-27b", "label": "Qwen3.5 27B", "vram": 18, "open": True},
        {"id": "qwen/qwen3-32b", "label": "Qwen3 32B", "vram": 20, "open": True},
        {"id": "qwen/qwen3-14b", "label": "Qwen3 14B", "vram": 10, "open": True},
        {"id": "qwen/qwen3-8b", "label": "Qwen3 8B", "vram": 6, "open": True},
        {"id": "mistralai/mistral-large-2512", "label": "Mistral Large 3", "vram": 72, "open": True},
        {"id": "meta-llama/llama-4-maverick", "label": "Llama 4 Maverick", "vram": 64, "open": True},
        {"id": "z-ai/glm-4.7-flash", "label": "GLM 4.7 Flash", "vram": 20, "open": True},
        {"id": "microsoft/phi-4", "label": "Phi-4 14B", "vram": 10, "open": True},
        {"id": "cohere/command-a", "label": "Command A", "vram": None, "open": False},
    ],
}


def run_prompt(api_key: str, model_id: str, prompt: dict) -> dict:
    """Run a single prompt against OpenRouter API."""
    start = time.time()
    try:
        resp = requests.post(
            f"{OPENROUTER_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": model_id,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT_CHUVASH if prompt.get("module") == "D" else SYSTEM_PROMPT},
                    {"role": "user", "content": prompt["text"]},
                ],
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
            },
            timeout=300,
        )
        elapsed = time.time() - start
        data = resp.json()

        if "error" in data:
            return {
                "success": False,
                "content": f"API ERROR: {data['error']}",
                "elapsed": round(elapsed, 1),
                "tokens": 0,
                "prompt_tokens": 0,
                "tok_per_sec": 0,
            }

        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        completion_tokens = usage.get("completion_tokens", 0)
        prompt_tokens = usage.get("prompt_tokens", 0)
        tok_per_sec = completion_tokens / elapsed if elapsed > 0 else 0

        return {
            "success": True,
            "content": content,
            "elapsed": round(elapsed, 1),
            "tokens": completion_tokens,
            "prompt_tokens": prompt_tokens,
            "tok_per_sec": round(tok_per_sec, 1),
        }
    except Exception as e:
        return {
            "success": False,
            "content": f"ERROR: {e}",
            "elapsed": round(time.time() - start, 1),
            "tokens": 0,
            "prompt_tokens": 0,
            "tok_per_sec": 0,
        }


def safe_filename(label: str) -> str:
    """Convert model label to safe filename."""
    return label.lower().replace(" ", "-").replace(".", "").replace("/", "-")


def run_model(api_key: str, model_info: dict) -> dict:
    """Run all prompts against a single model. Saves incrementally."""
    label = model_info["label"]
    result_file = RESULTS_DIR / f"{safe_filename(label)}.json"

    # Skip if already completed
    if result_file.exists():
        existing = json.loads(result_file.read_text())
        completed = len([r for r in existing.get("results", []) if r.get("success")])
        if completed >= len(PROMPTS):
            print(f"\n  {label}: Already completed ({completed}/{len(PROMPTS)}). Skipping.")
            return existing

    print(f"\n{'='*60}")
    print(f"  {label} ({model_info['id']})")
    if model_info.get("vram"):
        print(f"  Local deployment: {model_info['vram']}GB VRAM (Q4)")
    print(f"{'='*60}")

    results = []
    for i, prompt in enumerate(PROMPTS):
        print(f"  [{i+1}/{len(PROMPTS)}] {prompt['id']} {prompt['category']}...", end=" ", flush=True)

        result = run_prompt(api_key, model_info["id"], prompt)
        result["prompt_id"] = prompt["id"]
        result["module"] = prompt["module"]
        result["category"] = prompt["category"]
        results.append(result)

        if result["success"]:
            print(f"{result['tok_per_sec']} tok/s | {result['elapsed']}s | {result['tokens']} tok")
        else:
            print(f"FAILED: {str(result['content'])[:80]}")

        # Save after each prompt (incremental)
        output = {
            "model": model_info,
            "benchmark": "EduBench-RU",
            "version": BENCHMARK["version"],
            "timestamp": datetime.now().isoformat(),
            "system_prompt": SYSTEM_PROMPT,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "results": results,
        }
        result_file.write_text(json.dumps(output, ensure_ascii=False, indent=2))

    # Print model summary
    successful = [r for r in results if r["success"]]
    if successful:
        avg_speed = sum(r["tok_per_sec"] for r in successful) / len(successful)
        avg_time = sum(r["elapsed"] for r in successful) / len(successful)
        total_out = sum(r["tokens"] for r in successful)

        # Per-module breakdown
        for mod in ["A", "B", "C", "D"]:
            mod_results = [r for r in successful if r["module"] == mod]
            if mod_results:
                mod_avg = sum(r["tok_per_sec"] for r in mod_results) / len(mod_results)
                mod_tok = sum(r["tokens"] for r in mod_results)
                mod_name = {"A": "Pedagogy", "B": "Subject", "C": "Copilot", "D": "Chuvash"}[mod]
                print(f"  Module {mod} ({mod_name}): {mod_avg:.1f} tok/s | {mod_tok} tokens")

        print(f"  TOTAL: {avg_speed:.1f} tok/s avg | {avg_time:.1f}s avg | {total_out} output tokens")

    return output


def print_summary():
    """Print summary of all completed results."""
    print(f"\n\n{'='*80}")
    print("EduBench-RU — Results Summary")
    print(f"{'='*80}\n")

    results_files = sorted(RESULTS_DIR.glob("*.json"))
    if not results_files:
        print("  No results found.")
        return

    print(f"  {'Model':<30} | {'OK':>3}/{len(PROMPTS)} | {'tok/s':>7} | {'Total Tokens':>12} | {'Open':>4} | {'VRAM':>5}")
    print(f"  {'-'*30}-+-{'-'*3}---+-{'-'*7}-+-{'-'*12}-+-{'-'*4}-+-{'-'*5}")

    for f in results_files:
        data = json.loads(f.read_text())
        model = data["model"]
        results = data.get("results", [])
        successful = [r for r in results if r.get("success")]

        if successful:
            avg_speed = sum(r["tok_per_sec"] for r in successful) / len(successful)
            total_out = sum(r["tokens"] for r in successful)
            open_src = "Yes" if model.get("open") else "No"
            vram = f"{model['vram']}GB" if model.get("vram") else "API"

            print(f"  {model['label']:<30} | {len(successful):>3}/{len(PROMPTS)} | {avg_speed:>6.1f} | {total_out:>12} | {open_src:>4} | {vram:>5}")


def main():
    parser = argparse.ArgumentParser(description="EduBench-RU: Russian K-12 Education LLM Benchmark")
    parser.add_argument("--batch", default="all", choices=["frontier", "midtier", "opensource", "all"],
                        help="Which batch of models to run")
    parser.add_argument("--model", type=str, help="Run a single model by label (e.g., 'Claude Opus 4.6')")
    parser.add_argument("--summary", action="store_true", help="Print summary of existing results")
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        sys.exit(1)

    # Select models
    if args.model:
        all_models = MODELS["frontier"] + MODELS["midtier"] + MODELS["opensource"]
        models_to_run = [m for m in all_models if m["label"].lower() == args.model.lower()]
        if not models_to_run:
            print(f"Model not found: {args.model}")
            print("Available models:")
            for m in all_models:
                print(f"  {m['label']}")
            sys.exit(1)
    elif args.batch == "all":
        models_to_run = MODELS["frontier"] + MODELS["midtier"] + MODELS["opensource"]
    else:
        models_to_run = MODELS[args.batch]

    print(f"\nEduBench-RU v{BENCHMARK['version']} — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Batch: {args.batch} | Models: {len(models_to_run)} | Prompts: {len(PROMPTS)}")
    print(f"Modules: A({sum(1 for p in PROMPTS if p['module']=='A')}), "
          f"B({sum(1 for p in PROMPTS if p['module']=='B')}), "
          f"C({sum(1 for p in PROMPTS if p['module']=='C')}), "
          f"D({sum(1 for p in PROMPTS if p['module']=='D')})")

    for model_info in models_to_run:
        try:
            run_model(api_key, model_info)
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Partial results saved.")
            break
        except Exception as e:
            print(f"\n  ERROR running {model_info['label']}: {e}")
            continue

    print_summary()


if __name__ == "__main__":
    main()
