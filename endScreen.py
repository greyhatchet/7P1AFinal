import pygame

done = True
pygame.init()
# size of display screen
display_width = 800
display_height = 700

# colors
black = (0,0,0)
lavender = (221,160,221)
red = (205,92,92)
pale_blue = (175,228,238)


# Make the screen
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

# The text will be black
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# button with Text, x coordinate, y coordinate, width, height, initial color, accent color, and action (function)
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

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


def endMenu():
    #global player_scores
    global done
    done = True
    #print("Now in endscreen")

    #print(player_scores)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    f = open("scores.txt", "r")
    for i in f:
        #print("hi")
        x = i[1:-1]
        the_scores = x.split(", ")
    the_scores = [int(x) for x in the_scores]


    # clears display, blits title
    gameDisplay.fill(pale_blue)
    largeText = pygame.font.Font('mago3.ttf', 100)
    mediumText = pygame.font.Font('mago3.ttf', 50)
    TextSurf, TextRect = text_objects("Player " + str(the_scores.index(max(the_scores)) + 1) + " wins!", largeText)
    TextRect.center = ((display_width/2), (150))
    gameDisplay.blit(TextSurf, TextRect)


    # Iterate through each player and
    for i in range(len(the_scores)):
        textSurf, textRect = text_objects("Player " + str(i+1) + " " + "score: " + str(the_scores[i]), mediumText)
        textRect.center = ((display_width / 2), (250 + (i*50)))
        gameDisplay.blit(textSurf, textRect)

    # displays buttons that route to different functions
    button("Quit", 350, 550, 100, 50, red, lavender, quit)

    pygame.display.update()


