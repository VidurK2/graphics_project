import pygame as pg
import random
import numpy as np
import math
from pygame.locals import *

# class Ball:
#     def __init__(self, x, y, radius, color):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.color = color
#         self.vx = random.uniform(-1, 1)  # Random initial velocity
#         self.vy = random.uniform(-1, 1)

#     def update(self, tiles):
#         # Predict new ball position
#         new_x = self.x + self.vx
#         new_y = self.y + self.vy

#         # Handle collisions with tiles
#         ball_rect = pg.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)
#         for i in range(len(tiles)):
#             for j in range(len(tiles[i])):
#                 if tiles[i][j] == 1:  # If the tile is solid
#                     tile_rect = pg.Rect(j * 16, i * 16, 16, 16)
#                     if ball_rect.colliderect(tile_rect):
#                         # If the ball collides with the tile, reverse its direction
#                         self.vx *= -1
#                         self.vy *= -1
#                         return

#         # Update ball position
#         self.x = new_x
#         self.y = new_y

#         # Handle collisions with walls
#         if self.x - self.radius <= 0 or self.x + self.radius >= map_width:
#             self.vx *= -1
#         if self.y - self.radius <= 0 or self.y + self.radius >= map_height:
#             self.vy *= -1

#     def render(self, surface):
#         # Render the ball on the surface
#         pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# INITIALISATION
#======================================================================================================================
pg.init()
display_width = 800
display_height = 600
game_display = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Gravity Simulation')

map_width = 1200
map_height = 720

screen = pg.display.set_mode((map_width, map_height), pg.DOUBLEBUF)
display = pg.Surface((400, 240))
time = pg.time.Clock()
frames_per_second = 100

map_image = pg.transform.scale(pg.image.load("/Users/vidur/Desktop/Graphics/pygame_Lighting_Engine/Dungeon_Example_Project/mapMansion.png"), (160, 160))
map_image.convert_alpha()


# FUNCTIONS
#======================================================================================================================

def mapWall(a, b):
    surf = map_image.copy()
    surf.set_clip(pg.Rect(a*16, b*16, 16, 16))
    img = surf.subsurface(surf.get_clip())
    return img.copy()

wallTex = []

for i in range(10):
    for j in range(10):
        wallTex.append(mapWall(j, i))


def torchGlob(size, lightIntensity):
    noLight = pg.Surface(size).convert_alpha()
    
    noLight.fill((255,255,255,lightIntensity))

    return noLight


# CLASSES
#======================================================================================================================

class map:
    def __init__(self):
        self.walls = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                      [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
                      [1,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,1,1,0,0,0,0,0,1],
                      [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                      [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
                      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                      [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

        self.wallShadow = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                             [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
                             [1,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,1,1,0,0,0,0,0,1],
                             [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                             [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
                             [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                             [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
        self.texMap = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                            [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
                            [1,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0,1,1,0,0,0,0,0,1],
                            [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                            [1,0,0,0,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
                            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                            [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

        self.makeWall()
    

    def drawMap(self, canvas):
        wallLen = len(self.walls)
        for i in range(wallLen):
            for j in range(len(self.walls[i])):
                wallPos = [j*16, i*16]
                if self.walls[i][j]:
                    pg.draw.rect(canvas, (150,150,150), (wallPos[0], wallPos[1], 16, 16))
                else:
                    canvas.blit(wallTex[self.texMap[i][j]], wallPos)


    def makeWall(self):
        wallLen = len(self.walls)
        for i in range(wallLen):
            for j in range(len(self.walls[0])):
                self.texMap[i][j] = self.wallRender(i, j)
                if self.walls[i][j]:
                    if i == 14:
                        self.wallShadow[i][j] = 1
                    else:
                        if not self.walls[i+1][j]:
                            self.wallShadow[i][j] = 0
                        else:
                            self.wallShadow[i][j] = 1
                else:
                    self.wallShadow[i][j] = 0
    
    def wallRender(self, i, j):
        wallSt = []

        if i == 0:
            if j == 0:
                wallSt = [1,1,1,1,self.walls[i][j],self.walls[i][j+1],1,self.walls[i+1][j],self.walls[i+1][j+1]]
            elif j == 24:
                wallSt = [1,1,1,self.walls[i][j-1],self.walls[i][j],1,self.walls[i-1][j-1],self.walls[i-1][j],1]
            else:
                wallSt = [1,1,1,self.walls[i][j-1],self.walls[i][j],self.walls[i][j+1],self.walls[i+1][j-1],self.walls[i+1][j],self.walls[i+1][j+1]]
        
        elif i == 14:
            if j == 0:
                wallSt = [1,self.walls[i-1][j],self.walls[i-1][j+1],1,self.walls[i][j],self.walls[i][j+1],1,1,1]
            elif j == 24:
                wallSt = [self.walls[i-1][j-1],self.walls[i-1][j],1,self.walls[i][j-1],self.walls[i][j],1,1,1,1]
            else:
                wallSt = [self.walls[i-1][j-1],self.walls[i-1][j],self.walls[i-1][j+1],self.walls[i][j-1],self.walls[i][j],self.walls[i][j+1],1,1,1]
        
        else:
            if j == 0:
                wallSt = [1,self.walls[i-1][j],self.walls[i-1][j+1],1,self.walls[i][j],self.walls[i][j+1],1,self.walls[i+1][j],self.walls[i+1][j+1]]
            elif j == 24:
                wallSt = [self.walls[i-1][j-1],self.walls[i-1][j],1,self.walls[i][j-1],self.walls[i][j],1,self.walls[i+1][j-1],self.walls[i+1][j],1]
            else:
                wallSt = [self.walls[i-1][j-1],self.walls[i-1][j],self.walls[i-1][j+1],self.walls[i][j-1],self.walls[i][j],self.walls[i][j+1],self.walls[i+1][j-1],self.walls[i+1][j],self.walls[i+1][j+1]]

        if wallSt[4]:
            if (not wallSt[8] or not wallSt[5]) and wallSt[3] and wallSt[1] and wallSt[7]:
                return random.choice([0,10,20,30])

            elif (not wallSt[6] or not wallSt[3]) and wallSt[5] and wallSt[1] and wallSt[7]:
                return random.choice([5,15,25,35])

            elif not wallSt[7] and wallSt[1]:
                return random.choice([1,2,3,4])

            elif not wallSt[1] and wallSt[3] and wallSt[5] and wallSt[7]:
                return random.choice([41,42,43,44])

            elif not wallSt[2] and wallSt[1] and wallSt[5]:
                return 40

            elif not wallSt[0] and wallSt[1] and wallSt[3]:
                return 45

            elif not wallSt[3] and not wallSt[0] and not wallSt[1]:
                return random.choice([50,54])

            elif not wallSt[1] and not wallSt[2] and not wallSt[5]:
                return random.choice([53,55])

            else:
                return 78

        else:
            return random.choice([6,7,8,9,16,17,18,19,26,27,28,29])

    def createLightMask(self, torch_x, torch_y, light_radius):
        mask = pg.Surface((map_width, map_height)).convert_alpha()
        mask.fill((0, 0, 0, 255))
        pg.draw.circle(mask, (255, 255, 255, 0), (torch_x, torch_y), light_radius)
        return mask
    
    def changeColor(self, canvas):
        wallLen = len(self.walls)
        # for i in range(wallLen):
        #     for j in range(len(self.walls[i])):
        #         wallPos = [j*16, i*16]
        #         if self.walls[i][j] == 0:
        #             print(wallPos[0], wallPos[1])
        #             pg.draw.rect(canvas, (255,0,0), (wallPos[0], wallPos[1], 16, 16))
        
        zero_coordinates = [(x, y) for y in range(len(self.walls)) for x in range(len(self.walls[0])) if self.walls[y][x] == 0]
        random_coordinate = random.choice(zero_coordinates)

        return (random_coordinate[0]*16, random_coordinate[1]*16, 16, 16)



#======================================================================================================================

class torch:
    def __init__(self, lightSize, lightColour, lightIntensity, lightPoint, lightAngle = 0, lightAngleW = 360):
        self.lightSize = lightSize
        self.lightRadius = lightSize * 0.4
        self.lightMakeSurf = pg.Surface((lightSize, lightSize))
        self.lightIntensity = lightIntensity
        self.lightAngle = lightAngle
        self.lightAngleW = lightAngleW
        self.lightPoint = lightPoint
        self.lightShadelPixS = self.shadePix(np.full((lightSize, lightSize, 3), lightColour, dtype=np.uint16))
        self.lightMakeSurf.set_colorkey((0,0,0))
    

    def shadePix(self, listPixels):
        pixFinal = np.array(listPixels)
        pixFinalLen = len(pixFinal)

        for i in range(pixFinalLen):
            for j in range(len(pixFinal[i])):

                #Coding the radiul of the Light
                radDis = (i - self.lightRadius)**2 + (j - self.lightRadius)**2
                radDis = math.sqrt(radDis)

                radFall = (self.lightRadius - radDis) * (1 / self.lightRadius)

                if radFall <= 0:
                    radFall = 0

                #Coding the angle of the Light
                lightAngPoint = (180 / math.pi) * -math.atan2((self.lightRadius - i), (self.lightRadius - j)) + 180

                lightAng2 = abs(((self.lightAngle - lightAngPoint) + 180) % 360 - 180)

                lightAngFall = ((self.lightAngleW / 2) - lightAng2) * (1 / self.lightAngleW)

                if lightAngFall <= 0:
                    lightAngFall = 0
                
                if not self.lightPoint:
                    lightAngFall = 1
                
                #Coding the intensity of the Light
                lightFinalInt = lightAngFall * radFall * self.lightIntensity

                pixFinal[i][j] = pixFinal[i][j] * lightFinalInt

                #Returning
                makeSurf = pg.surfarray.make_surface(pixFinal)

                # print(lightFinalInt, lightAngFall, radFall)
        
        return makeSurf


    def lightWallFetch(self, walls, mouseX, mouseY):
        lightPoints = []

        for i in range(len(walls)):
            for j in range(len(walls[i])):
                if walls[i][j]:
                    if (j * 16 - mouseX >= (-self.lightRadius)-16 and j * 16 - mouseX <= self.lightRadius) and (i * 16 - mouseY >= (-self.lightRadius)-16 and i * 16 - mouseY <= self.lightRadius):
                        lightPoints.append([[j*16+16, i*16], [j*16, i*16], [j*16, i*16+16], [j*16+16, i*16+16]])
        
        return lightPoints



    def isVisible(self, lightPoints, disX, disY):
        makeSh = False

        if self.lightPoint:
            for p in lightPoints:
                try:
                    colour = self.lightShadelPixS.get_at((int(p[0] - disX), int(p[1] - disY)))
                except:
                    colour = (0, 0, 0, 255)
                
                if colour != (0, 0, 0, 255):
                    makeSh = True
        

        else:
            makeSh = True
        

        return makeSh


    
    def quadEdge(self, lightPoints, mouseX, mouseY):
        edges = [lightPoints[0], lightPoints[2], lightPoints[2]]

        if mouseX >= lightPoints[1][0] and mouseX <= lightPoints[0][0]:
            if mouseY < lightPoints[1][1]:
                edges = [lightPoints[0], lightPoints[1], lightPoints[1]]
            if mouseY > lightPoints[0][1]:
                edges = [lightPoints[2], lightPoints[3], lightPoints[3]]
        
        if mouseY >= lightPoints[0][1] and mouseY <= lightPoints[2][1]:#left / right
            if mouseX < lightPoints[1][0]: 
                edges = [lightPoints[1], lightPoints[2], lightPoints[2]]
            if mouseX > lightPoints[0][0]: 
                edges = [lightPoints[0], lightPoints[3], lightPoints[3]]

        if (mouseX < lightPoints[1][0] and mouseY < lightPoints[1][1]):
            edges = [lightPoints[0], lightPoints[2], lightPoints[1]]
        
        elif (mouseX > lightPoints[0][0] and mouseY > lightPoints[2][1]):
            edges = [lightPoints[0], lightPoints[2], lightPoints[3]]

        if (mouseX > lightPoints[0][0] and mouseY < lightPoints[1][1]):
            edges = [lightPoints[1], lightPoints[3], lightPoints[0]]
        elif (mouseX < lightPoints[1][0] and mouseY > lightPoints[2][1]):
            edges = [lightPoints[1], lightPoints[3], lightPoints[2]]

        return edges



    def shadowMake(self, lightMakeSurf, lightPoints):
        lightMakePoints = [lightPoints[0], lightPoints[4],lightPoints[1], lightPoints[2], lightPoints[3]]

        if lightPoints[2][0] + lightPoints[3][0] not in [1000,0] and lightPoints[2][1] + lightPoints[3][1] not in [1000,0]:
            if abs(lightPoints[2][0] - lightPoints[3][0]) == self.lightSize:

                if self.lightRadius < lightPoints[2][1]:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [0, self.lightSize], [self.lightSize, self.lightSize], lightPoints[3]]

                if self.lightRadius > lightPoints[2][1]:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [self.lightSize, 0], [0, 0], lightPoints[3]]
            

            elif abs(lightPoints[2][1] - lightPoints[3][1]) == self.lightSize:

                if self.lightRadius < lightPoints[2][0]:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [self.lightSize, self.lightSize], [self.lightSize, 0], lightPoints[3]]

                if self.lightRadius > lightPoints[2][0]:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [0, self.lightSize], [0, 0], lightPoints[3]]

            else:
                if lightPoints[2][0] != self.lightSize and lightPoints[2][0] != 0:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [lightPoints[3][0], lightPoints[2][1]], lightPoints[3]]
                    
                else:
                    lightMakePoints = [lightPoints[0], lightPoints[4], lightPoints[1], lightPoints[2], [lightPoints[2][0], lightPoints[3][1]], lightPoints[3]]
        
        pg.draw.polygon(lightMakeSurf, (0, 0, 0), lightMakePoints)




    def crossingPoint(self, pointA, pointB):
        disX = pointB[0] - pointA[0]
        disY = pointB[1] - pointA[1]

        if disX == 0:
            temp = [pointB[0], (0 if disY <= 0 else self.lightSize)]
            return temp
        
        if disY == 0:
            temp = [(0 if disX <= 0 else self.lightSize), pointB[1]]
            return temp
        

        gradY = disY / disX
        intercY = pointA[1] - (gradY * pointA[0])

        lineY = 0 if disX <= 0 else self.lightSize
        intersY = [lineY, (gradY * lineY) + intercY]

        if intersY[1] >= 0 and intersY[1] <= self.lightSize:
            return intersY
        

        gradX = disX / disY
        intercX = pointA[0] - (gradX * pointA[1])

        lineX = 0 if disY <= 0 else self.lightSize
        intersX = [(gradX * lineX) + intercX, lineX]

        if intersX[0] >= 0 and intersX[0] <= self.lightSize:
            return intersX

    
    
    def dynamicTorch(self, walls, disp, mouseX, mouseY):
        self.lightMakeSurf.fill((0,0,0))
        self.lightMakeSurf.blit(self.lightShadelPixS, (0,0))

        disX = mouseX - self.lightRadius
        disY = mouseY - self.lightRadius

        for p in self.lightWallFetch(walls, mouseX, mouseY):
            if self.isVisible(p, disX, disY):
                edges = self.quadEdge(p, mouseX, mouseY)
                edges = [[edges[0][0] - disX, edges[0][1] - disY], [edges[1][0] - disX, edges[1][1] - disY], [edges[2][0] - disX, edges[2][1] - disY]]

                self.shadowMake(self.lightMakeSurf, [edges[0], edges[1], self.crossingPoint([self.lightRadius] * 2, edges[1]), self.crossingPoint([self.lightRadius] * 2, edges[0]), edges[2]])
            
        
        pg.draw.circle(self.lightMakeSurf, (255,255,255), (self.lightRadius, self.lightRadius), 2)

        disp.blit(self.lightMakeSurf, (mouseX - self.lightRadius, mouseY - self.lightRadius), special_flags=pg.BLEND_RGBA_ADD)

        return disp


    





# RUNNING GAME
#======================================================================================================================

final_map = map()

# ball_radius = 10
# ball_color = (255, 0, 0) 
#ball = Ball(display_width // 2, display_height // 2, ball_radius, ball_color)

lightSize = 200
lightColor = (255, 185, 9)
lightIntensity = 1
lightPoint = False
minimum_light_size = 50

finalLight = torch(lightSize, lightColor, lightIntensity, lightPoint)

allLights = []
allSurf = []

light_mask_enabled = True

random_coordinate = final_map.changeColor(display)
score = 0
font = pg.font.Font(None, 20)

time_passed = 0
timer_duration = 30 * 1000 

# MAIN LOOP
while True:
    # Setting up vars and Map

    dt = pg.time.Clock().tick(frames_per_second)
    time_passed += dt

    if time_passed >= timer_duration:
        pg.quit()
        break

    time.tick(frames_per_second)
    display.fill((0, 0, 0))

    mouseX, mouseY = pg.mouse.get_pos()
    mouseX = round(mouseX // 3)
    mouseY = round(mouseY // 3)

    final_map.drawMap(display)
    display.blit(wallTex[90], (random_coordinate[0], random_coordinate[1]))
    light_mask = final_map.createLightMask(mouseX, mouseY, lightSize)
    display.blit(light_mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)


    # Torch Activity

    torchDisp = pg.Surface((display.get_size()))
    torchDisp.blit(torchGlob(display.get_size(), 50), (0,0))

    if light_mask_enabled:  # Apply light mask if enabled
        finalLight.dynamicTorch(final_map.wallShadow, torchDisp, mouseX, mouseY)
        for torch in allLights:
            torch[0].dynamicTorch(final_map.wallShadow, torchDisp, torch[1][0], torch[1][1])
            display.blit(wallTex[90], (torch[1][0] - 8, torch[1][1] - 8))

        display.blit(torchDisp, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_m:  # Toggle light mask feature on 'm' key press
                light_mask_enabled = not light_mask_enabled
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            mx = round(mx // 3)
            my = round(my // 3)
            print(mx, my)
            # Create a rectangle around the random coordinate
            random_rect = pg.Rect(random_coordinate[0], random_coordinate[1], 16, 16)
            print(random_coordinate)
            # Check if the mouse click position collides with the random rectangle
            if random_rect.collidepoint((mx,my)):
                score = score + 10
                random_coordinate = final_map.changeColor(display)
                lightSize -= 10
                lightSize = max(lightSize, minimum_light_size)
                finalLight = torch(lightSize, lightColor, lightIntensity, lightPoint)
                print(lightSize)
            


    finalLight.dynamicTorch(final_map.wallShadow, torchDisp, mouseX, mouseY)

    for torch in allLights:
        torch[0].dynamicTorch(final_map.wallShadow, torchDisp, torch[1][0], torch[1][1])
        display.blit(wallTex[90], (torch[1][0] - 8, torch[1][1] - 8))
    
    display.blit(torchDisp, (0,0), special_flags=pg.BLEND_RGBA_MULT)
    # display.blit(wallTex[90], (random_coordinate[0], random_coordinate[1]))

    scoreText = font.render("Score: " + str(score), True, (0, 0, 255))
    display.blit(scoreText, (100, 0))

    time_remaining = (timer_duration - time_passed) // 1000
    timeText = font.render("Time: " + str(time_remaining) + "s", True, (0, 0, 255))
    display.blit(timeText, (0,0))
    
    surf = pg.transform.scale(display, (map_width, map_height))
    screen.blit(surf,(0,0))

    pg.display.update()

print("Your Final Score : ", score)
