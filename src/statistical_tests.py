"""Paired tests for statistical significance between configurations."""
import json
from scipy import stats

def load_results(path):
    with open(path) as f:
        return json.load(f)

def passed(r):
    return 1 if (r.get("execution_passed") or r.get("final_passed")) else 0

baseline = load_results("data/results/baseline_evaluation.json")
rag = load_results("data/results/rag_evaluation.json")
multiagent = load_results("data/results/multiagent_evaluation.json")
full = load_results("data/results/full_evaluation.json")

# Build paired arrays (same order, by requirement_id)
def to_dict(results):
    return {r["requirement_id"]: passed(r) for r in results}

bl_d = to_dict(baseline)
rag_d = to_dict(rag)
ma_d = to_dict(multiagent)
fl_d = to_dict(full)

ids = sorted(bl_d.keys())
bl_arr = [bl_d[i] for i in ids]
rag_arr = [rag_d[i] for i in ids]
ma_arr = [ma_d[i] for i in ids]
fl_arr = [fl_d[i] for i in ids]


def mcnemar(a, b):
    """McNemar test for paired binary outcomes."""
    b01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    b10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    if b01 + b10 == 0:
        return float('nan'), 1.0, b01, b10
    chi2 = (abs(b01 - b10) - 1) ** 2 / (b01 + b10)
    p = 1 - stats.chi2.cdf(chi2, df=1)
    return chi2, p, b01, b10


def report(name1, name2, a, b):
    chi2, p, gained, lost = mcnemar(a, b)
    delta = (sum(b) - sum(a)) / len(a) * 100
    significance = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "n.s."))
    print(f"\n{name1} → {name2}")
    print(f"  Pass rate: {sum(a)/len(a)*100:.1f}% → {sum(b)/len(b)*100:.1f}% (Δ = +{delta:.1f}%)")
    print(f"  Tests gained (failed→passed): {gained}")
    print(f"  Tests lost (passed→failed):   {lost}")
    print(f"  McNemar χ² = {chi2:.3f}, p = {p:.4f} {significance}")


print(f"\n{'='*60}")
print(f"STATISTICAL SIGNIFICANCE TESTS (McNemar's test)")
print(f"{'='*60}")
print(f"n = {len(ids)} paired observations")
print(f"Significance: *** p<0.001, ** p<0.01, * p<0.05")

report("Baseline (A)", "RAG (B)", bl_arr, rag_arr)
report("RAG (B)", "Multi-Agent (C)", rag_arr, ma_arr)
report("Multi-Agent (C)", "Full System (D)", ma_arr, fl_arr)
report("Baseline (A)", "Full System (D)", bl_arr, fl_arr)

print(f"\n{'='*60}")
