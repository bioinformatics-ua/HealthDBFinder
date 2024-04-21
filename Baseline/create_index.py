import click
import json
import pandas as pd
from collections import defaultdict, OrderedDict
from tqdm import tqdm
import pyterrier as pt
import os
import shutil
import math


@click.command()
@click.argument("concept_file", help="Joao TODO")
@click.argument("achilles_results", help='Joao TODO')
@click.argument("pyterrier_index", help='Joao TODO')
@click.option("--datasources_file", help='Joao TODO', default=None)
@click.option("--countries_file", help='Joao TODO', default=None)
def main(concept_file, achilles_results, datasources_file, countries_file, pyterrier_index):
    
    concepts_map = {}
    
    # load concepts
    with open(concept_file, "r") as f:
        concepts_map = json.load(f)  
    
    db_table = pd.read_csv(achilles_results, usecols=[2,8], names=["concept_id", "datasource_id"])
   
    list_concepts_per_db = defaultdict(set)
    
    for _, row in tqdm(db_table.iterrows(), total=len(db_table)):
                
        concept_id = row["concept_id"]
             
        if isinstance(concept_id, str) and concept_id.isdigit():
            concept_id = int(concept_id)
        
        if isinstance(concept_id, int):           
            if str(concept_id) in concepts_map.keys():
                
                datasource_id = str(row["datasource_id"])
                
                list_concepts_per_db[ datasource_id ].add( concepts_map[str(concept_id)] )
    
    if datasources_file and countries_file:
        countries_db = pd.read_csv(countries_file, low_memory=False, usecols=[0, 1, 2], names=["id", "country", "continent"])
        datasources_db = pd.read_csv(datasources_file, low_memory=False, usecols=[0, 5], names=["database_id", "id"])
        
        db_countries = pd.merge(countries_db, datasources_db, on="id") 
        
        for _, row in tqdm(db_countries.iterrows(), total=len(db_countries)):
            list_concepts_per_db[row["database_id"]].add(row["country"])
            list_concepts_per_db[row["database_id"]].add(row["continent"])
    
    def load_collections():
        for db_id, concepts in list_concepts_per_db.items():
            for i, concept in enumerate(concepts):
                yield {
                    "docno":f"{db_id}_{i}",
                    "text": str(concept)
                }
    
    if not pt.started():
        pt.init()   
    
    pt.set_property("lowercase","true")
    pt.set_property("max.term.length",300)
    
    index_path = os.path.join("./", pyterrier_index)
    
    if os.path.exists(index_path):
        shutil.rmtree(index_path)

    indexer = pt.IterDictIndexer(index_path, meta={'docno': 100, 'text': 10000})  
    indexer.index(load_collections())
       
    
        
if __name__ == '__main__':
    main()