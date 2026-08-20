import os
# Represent each 11 indications represented as a vector R7 of unmet needs.

indications = [
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

def create_indication(indications: List[str]):
    vectors = {}
    with ("/data/raw_scores.csv", "r") as c:

        for indication in indications: 
            vectors[indication] = [w for w in ]
