import pygame
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

surf = pygame.Surface((100, 100))
rect = surf.get_rect(center=(100, 100))

run = 1
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
    pygame.display.flip()
    surf.fill((38, 44, 54))
pygame.quit()
