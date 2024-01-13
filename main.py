import pygame
import math

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width, window_height = screen.get_size()

clock = pygame.time.Clock()
running = True
font = pygame.font.Font("Bahnschrift.ttf", 20)

class And_gate:
    def __init__(self, pos, inp_lines=2, data=[0, 0]):
        self.pos = pygame.math.Vector2(pos)
        self.scale = pygame.math.clamp(0, 0.27, 8)
        self.width = 100 * self.scale
        self.surface = pygame.surface.Surface(
            pygame.math.Vector2(self.width, self.width)
        )
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.inp_no = inp_lines
        self.inps = data
        self.result = self.inps.pop(0)

    # Most of the decimal numbers are percentages so happy figuring out whats going on my mind rn
    def draw(self, screen):
        # vertical line
        v_line_start = pygame.math.Vector2(self.width * 0.3, self.width * 0.1)
        v_line_end = pygame.math.Vector2(self.width * 0.3, self.width * 0.9)

        # horizontal line
        difference = self.width / (self.inp_no + 1)
        initial_pos = difference
        # print(initial_pos)
        center = pygame.math.Vector2((self.width * 0.3), self.width / 2)
        width = int(self.width * 0.0375)
        compensation = width
        radius = v_line_start.distance_to(v_line_end) // 2 + compensation
        pygame.draw.line(self.surface, (255, 255, 255), v_line_start, v_line_end, width)
        pygame.draw.circle(self.surface, (255, 255, 255, 255), center, radius, width)
        pygame.draw.rect(self.surface, "black", (0, 0, self.width * 0.3, self.width))
        for i in range(self.inp_no):
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (0, initial_pos),
                (self.width * 0.3, initial_pos),
                width,
            )
            initial_pos += difference
        screen.blit(self.surface, self.rect)

    def logic(self):
        for i in self.inps:
            self.result = self.result and i


class Side_bar:
    def __init__(
        self,
    ):
        self.pos = (0, 0)
        self.width = window_width * 0.3
        self.height = window_height
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill((38, 44, 54))
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.elem_pos = (0, 0)
    
    def add_elem(self,name):
        pass

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


a = And_gate((500, 340))
sidebar = Side_bar()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")
    a.draw(screen)
    sidebar.draw(screen)

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
