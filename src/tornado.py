import numpy as np
import pandas as pd 
import os
import csv
from normalize import load_scores, normalize
from score import baseline_ranking

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw_scores.csv")

def tornado(X, indications):
    _, base_ranking = baseline_ranking(X, indications)

    rank_by_indication = {
        name: rank for rank, (name, _) in enumerate(base_ranking, 1)
    }
    # print(rank_by_indication)

    min_rank = dict(rank_by_indication)
    max_rank = dict(rank_by_indication)

    for i in range(X.shape[1]):
        for y in np.linspace(0, 1, 10):
            if y == 0:
                y = 0.001
            z = (1 - y) / (X.shape[1] - 1)
            M = np.full(X.shape[1], z)
            M[i] = y

            score = X @ M
            rank = np.argsort(-score, axis=0).argsort(axis=0) + 1

            for idx, indication in enumerate(indications):
                min_rank[indication] = min(min_rank[indication], rank[idx])
                max_rank[indication] = max(max_rank[indication], rank[idx])

    print("Tornado (rank sensitivity across all feature weightings):")
    print(f"{'Indication':<45}{'Baseline':>9}{'Best':>7}{'Worst':>7}{'Swing':>7}")
    for indication, base_rank in sorted(
        rank_by_indication.items(), key=lambda kv: kv[1]
    ):
        best = min_rank[indication]
        worst = max_rank[indication]
        print(
            f"{indication:<45}{base_rank:>9}{best:>7}{worst:>7}{worst - best:>7}"
        )


if __name__ == "__main__":
    raw = load_scores()
    INDICATIONS = list(raw.index)
    norm = normalize(raw)
    tornado(norm, INDICATIONS)

