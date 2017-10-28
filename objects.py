import math
import random

from color_palete import white, lightgrey, darkgrey, grey
from main import *
from manager import Manager


class Handler:
    resolution = Manager.get_setting("dsp_render_res")

    def __init__(self, settings):
        self.settings = settings
        self.active = False
        self.nodes = {}

        display_width = Manager.get_display().width
        display_height = Manager.get_display().height

        self.surface = pygame.Surface((1 + self.settings['width'] * (
            self.resolution + 1), 1 + self.settings['height'] * (
                                           self.resolution + 1)))
        self.rect = pygame.Rect((0, 20), (
            display_width, display_height - 20))
        Manager.get_display().font.nodeFont = pygame.font.SysFont(
            "Times New Roman",
            self.resolution - 2)
        self.surface.fill(white)
        self.over = False
        for x in xrange(0, self.settings['width']):
            for y in xrange(0, self.settings['height']):
                self.nodes[(x, y)] = Node(self, (x, y))
        self.scr_dim = display_width, display_height - 20
        if display_width / self.settings['width'] > (
                    display_height - 20) / self.settings['height']:
            self.scr_dim = display_height, display_height - 20
        else:
            self.scr_dim = display_width, display_width - 20
            self.scr_dim = display_width, display_width - 20
        self.rect.size = self.scr_dim
        self.rect.center = display_width / 2, (
            display_height + 20) / 2
        self.scrRatio = [1.0 * self.rect.width / self.surface.get_width(),
                         1.0 * self.rect.height / self.surface.get_height()]

    def translate(self, screencoords):
        result = [0, 0]
        result[0] = (1.0 * (screencoords[0] - self.rect.left) / self.scrRatio[
            0] - 1) / (self.resolution + 1) - 1
        result[1] = (1.0 * (screencoords[1] - self.rect.top) / self.scrRatio[
            1]) / (self.resolution + 1) - 1
        if (self.rect.width / self.settings['width'] < 10 and self.rect.height /
            self.settings['height']) and (
                            1.0 > result[0] % 1 > .9 or .1 > result[
                    1] % 1 > .0):
            result = (-1, -1)
        result = math.ceil(result[0]), math.ceil(result[1])
        return tuple(result)

    def queueref(self, target):
        self.surface.blit(*target.update())

    def update(self):
        if self.over:
            Manager.get_display().queue(
                pygame.transform.scale(self.surface, self.scr_dim), self.rect)
            return
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            pygame.event.post(event)
            target = self.translate(event.pos)
            if target not in self.nodes:
                return
            if event.button == 1:
                if not self.active:
                    Node.req_bombs = self.settings['bombs']
                    Node.req_nodes = len(self.nodes)
                    self.nodes[target].setup(True)
                    self.nodes[target].reveal()
                    self.active = True
                else:
                    self.nodes[target].reveal()
            if event.button == 3 and self.active:
                self.nodes[target].flag()
                Manager.get_display().queue(
                    pygame.transform.scale(self.surface, (self.scr_dim)),
                    self.rect)
        if self.over:
            del self.nodes

    def gameover(self, win=False):
        for x in self.nodes:
            t = self.nodes[x]
            if t.is_bomb:
                t.reveal(True)
        self.over = True
        if win:
            endtext = "You Won"
            Colour = "green"
        else:
            endtext = "Game Over"
            Colour = "darkred"
        self.surface.blit(*Manager.get_display().render(endtext, Colour, "nodefont",
                                                        centerx=self.surface.get_width() / 2,
                                                        centery=self.surface.get_height() / 2))
        Node.active_nodes = 0
        Node.bomb_nodes = 0
        Node.safe_bombs = 0
        Node.req_bombs = 0
        Node.bad_flags = 0
        Node.req_nodes = 0
        Node.rev_nodes = 0



class Node:
    active_nodes = 0
    bomb_nodes = 0
    safe_bombs = 0
    req_bombs = 0
    bad_flags = 0
    req_nodes = 0
    rev_nodes = 0

    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.rect = pygame.Rect(1 + pos[0] * (self.parent.resolution + 1),
                                1 + pos[1] * (self.parent.resolution + 1),
                                self.parent.resolution,
                                self.parent.resolution)
        self.is_setup = False
        self.is_bomb = None
        self.isrevealed = False
        self.flagged = False
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill(lightgrey)
        pygame.draw.rect(self.surface, darkgrey, (
            1, 1, self.parent.resolution - 2, self.parent.resolution - 2), 1)
        self.parent.queueref(self)

    def update(self):
        return self.surface, self.rect

    def setup(self, is_start=False):
        if self.is_setup: return
        if self.is_bomb is None and not self.req_bombs == self.bomb_nodes:
            self.is_bomb = random.randint(0,
                                          self.req_nodes - self.active_nodes) <= self.req_bombs - self.bomb_nodes + 1
        if self.is_bomb:
            Node.bomb_nodes += 1
        self.is_setup = True
        Node.active_nodes += 1
        if is_start:
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    target = self.pos[0] + x, self.pos[1] + y
                    if target not in self.parent.nodes:
                        continue
                    target = self.parent.nodes[target]
                    target.is_bomb = False
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                target = self.pos[0] + x, self.pos[1] + y
                if target not in self.parent.nodes:
                    continue
                target = self.parent.nodes[target]
                target.setup()

    def reveal(self, eg=False):
        if self.flagged:
            if not eg: return
            if self.is_bomb:
                self.surface.fill((0, 0, 255))
                self.surface.blit(
                    *Manager.get_display().render("F", "red", "nodefont",
                                             centery=self.glo.dsp_render_res / 2,
                                             centerx=self.glo.dsp_render_res / 2))
                self.parent.queueref(self)
                return
        if self.is_bomb:
            self.surface.fill((255, 0, 0))
            self.parent.queueref(self)
            if not eg: return self.parent.gameover()
            return
        nearby = 0
        self.isrevealed = True
        Node.rev_nodes += 1
        if self.rev_nodes + self.safe_bombs == self.req_nodes:
            self.parent.gameover(True)
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                # print x,y
                if x == 0 and y == 0: continue
                targetc = self.pos[0] + x, self.pos[1] + y
                if targetc in self.parent.nodes:
                    target = self.parent.nodes[targetc]
                    if target.is_bomb:
                        nearby += 1
        if not nearby > 0:
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    targetc = self.pos[0] + x, self.pos[1] + y
                    if targetc not in self.parent.nodes:
                        continue
                    target = self.parent.nodes[targetc]
                    if not target.isrevealed:
                        target.reveal()
        self.surface.fill(grey)
        if nearby > 0:
            self.surface.blit(
                *Manager.get_display().render(str(nearby), "red", "nodefont",
                                         centery=self.parent.resolution / 2,
                                         centerx=self.parent.resolution / 2))
        self.parent.queueref(self)

    def flag(self):
        if self.isrevealed: return
        if not self.flagged:
            self.flagged = True
            if self.is_bomb:
                Node.safe_bombs += 1
            else:
                Node.bad_flags += 1
            self.surface.fill(lightgrey)
            pygame.draw.rect(self.surface, darkgrey, (
                1, 1, self.parent.resolution - 2, self.parent.resolution - 2),
                             1)
            self.surface.blit(*Manager.get_display().render("F", "red", "nodefont",
                                                            centery=self.parent.resolution / 2,
                                                            centerx=self.parent.resolution / 2))
        else:
            if self.is_bomb:
                Node.safe_bombs -= 1
            else:
                Node.bad_flags -= 1
            self.flagged = False
            self.surface.fill(lightgrey)
            pygame.draw.rect(self.surface, darkgrey, (
                1, 1, self.parent.resolution - 2, self.parent.resolution - 2),
                             1)
        self.parent.queueref(self)

    def __repr__(self):
        return str.format("Node(%s) isBomb: %b, isDeployed: %b, isShown: %b",
                          repr(self.pos), self.is_bomb, self.is_setup,
                          self.isrevealed)
