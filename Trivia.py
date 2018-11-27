import os, sys
import pygame
from pygame.locals import *
from question_reader import *
import unittest



# Initialize tuples for use as screen colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
hardcore_blue = (0, 0, 200)
blue = (72, 61, 139)

# Skip used to print multi-line question/answer strings without overlapping
line_skip = 0

# Constants used to track current game mode for determining what to display
GAMEBOARD = 'gameboard'
QUESTION = 'question'
ANSWER = 'answer'

# Allowed answer keys for each type of question
MC_answer_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
TF_answer_keys = [pygame.K_1, pygame.K_2]

# Set number of players from input at initial.py
number_players = 0
player_list = []
active_player_num = 0




# Class defining a Player, initializes with 0 points and user defined name
class Player:
    def __init__(self, name):
        self.points = 0
        self.name = name

    # When player object printed, name returned
    def __str__(self):
        return self.name

    def addPoints(self, score):
        self.points += score

    def losePoints(self, score):
        if self.points > score:
            self.points -= score
        else:
            self.points = 0

    def getScore(self):
        return self.points


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


"""
Now, to take the questions and show them
"""


def drawTextCentered(self, str, y_skip=-75, x_skip=0, line_width=0):
    global line_skip
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
    cr.center = self.screen.get_rect().center

    # y coordinate shifted the value inputted (defaults to 75 pixels down)
    cr.y += y_skip
    cr.x += x_skip

    # blit text in appropiate position
    self.screen.blit(text, cr)

    # if string needed to be chopped, call function recursively w/ remainder of string
    if choperoo != len(str):
        line_skip += cr.height
        self.drawTextCentered(str[choperoo:], y_skip + cr.height, x_skip, line_width)















class Jeopardy:
    # Question_dict structure is as follows:
    # question_dict = {category name:category_questions}; category_questions = {number of points:question}
    # The questions that are values are MCQuestion or TFQuestion objects
    question_dict = {}
    # Board list is used for display; 0th index is list of category names, rest of indices are list of point values
    # E.g. board = [['cat1', ..., 'cat6'],[100, ..., 100],...,[500, ..., 500]]
    board = []
    mode = GAMEBOARD
    curQ = None  # Stores current question object

    def __init__(self, screen, category_list):
        self.screen = screen

        # load fonts
        self.extraSmallFont = pygame.font.Font(None, 36)
        self.smallFont = pygame.font.Font(None, 48)
        self.bigFont = pygame.font.Font(None, 80)


        # create gameboard w/ list of keys
        self.board.append(list(self.question_dict.keys()))

        # appends list w/ length 6 of point totals to board (grid visualization)
        for p in range(100, 501, 100):
            self.board.append([p] * 6)

    def loadQuestions(self, category, category_name):
        global num_questions
        new_q_info_list = readQuestion(category)
        # check if category key in dictionary already
        if category_name not in self.question_dict.keys():
            # if not, append category input as key into dictionary and the value an empty dictionary
            self.question_dict[category_name] = {}

        for i in range(num_questions):
            # iterate through list of questions create appropriate question type objects w/ point values
            new_question_info = new_q_info_list[i]
            new_question_score = (i + 1) * 100
            if new_question_info[0] == 'MC':
                new_question = MCQuestion(new_question_info[1], new_question_info[2], int(new_question_info[3]),
                                          new_question_score)
            elif new_question_info[0] == 'TF':
                new_question = TFQuestion(new_question_info[1], int(new_question_info[2]), new_question_score)
            # set the dictionary key to the current question as it's score, and the value as the question object
            self.question_dict[category_name][new_question_score] = new_question


    def keyPressed(self, active_player, key_num):
        global active_player_num
        global number_players
        if self.mode == QUESTION:
            # answer number for current question, check if input if the same
            correct_ans_num = self.curQ.getAnsNum()
            if key_num == correct_ans_num:
                # if correct input entered, add points, and go to answer state
                active_player.addPoints(self.curQ.getValue())
            if active_player_num < number_players - 1:
                active_player_num += 1
            else:
                active_player_num = 0
            self.mode = ANSWER
        elif self.mode == ANSWER:
            # if in answer state and enter key hit, go to gameboard
            if key_num == -1:
                self.mode = GAMEBOARD

    def askQuestion(self, col, row):
        # if valid screen position selected continue
        if row != 0:
            # variable indexes to the key for the column chosen by click (CATEGORY)
            cat = self.board[0][int(col)]
            # variable contains string with the appropriate point total for the selected question (POINTS)
            points = int(row) * 100
            # if valid screen position selected continue
            if points != 0 and self.board[int(row)][int(col)] != '':
                # indexes to current question object
                self.curQ = self.question_dict[cat][points]
                # label board location as a used question
                self.board[int(row)][int(col)] = ''
                # set current state to question
                self.mode = QUESTION

    def drawTextCentered(self, str, y_skip=-75, x_skip=0, line_width=0):
        global line_skip
        choperoo = len(str)

        font = self.smallFont

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
        cr.center = self.screen.get_rect().center

        # y coordinate shifted the value inputted (defaults to 75 pixels down)
        cr.y += y_skip
        cr.x += x_skip

        # blit text in appropiate position
        self.screen.blit(text, cr)

        # if string needed to be chopped, call function recursively w/ remainder of string
        if choperoo != len(str):
            line_skip += cr.height
            self.drawTextCentered(str[choperoo:], y_skip + cr.height, x_skip, line_width)

    def draw(self):
        global line_skip
        line_skip = 0
        # display functions depending on game state
        if self.mode == GAMEBOARD:
            self.drawBoard()
        elif self.mode == QUESTION:
            new_text_list = self.curQ.getQuestionText()
            for i in range(len(new_text_list)):
                self.drawTextCentered(new_text_list[i], y_skip=-75 + line_skip, x_skip=0,
                                      line_width=self.screen.get_rect().width)
                line_skip += 40
        elif self.mode == ANSWER:
            self.drawTextCentered(self.curQ.getAnswer(), line_width=self.screen.get_rect().width)

    def drawBoard(self):
        global active_player_num

        # Grid display
        xStart, xEnd = 0, 800
        yStart, yEnd = 0, 600
        xStep = xEnd // 6
        yStep = yEnd // 6

        # Display black lines outlining grid in appropriate locations
        for x in range(xStart, xEnd + 1, xStep):
            pygame.draw.line(self.screen, BLACK, (x, yStart), (x, yEnd), 5)
        for y in range(yStart, yEnd + 1, yStep):
            pygame.draw.line(self.screen, BLACK, (xStart, y), (xEnd, y), 5)
        for i in range(0, 800, 200):
            pygame.draw.line(self.screen, BLACK, (i, 600), (i, 700), 5)

        # display text in boxes
        for x in range(0, 6):

            # display column (category) title
            text = self.smallFont.render(self.board[0][x], 1, WHITE)
            if text.get_rect().width > xStep - 5:
                text = self.extraSmallFont.render(self.board[0][x], 1, WHITE)
            self.screen.blit(text, (x * xStep + 5, 25))

            for y in range(1, 6):
                # display point total
                text = self.bigFont.render(str(self.board[y][x]), 1, WHITE)
                self.screen.blit(text, (x * xStep + 7, y * yStep + 10))

        # display player scores
        for p in range(0, number_players):
            # active player color
            if p == active_player_num:
                text = self.smallFont.render("Player " + str(p + 1), 1, RED)
            else:
                text = self.smallFont.render("Player " + str(p + 1), 1, WHITE)
            score = self.smallFont.render(str(player_list[p].getScore()), 1, WHITE)
            self.screen.blit(text, ((p * 200) + 30, 610))
            self.screen.blit(score, ((p * 200) + 30, 650))
        player_scores = []
        f = open("scores.txt", "w")
        for i in range(number_players):
            player_scores.append(player_list[i].getScore())
        f.write(str(player_scores))
        f.close()
        for i in player_scores:
            if i >= 1500:
                from endScreen import endMenu

    def getCurQType(self):
        return self.curQ.getType()


def main():
    global category_list
    global MC_answer_keys
    global TF_answer_keys
    global number_players
    global player_list
    global active_player_num
    # initialize pygame, screen, and caption
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    pygame.display.set_caption('Jeopardy')
    # mouse set to be monitored
    pygame.mouse.set_visible(1)
    # fill background with blue and update (flip)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(blue)
    pygame.display.flip()
    # allsprites = pygame.sprite.renderPlain((fist, chimp))
    clock = pygame.time.Clock()

    # initialize jeopardy class at round 1 & input file
    jeopardy = Jeopardy(screen, category_list)
    for i in range(number_players):
        player_list.append(Player(str(i)))

    # game loop
    quit = False
    while not quit:
        # framerate
        clock.tick(60)

        # event handler (X out and escape quit the game)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit = True
            # on mouse click, call mouseClick function to interpret column & point selection
            elif event.type == MOUSEBUTTONDOWN:
                jeopardy.mouseClick(pygame.mouse.get_pos())
            elif event.type == KEYDOWN and jeopardy.getCurQType() == 'MC' and event.key in MC_answer_keys:
                answer_index = int(event.key) - 48 - 1
                jeopardy.keyPressed(player_list[active_player_num], answer_index)
            elif event.type == KEYDOWN and jeopardy.getCurQType() == 'TF' and event.key in TF_answer_keys:
                answer_index = int(event.key) - 48 - 1
                jeopardy.keyPressed(player_list[active_player_num], answer_index)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                jeopardy.keyPressed(player_list[active_player_num], -1)

        # blit background clean, call jeopardy draw function depending on game state, update display
        screen.blit(background, (0, 0))
        screen.blit(background, (0, 0))
        jeopardy.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
