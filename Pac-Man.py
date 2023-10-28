"""
Lincoln Lyon
10/26/23
CSSE, Tri 1, Per 1, 2023
Guillaume

Description: 
"""
import pygame
import time
import random

#Initiations
pygame.init()
Scolor = (3, 3, 3)
screen = pygame.display.set_mode((570,690))
Pcolor = (24, 150, 5)
score = 0
scorelen = 350
textPos = 0


#Makes the wall positions and sizes
walls = [pygame.Rect(0,50,570,30),pygame.Rect(0,660,570,30),pygame.Rect(0,50,30,210),pygame.Rect(540,50,30,210),pygame.Rect(0,240,120,30),pygame.Rect(450,240,120,30),pygame.Rect(0,300,120,30),pygame.Rect(450,300,120,30),pygame.Rect(450,270,30,30),pygame.Rect(90,270,30,30),pygame.Rect(450,360,120,30),pygame.Rect(0,360,120,30),pygame.Rect(90,360,30,90),pygame.Rect(450,360,30,90),pygame.Rect(0,420,120,30),pygame.Rect(450,420,120,30),pygame.Rect(0,420,30,690),pygame.Rect(540,420,30,690),pygame.Rect(60,110,60,30),pygame.Rect(150,110,90,30),pygame.Rect(270,80,30,60),pygame.Rect(330,110,90,30),pygame.Rect(450,110,60,30),pygame.Rect(60,170,60,30),pygame.Rect(150,170,30,150),pygame.Rect(210,170,150,30),pygame.Rect(450,110,60,30),pygame.Rect(270,170,30,90),pygame.Rect(390,170,30,150),pygame.Rect(450,170,60,30),pygame.Rect(150,230,90,30),pygame.Rect(330,230,90,30)]
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |End of outer areas / Start at top left this \ will indicate a new line                                                              \                                                                                                                                                                                               \

#Makes the wall images
def MakeWalls():
    for i in range(len(walls)):
        pygame.draw.rect(screen,(9, 75, 189),walls[i])




#Creates player and things the player can do
class Player:
    def __init__(self):
        self.Pos = [400,300]
        self.rotation = "R"
        self.rect = pygame.Rect((90,80,30,30))
        #Track detections
        self.leftD = pygame.Rect((399,315,1,1))
        self.topD = pygame.Rect((415,299,1,1))
        self.rightD = pygame.Rect((431,315,1,1))
        self.bottomD = pygame.Rect((415,331,1,1))
        
    
    def draw(self):
        pygame.draw.rect(screen,Pcolor,self.rect)
    
    def Move(self):
        if(self.rotation == "R" and self.rightD.colliderect() == True):
            xMove = 1
            yMove = 0
        elif(self.rotation == "U" and self.topD.colliderect() == True):
            xMove = 0
            yMove = -1
        elif(self.rotation == "L" and self.leftD.colliderect() == True):
            xMove = -1
            yMove = 0
        elif(self.rotation == "D" and self.bottomD.colliderect() == True):
            xMove = 0
            yMove = 1
        self.rect.move_ip(xMove,yMove)
        self.leftD.move_ip(xMove,yMove)
        self.topD.move_ip(xMove,yMove)
        self.rightD.move_ip(xMove,yMove)
        self.bottomD.move_ip(xMove,yMove)


screen.fill(Scolor)
P = Player()
P.draw()
time.sleep(1)

running = True
while(running):
    #Draws the screen, player, and score
    screen.fill(Scolor)
    P.draw()
    MakeWalls()
    scoreDisplay = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = scoreDisplay.render(str(score), False, (255, 255, 255))
    scorelen = 0
    for i in range(len(str(score))):
        scorelen += 19
    textPos = 570-scorelen
    screen.blit(text_surface, (textPos,0))


    """
    Give the player 4 small hitboxes on each side of player.
    Make bigger hit boxes that represent the areas the player can't go that only leave gaps that are exactly as big as the player hitbox.

    Detect when the player tries to change direction:
        Is there a wall in that direction:
            If so don't change anything
        else:
            change direction
    
    In movement updater:
        If wall in direction trying to move:
            don't do anything
        else:
            depending on rotation move forward
    """


    #Quits the program if trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Lets the window and backround programs load before running the code in the loop again.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
