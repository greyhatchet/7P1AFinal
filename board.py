import pygame
import random
pygame.init()

# size of display screen
display_width = 800
display_height = 700

# available colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (60, 179, 113)
blue = (0, 0, 200)
pink = (255, 192, 203)
lavender = (221, 160, 221)
red = (205, 92, 92)
yellow = (255,250,205)
pale_blue = (175,228,238)

# sets display, caption
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Waiting Game')
board = pygame.image.load('board.png').convert()
board = pygame.transform.scale(board, (800, 700))

#players
bear1 = pygame.image.load('bear1.jpg').convert()
bear1 = pygame.transform.scale(bear1, (75, 75))

owl2 = pygame.image.load('owl2.jpg').convert()
owl2 = pygame.transform.scale(owl2, (75, 75))

dear3 = pygame.image.load('dear3.jpg').convert()
dear3 = pygame.transform.scale(dear3, (75, 75))

skunk4 = pygame.image.load('skunk4.jpg').convert()
skunk4 = pygame.transform.scale(skunk4, (75, 75))

#dice
dice = pygame.image.load('dice.png').convert()
dice = pygame.transform.scale(dice, (75, 75))

func = True
num_players = 4
white = (255, 255, 255)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("mago1.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def message_display(text):
    largeText = pygame.font.Font('mago3.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
roll = False
def roll_dice():
    roll = True
    die = random.randint(1, 12)
    return die

def Board():
    global roll
    gameDisplay.blit(board, (0, 0))
    gameDisplay.blit(dice, (600, 615))

    smallmedText = pygame.font.Font('mago3.ttf', 50)
    #x, y , w, h
    button("Roll Dice", 580, 560, 100, 50, green, lavender)
    if roll == False:
        TextSurf, TextRect = text_objects(str(roll_dice()), smallmedText)
        TextRect.center = (750, 615)
        gameDisplay.blit(TextSurf, TextRect)
    else:
        pass

    #gameDisplay.blit()
    if num_players == 1:
        gameDisplay.blit(bear1, (10, 345))
    elif num_players == 2:
        gameDisplay.blit(bear1, (10, 345))
        gameDisplay.blit(owl2, (10, 435))
    elif num_players == 3:
        gameDisplay.blit(bear1, (10, 345))
        gameDisplay.blit(owl2, (10, 435))
        gameDisplay.blit(dear3, (10, 525))
    else:
        gameDisplay.blit(bear1, (10, 345))
        gameDisplay.blit(owl2, (10, 435))
        gameDisplay.blit(dear3, (10, 525))
        gameDisplay.blit(skunk4, (10, 615))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            func = False
            pygame.quit()
            quit()

    pygame.display.update()


def loop():
    global func
    while func:
        Board()
loop()