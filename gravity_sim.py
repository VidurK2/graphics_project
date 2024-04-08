import pygame
import numpy as np

main_color = (255, 255, 255)
wall_color = (120, 238, 74)
total_box_width = 500
total_box_height = 500
up_side = 50
down_side = up_side + total_box_height
left_side = 100
right_side = left_side + total_box_width
thickness_wall = 5
blocks = []

block_color = (50, 85, 140)
block_width = 1

height = 800
width = 600

pygame.init()
screen = pygame.display.set_mode((height, width))



gravity = False

def block_draw(block):
    circle = pygame.draw.circle(screen, color_block, (block.x, block.y), block.radius, width_block)
    return circle

# run
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_key = pygame.key.get_pressed()


    if pressed_key[pygame.K_RETURN] and not pressed_key[pygame.K_LSHIFT]:
        if gravity:
            gravity = False
        else:
            gravity = True
    
    screen.fill(main_color)
    pygame.display.set_caption("Gravity Simulation")
    collision_left = pygame.Rect(left_side, up_side, thickness_wall, total_box_height)
    collision_right = pygame.Rect(right_side, up_side, thickness_wall, total_box_height + thickness_wall)
    collision_up = pygame.Rect(left_side, up_side, total_box_width, thickness_wall)
    collision_down = pygame.Rect(left_side, down_side, total_box_width, thickness_wall)

    pygame.draw.rect(screen, wall_color, collision_left)
    pygame.draw.rect(screen, wall_color, collision_right)
    pygame.draw.rect(screen, wall_color, collision_up)
    pygame.draw.rect(screen, wall_color, collision_down)

    for block in blocks:
        if not paused:
            block.move()
        sq = block_draw(block)
        block.sq = sq
        block.check_collide()

    pygame.display.flip()


class block:
    def __init__(self, x, y, radius, color, width):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.width = width
        self.vx = 0
        self.vy = 0
        self.sq = None

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if gravity:
            self.vy += 0.1

    def check_collide(self):
        if self.sq.colliderect(collision_left) or self.sq.colliderect(collision_right):
            self.vx *= -1
        if self.sq.colliderect(collision_up) or self.sq.colliderect(collision_down):
            self.vy *= -1

    def draw(self):
        circle = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)
        return circle

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_color(self, color):
        self.color = color

    def set_radius(self, radius):
        self.radius = radius

    def set_width(self, width):
        self.width = width

    def set_square(self, sq):
        self.sq = sq

    def get_velocity(self):
        return self.vx, self.vy

    def get_position(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

    def get_width(self):
        return self.width

    def get_square(self):
        return self.sq

    def __str__(self):
        return f"Block at ({self.x}, {self.y}) with radius {self.radius} and color {self.color}"    

pygame.quit()
