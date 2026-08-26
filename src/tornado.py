import numpy as np
import pandas as pd 
import os
import csv
from normalize import load_scores, normalize
from score import baseline_ranking

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw_scores.csv")

def tornado(X, indications):
    _, base_ranking = baseline_ranking(X, indications)

    base_rank_by_indication = {
        name: rank for rank, (name, _) in enumerate(base_ranking, 1)
    }

    
    # min_rank
    # max_rank

    for feature in range(X.shape[1]):
        for y in np.linspace(0, 1, 10):
            if y == 0:
                y = 0.001
            z = (1 - y) / (X.shape[1] - 1)
            M = np.full(X.shape[1], z)
            M[feature] = y

            score = X @ M
            rank = np.argsort(-score, axis=0).argsort(axis=0) + 1


if __name__ == "__main__":
    raw = load_scores()
    INDICATIONS = list(raw.index)
    norm = normalize(raw)
    tornado(norm, INDICATIONS)

