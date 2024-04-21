import pprint
import json

from read_question_templates import read_question_templates
from convert_from_table import read_csv_file
from build_questions import build_questions
from build_gold_standard import build_gold_standard

def main():
    #Files location
    questions_path = 'aux/question_templates.txt'  
    concepts_path = [
        'datasets/sqllab_untitled_query_2_20240330T192808.csv',
        'datasets/sqllab_untitled_query_2_20240330T193153.csv'
    ]
    
    #Question templates
    characterization_questions = read_question_templates(questions_path)
    questions_template = characterization_questions["Characterization"]

    #Concepts
    concepts = dict()
    for file in concepts_path:
        concepts.update(read_csv_file(file))
    
    #Build questions
    questions = build_questions(questions_template, concepts)
    f = open("aux/questions.txt", "w")
    for concept in questions:
        f.write(f"{concept},{questions[concept]}\n")
    f.close()     
    
    #Build gold standard
    gold_standard = build_gold_standard(questions, concepts)
    with open("output/gold_standard.json", 'w') as json_file:
        json.dump(gold_standard, json_file, indent=4)
main()