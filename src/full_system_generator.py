"""Config D: Full RewardPlaywright system - RAG + multi-agent + reward-guided iterative refinement."""
import os
import sys
import time
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from groq import Groq
from dotenv import load_dotenv
from rag.rag_pipeline import retrieve
from agents.reviewer import review
from reward.reward_function import compute_reward, format_feedback
from executor import run_test, check_syntax

load_dotenv()
API_KEYS = [k.strip() for k in os.getenv("GROQ_API_KEYS", "").split(",") if k.strip()]
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
clients = [Groq(api_key=k) for k in API_KEYS]
current_key = 0

MAX_ITERATIONS = 5
REWARD_THRESHOLD = 0.8

WRITER_PROMPT = """You are an expert QA engineer. You write Playwright end-to-end tests in JavaScript.

RULES:
- Use @playwright/test syntax: import { test, expect } from '@playwright/test'
- Use data-testid selectors: page.getByTestId('...')
- Include meaningful assertions using expect()
- Each test must be independent and self-contained
- Use descriptive test names
- Handle async/await properly
- The app is a single-page app. Always navigate to '/' first.
- Do NOT navigate to /login or /todo or /search.
- To switch pages click nav links: page.getByTestId('nav-login'), page.getByTestId('nav-todo'), page.getByTestId('nav-search')
- Available data-testid: nav-login, nav-todo, nav-search, login-title, username-input, password-input, login-button, login-error, login-success, todo-title, todo-input, add-todo-button, todo-count, todo-list, search-title, search-input, search-results, search-count, search-result-item
- Dynamic IDs: todo-item-N, todo-check-N, todo-text-N, todo-delete-N

Below are EXAMPLES of correct Playwright tests. Study the patterns.

OUTPUT: Return ONLY the JavaScript code. No markdown, no explanation, no triple backticks."""


def call_writer(messages, max_retries=6):
    global current_key
    for attempt in range(max_retries):
        client = clients[current_key % len(clients)]
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                max_tokens=1024,
                messages=messages,
            )
            code = response.choices[0].message.content.strip()
            if code.startswith("```"):
                code = "\n".join(code.split("\n")[1:])
            if code.endswith("```"):
                code = "\n".join(code.split("\n")[:-1])
            current_key += 1
            return code
        except Exception as e:
            current_key += 1
            wait = (attempt + 1) * 3
            print(f"     Writer error (attempt {attempt+1}): {str(e)[:80]}")
            time.sleep(wait)
    return "// GENERATION FAILED"


def build_examples_block(examples):
    block = "\n=== RETRIEVED EXAMPLES ===\n"
    for i, ex in enumerate(examples, 1):
        block += f"\nExample {i} ({ex['category']}): {ex['description']}\n```\n{ex['code']}\n```\n"
    block += "\n=== END EXAMPLES ===\n"
    return block


def save_temp_test(code, requirement, iteration):
    """Save test to temp file for execution."""
    output_dir = "tests/generated/full_iter"
    os.makedirs(output_dir, exist_ok=True)
    slug = requirement[:40].lower()
    slug = "".join(c if c.isalnum() else "-" for c in slug).strip("-")
    filename = f"full-iter{iteration}-{slug}.spec.js"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(code)
    return filepath


def generate_test(requirement, k=5):
    """Run the full reward-guided refinement loop."""
    start = time.time()
    examples = retrieve(requirement, k=k)
    examples_block = build_examples_block(examples)

    initial_user_msg = f"{examples_block}\n\nWrite a Playwright test for this requirement:\n\n{requirement}"
    messages = [
        {"role": "system", "content": WRITER_PROMPT},
        {"role": "user", "content": initial_user_msg},
    ]

    iterations = []
    final_code = None
    final_reward = None
    final_passed = False

    for iter_num in range(1, MAX_ITERATIONS + 1):
        # 1. Writer generates code
        code = call_writer(messages)

        # 2. Reviewer critiques
        review_result = review(code, requirement)

        # 3. Save and execute
        filepath = save_temp_test(code, requirement, iter_num)
        syntax = check_syntax(code)
        if syntax["valid"]:
            exec_result = run_test(filepath, timeout=30)
        else:
            exec_result = {"passed": False, "exit_code": -1, "error_message": f"Syntax: {syntax['error']}", "duration_seconds": 0.0}

        # 4. Compute reward
        reward = compute_reward(code, syntax["valid"], exec_result["passed"], examples)

        iterations.append({
            "iteration": iter_num,
            "code": code,
            "syntax_valid": syntax["valid"],
            "syntax_error": syntax.get("error"),
            "execution_passed": exec_result["passed"],
            "execution_error": exec_result.get("error_message"),
            "review": review_result,
            "reward": reward,
        })

        final_code = code
        final_reward = reward
        final_passed = exec_result["passed"]

        # 5. Check if we're done
        if exec_result["passed"]:
            break

        # 6. Otherwise, build feedback and continue
        if iter_num < MAX_ITERATIONS:
            feedback = format_feedback(reward, syntax.get("error"), exec_result.get("error_message"), review_result)
            messages.append({"role": "assistant", "content": code})
            messages.append({"role": "user", "content": feedback})

    elapsed = round(time.time() - start, 2)
    return {
        "requirement": requirement,
        "code": final_code,
        "latency_seconds": elapsed,
        "method": "full",
        "retrieved_examples": [ex["id"] for ex in examples],
        "iterations": iterations,
        "iteration_count": len(iterations),
        "final_reward": final_reward,
        "final_passed": final_passed,
        "converged": final_passed,
    }


def save_test(result, output_dir="./tests/generated"):
    os.makedirs(output_dir, exist_ok=True)
    slug = result["requirement"][:50].lower()
    slug = "".join(c if c.isalnum() else "-" for c in slug).strip("-")
    filename = f"full-{slug}.spec.js"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(result["code"])
    return filepath


if __name__ == "__main__":
    print(f"Loaded {len(clients)} API keys | Model: {MODEL}")
    req = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Verify that the login button changes appearance on hover"
    print(f"\nRequirement: {req}\n")
    result = generate_test(req)
    print(f"\nIterations: {result['iteration_count']}")
    print(f"Converged: {result['converged']}")
    print(f"Final reward: {result['final_reward']['total']:.3f}")
    print(f"Final passed: {result['final_passed']}")
    print(f"Time: {result['latency_seconds']}s")
    for it in result["iterations"]:
        print(f"\n  Iter {it['iteration']}: reward={it['reward']['total']:.2f} | exec={'PASS' if it['execution_passed'] else 'FAIL'}")
        if it.get("execution_error"):
            print(f"    Error: {it['execution_error'][:80]}")
    save_test(result)
