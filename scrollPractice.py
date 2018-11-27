import pygame
from pygame.locals import *
import sys
import os
import random

num_players = 0
player_list = []

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

class BoardPiece():
	def __init__ (self, color, playerNumber):
		self.color = color
		self.piece = playerNumber
		self.xCord = 33
		self.yCord = 277 + (playerNumber - 1) * 20;
		self.absX = self.xCord
		self.absY = self.yCord

	def draw(self,background):
		pygame.draw.circle(background, self.color, (self.absX,self.absY),10,0)

	def diceRoll(self,x):
		#check position on board and move piece appropriately
		if self.xCord < 33 + (7 *44) or (self.xCord > 33 + (7*44) and self.xCord < 33 + (14*44) + 57):
			self.absX += 44
			self.xCord += 44
		elif self.xCord == 33 + (7*44):
			self.absX += 57
			self.xCord += 57
			self.absY -= 115
		elif self.xCord == 33 + (14*44) + 57:
			self.absX += 57
			self.xCord += 57
			self.absY += 115
		elif self.xCord > 33 + (14*44) + 57 and self.xCord < 33 + (26*44) + 57:
			self.absX += 44
			self.xCord += 44
		else:
			self.xCord = 33
			self.absX = self.xCord + x
		

	def worldScroll(self,scrollCord):
		self.absX = self.absX + scrollCord


def setNumPlayers(player_num):
	global num_players
	num_players = player_num


def showBoard():

	global num_players
	global player_list

	# define display surface
	W, H = 800, 700
	HW, HH = W / 2, H / 2
	AREA = W * H

	os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

	# setup pygame
	pygame.init()
	CLOCK = pygame.time.Clock()
	DS = pygame.display.set_mode((W, H))
	pygame.display.set_caption("Game Board")
	FPS = 120

	#player objects

	for i in range(num_players):
		new_player = BoardPiece((i * 80, i * 80, i * 80), i+1)
		player_list.append(new_player)

	#very background image
	wayBack = pygame.image.load("SeemsCool.jpg").convert()


	bkgd = pygame.image.load("board.png").convert_alpha()
	bkgd = pygame.transform.scale(bkgd,(1300,600))
	x = 0

	#number of player switches
	n = 0

	roundCount = 1
	# main loop
	while True:

		#background blit
		DS.blit(wayBack,(0,0))
		z = events()

		# relative x value
		rel_x = x % bkgd.get_rect().width
		DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 60))

		#number of Rounds
		numRounds = n // 4

		if rel_x < W:
			x = 0
			DS.blit(bkgd, (0, 60))

			#update character locations upon snapping back to start
			for player in player_list:
				player.absx = player.xCord

		#if spacebar is hit
		if z == True:
			dieNumber = random.randint(1,6)
			print("player"+ str((n % num_players) + 1) + " rolls " + str(dieNumber))
			for i in range(dieNumber):
				player_list[(n % num_players)].diceRoll(x)
			n += 1

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