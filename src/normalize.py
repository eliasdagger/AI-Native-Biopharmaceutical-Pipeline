import os
import csv
from score import create_indications_as_vector, INDICATIONS
from typing import Dict, List

unmet_needs = [
    "clinical_severity",
    "therepeutic_effectiveness_gap",
    "access_and_affordability_gap",
    "mechanistic_coverage_gap",
    "competitive_density",
    "repurposing_tractability"
]

def create_unmet_score_vectors(vectors: Dict[str, List[int]]):
    unmet_scores_normalized = {}
    for indication, scores in vectors.items():
        for i in scores:
            unmet_scores_normalized[unmet_needs[0]] = scores[i]
    return unmet_scores_normalized

def normalize_unmet_needs(unmet_vectors):
    normalized_scores = {}
    for __, scores in unmet_vectors:
        res = []
        for score in scores:
            
            min_score = min(scores)
            max_score = max(scores)

            res.append((score - min_score) / (max_score - min_score))
            
        for i in INDICATIONS:
            normalized_scores[INDICATIONS[i]].append(res[i])

    return normalized_scores

print(normalize_unmet_needs(create_unmet_score_vectors(create_indications_as_vector())))