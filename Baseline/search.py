import os, json, math
import pyterrier as pt
import pandas as pd
from tqdm import tqdm
from collections import defaultdict, OrderedDict

datasources_map = {}


def init_searcher():
    global datasources_map
    
    if not pt.started():
        pt.init()
        
    # load databases
    datasources_file = pd.read_csv("./api/ir/data_source-20-12.csv", low_memory=False, usecols=[0, 1, 10], names=["id", "name", "hash"])

    for _, row in tqdm(datasources_file.iterrows(), total=len(datasources_file)):
        datasources_map[ str(row["id"]) ] = { "name": row["name"], "hash": row["hash"] }
        
    index_path = "./api/collection/terrier_concepts_index"
    index_concepts = pt.IndexFactory.of(pt.IndexRef.of( index_path ))

    pt.set_property("lowercase","true")
    pt.set_property("max.term.length", 300)
    
    pt.ApplicationSetup.setProperty("stopwords.filename", "./api/ir/stop_words_english.txt")

    return pt.rewrite.tokenise() >> (pt.BatchRetrieve(index_concepts, wmodel="BM25", num_results=100)) >> pt.text.get_text(index_concepts, "text")
   
   

def search_concepts_group( qid, query, bm25 ):
    global datasources_map, threshold
    
    question_dataframe = pd.DataFrame([{"qid": qid, "query": query.lower()}])
    results = defaultdict(list)
    for i, row in bm25.transform(question_dataframe).iterrows():
        # group by db
        db_id = row["docno"].split("_")[0]
        results[db_id].append({
            "database_id": db_id,
            "score": row["score"],
            "concept": row["text"]
        })
    
    concepts = []
    rank_databases = []
    for db_id, list_r in results.items():
        
        database_name = datasources_map[db_id]["name"]
        _hash = datasources_map[db_id]["hash"]
        score = sum(map(lambda x:x["score"], list_r))
        
        if isinstance(_hash, float) and math.isnan(_hash): _hash = None
        
        if score >= threshold:
            rank_databases.append({
                "database_id": int(db_id),
                "name": database_name,
                "hash": "https://portal.ehden.eu/c/EHDEN/fingerprint/" + str(_hash) + "/1/",    #TODO: mudar no frontend de 'link' para 'hash'
                "score": score,
                # "concept_list": list(map(lambda x:x["concept"], list_r))
            })

        concepts.extend( set(map(lambda x:x["concept"], list_r)) )
    
    rank_databases.sort(key=lambda x:-x["score"])

    concepts = list(OrderedDict.fromkeys(concepts))
       
    for res in rank_databases: res.pop('score', None)            # remove the key 'score'    
    return rank_databases, concepts
    