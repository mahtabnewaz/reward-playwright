# RewardPlaywright

A multi-agent system that turns plain English into working Playwright end-to-end tests, validated against a live web application.

## What it does

You describe a test in one sentence — for example, *"Verify that adding three tasks shows count '3 tasks' then deleting one shows '2 tasks'"* — and the system produces a Playwright `.spec.js` file that actually runs and passes against a real browser.

It does this by combining three things:

- **Retrieval-augmented generation** — grounds the LLM in real Playwright examples to stop it from inventing fake selectors and fake API methods.
- **A multi-agent pipeline** — Writer, Reviewer, and Executor agents that mirror how a human QA engineer works.
- **A reward-guided loop** — runs the test against the live app, scores it on five quality signals, and feeds the error back to the Writer for another attempt if it fails (up to 5 iterations).

## Tech stack

Llama-3.3-70B (Groq Cloud) · ChromaDB · sentence-transformers · Playwright · Python 3.12 · Node.js 22

## Results

Tested on a benchmark of 49 natural-language test requirements across six categories and three difficulty tiers:

| Configuration       | Pass rate |
| ------------------- | --------- |
| Baseline (LLM only) | 57.1%     |
| + RAG               | 85.7%     |
| + Multi-Agent       | 93.9%     |
| **Full system**     | **100%**  |

Improvement from baseline to full system: **+42.9 percentage points**, statistically significant under McNemar's test.
Mean iterations under the full system: 1.22.

## Quick start

```bash
# Install
pip install -r requirements.txt
npm install
npx playwright install chromium

# Add your Groq API key to .env
echo "GROQ_API_KEYS=gsk_your_key_here" > .env

# Build the retrieval index
python src/rag/rag_pipeline.py build

# Start the target app (separate terminal)
npm run start:app

# Generate a single test
python src/full_system_generator.py "Verify the login button is visible"

# Run the full benchmark
python src/evaluate_full.py
```

## Paper

Accompanies the project paper *RewardPlaywright: Agentic RAG with Reward-Guided Multi-Agent Test Generation for Automated End-to-End Testing*, MS Software Quality Assurance course project, [University Name], 2026.

## License

MIT