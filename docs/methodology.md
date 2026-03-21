# EduBench-RU Methodology

## How to Run

### Prerequisites
- Python 3.10+
- OpenRouter API key (or adapt for direct API access)

### Running the Benchmark

```bash
# Full run (all models)
OPENROUTER_API_KEY=key python code/run_benchmark.py

# By tier
OPENROUTER_API_KEY=key python code/run_benchmark.py --batch=frontier
OPENROUTER_API_KEY=key python code/run_benchmark.py --batch=midtier
OPENROUTER_API_KEY=key python code/run_benchmark.py --batch=opensource

# Single model
OPENROUTER_API_KEY=key python code/run_benchmark.py --model="Claude Opus 4.6"

# View results summary
python code/run_benchmark.py --summary
```

### Results Format

Each model produces a JSON file in `data/results/<model-name>.json`:

```json
{
  "model": {"id": "...", "label": "...", "vram": null, "open": false},
  "benchmark": "EduBench-RU",
  "version": "0.1",
  "timestamp": "2026-03-21T...",
  "system_prompt": "...",
  "max_tokens": 8192,
  "temperature": 0.7,
  "results": [
    {
      "prompt_id": "A1.1",
      "module": "A",
      "category": "Lesson Planning",
      "success": true,
      "content": "...",
      "elapsed": 24.2,
      "tokens": 1320,
      "prompt_tokens": 180,
      "tok_per_sec": 54.5
    }
  ]
}
```

### Resumability

The runner saves after each prompt. If interrupted, re-running skips completed models automatically. Delete a model's JSON file to force re-run.

## Adding Models

Edit the `MODELS` dict in `code/run_benchmark.py`. Each model needs:
- `id`: OpenRouter model identifier
- `label`: Human-readable name (used for filenames and display)
- `vram`: Minimum VRAM in GB for local Q4 deployment (null for API-only)
- `open`: Whether the model weights are publicly available

## Adding Prompts

Edit `data/prompts.json`. Each prompt needs:
- `id`: Unique identifier (e.g., "A1.1", "D2.3")
- `module`: A, B, C, or D
- `category`: Human-readable category name
- `text`: The prompt text in Russian

## Local Model Testing

For models running on local hardware (LM Studio, Ollama, llama.cpp), use any OpenAI-compatible endpoint:

```bash
# Point to local LM Studio
OPENROUTER_API_KEY=not-needed \
  python code/run_benchmark.py --model="Local Model"
```

Modify the `OPENROUTER_URL` in the script or set it via environment variable.

## Evaluation

See [rubric.md](rubric.md) for the full scoring rubric.

Automated scoring (LLM-as-judge) script: `code/scoring/llm_judge.py` (coming soon).
