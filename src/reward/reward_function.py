"""Composite reward function for Playwright test generation."""
import os
import sys
import re
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer

WEIGHTS = {
    "syntax_valid": 0.25,
    "execution_pass": 0.35,
    "assertion_quality": 0.15,
    "style_similarity": 0.15,
    "coverage_proxy": 0.10,
}

KNOWN_TESTIDS = {
    "nav-login", "nav-todo", "nav-search",
    "login-title", "username-input", "password-input", "login-button", "login-error", "login-success",
    "todo-title", "todo-input", "add-todo-button", "todo-count", "todo-list",
    "search-title", "search-input", "search-results", "search-count", "search-result-item",
}

_embedder = None
def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def _cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def assertion_quality_score(code):
    """How many meaningful assertions does the test contain?"""
    expect_count = len(re.findall(r'expect\(', code))
    if expect_count == 0:
        return 0.0
    if expect_count >= 3:
        return 1.0
    return expect_count / 3.0


def style_similarity_score(code, retrieved_examples):
    """Cosine similarity between generated code and retrieved RAG examples."""
    if not retrieved_examples:
        return 0.5
    try:
        embedder = _get_embedder()
        gen_emb = embedder.encode(code).tolist()
        sims = []
        for ex in retrieved_examples:
            ex_emb = embedder.encode(ex["code"]).tolist()
            sims.append(_cosine(gen_emb, ex_emb))
        return sum(sims) / len(sims) if sims else 0.5
    except Exception:
        return 0.5


def coverage_proxy_score(code):
    """Proxy for test coverage: counts distinct testids and interactions."""
    used_testids = set(re.findall(r"getByTestId\(['\"]([^'\"]+)['\"]\)", code))
    valid_testids = used_testids & KNOWN_TESTIDS
    # Also count dynamic testids like todo-item-N
    dynamic = sum(1 for t in used_testids if re.match(r'(todo-(item|check|text|delete))-\d+', t))
    interactions = len(re.findall(r'\.(click|fill|check|uncheck|hover|press)\(', code))
    score = min(1.0, (len(valid_testids) + dynamic + interactions) / 8.0)
    return score


def compute_reward(code, syntax_valid, execution_passed, retrieved_examples=None):
    """Compute composite reward from all signals."""
    s1 = 1.0 if syntax_valid else 0.0
    s2 = 1.0 if execution_passed else 0.0
    s3 = assertion_quality_score(code)
    s4 = style_similarity_score(code, retrieved_examples or [])
    s5 = coverage_proxy_score(code)

    breakdown = {
        "syntax_valid": s1,
        "execution_pass": s2,
        "assertion_quality": round(s3, 3),
        "style_similarity": round(s4, 3),
        "coverage_proxy": round(s5, 3),
    }

    total = sum(WEIGHTS[k] * v for k, v in breakdown.items())
    breakdown["total"] = round(total, 3)
    breakdown["weights"] = WEIGHTS
    return breakdown


def format_feedback(reward, syntax_error, execution_error, review):
    """Format reward + errors into actionable feedback for the Writer."""
    parts = ["The previous attempt did not pass. Here is the feedback:\n"]

    parts.append(f"REWARD SCORE: {reward['total']:.2f} (target: 0.80+)")
    parts.append(f"  - Syntax valid: {reward['syntax_valid']:.0f}")
    parts.append(f"  - Execution pass: {reward['execution_pass']:.0f}")
    parts.append(f"  - Assertion quality: {reward['assertion_quality']:.2f}")
    parts.append(f"  - Style similarity: {reward['style_similarity']:.2f}")
    parts.append(f"  - Coverage proxy: {reward['coverage_proxy']:.2f}")

    if syntax_error:
        parts.append(f"\nSYNTAX ERROR:\n{syntax_error}")

    if execution_error:
        parts.append(f"\nEXECUTION ERROR:\n{execution_error}")

    if review and review.get("issues"):
        parts.append(f"\nREVIEWER ISSUES:")
        for issue in review["issues"]:
            parts.append(f"  - {issue}")
        if review.get("suggestions"):
            parts.append(f"\nREVIEWER SUGGESTIONS:")
            for s in review["suggestions"]:
                parts.append(f"  - {s}")

    parts.append("\nFix these specific issues and return ONLY the corrected JavaScript code.")
    return "\n".join(parts)


if __name__ == "__main__":
    sample_code = """import { test, expect } from '@playwright/test';
test('login', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username-input').fill('admin');
  await page.getByTestId('password-input').fill('password123');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-success')).toBeVisible();
});"""
    r = compute_reward(sample_code, True, True, [])
    import json
    print(json.dumps(r, indent=2))
