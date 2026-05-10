import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiagent_generator import generate_test, save_test
from executor import run_test, check_syntax, count_assertions

REQUIREMENTS_FILE = "data/requirements/requirements.json"
RESULTS_FILE = "data/results/multiagent_evaluation.json"
TESTS_DIR = "tests/generated/multiagent"


def evaluate():
    with open(REQUIREMENTS_FILE) as f:
        requirements = json.load(f)

    print(f"\n{'='*60}")
    print(f"MULTI-AGENT EVALUATION (Config C) - {len(requirements)} requirements")
    print(f"{'='*60}\n")

    results = []
    for i, req in enumerate(requirements):
        print(f"[{i+1}/{len(requirements)}] {req['id']}: {req['description'][:55]}...")

        gen_result = generate_test(req["description"])
        filepath = save_test(gen_result, output_dir=TESTS_DIR)

        syntax = check_syntax(gen_result["code"])
        assertion_count = count_assertions(gen_result["code"])

        if syntax["valid"]:
            exec_result = run_test(filepath, timeout=30)
        else:
            exec_result = {"passed": False, "exit_code": -1, "error_message": f"Syntax: {syntax['error']}", "duration_seconds": 0.0}

        passed = exec_result["passed"]
        status = "PASS" if passed else "FAIL"
        rev = "REV" if gen_result.get("revised") else "---"
        print(f"  -> {rev} | Syntax: {'OK' if syntax['valid'] else 'ERR'} | Run: {status} | Assertions: {assertion_count} | Time: {gen_result['latency_seconds']}s")
        if not passed and exec_result.get("error_message"):
            print(f"     Error: {exec_result['error_message'][:100]}")

        result = {
            "requirement_id": req["id"],
            "category": req["category"],
            "complexity": req["complexity"],
            "description": req["description"],
            "syntax_valid": syntax["valid"],
            "syntax_error": syntax.get("error"),
            "execution_passed": passed,
            "error_message": exec_result.get("error_message"),
            "assertion_count": assertion_count,
            "generation_latency": gen_result["latency_seconds"],
            "execution_duration": exec_result.get("duration_seconds", 0),
            "retrieved_examples": gen_result.get("retrieved_examples", []),
            "review": gen_result.get("review", {}),
            "revised": gen_result.get("revised", False),
            "filepath": filepath,
            "code": gen_result["code"],
            "code_v1": gen_result.get("code_v1", ""),
        }
        results.append(result)
        time.sleep(0.5)

    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print_summary(results)
    return results


def print_summary(results):
    total = len(results)
    syntax_ok = sum(1 for r in results if r["syntax_valid"])
    exec_pass = sum(1 for r in results if r["execution_passed"])
    revised = sum(1 for r in results if r["revised"])
    avg_assert = sum(r["assertion_count"] for r in results) / total
    avg_latency = sum(r["generation_latency"] for r in results) / total

    print(f"\n{'='*60}")
    print(f"MULTI-AGENT (Config C) RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total requirements:    {total}")
    print(f"Syntax valid:          {syntax_ok}/{total} ({syntax_ok/total*100:.1f}%)")
    print(f"Execution passed:      {exec_pass}/{total} ({exec_pass/total*100:.1f}%)")
    print(f"Reviewer revisions:    {revised}/{total} ({revised/total*100:.1f}%)")
    print(f"Avg assertions/test:   {avg_assert:.1f}")
    print(f"Avg generation time:   {avg_latency:.2f}s")

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
