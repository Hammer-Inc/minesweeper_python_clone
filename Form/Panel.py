import pygame

from Form.Element import Element
from color_palete import grey


class Panel(Element):
    def __init__(self, rect, *children):
        Element.__init__(self)
        self.children = children
        for element in children:
            element.__tick__()
        rect = pygame.Rect(rect)
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(grey)
        self.rect = rect
        self.enabled = False

    def post_tick(self):
        for element in self.children:
            element.__tick__()
