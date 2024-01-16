import pygame
import math

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width, window_height = screen.get_size()

clock = pygame.time.Clock()
running = True
font = pygame.font.Font("Bahnschrift.ttf", 20)

#! Most of the decimal numbers are percentages so happy figuring out whats going on my mind rn


# input/output bubble
class Bubble:
    def __init__(self, pos, value, size):
        self.value = value
        self.size = size
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (123, 0, 0)
        self.pos = pygame.math.Vector2(pos)

    def draw(self, screen):
        pygame.draw.circle(
            screen, (1, 1, 1), self.pos, self.size + int(self.size * 0.4)
        )
        pygame.draw.circle(
            screen, self.color, self.pos, self.size
        )  # drawing bigger circle for border

class Connector:
    def __init__(self,pos,value):
        self.start_pos=pygame.math.Vector2(pos)
        self.value=value
        if self.value:
            self.color=(255,0,0)
        else:
            self.color=(25,25,25)
        
        


class And_gate:
    def __init__(self, pos, inp_lines=2, data=[1, 1], screen_=screen, scale=10):
        self.pos = pygame.math.Vector2(pos)
        self.scale = pygame.math.clamp(scale, 2.67, 50)
        self.width = 1 * self.scale * 10
        self.surface = pygame.surface.Surface(
            pygame.math.Vector2(self.width, self.width)
        )
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.inp_no = inp_lines
        self.difference = self.width / (self.inp_no + 1)
        self.initial_pos = self.difference
        self.inps = []
        for i in data:
            self.inps.append(
                Bubble(
                    (int(self.width * 0.0375), self.initial_pos), i, self.width * 0.06
                )
            )
        self.result = self.inps[0]
        self.screen = screen_
        self.output_bubble = Bubble((0, 0), self.result, self.width * 0.06)
        self.logic()

    def draw(self):
        # vertical line
        v_line_start = pygame.math.Vector2(self.width * 0.3, self.width * 0.1)
        v_line_end = pygame.math.Vector2(self.width * 0.3, self.width * 0.9)

        self.difference = self.width / (
            self.inp_no + 1
        )  # gap at which inp lines should be at
        self.initial_pos = self.difference
        center = pygame.math.Vector2(
            (self.width * 0.3), self.width / 2
        )  # center of the semicircle
        width = int(self.width * 0.0375)  # border width of all the shapes
        radius = v_line_start.distance_to(v_line_end) // 2 + width
        pygame.draw.line(self.surface, (1, 1, 1), v_line_start, v_line_end, width)
        pygame.draw.circle(self.surface, (1, 1, 1), center, radius, width)
        pygame.draw.rect(
            self.surface, "black", (0, 0, self.width * 0.3, self.width)
        )  # to cover up the excess part of circle

        for i in self.inps:
            pygame.draw.line(
                self.surface,
                (1, 1, 1),
                (0, self.initial_pos),
                (self.width * 0.3, self.initial_pos),
                width,
            )  # input lines
            i.pos.y = self.initial_pos
            i.draw(self.surface)
            self.initial_pos += self.difference
        # output line
        pygame.draw.line(
            self.surface,
            (1, 1, 1),
            (center.x + radius, self.width // 2),
            (self.width, self.width // 2),
            width,
        )
        self.output_bubble.pos.x, self.output_bubble.pos.y = (
            self.width - int(self.width * 0.0375),
            self.width // 2,
        )
        self.output_bubble.draw(self.surface)
        # drawing borders
        pygame.draw.lines(
            self.surface,
            (1, 1, 1),
            True,
            [
                (0, 0 + width),
                (self.width-(width*0.5), 0 + width),
                (self.width-(width*0.5), self.width - width),
                (0, self.width - width),
            ],
            width,
        )

        self.screen.blit(self.surface, self.rect)

    def logic(self):
        for i in self.inps:
            self.result = self.result and i.value


class Side_bar:
    def __init__(self):
        self.pos = (0, 0)
        self.width = window_width * 0.3
        self.height = window_height
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill((38, 44, 54))
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.elem_pos = (0, 0)

    def add_elem(self, name):
        e_width = self.width
        e_height = self.height * 0.08
        elem = pygame.Surface((e_width, e_height))
        gate_elem = gates[name]((e_width * 0.013, e_height * 0.3), 2, [1, 1], scale=3.5)
        # gate_elem.scale=1
        # gate_elem.pos=(5,e_height*0.3)
        gate_elem.screen = self.surface
        gate_group.append(gate_elem)
        elem.fill((255, 255, 255))
        rect = elem.get_rect(topleft=self.elem_pos)
        self.elem_pos = rect.bottomleft
        text = font.render(name, 1, (0, 0, 0))
        textrect = text.get_rect(topleft=(e_width * 0.15, e_height * 0.55))
        elem.blit(text, textrect)
        self.surface.blit(elem, rect)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


gates = {"and": And_gate, "or": And_gate, "not": And_gate}
gate_group = [And_gate((500, 340), 2, [1, 0])]
sidebar = Side_bar()
sidebar.add_elem("and")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")
    # drawing gate_group
    sidebar.draw(screen)
    for i in gate_group:
        i.draw()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
