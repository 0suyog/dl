import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))

class b:
    def __init__(self,pos):
        self.pos=pos
        self.end_pos=pygame.mouse.get_pos()
        self.incrementing=True
    def draw(self,screen):
        if self.incrementing:
            self.end_pos=pygame.mouse.get_pos()
        pygame.draw.line(surface=screen,color=(0,0,0),start_pos=self.pos,end_pos=self.end_pos,width=5)

b_grp=[b((30,30))]
run = 1
start=(30,30)
while run:
    screen.fill("green")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
    end_pos=pygame.mouse.get_pos()
    # pygame.draw.line(surface=screen,color=(0,0,0),start_pos=start,end_pos=end_pos,width=5)
    for i in b_grp:
        i.draw(screen)
    # if rect.collidepoint((pygame.mouse.get_pos()[0]-300,pygame.mouse.get_pos()[1]-300)):
    #     print("meow")
    pygame.display.flip()

pygame.quit()