import os
import sys
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEYS = [k.strip() for k in os.getenv("GROQ_API_KEYS", "").split(",") if k.strip()]
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
clients = [Groq(api_key=k) for k in API_KEYS]
current_key = 0

SYSTEM_PROMPT = """You are an expert QA engineer. You write Playwright end-to-end tests in JavaScript.

RULES:
- Use @playwright/test syntax: import { test, expect } from '@playwright/test'
- Use data-testid selectors: page.getByTestId('...')
- Include meaningful assertions using expect()
- Each test must be independent and self-contained
- Use descriptive test names
- Handle async/await properly
- The app is a single-page app. Always navigate to '/' first.
- Do NOT navigate to /login or /todo or /search. They do not exist as routes.
- To switch pages click nav links: page.getByTestId('nav-login'), page.getByTestId('nav-todo'), page.getByTestId('nav-search')
- Available data-testid values: nav-login, nav-todo, nav-search, login-title, username-input, password-input, login-button, login-error, login-success, todo-title, todo-input, add-todo-button, todo-count, todo-list, search-title, search-input, search-results, search-count, search-result-item

OUTPUT: Return ONLY the JavaScript code. No markdown, no explanation, no triple backticks."""


def generate_test(requirement, max_retries=6):
    global current_key
    start = time.time()
    for attempt in range(max_retries):
        client = clients[current_key % len(clients)]
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Write a Playwright test for this requirement:\n\n{requirement}"},
                ],
            )
            code = response.choices[0].message.content.strip()
            if code.startswith("```"):
                code = "\n".join(code.split("\n")[1:])
            if code.endswith("```"):
                code = "\n".join(code.split("\n")[:-1])
            elapsed = round(time.time() - start, 2)
            current_key += 1
            return {"requirement": requirement, "code": code, "latency_seconds": elapsed, "method": "baseline"}
        except Exception as e:
            current_key += 1
            wait = (attempt + 1) * 3
            print(f"     Key error (attempt {attempt+1}/{max_retries}): {str(e)[:80]}")
            print(f"     Rotating key, waiting {wait}s...")
            time.sleep(wait)
    return {"requirement": requirement, "code": "// GENERATION FAILED", "latency_seconds": 0, "method": "baseline"}


def save_test(result, output_dir="./tests/generated"):
    os.makedirs(output_dir, exist_ok=True)
    slug = result["requirement"][:50].lower()
    slug = "".join(c if c.isalnum() else "-" for c in slug).strip("-")
    filename = f"baseline-{slug}.spec.js"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(result["code"])
    return filepath


if __name__ == "__main__":
    print(f"Loaded {len(clients)} API keys | Model: {MODEL}")
    req = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Verify that the login button is visible on the login page"
    print(f"\nRequirement: {req}\n")
    result = generate_test(req)
    filepath = save_test(result)
    print(f"Generated in {result['latency_seconds']}s")
    print(f"Saved to: {filepath}\n")
    print(result["code"])
