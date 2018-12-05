import ast

def readQuestion(file_name):
    question_list = []
    try:
        with open(str(file_name + '_questions.txt'),'r') as file:
            num_q_str = file.readline()
            num_q = int(num_q_str)
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
        num_q = 0
        question_list = []

    except(TypeError):
        print('Invalid file name. Returning empty list')
        num_q = 0
        question_list = []

    return num_q, question_list