import pygame
import numpy as np

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Gravity Simulation")

# Constants
G = 6.674 * 10**-11
dt = 0.1
scale = 1e-6

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Particles
class Particle:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass

particles = [
    Particle(400, 300, 0, 0, 5.972 * 10**24),
    Particle(400, 200, 0, 0, 7.342 * 10**22)
]

# Main loop
running = True
while running:
    screen.fill(white)

    for particle in particles:
        ax = 0
        ay = 0
        for other in particles:
            if other != particle:
                dx = other.x - particle.x
                dy = other.y - particle.y
                r = np.sqrt(dx**2 + dy**2)
                a = G * other.mass / r**2
                ax += a * dx / r
                ay += a * dy / r
        particle.vx += ax * dt
        particle.vy += ay * dt
        particle.x += particle.vx * dt
        particle.y += particle.vy * dt

        pygame.draw.circle(screen, black, (int(particle.x * scale), int(particle.y * scale)), 5)
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()