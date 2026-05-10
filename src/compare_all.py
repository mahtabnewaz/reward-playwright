import json

configs = [
    ("A: Baseline", "data/results/baseline_evaluation.json"),
    ("B: +RAG", "data/results/rag_evaluation.json"),
    ("C: +Multi-Agent", "data/results/multiagent_evaluation.json"),
    ("D: Full System", "data/results/full_evaluation.json"),
]

print(f"\n{'='*80}")
print(f"COMPARATIVE RESULTS — All Configurations")
print(f"{'='*80}\n")
print(f"{'Config':<20} {'Pass Rate':<12} {'Easy':<8} {'Medium':<8} {'Hard':<8} {'Avg Latency':<12}")
print("-" * 80)

for name, path in configs:
    with open(path) as f:
        results = json.load(f)
    total = len(results)
    passed = sum(1 for r in results if r.get("execution_passed") or r.get("final_passed"))
    
    easy = [r for r in results if r["complexity"] == "easy"]
    easy_pass = sum(1 for r in easy if r.get("execution_passed") or r.get("final_passed"))
    medium = [r for r in results if r["complexity"] == "medium"]
    medium_pass = sum(1 for r in medium if r.get("execution_passed") or r.get("final_passed"))
    hard = [r for r in results if r["complexity"] == "hard"]
    hard_pass = sum(1 for r in hard if r.get("execution_passed") or r.get("final_passed"))
    
    latency = sum(r.get("generation_latency", 0) for r in results) / total
    
    print(f"{name:<20} {passed}/{total} ({passed/total*100:.1f}%)  "
          f"{easy_pass}/{len(easy)} ({easy_pass/len(easy)*100:.0f}%)  "
          f"{medium_pass}/{len(medium)} ({medium_pass/len(medium)*100:.0f}%)  "
          f"{hard_pass}/{len(hard)} ({hard_pass/len(hard)*100:.0f}%)  "
          f"{latency:.2f}s")

print(f"\n{'='*80}")
