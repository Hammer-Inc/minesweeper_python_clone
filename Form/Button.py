import pygame

from Form.Element import Element
from color_palete import ColourFactory, lightgrey, darkgrey


class Button(Element):
    def __init__(self, colour, on_click, **position_args):
        Element.__init__(self)
        self.on_click = on_click
        self.colour = ColourFactory.create(colour)
        self.active = False
        rect = pygame.Rect((0, 0), (0, 0))

        for k in position_args:
            exec ("rect." + k + "=position_args[k]")

        surface = pygame.Surface(self.rect.size).convert_alpha()
        surface.fill(self.colour)

        pygame.draw.rect(surface, lightgrey, surface.get_rect(), 2)

        self.update_surface(surface)
        self.update_rect(rect)

    def reset(self):
        self.active = False

    def on_click_start(self):
        self.draw(clicked=True)

    def on_click_finish(self):
        self.draw(clicked=False)

    def draw(self, clicked):
        surface = self.surface
        surface.fill(self.colour)
        if clicked:
            pygame.draw.rect(surface, darkgrey, surface.get_rect(), 2)
            surface.set_alpha(50)
        else:
            pygame.draw.rect(surface, lightgrey, surface.get_rect(), 2)
            surface.set_alpha(0)
        self.update_surface(surface)
