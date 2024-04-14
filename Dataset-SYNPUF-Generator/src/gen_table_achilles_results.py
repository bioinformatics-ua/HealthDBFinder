import pandas as pd
import numpy as np
import random
import os

def generate_random_stratum():
    # Generate a random integer for stratum value
    return random.randint(1, 1000)

def generate_statistics(include_values):
    # These values are not relevant for this work, just to keep the dataset consistent with original database
    if include_values:
        value = random.randint(500, 1000)
        return {
            'min_value': value,
            'max_value': value * 100,
            'avg_value': value * 50,
            'stdev_value': value/10,
            'median_value': value * 49,
            'p10_value': value * 0.1,
            'p25_value': value * 0.3,
            'p75_value': value * 0.7,
            'p90_value': value * 0.95
        }
    else:
        return {
            'min_value': None,
            'max_value': None,
            'avg_value': None,
            'stdev_value': None,
            'median_value': None,
            'p10_value': None,
            'p25_value': None,
            'p75_value': None,
            'p90_value': None
        }
        
def generate_stratums(achilles, idx):
    concept = achilles["stratum_1"].iloc[idx]
    if not isinstance(concept, int):
        if isinstance(concept, float):
            if not concept.is_integer():
                concept = None
    return {
        'stratum_1': concept,
        'stratum_2': 8532 if random.random() > 0.55 else 8507 if random.random() > 0.5 else None,
        'stratum_3': None, # Always empty, only contains migration dates (database metadata)
        'stratum_4': None, # Always empty, only contains versions of databases or vocabularies(database metadata)
        'stratum_5': None, # Always empty, only contains versions of databases or vocabularies (database metadata)
    }
            
def generate_data(achilles, noise, noise2, s_id, e_id):
    data = []
    for idx in range(len(achilles)):
        include_values = random.random() > 0.7
        stats = generate_statistics(include_values)
        stratums = generate_stratums(achilles, idx)
        data_source_id = random.randint(s_id, e_id)
        value = int(achilles["count_value"].iloc[idx] * (random.random() + noise))
        data.append({
            'data_source_id': data_source_id,
            'analysis_id': achilles["analysis_id"].iloc[idx],
            **stratums,
            'count_value': int(random.randint(0, value) * (random.random() + noise2)),
            **stats
        })
    return pd.DataFrame(data)

def main():
    noise = 0.15
    noise2 = 0.25
    s_id = 1
    e_id = 500
    file_path = 'dataset/achilles_results.csv'
    input_path = "inputs/achilles_results-04-04.csv"
    
    achilles = pd.read_csv(input_path)
    achilles.columns = ["id", "analysis_id", "stratum_1", "stratum_2", "stratum_3", "stratum_4", "stratum_5", "count_value", "data_source_id", "avg_value", "max_value", "median_value", "min_value", "p10_value", "p25_value", "p75_value", "p90_value", "stdev_value"]
    
    df = generate_data(achilles, noise, noise2, s_id, e_id)
    df.to_csv(file_path, index=False)
    print(f"Data is ready and stored at '{file_path}'.")

if __name__ == '__main__':
    main()
