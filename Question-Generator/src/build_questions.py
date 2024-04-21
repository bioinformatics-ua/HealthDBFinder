from ollama import Client
import random

def exec_ollama(content):
    client = Client(host='http://192.168.238.77:443')
    response = client.chat(model='nous-hermes2-mixtral:latest', messages=[
        {
            'role': 'user',
            'content': 'Please rewrite the following question without further commets: ' + content,
        },
    ])
    return response

def get_question(quest):
    if quest == None:
        return None
    if quest.startswith("Question:"):
        return quest.replace("Question: ", "")
    if quest.startswith("Rewritten question:"):
        return quest.replace("Rewritten question: ", "")
    if quest.endswith("?") and len(quest.split(".")) == 1:
        return quest
    
    
def build_questions(questions_template, concepts):
    questions = dict()
    OLLAMA = False
    count = 0
    for concept in concepts:
        random_index =  random.randint(0, len(questions_template) - 1)
        question_template = questions_template[random_index]
        question_template = question_template.replace("…?", " "+concept+"?")
        if OLLAMA:
            quest = None
            while quest == None:
                quest = exec_ollama(question_template)["message"]["content"]
                quest = get_question(quest)
            questions[concept] = quest
        else: 
            questions[concept] = question_template
        OLLAMA = not OLLAMA
        count += 1
        print(count, end=" ")
    return questions