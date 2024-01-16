import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

runAnd = 1
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
    pygame.display.flip()

pygame.quit()
