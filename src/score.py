import os
import csv
# Represent each 11 indications represented as a vector R7 of unmet needs.

INDICATIONS = [
    "GBM",
    "AZ",
    "IPF",
    "SCD",
    "GI-ARS",
    "MPS-VI",
    "BC",
    "CAN",
    "HX",
    "BOF",
    "BCC"
]

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw_scores.csv")

def create_indications_as_vector():
    indication_vectors = {}
    with open(DATA_PATH, "r") as c:
        reader = csv.reader(c)
        header = next(reader)
        
        for indication in reader: 
            indication_vectors[indication[0]] = [w for w in indication[1:]]
            print(f"Created {indication[0]} as a vector ")

    return indication_vectors


