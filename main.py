import pygame
import math

pygame.init()
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1260, 680), pygame.RESIZABLE)
screen_rect = screen.get_rect()
window_width, window_height = screen.get_size()

clock = pygame.time.Clock()
running = True
font = pygame.font.Font("Bahnschrift.ttf", 20)

#! Most of the decimal numbers are percentages so happy figuring out whats going on my mind rn
# TODO STILL HAVE TO SEPERATE METHODS LIKE MAKE A DIFFERENT METHOD TO CALCULATE THE POSITIONS THAN DOING IT ALL WHILE DRAWING ITS GONNA MAKE THE APPLICATION FAST TOO


# input/output bubble
class Bubble:
    def __init__(self, pos, offset, value, size):
        self.value = value
        self.size = size
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        self.pos = pygame.math.Vector2(pos)
        self.offset = offset
        self.win_pos = self.pos + self.offset
        self.connected_wire = None

    # def connect(self):

    def draw(self, screen):
        self.rect = pygame.draw.circle(
            screen, (1, 1, 1), self.pos, self.size + int(self.size * 0.4)
        )
        # drawing bigger circle for border
        pygame.draw.circle(screen, self.color, self.pos, self.size)


class Connector:
    def __init__(self, pos, source, value):
        self.start_pos = pos

        self.source = source
        self.destination = None
        self.value = value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        self.end_pos = pygame.mouse.get_pos()
        self.open = 1

    def draw(self, screen):
        if self.open:
            self.end_pos = pygame.mouse.get_pos()
        else:
            self.end_pos = self.destination.win_pos

        pygame.draw.line(screen, self.color, self.source.win_pos, self.end_pos, 5)


class And_gate:
    def __init__(
        self,
        pos,
        inp_lines=1,
        data=[0, 0],
        screen_=screen,
        screen_rect_=screen_rect,
        scale=10,
    ):
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
        self.inp_bubbles = []
        for i in data:
            self.inp_bubbles.append(
                Bubble(
                    (int(self.width * 0.0375), self.initial_pos),
                    self.rect.topleft,
                    i,
                    self.width * 0.06,
                )
            )
            self.initial_pos += self.difference
        self.result = self.inp_bubbles[0]
        self.screen = screen_
        self.screen_rect = screen_rect_
        self.logic()
        self.output_bubble = Bubble(
            (0, 0), self.rect.topleft, self.result, self.width * 0.06
        )
        self.current_connecting_bubble = None
        self.current_wire = None
        self.moving=False
        self.calculate()
        # print(self.result)

    def calculate(self):
        self.v_line_start = pygame.math.Vector2(self.width * 0.3, self.width * 0.1)
        self.v_line_end = pygame.math.Vector2(self.width * 0.3, self.width * 0.9)

        self.difference = self.width / (
            self.inp_no + 1
        )  # gap at which inp lines should be at
        self.initial_pos = self.difference
        self.center = pygame.math.Vector2(
            (self.width * 0.3), self.width / 2
        )  # center of the semicircle
        self.border_width = int(self.width * 0.0375)  # border width of all the shapes
        self.radius = (
            self.v_line_start.distance_to(self.v_line_end) // 2 + self.border_width
        )

    def draw(self):
        pygame.draw.line(
            self.surface,
            (1, 1, 1),
            self.v_line_start,
            self.v_line_end,
            self.border_width,
        )
        pygame.draw.circle(
            self.surface, (1, 1, 1), self.center, self.radius, self.border_width
        )
        # to cover up the excess part of circle
        pygame.draw.rect(self.surface, "black", (0, 0, self.width * 0.3, self.width))

        # input lines
        self.initial_pos = self.difference
        for i in self.inp_bubbles:
            pygame.draw.line(
                self.surface,
                (1, 1, 1),
                (0, self.initial_pos),
                (self.width * 0.3, self.initial_pos),
                self.border_width,
            )
            # i.pos.y = self.initial_pos
            i.draw(self.surface)
            self.initial_pos += self.difference
        # output line
        pygame.draw.line(
            self.surface,
            (1, 1, 1),
            (self.center.x + self.radius, self.width // 2),
            (self.width, self.width // 2),
            self.border_width,
        )
        self.output_bubble.pos = pygame.math.Vector2(
            self.width - int(self.width * 0.0375),
            self.width // 2,
        )
        self.output_bubble.win_pos = self.output_bubble.pos + self.output_bubble.offset
        self.output_bubble.draw(self.surface)
        # drawing borders
        pygame.draw.lines(
            self.surface,
            (1, 1, 1),
            True,
            [
                (0, 0 + self.border_width),
                (self.width - (self.border_width * 0.5), 0 + self.border_width),
                (
                    self.width - (self.border_width * 0.5),
                    self.width - self.border_width,
                ),
                (0, self.width - self.border_width),
            ],
            self.border_width,
        )

        self.screen.blit(self.surface, self.rect)

    def logic(self):
        for i in self.inp_bubbles:
            self.result = self.result and i.value

    def collisionwcursor(self):
        for i in self.inp_bubbles:
            if i.rect.collidepoint(
                pygame.mouse.get_pos()[0] - self.rect.topleft[0],
                pygame.mouse.get_pos()[1] - self.rect.topleft[1],
            ):
                self.current_connecting_bubble = i
                return self

        if self.output_bubble.rect.collidepoint(
            pygame.mouse.get_pos()[0] - self.rect.topleft[0],
            pygame.mouse.get_pos()[1] - self.rect.topleft[1],
        ):
            self.current_connecting_bubble = self.output_bubble
            return self
            # self.wire_pos=self.output_bubble.rect.center

    def connect(self):
        self.current_wire = Connector(
            (
                self.rect.left + self.current_connecting_bubble.rect.centerx,
                self.rect.top + self.current_connecting_bubble.rect.centery,
            ),
            self.current_connecting_bubble,
            self.current_connecting_bubble.value,
        )
        connector_group.append(self.current_wire)
        # Connector((self.current_connecting_bubble.rect.centerx-self.rect.left,self.current_connecting_bubble.rect.centery-self.rect.top), self.current_connecting_bubble.value)
    def move(self):
        buttons=pygame.mouse.get_pressed(num_buttons=3)
        if buttons[0]:
            self.calculate()
            self.rect.center=pygame.mouse.get_pos()

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
        gate_elem = gates[name](
            (e_width * 0.013, e_height * 0.3),
            2,
            [1, 1],
            self.surface,
            self.rect,
            scale=3.5,
        )
        # gate_group.append(gate_elem)
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
gate_group = [And_gate((500, 340), 2, [1, 0]), And_gate((900, 340), 2, [1, 0])]
active_gate = None
active_bubbles = []
connector_group = []
sidebar = Side_bar()
sidebar.add_elem("and")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if active_gate == None:
                
                for i in gate_group:
                    active_gate = i.collisionwcursor()
                    if active_gate:
                        active_gate.connect()
                        break
                    elif i.rect.collidepoint(pygame.mouse.get_pos()):
                        i.move()
                        break
            elif active_gate != None:
                for i in gate_group:
                    
                    # active_gate = None
                    temp = i.collisionwcursor()
                    if temp and temp != active_gate:
                        temp.current_wire = active_gate.current_wire
                        active_gate.current_connecting_bubble = None
                        active_gate.current_wire = None
                        active_gate = temp
                        active_gate.current_wire.open = False
                        active_gate.current_wire.destination = (
                            active_gate.current_connecting_bubble
                        )
                        active_gate.current_connecting_bubble = None
                        active_gate.current_wire = None
                        active_gate = None
                        break
                # active_gate = None
    screen.fill("purple")
    sidebar.draw(screen)
    # drawing connectors
    for i in connector_group:
        # print(f"open = {i.open } mouse = {pygame.mouse.get_pos()} end_pos= {i.end_pos}")
        i.draw(screen)
    # drawing gate_group
    for i in gate_group:
        i.draw()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
