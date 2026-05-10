"""Config C: Writer + Reviewer (one revision pass, no execution feedback yet)."""
import os
import sys
import time
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from groq import Groq
from dotenv import load_dotenv
from rag.rag_pipeline import retrieve
from agents.reviewer import review

load_dotenv()
API_KEYS = [k.strip() for k in os.getenv("GROQ_API_KEYS", "").split(",") if k.strip()]
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
clients = [Groq(api_key=k) for k in API_KEYS]
current_key = 0

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


def generate_test(requirement, k=5):
    start = time.time()
    examples = retrieve(requirement, k=k)
    examples_block = build_examples_block(examples)

    # === Step 1: Writer generates initial code ===
    initial_user_msg = f"{examples_block}\n\nWrite a Playwright test for this requirement:\n\n{requirement}"
    messages = [
        {"role": "system", "content": WRITER_PROMPT},
        {"role": "user", "content": initial_user_msg},
    ]
    code_v1 = call_writer(messages)

    # === Step 2: Reviewer critiques ===
    review_result = review(code_v1, requirement)

    # === Step 3: If issues found, Writer revises ===
    if not review_result["valid"] and review_result["issues"]:
        feedback_msg = (
            f"The reviewer found these issues:\n\n"
            f"ISSUES:\n" + "\n".join(f"- {i}" for i in review_result["issues"]) +
            f"\n\nSUGGESTIONS:\n" + "\n".join(f"- {s}" for s in review_result["suggestions"]) +
            f"\n\nFix the code based on this feedback. Return ONLY the corrected JavaScript code."
        )
        messages.append({"role": "assistant", "content": code_v1})
        messages.append({"role": "user", "content": feedback_msg})
        code_final = call_writer(messages)
    else:
        code_final = code_v1

    elapsed = round(time.time() - start, 2)
    return {
        "requirement": requirement,
        "code": code_final,
        "code_v1": code_v1,
        "latency_seconds": elapsed,
        "method": "multiagent",
        "retrieved_examples": [ex["id"] for ex in examples],
        "review": review_result,
        "revised": not review_result["valid"],
    }


def save_test(result, output_dir="./tests/generated"):
    os.makedirs(output_dir, exist_ok=True)
    slug = result["requirement"][:50].lower()
    slug = "".join(c if c.isalnum() else "-" for c in slug).strip("-")
    filename = f"multiagent-{slug}.spec.js"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(result["code"])
    return filepath


if __name__ == "__main__":
    print(f"Loaded {len(clients)} API keys | Model: {MODEL}")
    req = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Verify that adding three tasks shows count 3 tasks then deleting one shows 2 tasks"
    print(f"\nRequirement: {req}\n")
    result = generate_test(req)
    print(f"Retrieved: {result['retrieved_examples']}")
    print(f"Review valid: {result['review']['valid']}")
    if result['review']['issues']:
        print(f"Issues: {result['review']['issues']}")
    print(f"Revised: {result['revised']}")
    filepath = save_test(result)
    print(f"\nGenerated in {result['latency_seconds']}s | Saved: {filepath}")
    print(f"\nFinal code:\n{result['code']}")
