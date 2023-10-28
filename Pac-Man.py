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
screen = pygame.display.set_mode((570,680))
score = 0
scorelen = 350
textPos = 0
moveTime = time.time()


#Makes the wall positions and sizes
walls = [pygame.Rect(0,50,570,30),pygame.Rect(0,650,570,30),pygame.Rect(0,50,30,210),pygame.Rect(540,50,30,210),pygame.Rect(0,230,120,30),pygame.Rect(450,230,120,30),pygame.Rect(0,290,120,30),pygame.Rect(450,290,120,30),pygame.Rect(450,260,30,30),pygame.Rect(90,260,30,30),pygame.Rect(450,350,120,30),pygame.Rect(0,350,120,30),pygame.Rect(90,350,30,90),pygame.Rect(450,350,30,90),pygame.Rect(0,410,120,30),pygame.Rect(450,410,120,30),pygame.Rect(0,410,30,280),pygame.Rect(540,410,30,280),pygame.Rect(60,110,60,30),pygame.Rect(150,110,90,30),pygame.Rect(270,80,30,60),pygame.Rect(330,110,90,30),pygame.Rect(450,110,60,30),pygame.Rect(60,170,60,30),pygame.Rect(150,170,30,150),pygame.Rect(210,170,150,30),pygame.Rect(450,110,60,30),pygame.Rect(270,170,30,90),pygame.Rect(390,170,30,150),pygame.Rect(450,170,60,30),pygame.Rect(150,230,90,30),pygame.Rect(330,230,90,30),pygame.Rect(210,290,30,90),pygame.Rect(210,290,150,30),pygame.Rect(330,290,30,90),pygame.Rect(150,350,30,90),pygame.Rect(210,350,150,30),pygame.Rect(390,350,30,90),pygame.Rect(210,410,150,30),pygame.Rect(270,410,30,90),pygame.Rect(60,470,60,30),pygame.Rect(90,470,30,90),pygame.Rect(150,470,90,30),pygame.Rect(330,470,90,30),pygame.Rect(450,470,30,90),pygame.Rect(450,470,60,30),pygame.Rect(30,530,30,30),pygame.Rect(150,530,30,90),pygame.Rect(210,530,150,30),pygame.Rect(270,530,30,90),pygame.Rect(390,530,30,90),pygame.Rect(510,530,30,30),pygame.Rect(60,590,180,30),pygame.Rect(330,590,180,30)]
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |End of outer areas / Start at top left this \ will indicate a new line                                                              \                                                                                                                                                                                               \                                                     \                                                                                \                                                                                 \                                                      \                                                                                                                                                               \                                                                                                                                                                 \

#Makes the wall images
def MakeWalls():
    for i in range(len(walls)):
        pygame.draw.rect(screen,(9, 75, 189),walls[i])




#Creates player and things the player can do
class Player:
    def __init__(self):
        self.Pos = [270,500]
        self.Pcolor = (24, 150, 5)
        self.rotation = "R"
        self.rect = pygame.Rect((270,500,30,30))
        #Track detections
        self.leftD = pygame.Rect((269,500,1,30))
        self.topD = pygame.Rect((270,499,30,1))
        self.rightD = pygame.Rect((300,500,1,30))
        self.bottomD = pygame.Rect((270,530,30,1))
        
    
    def draw(self):
        pygame.draw.rect(screen,self.Pcolor,self.rect)
    
    def Move(self,moveTimeP):
        if(time.time() >= moveTimeP + .0035):
            if(self.rotation == "R" and self.rightD.collidelist(walls) == -1):
                self.rect.move_ip(1,0)
                self.leftD.move_ip(1,0)
                self.topD.move_ip(1,0)
                self.rightD.move_ip(1,0)
                self.bottomD.move_ip(1,0)
            if(self.rotation == "U" and self.topD.collidelist(walls) == -1):
                self.rect.move_ip(0,-1)
                self.leftD.move_ip(0,-1)
                self.topD.move_ip(0,-1)
                self.rightD.move_ip(0,-1)
                self.bottomD.move_ip(0,-1)
            if(self.rotation == "L" and self.leftD.collidelist(walls) == -1):
                self.rect.move_ip(-1,0)
                self.leftD.move_ip(-1,0)
                self.topD.move_ip(-1,0)
                self.rightD.move_ip(-1,0)
                self.bottomD.move_ip(-1,0)
            if(self.rotation == "D" and self.bottomD.collidelist(walls) == -1):
                self.rect.move_ip(0,1)
                self.leftD.move_ip(0,1)
                self.topD.move_ip(0,1)
                self.rightD.move_ip(0,1)
                self.bottomD.move_ip(0,1)
            global moveTime
            moveTime = time.time()
        if(self.rect.x >= 570):
            self.rect.move_ip(-599,0)
            self.leftD.move_ip(-599,0)
            self.topD.move_ip(-599,0)
            self.rightD.move_ip(-599,0)
            self.bottomD.move_ip(-599,0)
        elif(self.rect.x <= -30):
            self.rect.move_ip(599,0)
            self.leftD.move_ip(599,0)
            self.topD.move_ip(599,0)
            self.rightD.move_ip(599,0)
            self.bottomD.move_ip(599,0)



P = Player()
running = True
while(running):
    #Draws the screen, player, and score
    screen.fill(Scolor)
    MakeWalls()
    P.draw()
    scoreDisplay = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = scoreDisplay.render(str(score), False, (255, 255, 255))
    scorelen = 0
    for i in range(len(str(score))):
        scorelen += 19
    textPos = 570-scorelen
    screen.blit(text_surface, (textPos,0))


    key = pygame.key.get_pressed()

    if(key[pygame.K_d] and P.rightD.collidelist(walls) == -1):
        P.rotation = "R"
    if(key[pygame.K_a] and P.leftD.collidelist(walls) == -1):
        P.rotation = "L"
    if(key[pygame.K_w] and P.topD.collidelist(walls) == -1):
        P.rotation = "U"
    if(key[pygame.K_s] and P.bottomD.collidelist(walls) == -1):
        P.rotation = "D"
    
    P.Move(moveTime)

    #Quits the program if trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Lets the window and backround programs load before running the code in the loop again.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
