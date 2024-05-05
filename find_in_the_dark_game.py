import pygame as pg
import random

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

def mapWall(a, b):
    surf = map_image.copy()
    surf.set_clip(pg.Rect(a*16, b*16, 16, 16))
    img = surf.subsurface(surf.get_clip())
    return img.copy()

wallTex = []

for i in range(10):
    for j in range(10):
        wallTex.append(mapWall(j, i))


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
                if self.walls[i][j] == 1:
                    pg.draw.rect(canvas, (255,255,255), (wallPos[0], wallPos[1], 16, 16))
                else:
                    canvas.blit(wallTex[self.texMap[i][j]], wallPos)

    def makeWall(self):
        wallLen = len(self.walls)
        for i in range(wallLen):
            for j in range(len(self.walls[i])):
                self.texMap[i][j] = self.wallRender(i, j)
                if self.walls[i][j] == 1:
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


#======================================================================================================================

final_map = map()


# ball_radius = 10
# ball_color = (255, 0, 0) 
#ball = Ball(display_width // 2, display_height // 2, ball_radius, ball_color)




while True:
    time.tick(frames_per_second)
    display.fill((0, 0, 0))

    mouseX, mouseY = pg.mouse.get_pos()
    mouseX, mouseY = round(mouseX // 3), round(mouseY // 3)

    final_map.drawMap(display)

    for event in pg.event.get():
        if event.type == pg.QUIT: 
            pg.quit()
    
    surf = pg.transform.scale(display, (map_width, map_height))
    screen.blit(surf,(0,0))

    pg.display.update()
