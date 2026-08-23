import numpy as np
from normalize import load_scores, normalize

def monte_carlo(X, num_samples=10000, seed=42):
    np.random.seed(seed)
    num_features = X.shape[1]

    W = np.random.dirichlet(np.ones(num_features), num_samples)

    all_scores = X @ W.T
    all_ranks = np.argsort(-all_scores, axis=0).argsort(axis=0) + 1
    print(all_ranks)
    
    expected_rank = all_ranks.mean(axis=1)
    rank_std = all_ranks.std(axis=1)
    rank_5th = np.percentile(all_ranks, 5, axis=1)
    rank_95th = np.percentile(all_ranks, 95, axis=1)

    return {
        "all_ranks": all_ranks,
        "expected_rank": expected_rank,
        "rank_std": rank_std,
        "rank_90_interval": list(zip(rank_5th, rank_95th)),
    }


if __name__ == "__main__":
    raw = load_scores()
    X = normalize(raw)
    indications = list(raw.index)

    results = monte_carlo(X)
    print(f"{'Indication':<44} {'E[rank]':>12} {'std':>3} {'90% int':>6}")
    for i, name in enumerate(indications):
        low, high = results["rank_90_interval"][i]
        print(f"{name:<45} {results['expected_rank'][i]:>8.2f} "
              f"{results['rank_std'][i]:>6.2f} [{low:.0f}, {high:.0f}]")