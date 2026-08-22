import os
import csv

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw_scores.csv")

# Represent each 11 indications represented as a vector R7 of unmet needs.
def create_indications_as_vector(file_path=DATA_PATH):
    indication_vectors = {}
    with open(file_path, "r") as c:
        reader = csv.reader(c)
        header = next(reader)
        print(header)
        
        for indication in reader: 
            indication_vectors[indication[0]] = [int(w) for w in indication[1:]]
            print(f"Created {indication[0]} as a vector ")

    return indication_vectors

def create_unmet_score_vectors(file_path=DATA_PATH):
    unmet_needs_vectors = {}
    with open(file_path, "r") as c:
        reader = csv.reader(c)
        header = next(reader)
        unmet_lst = [header[i] for i in range(len(header))]
        for unmet_need in reader:
            for i in range(1, len(header)):
                unmet_needs_vectors.setdefault(unmet_lst[i], []).append(int(unmet_need[i]))
                print(f"Mapped: {unmet_lst[i]} -> {unmet_need[i]}")

    return unmet_needs_vectors
        



    
print(create_indications_as_vector())
print(create_unmet_score_vectors())