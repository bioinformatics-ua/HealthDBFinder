
def read_question_templates(file_path):
    questions = {}
    current_key = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('!'):
                continue
            elif line.startswith('#'):
                current_key = line[1:].strip()
                questions[current_key] = []
            elif current_key is not None:
                questions[current_key].append(line)
            else:
                print("Something is wrong")

    return questions