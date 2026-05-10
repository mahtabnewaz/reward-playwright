import json
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("figures", exist_ok=True)

configs = [
    ("Baseline", "data/results/baseline_evaluation.json", "#888780"),
    ("+RAG", "data/results/rag_evaluation.json", "#7F77DD"),
    ("+Multi-Agent", "data/results/multiagent_evaluation.json", "#1D9E75"),
    ("Full System", "data/results/full_evaluation.json", "#E24B4A"),
]

# Load all data
all_results = {}
for name, path, color in configs:
    with open(path) as f:
        all_results[name] = json.load(f)


def passed(r):
    return r.get("execution_passed") or r.get("final_passed")


# ======== CHART 1: Overall Pass Rate Comparison ========
fig, ax = plt.subplots(figsize=(8, 5))
names = [c[0] for c in configs]
rates = []
for name, path, _ in configs:
    results = all_results[name]
    rate = sum(1 for r in results if passed(r)) / len(results) * 100
    rates.append(rate)
colors = [c[2] for c in configs]
bars = ax.bar(names, rates, color=colors, edgecolor='black', linewidth=0.5)
for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{rate:.1f}%',
            ha='center', fontsize=11, fontweight='bold')
ax.set_ylabel("Execution Pass Rate (%)", fontsize=12)
ax.set_title("Pass Rate Across All Configurations (n=49)", fontsize=13, fontweight='bold')
ax.set_ylim(0, 110)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig1_pass_rates.png", dpi=200)
plt.savefig("figures/fig1_pass_rates.pdf")
plt.close()
print("Saved figures/fig1_pass_rates.png")


# ======== CHART 2: Pass Rate by Complexity ========
fig, ax = plt.subplots(figsize=(10, 5))
complexities = ["easy", "medium", "hard"]
x = np.arange(len(complexities))
width = 0.2

for i, (name, path, color) in enumerate(configs):
    results = all_results[name]
    rates = []
    for comp in complexities:
        comp_r = [r for r in results if r["complexity"] == comp]
        rate = sum(1 for r in comp_r if passed(r)) / len(comp_r) * 100
        rates.append(rate)
    ax.bar(x + i*width, rates, width, label=name, color=color, edgecolor='black', linewidth=0.5)

ax.set_xticks(x + 1.5*width)
ax.set_xticklabels([c.capitalize() for c in complexities], fontsize=11)
ax.set_ylabel("Pass Rate (%)", fontsize=12)
ax.set_title("Pass Rate by Test Complexity", fontsize=13, fontweight='bold')
ax.set_ylim(0, 115)
ax.legend(fontsize=10, loc='upper right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig2_by_complexity.png", dpi=200)
plt.savefig("figures/fig2_by_complexity.pdf")
plt.close()
print("Saved figures/fig2_by_complexity.png")


# ======== CHART 3: Pass Rate by Category ========
fig, ax = plt.subplots(figsize=(11, 5))
categories = ["login", "navigation", "todo", "search", "cross-feature", "ui"]
x = np.arange(len(categories))

for i, (name, path, color) in enumerate(configs):
    results = all_results[name]
    rates = []
    for cat in categories:
        cat_r = [r for r in results if r["category"] == cat]
        if cat_r:
            rate = sum(1 for r in cat_r if passed(r)) / len(cat_r) * 100
        else:
            rate = 0
        rates.append(rate)
    ax.bar(x + i*width, rates, width, label=name, color=color, edgecolor='black', linewidth=0.5)

ax.set_xticks(x + 1.5*width)
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylabel("Pass Rate (%)", fontsize=12)
ax.set_title("Pass Rate by Category", fontsize=13, fontweight='bold')
ax.set_ylim(0, 115)
ax.legend(fontsize=10, loc='lower right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig3_by_category.png", dpi=200)
plt.savefig("figures/fig3_by_category.pdf")
plt.close()
print("Saved figures/fig3_by_category.png")


# ======== CHART 4: Iteration Distribution (Full System Only) ========
full_results = all_results["Full System"]
iter_counts = [r["iteration_count"] for r in full_results]
iter_dist = {}
for k in iter_counts:
    iter_dist[k] = iter_dist.get(k, 0) + 1

fig, ax = plt.subplots(figsize=(8, 5))
keys = sorted(iter_dist.keys())
vals = [iter_dist[k] for k in keys]
bars = ax.bar(keys, vals, color="#E24B4A", edgecolor='black', linewidth=0.5)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(v),
            ha='center', fontsize=11, fontweight='bold')
ax.set_xlabel("Number of Iterations", fontsize=12)
ax.set_ylabel("Number of Tests", fontsize=12)
ax.set_title(f"Iteration Distribution (Full System, avg={sum(iter_counts)/len(iter_counts):.2f})",
             fontsize=13, fontweight='bold')
ax.set_xticks(keys)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig4_iterations.png", dpi=200)
plt.savefig("figures/fig4_iterations.pdf")
plt.close()
print("Saved figures/fig4_iterations.png")


# ======== CHART 5: Reward Convergence for Multi-Iteration Tests ========
multi_iter = [r for r in full_results if r["iteration_count"] > 1]
if multi_iter:
    fig, ax = plt.subplots(figsize=(9, 5))
    for r in multi_iter:
        rewards = [it["reward"]["total"] for it in r["iterations"]]
        x = list(range(1, len(rewards) + 1))
        passed_iter = next((i+1 for i, it in enumerate(r["iterations"]) if it["execution_passed"]), None)
        ax.plot(x, rewards, marker='o', label=f"{r['requirement_id']}", linewidth=1.5, markersize=6)
        if passed_iter:
            ax.scatter([passed_iter], [rewards[passed_iter-1]], color='green', s=120,
                      marker='*', zorder=5, edgecolor='black', linewidth=0.8)
    ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.6, label='Threshold (0.8)')
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel("Reward Score", fontsize=12)
    ax.set_title("Reward Score Trajectory for Tests Requiring Refinement",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc='lower right', ncol=2)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig("figures/fig5_reward_trajectory.png", dpi=200)
    plt.savefig("figures/fig5_reward_trajectory.pdf")
    plt.close()
    print("Saved figures/fig5_reward_trajectory.png")


print("\nAll figures saved to figures/")
print("Files:")
for f in sorted(os.listdir("figures")):
    print(f"  figures/{f}")
