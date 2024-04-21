def get_info(databases):
    concept_set = set()
    domains = set()
    for db in databases:
        for concept in databases[db]["concepts"]:
            concept_set.add(concept["concept_id"])
            domains.add(concept["domain"])
    return list(concept_set), list(domains)

def build_gold_standard(questions, databases):
    gold_standard = list()
    
    for concept in questions:
        concept_set, domains = get_info(databases[concept])
        entry = {
            "question":questions[concept],
            "concept_set": concept_set,
            "domains": domains,
            "databases":databases[concept]
        }
        gold_standard.append(entry)
    return gold_standard