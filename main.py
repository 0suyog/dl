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


# input/output bubble
class Bubble:
    def __init__(self, pos, offset, value, size, type):
        self.value = value
        self.size = size
        self.type = type
        self.pos = pygame.math.Vector2(pos)
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        self.offset = offset
        self.win_pos = self.pos + self.offset
        self.connected_wire = None

    def connect(self):
        self.connected_wire = Connector(self)
        connector_group.append(self.connected_wire)

    def update(self, offset):
        self.offset = offset
        self.win_pos = self.pos + self.offset
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)

    def update_value(self, value):
        self.value = value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        # if self.connected_wire and self.type == "output":
        #     print(self.type)
        #     self.connected_wire.update_value(self.value)

    def draw(self, screen):
        self.rect = pygame.draw.circle(
            screen, (1, 1, 1), self.pos, self.size + int(self.size * 0.4)
        )
        # drawing bigger circle for border
        pygame.draw.circle(screen, self.color, self.pos, self.size)


class Out_Bubble(Bubble):
    def __init__(self, pos, offset, value, size, type):
        super().__init__(pos, offset, value, size, type)
        self.wires = []

    def connect(self):
        self.connected_wire = Connector(self)
        connector_group.append(self.connected_wire)
        self.wires.append(self.connected_wire)

    def update_value(self, value):
        self.value = value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        if self.connected_wire:
            for i in self.wires:
                i.update_value(self.value)


class Connector:
    def __init__(self, source):
        self.source = source
        self.start_pos = self.source.win_pos
        self.destination = None
        self.value = source.value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        self.end_pos = pygame.mouse.get_pos()
        self.open = 1

    def update(self):
        self.start_pos = self.source.win_pos
        self.end_pos = self.destination.win_pos

    def update_value(self, value):
        self.value = value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        if self.destination:
            self.destination.update_value(self.value)

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
        self.difference = self.width / (
            len(data) + 1
        )  # gap at which inp lines should be at
        self.initial_pos = self.difference
        self.inp_bubbles = []
        for i in data:
            self.inp_bubbles.append(
                Bubble(
                    (int(self.width * 0.0375), self.initial_pos),
                    self.rect.topleft,
                    i,
                    self.width * 0.06,
                    "input",
                )
            )
            self.initial_pos += self.difference
        self.result = 0
        self.screen = screen_
        self.screen_rect = screen_rect_
        self.output_bubble = Out_Bubble(
            (0, 0), self.rect.topleft, self.result, self.width * 0.06, "output"
        )
        self.logic()
        self.current_connecting_bubble = None
        self.current_wire = None
        self.connected_wires = []
        self.moving = False
        self.calculate()

    def calculate(self):
        self.v_line_start = pygame.math.Vector2(self.width * 0.3, self.width * 0.1)
        self.v_line_end = pygame.math.Vector2(self.width * 0.3, self.width * 0.9)

        self.difference = self.width / (
            len(self.inp_bubbles) + 1
        )  # gap at which inp lines should be at
        self.center = pygame.math.Vector2(
            (self.width * 0.3), self.width / 2
        )  # center of the semicircle
        self.border_width = int(self.width * 0.0375)  # border width of all the shapes
        self.radius = (
            self.v_line_start.distance_to(self.v_line_end) // 2 + self.border_width
        )

    def draw(self):
        self.logic()
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
        if self.moving:
            self.move()
        self.screen.blit(self.surface, self.rect)

    def logic(self):
        self.result = self.inp_bubbles[0].value
        for i in self.inp_bubbles:
            self.result = self.result and i.value
        self.output_bubble.update_value(self.result)

    def collisionwcursor(self):
        for i in self.inp_bubbles:
            if i.rect.collidepoint(
                pygame.mouse.get_pos()[0] - self.rect.topleft[0],
                pygame.mouse.get_pos()[1] - self.rect.topleft[1],
            ):
                self.current_connecting_bubble = i
                return i

        if self.output_bubble.rect.collidepoint(
            pygame.mouse.get_pos()[0] - self.rect.topleft[0],
            pygame.mouse.get_pos()[1] - self.rect.topleft[1],
        ):
            self.current_connecting_bubble = self.output_bubble
            return self.output_bubble
            # self.wire_pos=self.output_bubble.rect.center

        # Connector((self.current_connecting_bubble.rect.centerx-self.rect.left,self.current_connecting_bubble.rect.centery-self.rect.top), self.current_connecting_bubble.value)

    def move(self):
        self.output_bubble.update(self.rect.topleft)
        for i in self.inp_bubbles:
            i.update(self.rect.topleft)
        for i in self.connected_wires:
            i.update()
        buttons = pygame.mouse.get_pressed(num_buttons=3)
        if buttons[0]:
            self.calculate()
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.moving = False


class Or_gate:
    def __init__(
        self, pos, data=[0, 0], screen_=screen, screen_rect_=screen_rect, scale=10
    ):
        self.pos = pos


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
gate_group = [
    And_gate((500, 340), [1, 1]),
    And_gate((630, 340), [0, 0]),
    And_gate((760, 340), [0, 0]),
    And_gate((890, 340), [0, 0]),
]
active_bubble = None
connector_group = []
sidebar = Side_bar()
sidebar.add_elem("and")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if active_bubble == None:
                for i in gate_group:
                    active_bubble = i.collisionwcursor()
                    if active_bubble:
                        active_bubble.connect()
                        break
                    elif i.rect.collidepoint(pygame.mouse.get_pos()):
                        i.moving = True
                        break
            elif active_bubble != None:
                for i in gate_group:
                    temp = i.collisionwcursor()
                    if (
                        temp
                        and temp != active_bubble
                        and temp.type != active_bubble.type
                    ):
                        temp.connected_wire = active_bubble.connected_wire
                        active_bubble = temp
                        active_bubble.connected_wire.open = False
                        if active_bubble.type == "input":
                            active_bubble.connected_wire.destination = active_bubble
                        elif active_bubble.type == "output":
                            active_bubble.connected_wire.destination = (
                                active_bubble.connected_wire.source
                            )
                            active_bubble.connected_wire.source = active_bubble
                        active_bubble.update_value(active_bubble.connected_wire.value)
                        temp = None
                        active_bubble = None
                        break
    screen.fill("purple")
    sidebar.draw(screen)
    # drawing connectors
    for i in connector_group:
        i.draw(screen)
    # drawing gate_group
    for i in gate_group:
        i.draw()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
