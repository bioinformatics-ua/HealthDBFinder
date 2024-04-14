from ollama import Client
import random

def exec_ollama():
    client = Client(host='http://192.168.238.77:443')
    response = client.chat(model='cat1:latest', messages=[
        {
            'role': 'user',
            'content': 'generate 10 databases.',
        },
    ])
    return response

def use_ollama(NUM = 500):
    institutions = set()
    acronyms = list()

    while len(institutions) < NUM:
        data = exec_ollama()["message"]["content"]

        for line in data.splitlines():
            tmpLine = line.split("-")
            if len(tmpLine) == 2:
                acronym = tmpLine[0].strip().split(" ")
                if len(acronym) == 2:
                    acr = acronym[1].strip()
                    inst = acr+";"+tmpLine[1].strip()
                    if acr not in acronyms:
                        institutions.add(inst)
                        acronyms.append(acr)
                    print(inst, len(institutions))
        #print(data)
        
def write_file(institutions):
    f = open("aux/database_names.txt", "w")
    idx = 1
    for x in institutions:
        f.write(str(idx)+";"+x+"\n")
        idx += 1
    f.close()

def process_aux(file_path="aux/tmp_database_names.txt"):
    f = open(file_path, "r")
    institutions = set()
    acronyms = list()
    for x in f.readlines():
        line = x.strip().split(";")
        acr = line[0].strip()
        inst = " ".join(line[1].split()[:-1])
        inst = acr+";"+inst
        if acr not in acronyms:
            institutions.add(inst)
            acronyms.append(acr)
    return institutions

def main():
    institutions = process_aux()
    write_file(institutions)

if __name__ == '__main__':
    main()