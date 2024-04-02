import pygame
import numpy as np

wall_color = (120, 238, 74)
total_box_width = 500
total_box_height = 500
up_side = 50
down_side = up_side + total_box_height
left_side = 100
right_side = left_side + total_box_width
thickness_wall = 5

height = 800
width = 600

pygame.init()
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("Gravity Simulation")
collision_left = pygame.Rect(left_side, up_side, thickness_wall, total_box_height)
collision_right = pygame.Rect(right_side, up_side, thickness_wall, total_box_height + thickness_wall)
collision_up = pygame.Rect(left_side, up_side, total_box_width, thickness_wall)
collision_down = pygame.Rect(left_side, down_side, total_box_width, thickness_wall)


pygame.draw.rect(screen, wall_color, collision_left)
pygame.draw.rect(screen, wall_color, collision_right)
pygame.draw.rect(screen, wall_color, collision_up)
pygame.draw.rect(screen, wall_color, collision_down)

#run
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()