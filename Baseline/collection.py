from numpy import float64
import pyterrier as pt
import json, os
import shutil
import pickle
import pandas as pd
from collections import defaultdict
from tqdm import tqdm


def init_indexer():
    if not pt.started():
        pt.init()   
    
    pt.set_property("lowercase","true")
    pt.set_property("max.term.length",300)
      
    index_path = os.path.join("./", "collection/terrier_concepts_index")
    
    if os.path.exists(index_path):
        shutil.rmtree(index_path)

    return pt.IterDictIndexer(index_path, meta={'docno': 100, 'text': 10000})   


def process_file(file):
    """ create and process Achilles Results data """
    concepts_map = {}
    
    # load concepts
    with open("./api/ir/concepts_map.json", "r") as f:
        concepts_map = json.load(f)  
    
    db_table = pd.read_csv(file, usecols=[2,8], names=["concept_id", "datasource_id"])
   
    list_concepts_per_db = defaultdict(set)
    
    for _, row in tqdm(db_table.iterrows(), total=len(db_table)):
                
        concept_id = row["concept_id"]
             
        if isinstance(concept_id, str) and concept_id.isdigit():
            concept_id = int(concept_id)
        
        if isinstance(concept_id, int):           
            if str(concept_id) in concepts_map.keys():
                
                datasource_id = str(row["datasource_id"])
                
                list_concepts_per_db[ datasource_id ].add( concepts_map[str(concept_id)] )
    
    with open("./collection/list_concepts_per_db.p", "wb") as f:
        pickle.dump(list_concepts_per_db,f)
        


def load_collection():
    with open("./collection/list_concepts_per_db.p", "rb") as f:
        list_concepts_per_db = pickle.load(f)
        
    for db_id, concepts in list_concepts_per_db.items():
        for i, concept in enumerate(concepts):
            yield {
                "docno":f"{db_id}_{i}",
                "text": str(concept)
            }


def process_concepts():
    concepts_map = {}
    concepts_table = pd.read_csv("api/ir/concept-20-12.csv", low_memory=False)

    for _, row in tqdm(concepts_table.iterrows(), total=len(concepts_table)):
        concepts_map[int(row[0])] = row[1]   # concepts_map[row["concept_id"]] = row["concept_name"]
        
    with open("api/ir/concepts_map.json", "w") as f:
        json.dump(concepts_map, f)
        