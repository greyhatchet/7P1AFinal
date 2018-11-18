import ast

def readQuestion():
    question_list = []
    try:
        with open('questions.txt','r') as file:
            for line in file:
                if len(line) > 1:
                    question_lines = line.split(';')
                    question_lines = [x.strip() for x in question_lines]
                    if len(question_lines) == 4:
                        #0 is False, 1 is True
                        new_question = (question_lines[0], question_lines[1], question_lines[2])
                        question_list.append(new_question)
                    elif len(question_lines) == 5:
                        new_question = (question_lines[0], question_lines[1], ast.literal_eval(question_lines[2]), question_lines[3])
                        question_list.append(new_question)

    except(FileNotFoundError):
        print('Question file not found! Returning empty list')

    return question_list

print(readQuestion())