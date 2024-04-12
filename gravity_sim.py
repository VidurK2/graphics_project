import numpy
import pygame
import random
import time

pygame.init()

blockColor = (50, 85, 140)
screenColor = (255,255,255)
lineColor = (0,0,0)
shCol = (100, 100, 100)

total_box_width = 500
total_box_height = 500
thickness_wall = 5
blocks_no = 0
playing = True
times = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
blocks = []
isPause = False

up_side = 50
down_side = up_side + total_box_height
left_side = 100
right_side = left_side + total_box_width

collision_left = pygame.Rect(left_side, up_side, thickness_wall, total_box_height)
collision_right = pygame.Rect(right_side, up_side, thickness_wall, total_box_height + thickness_wall)
collision_up = pygame.Rect(left_side, up_side, total_box_width, thickness_wall)
collision_down = pygame.Rect(left_side, down_side, total_box_width, thickness_wall)

shapes = []
sizeBlockNew = 1
collide = True
blocksNew = 1
newBlockDraw = "Blocks"
click = False
prevKeyTime = 0
prevMousePointer = (0, 0)
isPause = True
clockTick = 1.0

""" gravity = False    
g_scale = 0  
self.last_shape_position = (0, 0)
self.boxes = []
self.circular_motion = False
self.centripetal_acceleration = 0 """



def move(block):

    block['posX'] += block['speedX'] * clockTick
    block['posY'] += block['speedY'] * clockTick

def wallHit(rect, block):

    # collision with walls
    if rect.colliderect(collision_left):
        block['posX'] += 2 
        block['speedX'] = -block['speedX'] * 1
        block['pastCollide'] = collision_left

    elif rect.colliderect(collision_right):
        block['posX'] -= 2 
        block['speedX'] = -block['speedX'] * 1
        block['pastCollide'] = collision_right

    elif rect.colliderect(collision_up):
        block['posY'] += 2 
        block['speedY'] = -block['speedY'] * 1
        block['pastCollide'] = collision_up

    elif rect.colliderect(collision_down):
        block['posY'] -= 2 
        block['speedY'] = -block['speedY'] * 1
        block['pastCollide'] = collision_down

def set_random_position(block):
    posX = random.randint(left_side + block['radius'], right_side - block['radius'])
    posY = random.randint(up_side + block['radius'], down_side - block['radius'])
    drawCircle = pygame.draw.circle(screen, blockColor, (posX, posY), block['radius'])

def blockCreate(box, mass, location=None, speedX=None, speedY=None):
    radius = mass * 5

    if speedX is None:
        speedX = random.random() * random.randint(-2, 2)
    
    else:
        speedX = speedX

    if speedY is None:
        speedY = random.random() * random.randint(-2, 2)
    
    else:
        speedY = speedY
    
    if not location:
        posX = random.randint(left_side + radius, right_side - radius)
        posY = random.randint(up_side + radius, down_side - radius)
    
    else:
        posX, posY = location[0], location[1]
    
    drawCircle = pygame.draw.circle(screen, blockColor, (posX, posY), radius)
    pastCollide = None

    return {
        'box': box,
        'mass': mass,
        'radius': radius,
        'speedX': speedX,
        'speedY': speedY,
        'posX': posX,
        'posY': posY,
        'drawCircle': drawCircle,
        'pastCollide': pastCollide
    }

def blockAdd(block=None):
    global blocks_no

    if not block:
        block = blockCreate(screen, sizeBlockNew)

    disPos = False

    blocks.append(block)
    blocks_no += 1


def play():
    global playing, collide, blocksNew, sizeBlockNew, newBlockDraw, click, prevKeyTime, prevMousePointer, isPause
    while playing:
        times.tick(240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            
            key = pygame.key.get_pressed()

            if key[pygame.K_BACKSPACE]:
                print("Pressed Backspace", collide)
                if collide:
                    collide = False
                else:
                    collide = True

            if key[pygame.K_p]:
                print("Pressed P", newBlockDraw)
                newBlockDraw = "Blocks"
            
            if key[pygame.K_LEFT]:
                if blocksNew != 1:
                    blocksNew //= 2
            
            if key[pygame.K_RIGHT]:
                if blocksNew != 64:
                    blocksNew = blocksNew * 2
            
            if key[pygame.K_UP]:
                if sizeBlockNew < 5:
                    sizeBlockNew = sizeBlockNew + 1
            
            if key[pygame.K_DOWN]:
                if sizeBlockNew > 1:
                    sizeBlockNew = sizeBlockNew - 1
            
            """ if key[pygame.K_ESCAPE]:
                  reset()  """    

            if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                    click = False
            
            if key[pygame.K_SPACE]:
                print(isPause)
                if time.monotonic() - prevKeyTime > 0.1:
                    prevKeyTime = time.monotonic()
                    if isPause:
                        isPause = False
                    else:
                        isPause = True

            if click:
                if newBlockDraw == "Blocks":
                    if blocksNew == 1:
                        new_x, new_y = pygame.mouse.get_pos()
                        prev_x, prev_y = prevMousePointer
                        if abs(new_x - prev_x) > 15 or abs(new_y - prev_y) > 15:
                            blockAddBlock = blockCreate(screen, sizeBlockNew, (new_x, new_y))
                            blockAdd(blockAddBlock)
                            prevMousePointer = new_x, new_y
                    else:
                        for i in range(blocksNew):
                            blockAddScreen = blockCreate(screen, sizeBlockNew)
                            screen.blockAdd(blockAddScreen)
            
            screen.fill(screenColor)

            pygame.draw.rect(screen, lineColor, collision_left)
            pygame.draw.rect(screen, lineColor, collision_right)
            pygame.draw.rect(screen, lineColor, collision_up)
            pygame.draw.rect(screen, lineColor, collision_down)
        

            # draw_text()

            for block in blocks:
                if not isPause:
                    move(block)
                
                rect = pygame.draw.circle(screen, blockColor, (block['posX'], block['posY']), block['radius'], 1)

                block['rect'] = rect
                wallHit(rect, block)

            pygame.display.flip()
    pygame.quit()

play()
