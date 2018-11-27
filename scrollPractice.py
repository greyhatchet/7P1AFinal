import pygame
from pygame.locals import *
import sys
import os
import random

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

p1 = BoardPiece((0,0,0),1)
p2 = BoardPiece((100,100,100),2)
p3 = BoardPiece((200,200,200),3)
p4 = BoardPiece((255,255,255),4)

playerList = [p1,p2,p3,p4]

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
		p1.absX = p1.xCord
		p2.absX = p2.xCord
		p3.absX = p3.xCord
		p4.absX = p4.xCord

	#if spacebar is hit
	if z == True:
		dieNumber = random.randint(1,6)
		print("player"+ str((n % 4) + 1) + " rolls " + str(dieNumber))
		for i in range(dieNumber):
			playerList[(n % 4)].diceRoll(x)
		n+= 1

	elif z == False:
		x -= 44
		p1.worldScroll(-44)
		p2.worldScroll(-44)
		p3.worldScroll(-44)
		p4.worldScroll(-44)
		
	elif z == "y" and x < 0:
		x += 44
		p1.worldScroll(44)
		p2.worldScroll(44)
		p3.worldScroll(44)
		p4.worldScroll(44)
		


	p1.draw(DS)
	p2.draw(DS)
	p3.draw(DS)
	p4.draw(DS)

	pygame.display.update()
	CLOCK.tick(FPS)