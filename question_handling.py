import os, sys
import pygame
from pygame.locals import *
from question_reader import *
import unittest
import random


# Initialize tuples for use as screen colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
hardcore_blue = (0, 0, 200)
blue = (72, 61, 139)

# Class for multiple choice questions
class MCQuestion:
    def __init__(self, q, a_list, a_num, value):
        self.q = q  # Question string
        self.a_list = a_list  # Tuple of answer strings
        self.a_num = int(a_num)  # Index of correct answer in a_list tuple
        self.value = value  # Point value of question

    # str() was previously used for displaying question but due to issues w/ drawTextCentered
    # it has been deprecated in favor of getQuestionText()
    def __str__(self):
        self_str = "Q: " + self.q + "\n\n"
        for i in range(len(self.a_list)):
            self_str += str(i + 1) + ": " + self.a_list[i] + "\n"
        return self_str

    # Returns list containing question string and answer strings, iterated
    # through when displaying question using drawTextCentered
    def getQuestionText(self):
        self_text_list = []
        self_text_list.append(self.q)
        for i in range(len(self.a_list)):
            self_text_list.append(str(i + 1) + ": " + self.a_list[i])
        return self_text_list

    def getAnsNum(self):
        return self.a_num

    def getValue(self):
        return self.value

    # Returns string of correct answer and its index for display on game board
    def getAnswer(self):
        ans_str = str(self.a_num + 1) + ": " + self.a_list[self.a_num]
        return ans_str

    def getType(self):
        return 'MC'


# Class for true/false questions
class TFQuestion:
    def __init__(self, q, a, value):
        self.q = q  # Question string
        self.a = a  # Int value of answer (False = 0, True = 1 by convention)
        self.value = value  # Point value of question

    # str() was previously used for displaying question but due to issues w/ drawTextCentered
    # it has been deprecated in favor of getQuestionText()
    def __str__(self):
        self_str = "Q: " + self.q + "\n1: True\n2: False"
        return self_str

    # Returns list containing question string and answer strings, iterated
    # through when displaying question using drawTextCentered
    def getQuestionText(self):
        self_text_list = []
        self_text_list.append(self.q)
        self_text_list.append("1: False")
        self_text_list.append("2: True")
        return self_text_list

    def getAnsNum(self):
        return self.a

    def getValue(self):
        return self.value

    # Returns string of answer for displaying on board
    def getAnswer(self):
        answer = "False"
        if self.a == 1:
            answer = "True"
        return answer

    def getType(self):
        return 'TF'


def drawTextCentered(str, center, screen, y_skip=-75, x_skip=0, line_width=0, line_skip=0):
    line_skip = line_skip
    smallFont = pygame.font.Font(None, 48)
    choperoo = len(str)
    font = smallFont

    # render string and compare length to screen width
    text = font.render(str, 1, WHITE)

    # if string too long, break up at first space in the last half of the string
    while text.get_rect().width > line_width:
        for c in range(int(choperoo / 2), choperoo):
            if str[c] == ' ':
                choperoo = c
                break

        # render first part of string
        text = font.render(str[:choperoo], 1, WHITE)

    # cr is first part of string get_rect() object
    cr = text.get_rect()

    # center of text is placed in the center of the screen
    cr.center = center

    # y coordinate shifted the value inputted (defaults to 75 pixels down)
    cr.y += y_skip
    cr.x += x_skip

    # blit text in appropiate position
    screen.blit(text, cr)

    # if string needed to be chopped, call function recursively w/ remainder of string
    if choperoo != len(str):
        line_skip += cr.height
        line_skip += drawTextCentered(str[choperoo:], center, screen, y_skip + cr.height, x_skip, line_width, line_skip)

    return line_skip


def loadQuestions(file_name, num_questions, question_score):
    question_list = []
    new_q_info_list = readQuestion(file_name)
    for i in range(num_questions):
        # Iterate through list of questions and create appropriate question type objects
        new_question_info = new_q_info_list[i]
        if new_question_info[0] == 'MC':
            new_question = MCQuestion(new_question_info[1], new_question_info[2], int(new_question_info[3]),
                                      question_score)
        elif new_question_info[0] == 'TF':
            new_question = TFQuestion(new_question_info[1], int(new_question_info[2]), question_score)
        question_list.append(new_question)

    return question_list


def drawQuestion(current_question, current_mode, screen_width, center, screen):
    line_skip = 0
    # display functions depending on game state
    if current_mode == 'question':
        new_text_list = current_question.getQuestionText()
        for i in range(len(new_text_list)):
            line_skip += drawTextCentered(new_text_list[i], center, screen,
                             y_skip=-75 + line_skip, x_skip=0,
                             line_width=screen_width)
            line_skip += 40
    elif current_mode == 'answer':
        drawTextCentered(current_question.getAnswer(), center, screen, line_width=screen_width)
