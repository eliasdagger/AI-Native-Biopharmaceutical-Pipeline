import numpy as np
import pandas as pd 
import os
import csv
import matplotlib.pyplot as plt
from normalize import load_scores, normalize
from score import baseline_ranking

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw_scores.csv")

def tornado(X, indications):

    _, base_ranked = baseline_ranking(X, indications)
    
    rank_by_indication = {name : rank for rank, (name, _) in enumerate(base_ranked, 1)}

    min_dct = dict(rank_by_indication)
    max_dct = dict(rank_by_indication)

    for i in range(X.shape[1]): 
        for y in np.linspace(0, 10, 100):
            if y == 0:
                y = 0.001
            z = (1 - y) / (X.shape[1] - 1)
            M = np.full(X.shape[1], z)
            M[i] = y

            score = X @ M

            rank = np.argsort(-score, axis=0).argsort(axis=0) + 1

            for idx, indication in enumerate(indications):
                min_dct[indication] = min(min_dct[indication], rank[idx])
                max_dct[indication] = max(max_dct[indication], rank[idx])

    print(f"Tornado Ranking (ranked sensitivity access all feature weights")
    print(f"{'Indication':<45} {'Baseline':<9} {'Best':<7} {'Worst':<7} {'Swing':<7}")
    for indication, base_rank in sorted(
            rank_by_indication.items(), key=lambda kv: kv[1]
    ):
        best = min_dct[indication]
        worst = max_dct[indication]
        print(
            f"{indication:<45}{base_rank:>9}{best:>7}{worst:>7}{worst - best:>7}"
        )
    return rank_by_indication, min_dct, max_dct

if __name__ == "__main__":
    raw = load_scores()
    X = normalize(raw)
    indications = list(raw.index)
    baseline_ranks, min_ranks, max_ranks = tornado(X, indications)
    """
    Create Tornado Analysis using Matplotlib
    """

    baseline = np.array([])
    low_range = np.array([])
    high_range = np.array([])

    for i in range(len(indications)):
        np.append(low_range, min_ranks[indications[i]])
        np.append(high_range, min_ranks[indications[i]])
        np.append(baseline, baseline_ranks[indications[i]])

    print(f"{baseline_dct}")


    



# 3. Calculate shifts relative to the baseline
low_shifts = low_range - baseline
high_shifts = high_range - baseline

# 4. Calculate total swing width to sort the data (Crucial for the "Tornado" shape)
widths = np.abs(high_range - low_range)
sorted_indices = np.argsort(widths)  # Sorts smallest to largest

# Reorder everything so the largest impact is at the top
indications = [indications[i] for i in sorted_indices]
low_shifts = low_shifts[sorted_indices]
high_shifts = high_shifts[sorted_indices]

# 5. Build the Tornado Chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Low Range bars (left or right of baseline depending on shift)
ax.barh(indications, low_shifts, left=baseline, color='#d95f02', 
        alpha=0.8, edgecolor='black', label='Low Range Impact')

# Plot High Range bars (left or right of baseline depending on shift)
ax.barh(indications, high_shifts, left=baseline, color='#1f77b4', 
        alpha=0.8, edgecolor='black', label='High Range Impact')

# Draw a vertical dashed line straight down the baseline
ax.axvline(baseline, color='black', linestyle='--', linewidth=1.5, label=f'Baseline ({baseline})')

# 6. Clean and format the layout
ax.set_title('Sensitivity Analysis (Tornado Diagram)', fontsize=14, pad=15, fontweight='bold')
ax.set_xlabel('Output / Value Metric', fontsize=12)
ax.spines[['top', 'right', 'left']].set_visible(False)  # Remove clean clutter
ax.grid(axis='x', linestyle=':', alpha=0.6)
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()

