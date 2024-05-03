import pygame
import random
import time
import numpy as np

pygame.init()

screen_width = 1200
screen_height = 1000
blockColor = (249, 230, 242)
screenColor = (0, 0, 0)
lineColor = (255, 255, 255)
shCol = (100, 100, 100)

total_box_width = 900
total_box_height = 900
thickness_wall = 5
blocks_no = 0
playing = True
times = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
blocks = []
isPause = True

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
gravity = False

def create_particle(pos):
    # Generate random color components within the valid range
    r = max(0, min(random.randint(100, 255), 255))
    g = max(0, min(random.randint(100, 255), 255))
    b = max(0, min(random.randint(100, 255), 255))
    
    return {
        'x': pos[0],
        'y': pos[1],
        'vx': random.uniform(-0.5, 0.5),
        'vy': random.uniform(-0.5, 0.5),
        'rad': random.randint(2, 4),  # Randomize radius for variety
        'color': (r, g, b),  # Construct color tuple
        'creation_time': time.monotonic()
    }



def update_particle(particle):
    particle['x'] += particle['vx']
    particle['y'] += particle['vy']
    particle['vx'] += random.uniform(-0.1, 0.1)
    particle['vy'] += random.uniform(-0.1, 0.1)
    particle['rad'] = max(1, particle['rad'] - 0.05)

def draw_particle(particle, surface):
    print("Particle color before drawing:", particle['color'])
    pygame.draw.circle(surface, particle['color'], (int(particle['x']), int(particle['y'])), particle['rad'])


def create_line_trail(pos):
    particles = []
    for _ in range(10):  # Adjust the number of particles for the desired density
        particles.append(create_particle(pos))
    return particles

def update_line_trail(particles):
    for particle in particles:
        update_particle(particle)

def draw_line_trail(particles, surface):
    for particle in particles:
        draw_particle(particle, surface)

def wallHit(rect, block):
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

def interpolate_color(color1, color2, factor):
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    return (r, g, b)

def draw_height_indicators():
    font = pygame.font.SysFont(None, 20)
    for i in range(up_side, down_side + 1, 10):
        text = font.render(str(i), True, (255, 255, 255))
        screen.blit(text, (10, screen_height - (i - up_side) * screen_height // total_box_height))

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
        'pastCollide': pastCollide,
        'prevPosX': posX,
        'prevPosY': posY,
        'line_trail': create_line_trail((posX, posY)),  # Initialize line trail
        'gravity': gravity 
    }

def move(block):
    if block['gravity']:
        block['speedY'] += 0.005 * 9.81 * clockTick

    block['prevPosX'] = block['posX']
    block['prevPosY'] = block['posY']

    block['posX'] += block['speedX'] * clockTick
    block['posY'] += block['speedY'] * clockTick

def blockAdd(block=None):
    global blocks_no

    if not block:
        block = blockCreate(screen, sizeBlockNew)

    blocks.append(block)
    blocks_no += 1

def play():
    global playing, collide, blocksNew, sizeBlockNew, newBlockDraw, click, prevKeyTime, prevMousePointer, isPause
    screen.fill(screenColor)
    last_fill_time = time.monotonic()
    while playing:
        times.tick(240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            
            key = pygame.key.get_pressed()

            if key[pygame.K_BACKSPACE]:
                collide = not collide

            if key[pygame.K_RETURN]:
                for block in blocks:
                    block['gravity'] = not block['gravity']

            if key[pygame.K_p]:
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
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
                            blockAdd(blockAddScreen)

            if event.type == pygame.MOUSEBUTTONUP:
                click = False
            
            if key[pygame.K_SPACE]:
                if time.monotonic() - prevKeyTime > 0.1:
                    prevKeyTime = time.monotonic()
                    isPause = not isPause

        pygame.draw.rect(screen, lineColor, collision_left)
        pygame.draw.rect(screen, lineColor, collision_right)
        pygame.draw.rect(screen, lineColor, collision_up)
        pygame.draw.rect(screen, lineColor, collision_down)

        draw_height_indicators()

        for block in blocks:
            if not isPause:
                move(block)

            # Determine the vertical position of the block relative to the screen height
            vertical_position_ratio = 1 - (block['posY'] - up_side) / total_box_height

            # Interpolate between colors based on the vertical position
            block_color = interpolate_color((0, 255, 0), (255, 0, 0), vertical_position_ratio)


            # Update line trail colors based on the block's color
            for particle in block['line_trail']:
                particle['color'] = block_color

            draw_line_trail(block['line_trail'], screen)  # Draw line trail

            rect = pygame.draw.circle(screen, block_color, (block['posX'], block['posY']), block['radius'], 1)
            block['rect'] = rect
            wallHit(rect, block)

            if time.monotonic() - last_fill_time >= 10:
                screen.fill(screenColor)
                last_fill_time = time.monotonic()

        pygame.display.flip()
    pygame.quit()

play()
