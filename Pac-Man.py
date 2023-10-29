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
score = -30
scorelen = 350
textPos = 0
moveTimePT = time.time()
moveTimeGT = time.time()
place = True



#Makes the wall positions and sizes
walls = [pygame.Rect(0,50,570,30),pygame.Rect(0,650,570,30),pygame.Rect(0,50,30,210),pygame.Rect(540,50,30,210),pygame.Rect(0,230,120,30),pygame.Rect(450,230,120,30),pygame.Rect(0,290,120,30),pygame.Rect(450,290,120,30),pygame.Rect(450,260,30,30),pygame.Rect(90,260,30,30),pygame.Rect(450,350,120,30),pygame.Rect(0,350,120,30),pygame.Rect(90,350,30,90),pygame.Rect(450,350,30,90),pygame.Rect(0,410,120,30),pygame.Rect(450,410,120,30),pygame.Rect(0,410,30,280),pygame.Rect(540,410,30,280),pygame.Rect(60,110,60,30),pygame.Rect(150,110,90,30),pygame.Rect(270,80,30,60),pygame.Rect(330,110,90,30),pygame.Rect(450,110,60,30),pygame.Rect(60,170,60,30),pygame.Rect(150,170,30,150),pygame.Rect(210,170,150,30),pygame.Rect(450,110,60,30),pygame.Rect(270,170,30,90),pygame.Rect(390,170,30,150),pygame.Rect(450,170,60,30),pygame.Rect(150,230,90,30),pygame.Rect(330,230,90,30),pygame.Rect(210,290,30,90),pygame.Rect(210,290,150,30),pygame.Rect(330,290,30,90),pygame.Rect(150,350,30,90),pygame.Rect(210,350,150,30),pygame.Rect(390,350,30,90),pygame.Rect(210,410,150,30),pygame.Rect(270,410,30,90),pygame.Rect(60,470,60,30),pygame.Rect(90,470,30,90),pygame.Rect(150,470,90,30),pygame.Rect(330,470,90,30),pygame.Rect(450,470,30,90),pygame.Rect(450,470,60,30),pygame.Rect(30,530,30,30),pygame.Rect(150,530,30,90),pygame.Rect(210,530,150,30),pygame.Rect(270,530,30,90),pygame.Rect(390,530,30,90),pygame.Rect(510,530,30,30),pygame.Rect(60,590,180,30),pygame.Rect(330,590,180,30)]
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |End of outer areas / Start at top left this \ will indicate a new line                                                              \                                                                                                                                                                                               \                                                     \                                                                                \                                                                                 \                                                      \                                                                                                                                                               \                                                                                                                                                                 \
#Specifies the out of bounds areas so the pellets don't spawn there
outabounds = [pygame.Rect(0,260,90,30),pygame.Rect(480,260,90,30),pygame.Rect(0,380,90,30),pygame.Rect(480,380,90,30),pygame.Rect(240,320,90,30)]

#Creates the pellets
pellets = []
for y in range(95,640,15):
    for x in range(43,528,15):
        place = True
        for a in range(len(walls)):
            if(walls[a].collidepoint(x,y) == True):
                place = False
            if(walls[a].collidepoint(x+3,y-3) == True):
                place = False
            if(walls[a].collidepoint(x+3,y) == True):
                place = False
            if(walls[a].collidepoint(x,y-3) == True):
                place = False
        for b in range(len(outabounds)):
            if(outabounds[b].collidepoint(x,y) == True):
                place = False
        if(place == True):
            pellets.append(pygame.Rect(x,y,4,4))


#Makes the wall images
def MakeWalls():
    for i in range(len(walls)):
        pygame.draw.rect(screen,(9, 75, 189),walls[i])

#Makes the pellet images
def MakePellets():
    for i in range(len(pellets)):
        pygame.draw.rect(screen,(235, 229, 52),pellets[i])



class Ghost:
    def __init__(self,type):
        self.type = type
        self.rect = pygame.Rect((270,260,30,30))
        self.rotation = "R"
        self.rotationR = "L"
        self.XPD = 0
        self.YPD = 0
        self.notTlist = []
        if(self.type == 1):
            self.color = (13, 194, 214)
        elif(self.type == 2):
            self.color = (214, 144, 13)
        elif(self.type == 3):
            self.color = (214, 13, 13)
        elif(self.type == 4):
            self.color = (219, 26, 187)
        #Track detections
        self.leftD = pygame.Rect((269,260,1,30))
        self.topD = pygame.Rect((270,259,30,1))
        self.rightD = pygame.Rect((300,260,1,30))
        self.bottomD = pygame.Rect((270,290,30,1))
    
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
    
    def MoveDecide(self):
        self.notTlist.clear()
        self.XPD = P.rect.x - self.rect.x
        self.YPD = P.rect.y - self.rect.y
        if(self.topD.collidelist(walls) == -1):
            self.notTlist.append("U")
        if(self.rightD.collidelist(walls) == -1):
            self.notTlist.append("R")
        if(self.bottomD.collidelist(walls) == -1):
            self.notTlist.append("D")
        if(self.leftD.collidelist(walls) == -1):
            self.notTlist.append("L")
        
        if(self.rotation == "R"):
            self.rotationR = "L"
        elif(self.rotation == "L"):
            self.rotationR = "R"
        elif(self.rotation == "U"):
            self.rotationR = "D"
        elif(self.rotation == "D"):
            self.rotationR = "U"
        
        if(self.rotation == "R"):
            if("L" in self.notTlist):
                self.notTlist.remove("L")
        if(self.rotation == "L"):
            if("R" in self.notTlist):
                self.notTlist.remove("R")
        if(self.rotation == "U"):
            if("D" in self.notTlist):
                self.notTlist.remove("D")
        if(self.rotation == "D"):
            if("U" in self.notTlist):
                self.notTlist.remove("U")
        
        print(self.notTlist)




        if(self.type == 4):
            if(len(self.notTlist) == 2):
                if(abs(self.XPD) >= abs(self.YPD)):
                    #change direction to go to player
                    if(self.XPD > 0 and "R" in self.notTlist):
                        self.rotation = "R"
                    elif(self.XPD < 0 and "L" in self.notTlist):
                        self.rotation = "L"
                    elif(self.XPD > 0 and "R" not in self.notTlist):
                        if(self.YPD > 0 and "D" in self.notTlist):
                            self.rotation = "D"
                        else:
                            self.rotation = "U"
                    elif(self.XPD < 0 and "L" not in self.notTlist):
                        if(self.YPD > 0 and "D" in self.notTlist):
                            self.rotation = "D"
                        else:
                            self.rotation = "U"
                elif(abs(self.XPD) <= abs(self.YPD)):
                    #change direction to go to player
                    if(self.YPD > 0 and "D" in self.notTlist):
                        self.rotation = "D"
                    elif(self.YPD < 0 and "U" in self.notTlist):
                        self.rotation = "U"
                    elif(self.YPD > 0 and "D" not in self.notTlist):
                        if(self.XPD > 0 and "R" in self.notTlist):
                            self.rotation = "R"
                        else:
                            self.rotation = "L"
                    elif(self.YPD < 0 and "U" not in self.notTlist):
                        if(self.XPD > 0 and "R" in self.notTlist):
                            self.rotation = "R"
                        else:
                            self.rotation = "L"
            elif(len(self.notTlist) == 3):
                if(abs(self.XPD) >= abs(self.YPD)):
                    if(self.XPD > 0 and "R" in self.notTlist):
                        self.rotation = "R"
                    elif(self.XPD < 0 and "L" in self.notTlist):
                        self.rotation = "L"
                    elif(self.XPD > 0 and "R" not in self.notTlist):
                        if(self.YPD > 0):
                            self.rotation = "D"
                        else:
                            self.rotation = "U"
                    elif(self.XPD < 0 and "L" not in self.notTlist):
                        if(self.YPD > 0):
                            self.rotation = "D"
                        else:
                            self.rotation = "U"
                elif(abs(self.XPD) <= abs(self.YPD)):
                    #change direction to go to player
                    if(self.YPD > 0 and "D" in self.notTlist):
                        self.rotation = "D"
                    elif(self.YPD < 0 and "U" in self.notTlist):
                        self.rotation = "U"
                    elif(self.YPD > 0 and "D" not in self.notTlist):
                        if(self.XPD > 0):
                            self.rotation = "R"
                        else:
                            self.rotation = "L"
                    elif(self.YPD < 0 and "U" not in self.notTlist):
                        if(self.XPD > 0):
                            self.rotation = "R"
                        else:
                            self.rotation = "L"
        

        #This goes after all of the ghost types
        if(len(self.notTlist) == 1):
            self.rotation = self.notTlist[0]
    
    def Move(self,moveTimeG):
        if(time.time() >= moveTimeG + .0035):
            if(self.rotation == "R"):
                self.rect.move_ip(1,0)
                self.leftD.move_ip(1,0)
                self.topD.move_ip(1,0)
                self.rightD.move_ip(1,0)
                self.bottomD.move_ip(1,0)
            if(self.rotation == "U"):
                self.rect.move_ip(0,-1)
                self.leftD.move_ip(0,-1)
                self.topD.move_ip(0,-1)
                self.rightD.move_ip(0,-1)
                self.bottomD.move_ip(0,-1)
            if(self.rotation == "L"):
                self.rect.move_ip(-1,0)
                self.leftD.move_ip(-1,0)
                self.topD.move_ip(-1,0)
                self.rightD.move_ip(-1,0)
                self.bottomD.move_ip(-1,0)
            if(self.rotation == "D"):
                self.rect.move_ip(0,1)
                self.leftD.move_ip(0,1)
                self.topD.move_ip(0,1)
                self.rightD.move_ip(0,1)
                self.bottomD.move_ip(0,1)
            global moveTimeGT
            moveTimeGT = time.time()
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







#Creates player and things the player can do
class Player:
    def __init__(self):
        self.Pcolor = (24, 150, 5)
        self.rotation = "D"
        self.rect = pygame.Rect((270,500,30,30))
        #Track detections
        self.leftD = pygame.Rect((269,500,1,30))
        self.topD = pygame.Rect((270,499,30,1))
        self.rightD = pygame.Rect((300,500,1,30))
        self.bottomD = pygame.Rect((270,530,30,1))
        
    #Creates the player image on screen
    def draw(self):
        #Place holder for if I decide to make a custom image
        pygame.draw.rect(screen,self.Pcolor,self.rect)
    
    #Moves the player and its wall detectors based on the way its facing
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
            global moveTimePT
            moveTimePT = time.time()
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


#Initializes the player and starts the main game loop.
P = Player()
G = Ghost(4)
running = True
while(running):
    #Draws the screen, player, walls, pellets, and score
    screen.fill(Scolor)
    MakeWalls()
    MakePellets()
    P.draw()
    G.draw()
    scoreDisplay = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = scoreDisplay.render(str(score), False, (255, 255, 255))
    scorelen = 0
    for i in range(len(str(score))):
        scorelen += 19
    textPos = 570-scorelen
    screen.blit(text_surface, (textPos,0))


    #Changes player direction if there isn't a wall in the way.
    key = pygame.key.get_pressed()
    if(key[pygame.K_d] and P.rightD.collidelist(walls) == -1):
        P.rotation = "R"
    if(key[pygame.K_a] and P.leftD.collidelist(walls) == -1):
        P.rotation = "L"
    if(key[pygame.K_w] and P.topD.collidelist(walls) == -1):
        P.rotation = "U"
    if(key[pygame.K_s] and P.bottomD.collidelist(walls) == -1):
        P.rotation = "D"
    
    #Moves the player based on this direction, collects the pellets
    P.Move(moveTimePT)
    G.MoveDecide()
    G.Move(moveTimeGT)
    if(P.rect.collidelist(pellets) >=0):
        score += 10
        pellets.pop(P.rect.collidelist(pellets))

    #Quits the program if trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Lets the window and backround programs load before running the code in the loop again.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
