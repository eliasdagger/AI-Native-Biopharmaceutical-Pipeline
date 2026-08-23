import os

import numpy as np
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "raw_scores.csv")


def load_scores(file_path=DATA_PATH):
    """Load raw 0-10 scores. Rows = indications, cols = criteria.
    Returns the DataFrame so labels (index, columns) are preserved for plotting.

    # -- My manual implementation for transparency -----
    # def create_indications_as_vector(file_path=DATA_PATH):
    #     indication_vectors = {}
    #     with open(file_path, "r") as c:
    #         reader = csv.reader(c)
    #         header = next(reader)
    #         print(header)
            
    #         for indication in reader: 
    #             indication_vectors[indication[0]] = [int(w) for w in indication[1:]]
    #             print(f"Created {indication[0]} as a vector ")

    #     return indication_vectors

    # def create_unmet_score_vectors(file_path=DATA_PATH):
    #     unmet_needs_vectors = {}
    #     with open(file_path, "r") as c:
    #         reader = csv.reader(c)
    #         header = next(reader)
    #         unmet_lst = [header[i] for i in range(len(header))]
    #         for unmet_need in reader:
    #             for i in range(1, len(header)):
    #                 unmet_needs_vectors.setdefault(unmet_lst[i], []).append(int(unmet_need[i]))
    #                 print(f"Mapped: {unmet_lst[i]} -> {unmet_need[i]}")

    #     return unmet_needs_vectors
    """
    raw = pd.read_csv(file_path, index_col=0)
    return raw


def normalize(raw):
    """
    Normalize each unmet needs criterion for each indication (col-wise) 

    -- Manual implementation -----
    # normalized_scores = {}
    
    #     for unmet_need, scores in unmet_vectors.items():
    #         res = []
    #         min_score = min(scores)
    #         max_score = max(scores)
    
    #         for i in scores:
    #             if max_score == min_score:
    #                 res = [0.5] * len(scores)
    #             else:
    #                 res = [(i - min_score) / (max_score - min_score) for i in scores]
    
    #         normalized_scores[unmet_need] = res
    
    #     return normalized_scores
    
    """
    X_raw = raw.values.astype(float)
    col_min = X_raw.min(axis=0)
    col_max = X_raw.max(axis=0)

    denominator = col_max - col_min
    denominator[denominator == 0] = 1                      
    X = (X_raw - col_min) / denominator
    X[:, (col_max - col_min) == 0] = 0.5

    return X


if __name__ == "__main__":
    raw = load_scores()
    X = normalize(raw)
    print("Indications:\n", list(raw.index))
    print("Criteria:\n", list(raw.columns))
    print("Normalized matrix:\n", X)
    