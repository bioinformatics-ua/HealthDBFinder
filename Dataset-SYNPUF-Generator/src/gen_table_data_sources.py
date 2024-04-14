import pandas as pd
import random
import hashlib
import datetime

def load_databases(file_path="aux/database_names.txt"):
    f = open(file_path)
    dbs = []
    for x in f.readlines():
        line = x.strip().split(";")
        dbs.append([line[1], line[2]])
    return dbs
    
def load_countries(file_path="dataset/countries.csv"):
    f = open(file_path)
    possibleIdx = []
    for x in f.readlines():
        idx = x.split(",")[0]
        if idx.isdigit():
            possibleIdx.append(idx)
    return possibleIdx
    
def get_country_id(possibleIdx):
    return possibleIdx[random.randint(0, len(possibleIdx)-1)]
    
def hash_generator():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

def random_date_generator(start_year=2030, end_year=2035):
    """ Generates a random date between start_year and end_year. """
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Keeping it simple by maxing at 28
    return datetime.date(year, month, day).isoformat()

def generate_data(num_records):
    countries = load_countries()
    databases = load_databases()
    data = {
        "Id":[id for id in range(num_records)],
        'Name': [databases[idx][0] for idx in range(num_records)],
        'Acronym': [databases[idx][1] for idx in range(num_records)],
        
        'Hash': [hash_generator() for _ in range(num_records)],
        'Release_Date': [random_date_generator() if random.random() > 0.5 else '' for _ in range(num_records)],
        'Country_ID': [get_country_id(countries) for _ in range(num_records)]
    }
    return pd.DataFrame(data)

def main():
    num_records = 771  # Specify the number of records to generate
    df = generate_data(num_records)
    df.to_csv('dataset/data_sources.csv', index=False)
    print("Data sources CSV file has been generated and saved.")

if __name__ == '__main__':
    main()