import pygame
from pygame.locals import *
import sys
import os
import random
import platform
from question_handling import *

RED = (255, 0, 0)

# define display surface
W, H = 800, 700
HW, HH = W / 2, H / 2
AREA = W * H

os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

# setup pygame
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Game Board")
FPS = 120

# Actions if keys are pressed
def boardEvents():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            return True
        elif event.type == KEYDOWN and event.key == K_r:
            return '-x'
        elif event.type == KEYDOWN and event.key == K_a:
            return 'x'
    return

# Player Class
class BoardPiece:
    def __init__(self, color, playerNumber):
        self.color = color
        self.piece = playerNumber
        self.xCord = 33
        self.yCord = 277 + (playerNumber - 1) * 20
        self.absX = self.xCord
        self.absY = self.yCord
        self.cell_num = 0 # Stores which cell the player is in to check if they land on a minigame
        self.score = 0

    def draw(self, background):
        pygame.draw.circle(background, self.color, (self.absX, self.absY), 10, 0)

    def diceRoll(self, x):
        # check position on board and move piece appropriately
        if self.xCord < 33 + (7 * 44) or (self.xCord > 33 + (7 * 44) and self.xCord < 33 + (14 * 44) + 57):
            self.absX += 44
            self.xCord += 44
        elif self.xCord == 33 + (7 * 44):
            self.absX += 57
            self.xCord += 57
            self.absY -= 115
        elif self.xCord == 33 + (14 * 44) + 57:
            self.absX += 57
            self.xCord += 57
            self.absY += 115
        elif self.xCord > 33 + (14 * 44) + 57 and self.xCord < 33 + (26 * 44) + 57:
            self.absX += 44
            self.xCord += 44
        else:
            self.xCord = 33
            self.absX = self.xCord + x

    def worldScroll(self, scrollCord):
        self.absX = self.absX + scrollCord

    def getScore(self):
        return int(self.score)

    def addScore(self, value):
        self.score += value

    def moveCells(self, move):
        self.cell_num += move
        print(self.cell_num)

    def getCell(self):
        return self.cell_num

def message_to_screen(msg, color, x_displace=0, y_displace=0, font_size=0):
    nice_font = pygame.font.Font('freesansbold.ttf', font_size)
    textSurface = nice_font.render(msg, True, color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = (W / 2) + x_displace, (H / 2) + y_displace
    DS.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()


# Trivia question loading parameters and constants for tracking mode
num_questions = 5
easy_questions = loadQuestions('easy', num_questions, 100)
#medium_questions = loadQuestions('medium', num_questions, 200)
#hard_questions = loadQuestions('hard', num_question, 300)
QUESTION = 'question'
ANSWER = 'answer'

# Allowed answer keys for each type of question
MC_answer_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
TF_answer_keys = [pygame.K_1, pygame.K_2]

# triviaEvents catches user key input for answerring questions and returning to the game board
def triviaEvents(current_question, current_mode, active_player):
    global MC_answer_keys
    global TF_answer_keys
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if current_mode == QUESTION and \
                (current_question.getType() == 'MC' and event.key in MC_answer_keys) or \
                    (current_question.getType() == 'TF' and event.key in TF_answer_keys):
                # key_num converts character code into a list index (e.g. K_3 -> 51 -> 3 -> 2)
                key_num = int(event.key) - 48 - 1
                correct_ans_num = current_question.getAnsNum()
                if key_num == correct_ans_num:
                    # If correct input entered, add points, and go to answer state
                    active_player.addScore(current_question.getValue())
                    print('Correct! +' + str(current_question.getValue()) + ' points')
                return 'answered'
            elif current_mode == ANSWER and (event.key == K_RETURN) or (event.key == K_SPACE):
                # If enter key is pressed while answer is displayed, return to the game board
                return 'done'
    return


# triviaMinigame loops until player answers question and hits enter to return to game board
def triviaMinigame(question_list, active_player):
    global num_questions
    print('Beginning trivia game')
    trivia_mode = QUESTION
    current_question = question_list[random.randint(0, num_questions - 1)]
    minigame_over = False
    while not minigame_over:
        DS.blit(wayBack, (0, 0))
        drawQuestion(current_question, trivia_mode, W, (HW, HH), DS)
        pygame.display.update()
        new_event = triviaEvents(current_question, trivia_mode, active_player)
        if new_event == 'answered':
            trivia_mode = ANSWER
        elif new_event == 'done':
            minigame_over = True
            break

# def platformMinigame():
#    import platform
#    print('Beginning platform game')
#    minigame_over = False
#    while not minigame_over:
#        DS.blit(wayBack, (0,0))
#        platform.gameLoop()
#        pygame.display.update()
#        if game_over == True:
#            break

# player objects
num_players = 1
p1 = BoardPiece((0, 0, 0), 1)
p2 = BoardPiece((100, 100, 100), 2)
p3 = BoardPiece((200, 200, 200), 3)
p4 = BoardPiece((255, 255, 255), 4)
all_player_list, player_list = [p1, p2, p3, p4], []

# grabs number of players from mainMenu.py
def setNumPlayers(player_num):
    global num_players
    global all_player_list
    global player_list
    num_players = player_num
    player_list = all_player_list[:num_players]


# very background image
wayBack = pygame.image.load("SeemsCool.jpg").convert()

# dice that blits for 0.5 seconds
dice = pygame.image.load('dice2.png').convert_alpha()

# Game board that is blit continuously 
bkgd = pygame.image.load("board1.png").convert_alpha()
bkgd = pygame.transform.scale(bkgd, (1300, 600))

# Minigame screen that blits only when minigame is triggered
minigame = pygame.image.load("minigame.png")
minigame = pygame.transform.scale(minigame, (800,700))

# x is the position
x = 0 
# number of player switches
n = 0
# we want to stop at a certain number of rounds. 
roundCount = 1

# Variable for tracking game over state
game_over = False

# Lists for storing the cell numbers which contain minigames
trivia_cells = [2, 5, 7, 10, 16, 21, 26, 32, 38, 43, 47, 51]
platform_cells = [1, 3, 6, 11, 15, 19, 25, 27, 29, 34, 39, 41, 49, 50]  # Need to complete list of platform cells

# main function, handles everything between starting from player select menu and game over
# loops until game over state, at which point gameOver() is called
def boardLoop():
    global player_list
    global num_players
    global x
    global n
    global game_over
    global trivia_cells
    global platform_cells

    while not game_over:

        # background blit
        DS.blit(wayBack, (0, 0))
        z = boardEvents()

        current_player_index = n % num_players
        # relative x value
        rel_x = x % bkgd.get_rect().width
        DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 60))
        # blit some information about Active player number to screen
        message_to_screen("Player " + str((n % num_players) + 1) + " rolls ", RED, -290, -300, 24)
        message_to_screen("Press space to roll", RED, -262, -270, 24)
        message_to_screen("Press R to scroll", RED, -275, -240, 24)
        for i in range(num_players):
            message_to_screen("Player " + str(i + 1) + " score: " + str(player_list[i].getScore()),
                              RED, -275, 250 + (i * 25), 24)
        # number of Rounds
        numRounds = n // num_players

        if rel_x < W:
            x = 0
            DS.blit(bkgd, (0, 60))

            # update character locations upon snapping back to start
            for player in player_list:
                player.absX = player.xCord

        for player in player_list:
            player.draw(DS)

        # if spacebar is hit
        if z == True:
            print('Player rolling : ', current_player_index)
            die_number = random.randint(1, 6)
            print("Player" + str(current_player_index + 1) + " rolls " + str(die_number))
            player_list[current_player_index].moveCells(die_number)
            for i in range(die_number):
                player_list[current_player_index].diceRoll(x)

            # Display the dice and rolled number for 0.5 seconds.
            medium_text = pygame.font.Font('mago3.ttf', 50)
            text_surf, text_rect = text_objects(str(die_number), medium_text)
            text_rect.center = (360, 98)
            DS.blit(dice, (250, 0))
            DS.blit(text_surf, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)

            # Check if player lands on a trivia or platform minigame cell
            if player_list[current_player_index].getCell() in trivia_cells:
                DS.blit(minigame, (0,0))
                pygame.display.update()
                pygame.time.delay(1500)
                triviaMinigame(easy_questions, player_list[current_player_index])
                print('Current player score: ', player_list[current_player_index].getScore())

            elif player_list[current_player_index].getCell() in platform_cells:
                DS.blit(minigame, (0, 0))
                pygame.display.update()
                pygame.time.delay(1500)
                NewScore = platform.gameLoop()
                print(NewScore)
                player_list[current_player_index].addScore(NewScore)
                print('Current player score: ', player_list[current_player_index].getScore())

                # Need to set up randomized levels


            n += 1

        # If the user wants to scroll: presses r
        elif z == '-x':
            x -= 44
            for player in player_list:
                player.worldScroll(-44)

        elif z == 'x' and x < 0:
            x += 44
            for player in player_list:
                player.worldScroll(44)

        # draw each player dot


        pygame.display.update()
        CLOCK.tick(FPS)


def gameOver():
    # Some code to execute when one player wins or whatever
    global game_over
