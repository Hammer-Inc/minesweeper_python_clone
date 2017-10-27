import pygame
from main import *


@ConfigGLO
class Button:
    def __init__(self, colour, fn_on_click, show_press=0, **position_args):
        self.onClick = fn_on_click
        self.rect = pygame.Rect((0, 0), (0, 0))
        for k in position_args:
            exec ("self.rect." + k + "=position_args[k]")
        self.surfNorm = pygame.Surface(self.rect.size)
        if type(colour) is str:
            colour = self.glo.display[colour]
        self.colour = colour
        self.showpress = show_press
        self.surfNorm.fill(colour)
        self.surfClicked = self.surfNorm.copy()
        if show_press == 1:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)
        elif show_press == 2:
            self.surfClicked.fill(tuple(x / 2 for x in self.colour))
        self.active = False
        self.down = False
        self.enabled = True

    def recolour(self, colour, showpress=2):
        if type(colour) is str:
            colour = self.glo.display[colour]
        self.surfNorm.fill(colour, (0, 0, self.rect.width, self.rect.height))
        self.surfClicked.fill(colour, (0, 0, self.rect.width, self.rect.height))
        if showpress == 1:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)
        elif showpress == 2:
            self.surfClicked.fill(tuple(x / 2 for x in colour))

    def update(self, check=True):
        if not self.enabled: return
        if not check:
            self.glo.display.queue(self.surfNorm, self.rect)
            return
        if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.down = True
        if pygame.event.peek(pygame.MOUSEBUTTONUP):
            if self.rect.collidepoint(pygame.mouse.get_pos()) and self.down:
                self.active = not self.active
                self.onClick(self)
            self.down = False
        if self.down:
            if not self.rect.collidepoint(pygame.mouse.get_pos()):
                self.glo.display.queue(self.surfNorm, self.rect)
                return
            self.glo.display.queue(self.surfClicked, self.rect)
        else:
            self.glo.display.queue(self.surfNorm, self.rect)


class TButton(Button):
    def __init__(self, text, colour, fnOnClick, show_press=0, **positionArgs):
        Button.__init__(self, colour, fnOnClick, show_press, **positionArgs)
        self.onClick = fnOnClick
        self.rect = pygame.Rect((0, 0), (0, 0))
        for k in positionArgs:
            exec ("self.rect." + k + "=positionArgs[k]")
        self.surfNorm = pygame.Surface(self.rect.size)
        if type(colour) is str:
            colour = self.glo.display[colour]
        self.colour = colour
        self.text = text
        self.showpress = show_press
        self.surfNorm.fill(colour)
        self.surfNorm.blit(
            *self.glo.display.render(self.text, "black", "optionfont",
                                     center=self.rect.center))
        self.surfClicked = self.surfNorm.copy()
        if show_press == 1:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)
        elif show_press == 2:
            self.surfClicked.fill(tuple(x / 2 for x in self.colour))
        self.active = False
        self.down = False
        self.enabled = True

    def recolour(self, colour, showpress=2):
        if type(colour) is str:
            colour = self.glo.display[colour]
        self.surfNorm.fill(colour, (0, 0, self.rect.width, self.rect.height))
        self.surfNorm.blit(
            *self.glo.display.render(self.text, "black", "optionfont",
                                     center=self.rect.center))
        self.surfClicked = self.surfNorm.copy()
        if showpress == 1:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)
        elif showpress == 2:
            self.surfClicked.fill(tuple(x / 2 for x in colour))


class AlphaButton(Button):
    def __init__(self, colour, opacity, fn_on_click, show_press=True,
                 **position_args):
        Button.__init__(self, colour, fn_on_click, show_press, **position_args)
        self.onClick = fn_on_click
        self.rect = pygame.Rect((0, 0), (0, 0))
        for k in position_args:
            exec ("self.rect." + k + "=position_args[k]")
        self.surfNorm = pygame.Surface(self.rect.size).convert_alpha()
        if type(colour) is str:
            colour = self.glo.display[colour]
        colour = colour + tuple([opacity])
        self.surfNorm.fill(colour)
        self.surfClicked = self.surfNorm.copy()
        if show_press:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)
        self.active = False
        self.down = False

    def recolour(self, colour, opacity, show_press=True):
        if type(colour) is str:
            colour = self.glo.display[colour]
        colour = colour + tuple([opacity])
        self.surfNorm.fill(colour)
        self.surfClicked.fill(colour)
        if show_press:
            pygame.draw.rect(self.surfNorm, self.glo.display.lightgrey,
                             self.surfNorm.get_rect(), 2)
            pygame.draw.rect(self.surfClicked, self.glo.display.darkgrey,
                             self.surfClicked.get_rect(), 2)


@ConfigGLO
class MultipleChoice:
    def __init__(self, fn_on_click, title, options, selected_index, top_left,
                 width=200, chk_size=(20, 20)):
        self.onClick = fn_on_click
        self.selOption = options[selected_index]
        self.Surface = pygame.Surface(
            (width, (chk_size[1] + 2) * len(options))).convert_alpha()
        self.surfnorm = pygame.Surface(chk_size)
        self.rect = pygame.Rect(top_left, self.Surface.get_size())
        self.surfselect = self.surfnorm.copy()
        pygame.draw.rect(self.surfnorm, self.glo.display.red,
                         self.surfnorm.get_rect(), 2)
        pygame.draw.rect(self.surfselect, self.glo.display.green,
                         self.surfselect.get_rect(), 2)
        self.options = []
        for op in xrange(0, len(options)):
            self.options.append((options[op],
                                 self.glo.display.render(options[op], 'grey',
                                                         "optionfont",
                                                         top=op * (
                                                             chk_size[1] + 2),
                                                         left=0), pygame.Rect(
                (self.rect.width - 20, op * (chk_size[1] + 2)), chk_size)))

    def update(self):
        if pygame.event.peek(pygame.MOUSEBUTTONUP):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                for op in self.options:
                    if op[2].move(self.rect.topleft).collidepoint(
                            pygame.mouse.get_pos()):
                        self.selOption = op[0]
                        self.onClick(self)
        self.Surface.fill((0, 0, 0, 0))
        for op in self.options:
            self.Surface.blit(*op[1])
            if op[0] == self.selOption:
                self.Surface.blit(self.surfselect, op[2])
            else:
                self.Surface.blit(self.surfnorm, op[2])
        self.glo.display.queue(self.Surface, self.rect)
