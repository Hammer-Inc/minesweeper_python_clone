import pygame

from Form.Button import Button
from color_palete import black, lightgrey, darkgrey
from manager import Manager


class TextButton(Button):
    def __init__(self, text, colour, on_click, **position_args):
        self.text = text
        Button.__init__(self, colour, on_click, **position_args)

    def draw(self, clicked):
        surface = self.surface
        surface.fill(self.colour)
        if clicked:
            pygame.draw.rect(surface, darkgrey, surface.get_rect(), 2)
            surface.set_alpha(50)
        else:
            pygame.draw.rect(surface, lightgrey, surface.get_rect(), 2)
            surface.set_alpha(0)
        text = Manager.get_singleton().display.render(self.text, black,
                                                      "optionfont",
                                                      center=self.rect.center)
        self.surface.blit(*text)
        self.update_surface(surface)


