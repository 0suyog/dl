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
        self.connected_wire = Connector(self,True)
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
        if self.connected_wire and self.type == "output":
            self.connected_wire.update_value(self.value)

    def draw(self, screen):
        self.rect = pygame.draw.circle(
            screen, (1,1,1), self.pos, self.size + int(self.size * 0.4)
        )
        # drawing bigger circle for border
        pygame.draw.circle(screen, self.color, self.pos, self.size)


class Out_Bubble(Bubble):
    def __init__(self, pos, offset, value, size, type):
        super().__init__(pos, offset, value, size, type)
        self.wires = []

    def connect(self):
        self.connected_wire = Connector(self,True)
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
    def __init__(self, source,initial=False):
        self.source = source
        self.initial=initial
        self.value = source.value
        if self.value:
            self.color = (255, 0, 0)
        else:
            self.color = (25, 25, 25)
        self.open = True
        self.alpha=50
        if self.initial:
            self.start_pos = self.source.win_pos
            self.end_pos = (self.start_pos[0],pygame.mouse.get_pos()[1])
            self.destination=Connector(self)
            connector_group.append(self.destination)
        else:
            print(self.source.start_pos)
            self.end_pos = pygame.mouse.get_pos()
            self.start_pos = (pygame.mouse.get_pos()[0],self.source.end_pos[1])
            self.destination = None
        

    def update(self):
        if self.initial:
            self.start_pos = self.source.start_pos
            self.end_pos = self.destination.start_pos
        else:
            self.start_pos=self.source.end_pos
            self.end_pos=self.destination.win_pos
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
            if self.initial:
                self.end_pos = (pygame.mouse.get_pos()[0],self.start_pos[1])
            else:
                if self.source.open==False:
                    self.open=False
                self.start_pos=self.source.end_pos
                self.end_pos=pygame.mouse.get_pos()
        else:
            if self.initial:
                self.end_pos = (self.destination.start_pos[0],self.start_pos[1])
            else:
                self.open=self.source.open
                self.start_pos=self.source.end_pos
                self.end_pos = self.destination.win_pos
                # self.end_pos=pygame.mouse.get_pos()
        print(self.source,self.open)
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 5)


class Gate:
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
        self.prev_pos=(540,self.width*0.5)
        self.surface = pygame.surface.Surface(
            pygame.math.Vector2(self.width, self.width)
        )
        self.alpha=255
        self.surface.set_alpha(self.alpha)
        self.color=(1,1,1)
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect(topleft=self.pos) 
        self.border_width = int(self.width * 0.0375)  # border width of all the shapes
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
        self.current_connecting_bubble = None
        self.connected_wires = []
        self.moving = False
        self.output_bubble.pos = pygame.math.Vector2(
            self.width - int(self.width * 0.0375),
            self.width // 2,
        )
        self.output_bubble.win_pos = self.output_bubble.pos + self.output_bubble.offset
        self.invalid_pos=False
        self.resizing=False
        # self.borders=[pygame.draw.line(surface=self.surface,color=self.color,start_pos=(0,self.border_width*0.45),end_pos=(self.width,self.border_width*0.45),width=self.border_width),
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.border_width*0.5),end_pos=(self.width-(self.border_width*0.5),self.width),width=self.border_width),
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),end_pos=(0,self.width-(self.border_width*0.5)),width=self.border_width),
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.border_width*0.45,self.width-(self.border_width*0.5)),end_pos=(self.border_width*0.45,0),width=self.border_width)
        # ]
        # self.borders_pos=[((0,self.border_width*0.45),(self.width,self.border_width*0.45)),
        #                   ((self.width-(self.border_width*0.5),self.border_width*0.5),(self.width-(self.border_width*0.5),self.width)),
        #                   ((self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),(0,self.width-(self.border_width*0.5))),
        #                   ((self.border_width*0.45,self.width-(self.border_width*0.5)),(self.border_width*0.45,0))]

    def collisionwcursor(self):
        if not self.resizing:
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
        self.alpha=100
        buttons = pygame.mouse.get_pressed(num_buttons=3)
        if buttons[0]:
            self.invalid_pos=self.rect.colliderect(sidebar.rect)
            if self.invalid_pos:
                # print(self.rect.colliderect(sidebar.rect))
                # self.alpha=255
                self.color=(255,0,0)
            else:
                # self.alpha=100
                self.color=(1,1,1)
            self.calculate()
            self.rect.center = pygame.mouse.get_pos()
        else:
            if self.invalid_pos:
                self.rect.center=self.prev_pos
            self.color=(1,1,1)
            self.alpha=255
            self.moving = False
        self.output_bubble.update(self.rect.topleft)
        for i in self.inp_bubbles:
            i.update(self.rect.topleft)
        for i in self.connected_wires:
            i.update()
        self.surface.set_alpha(self.alpha)



class And_gate(Gate):
    def __init__(
        self, pos, data=[0, 0], screen_=screen, screen_rect_=screen_rect, scale=10
    ):
        super().__init__(pos, data, screen_, screen_rect_, scale)
        self.logic()
        self.calculate()

    def calculate(self):
        self.border_width = int(self.width * 0.0375)
        self.v_line_start = pygame.math.Vector2(
            self.width * 0.3, self.width * 0.1
        )  # backbone of and gate
        self.v_line_end = pygame.math.Vector2(self.width * 0.3, self.width * 0.9)

        self.difference = self.width / (

            len(self.inp_bubbles) + 1
        )  # gap at which inp lines should be at
        self.center = pygame.math.Vector2(
            (self.width * 0.3), self.width / 2
        )  # center of the semicircle
        self.radius = (
            self.v_line_start.distance_to(self.v_line_end) // 2 + self.border_width
        )
        # self.borders_pos=[((0,self.border_width*0.45),(self.width,self.border_width*0.45)),
        #                   ((self.width-(self.border_width*0.5),self.border_width*0.5),(self.width-(self.border_width*0.5),self.width)),
        #                   ((self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),(0,self.width-(self.border_width*0.5))),
        #                   ((self.border_width*0.45,self.width-(self.border_width*0.5)),(self.border_width*0.45,0))]


    def draw(self):
        self.logic()
        if self.moving:
            self.move()
        pygame.draw.line(
            self.surface,
            self.color,
            self.v_line_start,
            self.v_line_end,
            self.border_width,
        )
        pygame.draw.circle(
            self.surface, self.color, self.center, self.radius, self.border_width
        )
        # to cover up the excess part of circle
        pygame.draw.rect(self.surface,(0,0,0), (0, 0, self.width * 0.3, self.width))
        # input lines
        self.initial_pos = self.difference
        for i in self.inp_bubbles:
            pygame.draw.line(
                self.surface,
                self.color,
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
            self.color,
            (self.center.x + self.radius, self.width // 2),
            (self.width, self.width // 2),
            self.border_width,
        )

        self.output_bubble.draw(self.surface)
        # drawing borders
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(0,self.border_width*0.45),end_pos=(self.width,self.border_width*0.45),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.border_width*0.5),end_pos=(self.width-(self.border_width*0.5),self.width),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),end_pos=(0,self.width-(self.border_width*0.5)),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.border_width*0.45,self.width-(self.border_width*0.5)),end_pos=(self.border_width*0.45,0),width=self.border_width)
        self.screen.blit(self.surface, self.rect)





    def logic(self):
        self.result = self.inp_bubbles[0].value
        for i in self.inp_bubbles:
            self.result = self.result and i.value
        self.output_bubble.update_value(self.result)


class Or_gate(Gate):
    def __init__(
        self, pos, data=[0, 0], screen_=screen, screen_rect_=screen_rect, scale=10
    ):
        super().__init__(pos, data, screen_, screen_rect_, scale)
        self.logic()
        self.calculate()

    def draw(self):
        self.logic()
        pygame.draw.circle(
            self.surface, self.color, self.arc_center, self.arc_radius, self.border_width
        )
        pygame.draw.ellipse(
            self.surface,
            self.color,
            (
                -self.width*0.9,
                (self.width * 0.05),
                self.width + (self.width * 0.7),
                (self.width - (self.width * 0.1)),
            ),
            self.border_width,
        )
        pygame.draw.rect(self.surface, (0,0,0), (0, 0, self.width * 0.17, self.width))
        self.initial_pos = self.difference
        for i in self.inp_bubbles:
            pygame.draw.line(
                self.surface,
                self.color,
                (0, self.initial_pos),
                (
                    self.arc_center[0]+ math.sqrt(pow(self.arc_radius, 2)- pow(self.arc_center[1] - self.initial_pos, 2))- (self.border_width // 2),
                    self.initial_pos,
                ),
                self.border_width,
            )
            self.initial_pos += self.difference
            i.draw(self.surface)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=((self.width + (self.width * 0.7))-self.width*0.9,self.width*0.5),end_pos=(self.width,self.width*0.5),width=self.border_width)
        self.output_bubble.draw(screen=self.surface)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(0,self.border_width*0.45),end_pos=(self.width,self.border_width*0.45),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.border_width*0.5),end_pos=(self.width-(self.border_width*0.5),self.width),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),end_pos=(0,self.width-(self.border_width*0.5)),width=self.border_width)
        # pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.border_width*0.45,self.width-(self.border_width*0.5)),end_pos=(self.border_width*0.45,0),width=self.border_width)
        if self.moving:
            self.move()
        self.screen.blit(self.surface, self.rect)

    def logic(self):
        self.result = self.inp_bubbles[0].value
        for i in self.inp_bubbles:
            self.result = self.result or i.value
        self.output_bubble.update_value(self.result)

    def calculate(self):
        self.arc_radius = self.width - (self.width * 0.2)
        self.arc_center = (-self.width * 0.5, self.width * 0.5)

class Not_gate():
    def __init__(self, pos, data=0, screen_=screen, screen_rect_=screen_rect, scale=10):
        self.pos = pygame.math.Vector2(pos)
        self.prev_pos=(540,0)
        self.scale = pygame.math.clamp(scale, 2.67, 50)
        self.width = 1 * self.scale * 10
        self.surface = pygame.surface.Surface(
            pygame.math.Vector2(self.width, self.width)
        )
        self.surface.set_colorkey((0, 0, 0))
        self.alpha=255
        self.color=(1,1,1)
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.border_width = int(self.width * 0.0375)  # border width of all the shapes
        self.difference = self.width / 2 # gap at which inp lines should be at
        self.initial_pos = self.difference
        self.inp_bubbles =Bubble(pos=(int(self.width * 0.0375), self.initial_pos),offset=self.rect.topleft,value=data,size=self.width * 0.06,type="input")
        self.result = 1
        self.screen = screen_
        self.screen_rect = screen_rect_
        self.output_bubble = Out_Bubble(
            (0, 0), self.rect.topleft, self.result, self.width * 0.06, "output"
        )
        self.current_connecting_bubble = None
        self.connected_wires = []
        self.moving = False
        self.output_bubble.pos = pygame.math.Vector2(
            self.width - int(self.width * 0.0375),
            self.width // 2,
        )
        self.output_bubble.win_pos = self.output_bubble.pos + self.output_bubble.offset
        self.logic()
    
    def draw(self):
        self.logic()
        self.surface.set_alpha(self.alpha)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width*0.31,self.width*0.3),end_pos=(self.width*0.31,self.width*0.7),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color, start_pos=(self.width*0.31, self.width*0.3), end_pos=(self.width*0.56,self.width*0.5),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width*0.31,self.width*0.7),end_pos=(self.width*0.56,self.width*0.5),width=self.border_width)
        pygame.draw.circle(surface=self.surface,color=self.color,center=((self.width*0.585)+self.border_width,self.width*0.5),radius=self.width*0.07,width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(0,self.initial_pos),end_pos=(self.width*0.31,self.initial_pos),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=((self.width*0.585)+(2*self.border_width),self.width*0.5),end_pos=(self.width,self.width*0.5),width=self.border_width)
        self.inp_bubbles.draw(self.surface)
        self.output_bubble.draw(self.surface)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(0,self.border_width*0.45),end_pos=(self.width,self.border_width*0.45),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.border_width*0.5),end_pos=(self.width-(self.border_width*0.5),self.width),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.width-(self.border_width*0.5),self.width-(self.border_width*0.5)),end_pos=(0,self.width-(self.border_width*0.5)),width=self.border_width)
        pygame.draw.line(surface=self.surface,color=self.color,start_pos=(self.border_width*0.45,self.width-(self.border_width*0.5)),end_pos=(self.border_width*0.45,0),width=self.border_width)
        if self.moving:
            self.move()
        self.screen.blit(self.surface,self.rect)
    def logic(self):
        self.result=not self.inp_bubbles.value
        self.output_bubble.update_value(self.result)

    def move(self):
        self.alpha=100
        buttons = pygame.mouse.get_pressed(num_buttons=3)
        if buttons[0]:
            self.invalid_pos=self.rect.colliderect(sidebar.rect)
            if self.invalid_pos:
                # print(self.rect.colliderect(sidebar.rect))
                # self.alpha=255
                self.color=(255,0,0)
            else:
                # self.alpha=100
                self.color=(1,1,1)
            # self.calculate()
            self.rect.center = pygame.mouse.get_pos()
        else:
            if self.invalid_pos:
                self.rect.center=self.prev_pos
            self.color=(1,1,1)
            self.alpha=255
            self.moving = False
        self.output_bubble.update(self.rect.topleft)
        self.inp_bubbles.update(self.rect.topleft)
        for i in self.connected_wires:
            i.update()
        self.surface.set_alpha(self.alpha)
    def collisionwcursor(self):
        if self.inp_bubbles.rect.collidepoint(pygame.mouse.get_pos()[0] - self.rect.topleft[0],pygame.mouse.get_pos()[1] - self.rect.topleft[1],):
            self.current_connecting_bubble = i
            return self.inp_bubbles

        if self.output_bubble.rect.collidepoint(pygame.mouse.get_pos()[0] - self.rect.topleft[0],pygame.mouse.get_pos()[1] - self.rect.topleft[1],):
            self.current_connecting_bubble = self.output_bubble
            return self.output_bubble

class Bar_elem:
    def __init__(self,name,pos,width,height):
        self.pos=pos
        self.name=name 
        self.width=width
        self.height=height
        self.border_color=(1,1,1)
        self.surface=pygame.Surface((self.width,self.height))
        self.rect=self.surface.get_rect(topleft=self.pos)
        self.text = font.render(self.name, 1, (0, 0, 0))
        self.textrect = self.text.get_rect(topleft=(self.width * 0.2, self.height * 0.4))
        self.gate=gates[self.name](pos=(self.width*0.025,self.height*0.25),screen_=self.surface,screen_rect_=self.rect,scale=3.5)
    def draw(self,screen):
        self.surface.fill("white")
        pygame.draw.line(surface=self.surface,color=self.border_color,start_pos=(0,0),end_pos=(self.width,0),width=3)
        pygame.draw.line(surface=self.surface,color=self.border_color,start_pos=(self.width,0),end_pos=(self.width,self.height),width=3)
        pygame.draw.line(surface=self.surface,color=self.border_color,start_pos=(self.width,self.height),end_pos=(0,self.height),width=3)
        pygame.draw.line(surface=self.surface,color=self.border_color,start_pos=(0,self.height),end_pos=(0,0),width=3)

        # pygame.draw.line()
        self.surface.blit(self.text,self.textrect)
        self.gate.draw()
        screen.blit(self.surface,self.rect)


class Side_bar:
    def __init__(self):
        self.pos = (0, 0)
        self.width = window_width * 0.2
        self.height = window_height
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill((38, 44, 54))
        self.rect = self.surface.get_rect(topleft=self.pos)
        self.elem_pos = (0, 0)
        self.elem_width=self.width
        self.elem_height=self.height*0.08
        self.just4show=[]
        self.bars=[]
        self.bar_rects=[]
        self.gate_pos=(0,0)

    def add_elem(self, name):
        self.bar_elem = Bar_elem(name=name,pos=self.elem_pos,width=self.elem_width,height=self.elem_height)
        self.bars.append(self.bar_elem)
        self.elem_pos = self.bar_elem.rect.bottomleft

    def collisionwcursor(self):
        for i in self.bars:
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                created_gate=gates[i.name](pos=pygame.mouse.get_pos())
                gate_group.append(created_gate)
                created_gate.moving=True
                return created_gate
            


    def draw(self, screen):
        # self.surface.blit(self.bar_elem, self.bar_rect)
        for i in self.bars:
            i.draw(self.surface)
        for i in self.just4show:
            i.draw()
        screen.blit(self.surface, self.rect)
        # self.collisionwcursor()


class merged_gates(Gate):
    def __init__(self,*args):
        self.result=args[0].value
        for i in args:
            self.result=i.value
        print(self.result)



gates = {"And": And_gate, "Or": Or_gate, "Not": Not_gate}
gate_group = [
    Or_gate((500, 340), [0,0]),And_gate((630, 340), [0,0]),Not_gate((760,340),0)
]

active_bubble = None
connector_group = []
sidebar = Side_bar()
sidebar.add_elem("And")
sidebar.add_elem("Or")
sidebar.add_elem("Not")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if active_bubble == None:
                #  checking collision with bar elem in side bar to create new gate  
                # doing this here cuz you cant add new element if you are aready dragging a wire
                if not sidebar.collisionwcursor():
                    for i in gate_group:
                        active_bubble = i.collisionwcursor()
                        if active_bubble:
                            active_bubble.connect()
                            break
                        elif i.rect.collidepoint(pygame.mouse.get_pos()):
                            i.moving = True
                            i.prev_pos=i.rect.center
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
                        # active_bubble.connected_wire.destination.open=False
                        if active_bubble.type == "input":
                            active_bubble.connected_wire.destination.destination = active_bubble
                        elif active_bubble.type == "output":
                            # active_bubble.connected_wire.source=active_bubble.destination.destination
                            # active_bubble.connected_wire.destination.initial=False
                            active_bubble.connected_wire.destination.destination = (
                                active_bubble.connected_wire.source
                            )
                            active_bubble.connected_wire.source = active_bubble
                            active_bubble.connected_wire.destination
                            active_bubble.connected_wire.initial=True
                            # active_bubble.connected_wire.destination=active_bubble.connected_wire
                            # active_bubble.connected_wire.initial=True
                            active_bubble.wires.append(active_bubble.connected_wire)
                            active_bubble.connected_wire.update_value(active_bubble.value)
                        # print(f"should be input {active_bubble.connected_wire.destination.value}, should be output={active_bubble.connected_wire.source.value}")
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
