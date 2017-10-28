import pygame

from Form.Element import Element
from color_palete import ColourFactory, lightgrey, darkgrey
from manager import Manager


class Button(Element):
    def __init__(self, colour, on_click, show_press=0, **position_args):
        self.onClick = on_click
        self.colour = ColourFactory.create(colour)
        self.show_press = show_press
        self.active = False
        self.down = False
        self.enabled = True
        self.visible = True
        self.rect = pygame.Rect((0, 0), (0, 0))

        for k in position_args:
            exec ("self.rect." + k + "=position_args[k]")

        self.normal = pygame.Surface(self.rect.size).convert_alpha()
        self.clicked = pygame.Surface(self.rect.size).convert_alpha()

        self.redraw_buttons()

    def recolour(self, colour, show_press=None):
        self.colour = ColourFactory.create(colour)
        self.show_press = show_press if show_press is not None \
            else self.show_press
        self.redraw_buttons()

    def update(self, check=True):
        if not self.visible:
            return
        if not check:
            Manager.get_singleton().display.queue(self.normal, self.rect)
            return

        if self.down:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.enabled and pygame.event.peek(pygame.MOUSEBUTTONUP):
                    self.active = not self.active
                    self.onClick(self)
                    self.down = False
                Manager.get_singleton().display.queue(self.clicked,
                                                      self.rect)
            else:
                Manager.get_singleton().display.queue(self.normal, self.rect)
        elif self.enabled and pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.down = True

        Manager.get_singleton().display.queue(self.normal, self.rect)

    def reset(self):
        self.active = False

    def set_enabled(self, value):
        self.enabled = value
        self.redraw_buttons()

    def redraw_buttons(self):
        self.normal.fill(self.colour)

        self.clicked.fill(self.colour)

        if not self.enabled:
            self.clicked.set_alpha(100)
        else:
            self.clicked.set_alpha(0)
        if self.show_press == 1:
            pygame.draw.rect(self.normal, lightgrey,
                             self.normal.get_rect(), 2)
            pygame.draw.rect(self.clicked, darkgrey,
                             self.clicked.get_rect(), 2)
        elif self.show_press == 2:
            self.clicked.set_alpha(150)