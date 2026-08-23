import numpy as np
from normalize import load_scores, normalize

def baseline_ranking(X, indications):
    """Define a ranking function which allocates equal weights to all features/unmet needs
    
    score_i = w . x'_i
    """

    # Count n cols in our mxn matrix
    num_features = X.shape[1]
    # Set all weights to 0
    w_baseline = np.ones(num_features) / num_features

    scores = X @ w_baseline
    # Order desc, highest/best first
    ordered = np.argsort(-scores)
    ranked = [(indications[i], ordered[i]) for i in ordered]

    return scores, ranked

if __name__ == "__main__":
    raw_scores = load_scores()
    normalized_scores = normalize(raw_scores)
    indications = list(raw_scores.index)

    scores, ranked = baseline_ranking(normalized_scores, indications)

    print("Equal Weight Rankings:")
    for rank, (name, s) in enumerate(ranked, 1):
        print(f"{rank:2d}. {name:<45} {s:.4f}")