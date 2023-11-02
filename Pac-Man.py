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
lives = 3
ghostSpeed = .004
moveTimePT = time.time()
moveTimeG1T = time.time()
moveTimeG2T = time.time()
moveTimeG3T = time.time()
moveTimeG4T = time.time()
place = True
canMove = True


#Makes the wall positions and sizes
walls = [pygame.Rect(0,50,570,30),pygame.Rect(0,650,570,30),pygame.Rect(0,50,30,210),pygame.Rect(540,50,30,210),pygame.Rect(0,230,120,30),pygame.Rect(450,230,120,30),pygame.Rect(0,290,120,30),pygame.Rect(450,290,120,30),pygame.Rect(450,260,30,30),pygame.Rect(90,260,30,30),pygame.Rect(450,350,120,30),pygame.Rect(0,350,120,30),pygame.Rect(90,350,30,90),pygame.Rect(450,350,30,90),pygame.Rect(0,410,120,30),pygame.Rect(450,410,120,30),pygame.Rect(0,410,30,280),pygame.Rect(540,410,30,280),pygame.Rect(60,110,60,30),pygame.Rect(150,110,90,30),pygame.Rect(270,80,30,60),pygame.Rect(330,110,90,30),pygame.Rect(450,110,60,30),pygame.Rect(60,170,60,30),pygame.Rect(150,170,30,150),pygame.Rect(210,170,150,30),pygame.Rect(450,110,60,30),pygame.Rect(270,170,30,90),pygame.Rect(390,170,30,150),pygame.Rect(450,170,60,30),pygame.Rect(150,230,90,30),pygame.Rect(330,230,90,30),pygame.Rect(210,290,30,90),pygame.Rect(210,290,150,30),pygame.Rect(330,290,30,90),pygame.Rect(150,350,30,90),pygame.Rect(210,350,150,30),pygame.Rect(390,350,30,90),pygame.Rect(210,410,150,30),pygame.Rect(270,410,30,90),pygame.Rect(60,470,60,30),pygame.Rect(90,470,30,90),pygame.Rect(150,470,90,30),pygame.Rect(330,470,90,30),pygame.Rect(450,470,30,90),pygame.Rect(450,470,60,30),pygame.Rect(30,530,30,30),pygame.Rect(150,530,30,90),pygame.Rect(210,530,150,30),pygame.Rect(270,530,30,90),pygame.Rect(390,530,30,90),pygame.Rect(510,530,30,30),pygame.Rect(60,590,180,30),pygame.Rect(330,590,180,30)]
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |End of outer areas / Start at top left this \ will indicate a new line                                                              \                                                                                                                                                                                               \                                                     \                                                                                \                                                                                 \                                                      \                                                                                                                                                               \                                                                                                                                                                 \
#Specifies the out of bounds areas so the pellets don't spawn there and so the ghosts don't leave spawn
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

PowerPellets = [pygame.Rect(40,212,10,10),pygame.Rect(520,212,10,10),pygame.Rect(40,512,10,10),pygame.Rect(520,512,10,10)]

livesDis = [pygame.Rect(10,10,30,30),pygame.Rect(50,10,30,30),pygame.Rect(90,10,30,30)]

#Makes the wall images
def MakeWalls():
    for i in range(len(walls)):
        pygame.draw.rect(screen,(9, 75, 189),walls[i])

#Makes the pellet images
def MakePellets():
    for i in range(len(pellets)):
        pygame.draw.rect(screen,(235, 229, 52),pellets[i])
    for i in range(len(PowerPellets)):
        pygame.draw.rect(screen,(77, 255, 28),PowerPellets[i])

def MakeLives():
    for i in range(len(livesDis)):
        pygame.draw.rect(screen,(24, 150, 5),livesDis[i])

class Ghost:
    def __init__(self,type):
        self.type = type
        self.rect = pygame.Rect((270,320,30,30))
        self.rotation = "R"
        self.rotationR = "L"
        self.XPD = 0
        self.YPD = 0
        self.relTimer = 0
        self.notTlist = []
        self.powerActive = False
        if(self.type == 1):
            self.color = (13, 194, 214)
        elif(self.type == 2):
            self.color = (214, 144, 13)
        elif(self.type == 3):
            self.color = (214, 13, 13)
        elif(self.type == 4):
            self.color = (219, 26, 187)
        #Track detections
        self.leftD = pygame.Rect((269,320,1,30))
        self.topD = pygame.Rect((270,319,30,1))
        self.rightD = pygame.Rect((300,320,1,30))
        self.bottomD = pygame.Rect((270,350,30,1))
    
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
    
    def MoveDecide(self):
        self.notTlist.clear()
        if(self.powerActive == False):
            self.XPD = P.rect.x - self.rect.x
            self.YPD = P.rect.y - self.rect.y
        elif(self.powerActive == True):
            self.XPD = 270 - self.rect.x
            self.YPD = 260 - self.rect.y
        if(self.topD.collidelist(walls) == -1):
            self.notTlist.append("U")
        if(self.rightD.collidelist(walls) == -1):
            self.notTlist.append("R")
        if(self.bottomD.collidelist(walls) == -1):
            self.notTlist.append("D")
        if(self.leftD.collidelist(walls) == -1):
            self.notTlist.append("L")
        
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

        if(self.powerActive == True and self.rect.x == 270 and self.rect.y == 260):
            self.rect.move_ip(0,60)
            self.leftD.move_ip(0,60)
            self.rightD.move_ip(0,60)
            self.topD.move_ip(0,60)
            self.bottomD.move_ip(0,60)
            self.powerActive = False

        if(self.powerActive == True):
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
        elif(self.type == 4):
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
        elif(self.type == 1):
            if(len(self.notTlist) >= 1):
                self.rotation = random.choice(self.notTlist)
        elif(self.type == 2):
            decision = random.randrange(1,101)
            if(decision >= 33):
                if(len(self.notTlist) >= 1):
                    self.rotation = random.choice(self.notTlist)
            else:
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
        elif(self.type == 3):
            decision = random.randrange(1,101)
            if(decision >= 66):
                if(len(self.notTlist) >= 1):
                    self.rotation = random.choice(self.notTlist)
            else:
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
        if(time.time() >= moveTimeG + ghostSpeed):
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
            global moveTimeG1T
            global moveTimeG2T
            global moveTimeG3T
            global moveTimeG4T
            if(self.type == 1):
                moveTimeG1T = time.time()
            elif(self.type == 2):
                moveTimeG2T = time.time()
            elif(self.type == 3):
                moveTimeG3T = time.time()
            elif(self.type == 4):
                moveTimeG4T = time.time()
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
    

    def GhostrelT(self):
        if(self.rect.collidelist(outabounds) >= 0):
            if(self.relTimer == 0):
                self.relTimer = time.time()
            if(self.type == 1 and time.time() >= self.relTimer + 2):
                self.rect.move_ip(0,-60)
                self.leftD.move_ip(0,-60)
                self.topD.move_ip(0,-60)
                self.rightD.move_ip(0,-60)
                self.bottomD.move_ip(0,-60)
                self.relTimer = 0
            if(self.type == 2 and time.time() >= self.relTimer + 4):
                self.rect.move_ip(0,-60)
                self.leftD.move_ip(0,-60)
                self.topD.move_ip(0,-60)
                self.rightD.move_ip(0,-60)
                self.bottomD.move_ip(0,-60)
                self.relTimer = 0
            if(self.type == 3 and time.time() >= self.relTimer + 6):
                self.rect.move_ip(0,-60)
                self.leftD.move_ip(0,-60)
                self.topD.move_ip(0,-60)
                self.rightD.move_ip(0,-60)
                self.bottomD.move_ip(0,-60)
                self.relTimer = 0
            if(self.type == 4 and time.time() >= self.relTimer + 8):
                self.rect.move_ip(0,-60)
                self.leftD.move_ip(0,-60)
                self.topD.move_ip(0,-60)
                self.rightD.move_ip(0,-60)
                self.bottomD.move_ip(0,-60)
                self.relTimer = 0



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


def Reset(lifeD):
    global canMove
    canMove = False
    global lives
    lives -= lifeD
    if(lives == 2):
        livesDis.pop(2)
    if(lives == 1):
        livesDis.pop(1)
    if(lives == 0):
        livesDis.pop(0)
    P.rotation = "D"
    P.rect.x = 270
    P.rect.y = 500
    P.leftD.x = 269
    P.leftD.y = 500
    P.rightD.x = 300
    P.rightD.y = 500
    P.topD.x = 270
    P.topD.y = 499
    P.bottomD.x = 270
    P.bottomD.y = 530
    G1.rect.x = 270
    G1.rect.y = 320
    G1.leftD.x = 269
    G1.leftD.y = 320
    G1.rightD.x = 300
    G1.rightD.y = 320
    G1.topD.x = 270
    G1.topD.y = 319
    G1.bottomD.x = 270
    G1.bottomD.y = 350
    G2.rect.x = 270
    G2.rect.y = 320
    G2.leftD.x = 269
    G2.leftD.y = 320
    G2.rightD.x = 300
    G2.rightD.y = 320
    G2.topD.x = 270
    G2.topD.y = 319
    G2.bottomD.x = 270
    G2.bottomD.y = 350
    G3.rect.x = 270
    G3.rect.y = 320
    G3.leftD.x = 269
    G3.leftD.y = 320
    G3.rightD.x = 300
    G3.rightD.y = 320
    G3.topD.x = 270
    G3.topD.y = 319
    G3.bottomD.x = 270
    G3.bottomD.y = 350
    G4.rect.x = 270
    G4.rect.y = 320
    G4.leftD.x = 269
    G4.leftD.y = 320
    G4.rightD.x = 300
    G4.rightD.y = 320
    G4.topD.x = 270
    G4.topD.y = 319
    G4.bottomD.x = 270
    G4.bottomD.y = 350
    G1.relTimer = 0
    G2.relTimer = 0
    G3.relTimer = 0
    G4.relTimer = 0
    startTime = time.time()
    startDisplay = pygame.font.SysFont('Comic Sans MS', 30)
    while(time.time() <= startTime + 1):
        MakeWalls()
        Start_surface = startDisplay.render("3", False, (255, 255, 255))
        screen.blit(Start_surface, (274,342))
        pygame.display.update()
    while(time.time() <= startTime + 2 and time.time() > startTime + 1):
        MakeWalls()
        Start_surface = startDisplay.render("2", False, (255, 255, 255))
        screen.blit(Start_surface, (274,342))
        pygame.display.update()
    G1.relTimer = 0
    G2.relTimer = 0
    G3.relTimer = 0
    G4.relTimer = 0
    while(time.time() <= startTime + 3 and time.time() > startTime + 2):
        MakeWalls()
        Start_surface = startDisplay.render("1", False, (255, 255, 255))
        screen.blit(Start_surface, (274,342))
        pygame.display.update()
    G1.relTimer = 0
    G2.relTimer = 0
    G3.relTimer = 0
    G4.relTimer = 0
    canMove = True


def End(scoreE):
    EscoreDisplay = pygame.font.SysFont("Comic Sans MS", 30)
    END = True
    while END:
        screen.fill(Scolor)
        EscoreSurface = EscoreDisplay.render(str(scoreE), False, (255,255,255))
        screen.blit(EscoreSurface, (10,200))

        #Quits the program if trying to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END = False
                running = False

        pygame.display.flip()
        pygame.display.update()






#Initializes the player and starts the main game loop.
P = Player()
G4 = Ghost(4)
G3 = Ghost(3)
G2 = Ghost(2)
G1 = Ghost(1)
screen.fill(Scolor)
MakeWalls()
MakePellets()
P.draw()
G4.draw()
G3.draw()
G2.draw()
G1.draw()
scoreDisplay = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = scoreDisplay.render(str(score), False, (255, 255, 255))
scorelen = 0
for i in range(len(str(score))):
    scorelen += 19
textPos = 570-scorelen
screen.blit(text_surface, (textPos,0))
pygame.display.flip()
pygame.display.update()


running = True
while(running):
    #Draws the screen, player, walls, pellets, and score
    screen.fill(Scolor)
    MakeWalls()
    MakePellets()
    MakeLives()
    P.draw()
    G4.draw()
    G3.draw()
    G2.draw()
    G1.draw()
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
    if(key[pygame.K_e]):
        Reset(1)
    
    #Moves the player based on this direction, collects the pellets
    if(canMove):
        P.Move(moveTimePT)
        if(G4.rect.collidelist(outabounds) == -1):
            G4.MoveDecide()
            G4.Move(moveTimeG4T)
        if(G3.rect.collidelist(outabounds) == -1):
            G3.MoveDecide()
            G3.Move(moveTimeG3T)
        if(G2.rect.collidelist(outabounds) == -1):
            G2.MoveDecide()
            G2.Move(moveTimeG2T)
        if(G1.rect.collidelist(outabounds) == -1):
            G1.MoveDecide()
            G1.Move(moveTimeG1T)
        G4.GhostrelT()
        G3.GhostrelT()
        G2.GhostrelT()
        G1.GhostrelT()
    if(P.rect.collidelist(pellets) >=0):
        score += 10
        pellets.pop(P.rect.collidelist(pellets))
    if(P.rect.collidelist(PowerPellets) >= 0):
        score += 100
        PowerPellets.pop(P.rect.collidelist(PowerPellets))
        G4.powerActive = True
        G3.powerActive = True
        G2.powerActive = True
        G1.powerActive = True
    
    if(P.rect.colliderect(G1.rect) or P.rect.colliderect(G2.rect) or P.rect.colliderect(G3.rect) or P.rect.colliderect(G4.rect)):
        Reset(1)
    
    if(len(pellets) == 0):
        Reset(0)
        score -= 30
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
        PowerPellets = [pygame.Rect(40,212,10,10),pygame.Rect(520,212,10,10),pygame.Rect(40,512,10,10),pygame.Rect(520,512,10,10)]
        ghostSpeed -= .0002
    
    if(lives == 0):
        End(score)

    #Quits the program if trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Lets the window and backround programs load before running the code in the loop again.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()
