import pygame
from pygame.locals import *
import sys
import os
import random

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

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            return True
        elif event.type == KEYDOWN and event.key == K_r:
            return False
        elif event.type == KEYDOWN and event.key == K_a:
            return "y"
    return


class BoardPiece:
    def __init__(self, color, playerNumber):
        self.color = color
        self.piece = playerNumber
        self.xCord = 33
        self.yCord = 277 + (playerNumber - 1) * 20
        self.absX = self.xCord
        self.absY = self.yCord
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
        return self.score

    def addScore(self, value):
        self.score += value


def message_to_screen(msg, color, x_displace=0, y_displace=0, font_size=0):
    nice_font = pygame.font.Font('freesansbold.ttf', font_size)
    textSurface = nice_font.render(msg, True, color)
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = (W / 2) + x_displace, (H / 2) + y_displace
    DS.blit(textSurf, textRect)


def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()


# player objects
num_players = 1
p1 = BoardPiece((0, 0, 0), 1)
p2 = BoardPiece((100, 100, 100), 2)
p3 = BoardPiece((200, 200, 200), 3)
p4 = BoardPiece((255, 255, 255), 4)
all_player_list, player_list = [p1, p2, p3, p4], []

def setNumPlayers(player_num):
    global num_players
    global all_player_list
    global player_list
    num_players = player_num
    player_list = all_player_list[:num_players]


# very background image
wayBack = pygame.image.load("SeemsCool.jpg").convert()

dice = pygame.image.load('dice2.png').convert_alpha()
# dice = pygame.transform.scale(dice, (75, 75))

bkgd = pygame.image.load("board1.png").convert_alpha()
bkgd = pygame.transform.scale(bkgd, (1300, 600))
x = 0
# number of player switches
n = 0

roundCount = 1

# Variable + constants for tracking current game mode and game over state
BOARD = 'board'
TRIVIA = 'trivia'
PLATFORM = 'platform'
current_mode = BOARD
game_over = False

# main function, handles everything between starting from player select menu and game over
# loops until game over state, at which point gameOver() is called
def boardLoop():
    global player_list
    global num_players
    global x
    global n
    global current_mode
    global game_over

    while not game_over:

        if current_mode == BOARD:
            # background blit
            DS.blit(wayBack, (0, 0))
            z = events()

            # relative x value
            rel_x = x % bkgd.get_rect().width
            DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 60))
            message_to_screen("Player " + str((n % num_players) + 1) + " rolls ", RED, -290, -300, 24)
            message_to_screen("Press space to roll", RED, -262, -270, 24)
            message_to_screen("Press R to scroll", RED, -275, -240, 24)
            # number of Rounds
            numRounds = n // num_players

            if rel_x < W:
                x = 0
                DS.blit(bkgd, (0, 60))

                # update character locations upon snapping back to start
                for player in player_list:
                    player.absX = player.xCord

            # if spacebar is hit
            if z == True:
                die_number = random.randint(1, 6)

                print("player" + str((n % num_players) + 1) + " rolls " + str(die_number))
                for i in range(die_number):
                    player_list[(n % num_players)].diceRoll(x)
                n += 1

                medium_text = pygame.font.Font('mago3.ttf', 50)

                text_surf, text_rect = text_objects(str(die_number), medium_text)
                text_rect.center = (360, 98)
                DS.blit(dice, (250, 0))
                DS.blit(text_surf, text_rect)
                pygame.display.update()
                pygame.time.delay(500)

            elif z == False:
                x -= 44
                for player in player_list:
                    player.worldScroll(-44)

            elif z == "y" and x < 0:
                x += 44
                for player in player_list:
                    player.worldScroll(44)

            for player in player_list:
                player.draw(DS)

            pygame.display.update()
            CLOCK.tick(FPS)


def triviaMinigame(current_player):
    global current_mode


def gameOver():
    # Some code to execute when one player wins or whatever
    global game_over
