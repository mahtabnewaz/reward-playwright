import json
import os

os.makedirs("data/results/qualitative", exist_ok=True)

with open("data/results/full_evaluation.json") as f:
    full = json.load(f)

multi_iter = [r for r in full if r["iteration_count"] > 1]
multi_iter.sort(key=lambda r: -r["iteration_count"])

print(f"\n{'='*70}")
print(f"QUALITATIVE EXAMPLES")
print(f"{'='*70}\n")

for r in multi_iter:
    print(f"\n{'-'*70}")
    print(f"### {r['requirement_id']} ({r['complexity']}, {r['category']})")
    print(f"### Iterations: {r['iteration_count']}, Final reward: {r['final_reward']:.3f}")
    print(f"### Requirement: {r['description']}")
    print(f"{'-'*70}")
    for it in r["iterations"]:
        n = it["iteration"]
        status = "PASS" if it["execution_passed"] else "FAIL"
        print(f"\n--- Iteration {n} ({status}, reward={it['reward']['total']:.2f}) ---")
        if it.get("execution_error"):
            print(f"Error: {it['execution_error'][:200]}")
        code_lines = it["code"].split("\n")
        print("Code (last 8 lines):")
        for line in code_lines[-8:]:
            print(f"  {line}")

with open("data/results/qualitative/multi_iter_trajectories.json", "w") as f:
    json.dump(multi_iter, f, indent=2)

print(f"\nSaved {len(multi_iter)} trajectories")
