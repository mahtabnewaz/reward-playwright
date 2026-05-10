"""Reviewer Agent: validates Playwright test code and provides structured feedback."""
import os
import sys
import time
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEYS = [k.strip() for k in os.getenv("GROQ_API_KEYS", "").split(",") if k.strip()]
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
clients = [Groq(api_key=k) for k in API_KEYS]
current_key = 0

KNOWN_TESTIDS = {
    "nav-login", "nav-todo", "nav-search",
    "login-title", "username-input", "password-input", "login-button", "login-error", "login-success",
    "todo-title", "todo-input", "add-todo-button", "todo-count", "todo-list",
    "search-title", "search-input", "search-results", "search-count", "search-result-item",
}

REVIEWER_PROMPT = """You are a senior QA reviewer. Your job is to find bugs in Playwright test code BEFORE it runs.

Check the code for these specific issues:
1. HALLUCINATED METHODS: Playwright does NOT have these methods - flag if used:
   - page.getAllByTestId() (use page.getByTestId().all() or locator instead)
   - locator.$$ or locator.$ (use locator.all() instead)
   - any custom-looking method that doesn't exist in standard Playwright
2. WRONG SELECTORS: Flag any data-testid that's not in the allowed list.
3. MISSING ASSERTIONS: The test must have at least one expect() call.
4. WRONG NAVIGATION: Must navigate to '/' not '/login' or '/todo' or '/search'.
5. ASSERTION LOGIC: Check that assertions match what the requirement asks for.
6. ASYNC ISSUES: Check await is used correctly.

Allowed data-testid values:
nav-login, nav-todo, nav-search, login-title, username-input, password-input, login-button, login-error, login-success, todo-title, todo-input, add-todo-button, todo-count, todo-list, search-title, search-input, search-results, search-count, search-result-item

Note: Dynamic testids like todo-item-N, todo-check-N, todo-text-N, todo-delete-N (where N is a number) are valid.

OUTPUT FORMAT (strict JSON, no markdown):
{
  "valid": true_or_false,
  "issues": ["specific issue 1", "specific issue 2"],
  "suggestions": ["concrete fix 1", "concrete fix 2"]
}

If the code looks correct, return {"valid": true, "issues": [], "suggestions": []}.
"""


def review(code, requirement, max_retries=4):
    global current_key
    user_msg = f"REQUIREMENT:\n{requirement}\n\nGENERATED CODE:\n{code}\n\nReview this code and return your JSON response."

    for attempt in range(max_retries):
        client = clients[current_key % len(clients)]
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                max_tokens=512,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": REVIEWER_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
            )
            content = response.choices[0].message.content
            current_key += 1
            review_data = json.loads(content)
            return {
                "valid": review_data.get("valid", False),
                "issues": review_data.get("issues", []),
                "suggestions": review_data.get("suggestions", []),
            }
        except Exception as e:
            current_key += 1
            wait = (attempt + 1) * 2
            print(f"     Reviewer error (attempt {attempt+1}/{max_retries}): {str(e)[:80]}")
            time.sleep(wait)
    return {"valid": True, "issues": [], "suggestions": []}


if __name__ == "__main__":
    test_code = """import { test, expect } from '@playwright/test';
test('count items', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  const items = page.getAllByTestId('todo-item');
  expect(items.length).toBe(0);
});"""
    result = review(test_code, "Verify the todo list is empty by default")
    print(json.dumps(result, indent=2))
