import subprocess
import json
import os
import re


def run_test(filepath, timeout=30):
    try:
        result = subprocess.run(
            ["npx", "playwright", "test", filepath, "--reporter=json"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
        error_msg = None
        duration = 0.0
        try:
            report = json.loads(result.stdout)
            for suite in report.get("suites", []):
                for spec in suite.get("specs", []):
                    for test in spec.get("tests", []):
                        for r in test.get("results", []):
                            duration = r.get("duration", 0) / 1000.0
                            if r.get("status") == "failed":
                                err = r.get("error", {})
                                error_msg = err.get("message", "Unknown error")[:300]
        except (json.JSONDecodeError, KeyError):
            if result.returncode != 0:
                error_msg = result.stderr[:300] if result.stderr else result.stdout[:300]
        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "error_message": error_msg,
            "duration_seconds": round(duration, 2),
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "exit_code": -1, "error_message": f"Timeout after {timeout}s", "duration_seconds": float(timeout)}
    except FileNotFoundError:
        return {"passed": False, "exit_code": -1, "error_message": "Playwright not found", "duration_seconds": 0.0}


def check_syntax(code):
    try:
        tmp = "/tmp/_syntax_check.js"
        with open(tmp, "w") as f:
            f.write(code)
        result = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, timeout=10)
        os.remove(tmp)
        return {"valid": result.returncode == 0, "error": result.stderr.strip()[:300] if result.returncode != 0 else None}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def count_assertions(code):
    patterns = [r'expect\(', r'\.toBeVisible\(', r'\.toHaveText\(', r'\.toContainText\(', r'\.toHaveValue\(', r'\.toBeHidden\(', r'\.toHaveCount\(', r'\.toHaveAttribute\(', r'\.toHaveURL\(', r'\.toHaveTitle\(']
    count = 0
    for p in patterns:
        count += len(re.findall(p, code))
    return count
