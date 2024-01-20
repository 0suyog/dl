import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))

class b:
    def __init__(self,pos,offset):
        self.pos=pos
        self.offset=offset
        self.win_pos=self.pos+self.offset
    def draw(self,screen):
        pygame.draw.circle(screen,(255,255,255),self.pos,pygame.mouse.get_pos(),10)

class r:
    def __init__(self,pos):
        self.surf=pygame.Surface((50,50))
        self.rect=self.surf.get_rect(topleft=(100,100))
        self.ball=b(self.rect.center,self.rect.topleft)

b_grp=[]
run = 1
while run:
    screen.fill("green")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
    if rect.collidepoint((pygame.mouse.get_pos()[0]-300,pygame.mouse.get_pos()[1]-300)):
        print("meow")
    pygame.display.flip()

pygame.quit()