import click
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import pyterrier as pt
import math


@click.command()
@click.argument("pyterrier_index", help='Joao TODO')
@click.option("--datasources_file", help='Joao TODO', default=None)
def main(datasources_file, pyterrier_index):

    indexer = pt.IndexFactory.of(pt.IndexRef.of(pyterrier_index))
    
    searcher = pt.rewrite.tokenise() >> (pt.BatchRetrieve(indexer, wmodel="BM25", num_results=100)) >> pt.text.get_text(indexer, "text")

    datasources_db = pd.read_csv(datasources_file, low_memory=False, usecols=[0, 1, 4], names=["id", "name", "hash"])
    data_sources =  {}
    for _, row in tqdm(datasources_db.iterrows(), total=len(datasources_db)):
        data_sources[ str(row["id"]) ] = { "name": row["name"], "hash": row["hash"] }

    # TODO: read the query file and search for each query

    question_dataframe = pd.DataFrame([{"query": query.lower()}])
    results = defaultdict(list)
    for i, row in searcher.transform(question_dataframe).iterrows():
        # group by db
        db_id = row["docno"].split("_")[0]
        results[db_id].append({
            "database_id": db_id,
            "score": row["score"],
            "concept": row["text"]
        })
    
    rank_databases = []
    for db_id, list_r in results.items():
        
        database_name = data_sources[db_id]["name"]
        _hash = data_sources[db_id]["hash"]
        score = sum(map(lambda x:x["score"], list_r))
        
        if isinstance(_hash, float) and math.isnan(_hash): _hash = None
        
        rank_databases.append({
            "database_id": int(db_id),
            "name": database_name,
            "hash": str(_hash),
            "score": score,
            "concept_list": list(map(lambda x:x["concept"], list_r))
        })

    rank_databases.sort(key=lambda x:-x["score"])


        
if __name__ == '__main__':
    main()