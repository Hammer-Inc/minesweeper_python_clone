import pygame

from color_palete import ColourFactory


class Display:
    width = 0
    height = 0
    display_mode = None

    def __init__(self, settings, title, background):
        pygame.init()

        self.display = None
        self.lstClean = None
        self.lstRefresh = None

        self.settings = settings
        self.title = title
        self.background = background

        self.width = self.settings("dsp_window_width")
        self.height = self.settings("dsp_window_height")

        self.display_mode = pygame.FULLSCREEN if self.settings(
            "dsp_screen_mode") else 0

        self.refresh()
        self.clock = pygame.time.Clock()
        self.font = Fonts()

        pygame.display.set_caption(title)

    def fill(self, colour, rect=None):
        colour = ColourFactory.create(colour)
        self.display.fill(colour, rect)

    def queue(self, obj, rect, area=None):
        if type(rect) is tuple or type(rect) is list:
            if len(rect) == 2 and type(obj) is pygame.Surface:
                rect = pygame.Rect(rect, obj.get_size())
            elif len(rect) == 4:
                rect = pygame.Rect(rect)
        else:
            try:
                rect = pygame.Rect(rect)
            except Exception:
                if not area is None:
                    rect = pygame.Rect(area)
                else:
                    rect = pygame.Rect((0, 0, 0, 0))

        if type(obj) is not pygame.Surface:
            obj = ColourFactory.create(obj)
            surf = pygame.Surface(rect.size)
            surf.fill(obj)
        self.lstRefresh.append([obj, rect, area])

    def cancel(self):
        self.lstRefresh = []
        self.lstClean = []

    def refresh(self):
        self.display = pygame.display.set_mode((self.width, self.height),
                                               self.display_mode)
        self.display.fill(self.background)

        pygame.display.update()
        self.lstRefresh = []
        self.lstClean = []

    def render(self, text, colour, font, **position):
        colour = ColourFactory.create(colour)
        txt = self.font[font].render(text, self.settings(
            "dsp_use_antialias"), colour)
        recttxt = txt.get_rect()
        for key in position:
            exec ('recttxt.' + key + '= position[key]')
        return txt, recttxt

    def update(self):
        # blit pair to the screen, update the rects in lstClean, and lstRefresh
        # update lstClean to the rects in lstRefresh
        # clear lstRefresh
        for pair in self.lstRefresh:
            self.display.blit(*pair)
        self.lstClean.extend(x[1] for x in self.lstRefresh)
        pygame.display.update(self.lstClean)
        self.lstClean = list(x[1] for x in self.lstRefresh)
        self.lstRefresh = []


class Fonts():
    pygame.font.init()
    default = pygame.font.SysFont("ariel", 10)
    title = pygame.font.SysFont("AR CARTER", 50)
    text = pygame.font.SysFont("AR CARTER", 20, 1)
    menu_title = pygame.font.SysFont("AR CARTER", 25, 1)
    optionfont = pygame.font.SysFont("AR CARTER", 20)
    uitext = pygame.font.SysFont("Times New Roman", 15)
    nodefont = pygame.font.SysFont("Times New Roman", 20)

    def __getitem__(self, name):
        return eval('self.' + name)

    def __getattr__(self, name):
        return self.default
