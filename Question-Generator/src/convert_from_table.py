import csv
import pprint

def calculate_position_index(content):
    new_content = dict()
    for concept in content:
        db_drc = list()
        for db in content[concept]:
            db_drc.append((db, content[concept][db]["sum_drc"]))
        sorted_list = sorted(db_drc, key=lambda x: 0-x[1])
        index = 0
        for x in sorted_list:
            new_content[concept] = content[concept]
            new_content[concept][x[0]]["position_index"] = index
            index += 1
    return new_content
    
def read_csv_file(csv_file):
    content = dict()

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'name' in row and 'acronym' in row and 'database_type' in row and 'country' in row and 'concept_id' in row and 'concept_name' in row and 'domain_id' in row and 'rc' in row and 'drc' in row:
                if not row['concept_name'][0].isdigit():
                    concept = row['concept_name'].split()[0]
                    if concept not in content:
                        content[concept] = dict()
                    if row['acronym'] not in content[concept]:
                        content[concept][row['acronym']] = {
                           "position_index": 0, 
                           "concepts": list(),
                           "sum_rc": 0,
                           "sum_drc": 0,
                        }
                    
                    row_dict = {
                        "domain": row['domain_id'],
                        "concept_name": row['concept_name'],
                        "concept_id": int(row['concept_id']),
                        "rc": int(row['rc']),
                        "drc": int(row['drc'])
                    }
                    content[concept][row['acronym']]["concepts"].append(row_dict)
                    content[concept][row['acronym']]["sum_rc"] += int(row['rc'])
                    content[concept][row['acronym']]["sum_drc"] += int(row['drc'])
            else:
                print("Warning: Skipping row - missing required columns")
    
    return calculate_position_index(content)