import pygame

global look_forward
look_forward = True
current_level_no = 0
total_score = 0.0
current_level_score = 0.0
lives_left = 3
enemies_killed = 0
current_enemies_killed = 0
game_over = False

# size of display screen
display_width = 800 
display_height = 700 

# available colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (53, 22, 0)

pygame.init()

# sets display, caption, and clock
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Waiting Game - Platformer")
clock = pygame.time.Clock()

# 
BULLET_IMG = pygame.Surface((15, 9))
BULLET_IMG.fill(pygame.Color('aquamarine2'))

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)

        # Return the image
        return image

class Player(pygame.sprite.Sprite):

    # This class represents the bar at the bottom that the player controls.

    def __init__(self):
        # Constructor function

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        width = 30
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []

        # What direction is the player facing?
        self.direction = "R"

        # Player Health
        self.health = 3

        # List of sprites we can bump against
        self.level = None

        sprite_sheet = SpriteSheet("astronaut.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(20, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(80, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(140, 3, 40, 50)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(200, 3, 40, 50)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(20, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(80, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(140, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(200, 3, 40, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        # Move the player.
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        # Calculate effect of gravity.
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= display_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = display_height - self.rect.height

    def jump(self):
        # Called when user hits the up arrow.

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= display_height:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        # Called when the user hits the left arrow.
        self.change_x = -6
        self.direction = "L"
        look_forward = False

    def go_right(self):
        # Called when the user hits the right arrow.
        self.change_x = 6
        self.direction = "R"
        look_forward = True

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0

    def collide(self, enemy, enemy_list):
        if self.rect.colliderect(enemy.rect):  # Tests if the player is touching an enemy
            self.rect.x -= 50  # Pushes player to left if hit
            self.health = self.health - 1
            # hit_sfx.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(450, 0)
        self.damage = 10

        # List of sprites we can bump against
        self.level = None

    def update(self, dt):

        global current_enemies_killed
        global current_level_score

        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos  # Update the rect pos.
        if self.rect.right <= 0 or self.rect.left <= -20:
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for block in block_hit_list:
            self.kill()
            block.kill()
            current_enemies_killed += 1
            current_level_score += 100


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Create enemies

        super().__init__()

        width = 50
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []

        # What direction is the player facing?
        self.direction = "R"

        # List of sprites we can bump against
        self.level = None

        sprite_sheet = SpriteSheet("alien.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(45, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(90, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(135, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(180, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(225, 0, 45, 60)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(265, 0, 45, 60)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(45, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(90, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(135, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(180, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(225, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(265, 0, 45, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # set movement counter
        self.counter = 0

    # Set the position of the enemy
    def setPosition(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move(self):
        # enemy movement, paces left and right
        # distance sets how far
        # speed sets how fast
        distance = 70
        speed = 2

        if self.counter >= 0 and self.counter <= distance:
            self.direction = "R"
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.direction = "L"
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

        # Move left/right
        # self.rect.x += self.change_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:  # need to include left direction of enemy
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]


class Platform(pygame.sprite.Sprite):
    # Platform the user can jump on

    def __init__(self, width, height):
        """
        Platform constructor. Assumes constructed with user passing in
        an array of 5 numbers like what's defined at the top of this code.
        """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BROWN)
        
        pltfrm = pygame.image.load('plt_tile.png')
        
        self.rect = self.image.get_rect()
        self.image.blit(pltfrm, self.rect)

class Level():

    def __init__(self, player):

        # Constructor.

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        self.world_shift = 0

        # local enemy list to add
        self.enemy_to_spawn = []

        #countdown timer for each level
        self.level_time = 14

    # Update everythign on this level
    def update(self):
        # Update everything in this level.
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, game_display):
        # Draw everything on this level.

        # Draw the background
        game_display.fill(BROWN)
        game_display.blit(self.background, (0,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(game_display)
        self.enemy_list.draw(game_display)
        for enemy in self.enemy_list:
            enemy.move()
            self.player.collide(enemy, self.enemy_list)  # Checks if enemy is touching player

    def shift_world(self, shift_x):

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        # function to kill and respawn all enemies upon death or restart

    def respawnEnemies(self):
        for enemy in self.enemy_list:
            enemy.kill()

        for i in range(0, len(self.enemy_to_spawn), 2):
            newEn = Enemy()
            newEn.setPosition(self.enemy_to_spawn[i], self.enemy_to_spawn[i + 1])
            self.enemy_list.add(newEn)


# Create platforms for the level
class Level_00(Level):
    # Definition for level 0.

    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)

        # Set the background
        self.background = pygame.image.load("background-purple.png").convert()

        self.level_limit = -1400
        self.level_limit_back = 200

        # spawn enemies
        enemy_1 = Enemy()
        enemy_1.setPosition(775, 440)
        self.enemy_to_spawn.append(enemy_1.rect.x)
        self.enemy_to_spawn.append(enemy_1.rect.y)
        self.enemy_list.add(enemy_1)

        # Array with width, height, x, and y of platform
        level = [
        	[1500, 30, 0, -10],  # roof
        	[1500, 30, 1500, -10],  # roof
            [30, 1000, 0, 0],  # left blocking
            [500, 30, 0, 670],  # ground

            [70, 70, 500, 650],  #
            [70, 70, 700, 550],  #
            [70, 70, 750, 550],  #

            [210, 70, 500, 600],  #

            [210, 70, 800, 500],  #
            [70, 70, 1000, 550],  #
            [210, 70, 1000, 600],  #
            [210, 70, 1120, 380],  #
            [210, 30, 1400, 550],
            [210, 30, 1650, 470],
            [210, 30, 1800, 370],

            [2000, 30, 1210, 670],  # #bottom
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def gameLoop():
    # Load required global variables
    global current_level_no
    global lives_left
    global enemies_killed
    global current_enemies_killed
    global total_score
    global current_level_score
    global game_over

    # load and play game music
    # gameMusic attributed to: http://cynicmusic.com http://pixelsphere.org
    # pygame.mixer.music.stop()
    # pygame.mixer.music.load('gameMusic.mp3')
    # pygame.mixer.music.play(-1)
    # playsound = False


    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    # change levels and update this
    level_list.append(Level_00(player))
    # level_list.append(Level_01(player))
    # level_list.append(Level_02(player))
    # level_list.append(Level_03(player))
    # level_list.append(Level_04(player))

    # Set the current level
    current_level = level_list[current_level_no]

    # Start time of the level initialization
    starting_time = pygame.time.get_ticks()

    active_sprite_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    player.level = current_level

    # set player position
    player.rect.x = 340
    position_scroll = 0
    player.rect.y = 500  # display_height - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # clock for shoot
    Sentinel = 0
    look_forward = True
    dt = clock.tick(60) / 1000

    #valuable booleans for restart and end game
    endgame = False
    mScreen = False
    pause_length = 0

    # Preliminarily update save info
    # updateSaveInfo()

    # -------- Main Program Loop -----------
    while not done:
        if not game_over:
            # boolean to restart current level
            restart_level = False

            #current level time
            current_time = (pygame.time.get_ticks()- starting_time)/ 1000
            countdown_time = current_level.level_time - current_time + pause_length


            if mScreen:
                player.jump()
            for event in pygame.event.get():

                # if window closed, quit
                if event.type == pygame.QUIT:
                    done = True

                # interpret event of keys being pressed
                if event.type == pygame.KEYDOWN and mScreen == False:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.go_left()
                        look_forward = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.go_right()
                        look_forward = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.jump()
                    if event.key == pygame.K_SPACE:
                        # shoot_sfx.play()
                        Sentinel = 1
                        if look_forward == True:
                            pos = [player.rect.x + 40,
                                   player.rect.y + 30]
                            bullet = Bullet(pos)
                            bullet.vel = pygame.math.Vector2(450, 0)
                            bullet.level = current_level
                            bullet_list.add(bullet)

                        elif look_forward == False:
                            pos = [player.rect.x,
                                   player.rect.y + 30]
                            bullet = Bullet(pos)
                            bullet.vel = pygame.math.Vector2(-450, 0)
                            bullet.level = current_level
                            bullet_list.add(bullet)

                    if event.key == pygame.K_r:
                        restart_level = True


                # if at end game screen, press q to quit and r to restart level
                elif event.type == pygame.KEYDOWN and mScreen == True:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_r:
                        restart_level = True
                        mScreen = False
                        starting_time = pygame.time.get_ticks()
                        current_time = (pygame.time.get_ticks()- starting_time)/ 1000
                        countdown_time = current_level.level_time - current_time
                        pygame.mixer.music.play(-1)
                        endgame = False

                # interpret event of keys being released
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                        player.stop()
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                        player.stop()

            # Update the player.
            active_sprite_list.update()
            if Sentinel == 1:
                bullet_list.update(dt)

            # Update items in the level
            current_level.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                position_scroll += diff
                current_level.shift_world(-diff)

            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                position_scroll -= diff
                current_level.shift_world(diff)

            # Player Death
            if player.health == 0 or player.rect.y >= 650 or (countdown_time < 0 and endgame == False):
                # death_sfx.play()
                lives_left -= 1
                # updateSaveInfo()
                player.health = 3
                restart_level = True
                if lives_left <= 0:
                	pygame.mixer.music.stop()
                	pygame.mixer.stop()
                	game_over = True
                	# game_over_sfx.play()

            # if r is pressed, return block to initial level position
            if restart_level == True:
                if position_scroll != 0:
                    current_level.shift_world(position_scroll)
                    position_scroll = 0
                    player.rect.x = 120
                    player.rect.y = 500  # display_height - player.rect.height
                    bullet_list = pygame.sprite.Group()
                    current_level.respawnEnemies()
                    starting_time = pygame.time.get_ticks()
                    pause_length = 0

            # If the player gets to the end of the level, go to the next level, if at end of last level, print you win
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                if current_level_no < len(level_list) - 1:
                    player.rect.x = 120
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level
                    position_scroll = 0
                    bullet_list = pygame.sprite.Group()
                    #updateSaveInfo()
                    starting_time = pygame.time.get_ticks()
                    pause_length = 0
                else:
                    mScreen = True
                    #updateSaveInfo()
                    '''
                    # make sure game over sound only plays once
                    if playsound == 0:
                        playsound = 1'''

            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(game_display)
            active_sprite_list.draw(game_display)
            if Sentinel == 1:
                bullet_list.draw(game_display)

            if mScreen:
                # stop looking for ways to kill character
                endgame = True
                '''
                pygame.mixer.music.stop()
                message_to_screen("You win! Yuhhhhh", RED, 0, -50, 25)
                message_to_screen('To quit: press q', GREY, 0, -30, 16)
                message_to_screen('To restart level: press r', GREY, 0, -15, 16)
                if playsound == 1:
                    win_sfx.play()
                    playsound += 1
                player.stop()
            else:
                message_to_screen("Countdown: " + str(countdown_time)[:4], RED, -10, -225,30)
                message_to_screen("Level " + str((current_level_no)), RED, -400, -300, 24)
                message_to_screen("If stuck, press r to restart level", RED, -307, -275, 18)
                message_to_screen("Press P to pause", RED, -368, -250, 18)
                message_to_screen("Lives left: " + str(lives_left), RED, -390, -225, 18)
                message_to_screen("Total score: " + str(int(total_score + current_level_score)), RED, -383, -200, 18)
                message_to_screen("Enemies killed: " + str(enemies_killed + current_enemies_killed), RED, -366, -175,
                                  18)'''
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    pygame.quit()
    quit()

playGame()