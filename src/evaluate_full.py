import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from full_system_generator import generate_test, save_test
from executor import check_syntax, count_assertions

REQUIREMENTS_FILE = "data/requirements/requirements.json"
RESULTS_FILE = "data/results/full_evaluation.json"
TESTS_DIR = "tests/generated/full"


def evaluate():
    with open(REQUIREMENTS_FILE) as f:
        requirements = json.load(f)

    print(f"\n{'='*60}")
    print(f"FULL SYSTEM EVALUATION (Config D) - {len(requirements)} requirements")
    print(f"{'='*60}\n")

    results = []
    for i, req in enumerate(requirements):
        print(f"[{i+1}/{len(requirements)}] {req['id']}: {req['description'][:55]}...")

        gen_result = generate_test(req["description"])
        filepath = save_test(gen_result, output_dir=TESTS_DIR)

        assertion_count = count_assertions(gen_result["code"])
        passed = gen_result["final_passed"]
        iters = gen_result["iteration_count"]
        reward = gen_result["final_reward"]["total"] if gen_result["final_reward"] else 0

        status = "PASS" if passed else "FAIL"
        print(f"  -> Iters: {iters} | Reward: {reward:.2f} | Run: {status} | Assertions: {assertion_count} | Time: {gen_result['latency_seconds']}s")

        result = {
            "requirement_id": req["id"],
            "category": req["category"],
            "complexity": req["complexity"],
            "description": req["description"],
            "execution_passed": passed,
            "final_reward": reward,
            "iteration_count": iters,
            "assertion_count": assertion_count,
            "generation_latency": gen_result["latency_seconds"],
            "retrieved_examples": gen_result.get("retrieved_examples", []),
            "iterations": gen_result["iterations"],
            "filepath": filepath,
            "code": gen_result["code"],
        }
        results.append(result)

    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print_summary(results)
    return results


def print_summary(results):
    total = len(results)
    exec_pass = sum(1 for r in results if r["execution_passed"])
    avg_iters = sum(r["iteration_count"] for r in results) / total
    avg_reward = sum(r["final_reward"] for r in results) / total
    avg_assert = sum(r["assertion_count"] for r in results) / total
    avg_latency = sum(r["generation_latency"] for r in results) / total

    # Iteration distribution
    iter_dist = {}
    for r in results:
        k = r["iteration_count"]
        iter_dist[k] = iter_dist.get(k, 0) + 1

    # Tests recovered by reward loop (passed in iter > 1)
    recovered = sum(1 for r in results if r["execution_passed"] and r["iteration_count"] > 1)

    print(f"\n{'='*60}")
    print(f"FULL SYSTEM (Config D) RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total requirements:    {total}")
    print(f"Execution passed:      {exec_pass}/{total} ({exec_pass/total*100:.1f}%)")
    print(f"Avg iterations:        {avg_iters:.2f}")
    print(f"Avg final reward:      {avg_reward:.3f}")
    print(f"Tests recovered by loop: {recovered} (passed after iter 1)")
    print(f"Avg assertions/test:   {avg_assert:.1f}")
    print(f"Avg generation time:   {avg_latency:.2f}s")

    print(f"\n--- Iteration Distribution ---")
    for k in sorted(iter_dist.keys()):
        print(f"  {k} iteration(s):  {iter_dist[k]} tests")

    print(f"\n--- By Category ---")
    for cat in sorted(set(r["category"] for r in results)):
        cat_r = [r for r in results if r["category"] == cat]
        cat_pass = sum(1 for r in cat_r if r["execution_passed"])
        print(f"  {cat:15s}  {cat_pass}/{len(cat_r)} passed ({cat_pass/len(cat_r)*100:.1f}%)")

    print(f"\n--- By Complexity ---")
    for comp in ["easy", "medium", "hard"]:
        comp_r = [r for r in results if r["complexity"] == comp]
        if comp_r:
            comp_pass = sum(1 for r in comp_r if r["execution_passed"])
            print(f"  {comp:15s}  {comp_pass}/{len(comp_r)} passed ({comp_pass/len(comp_r)*100:.1f}%)")

    print(f"\nResults saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    evaluate()
