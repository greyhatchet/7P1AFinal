# File: playGame.py
# Description: play the waiting game from this file, be sure to have pygame downloaded, 
#   initial menu should be start menu, which leads to the board/map, and later, an end menu
# Start Game - menus (start game, end game), draw board
# Import - load questions from trivia, platform levels

# Credits - 
# Fonts used from magofonts: mago1, mago3
# Fonts attributed to: magodev
# https://magodev.itch.io/

import pygame

pygame.init()

# global variables
# player_number = 0
intro = True

# size of display screen
display_width = 800 
display_height = 700 

# available colors
black = (0,0,0)
white = (255,255,255)
true_red = (255,0,0)
green = (60,179,113)
blue = (0, 0, 200)
pink = (255,192,203)
lavender = (221,160,221)
red = (205,92,92)

# sets display, caption, and clock
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Waiting Game')
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

    smallText = pygame.font.Font("mago1.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(textSurf, textRect)

def message_display(text):
    largeText = pygame.font.Font('mago3.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    game_display.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)

def start_menu():
    global intro
    #global how_to
    #global playnum_screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # clears display, blits title
    game_display.fill(pink)
    largeText = pygame.font.Font('mago3.ttf', 100)
    mediumText = pygame.font.Font('mago3.ttf', 50)
    TextSurf, TextRect = text_objects("Waiting Game", largeText)
    TextRect.center = ((display_width/2),(display_height/2)-50)
    game_display.blit(TextSurf, TextRect)

    # displays buttons that route to different functions
    button("Enter",250,450,100,50,green,lavender)# insert function here, currently is an empty button
    button("Quit",450,450,100,50,red,lavender,quit)

    pygame.display.update()
    clock.tick(40)

while intro:
    start_menu()