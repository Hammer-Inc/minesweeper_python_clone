import math
import random

from main import *


@ConfigGLO
class Manager:
    def __init__(self, parent):
        self.parent = parent
        self.settings = parent.GameOptions
        self.boolactive = False

        self.lstNodes = {}

        self.Surface = pygame.Surface((1 + self.settings['width'] * (
            self.glo.dsp_render_res + 1), 1 + self.settings['height'] * (
                                           self.glo.dsp_render_res + 1)))
        self.rect = pygame.Rect((0, 20), (
            self.glo.dsp_window_width, self.glo.dsp_window_height - 20))
        self.glo.display.font.nodeFont = pygame.font.SysFont("Times New Roman",
                                                             self.glo.dsp_render_res - 2)
        self.Surface.fill(self.glo.display.white)
        self.Over = False
        for x in xrange(0, self.parent.GameOptions['width']):
            for y in xrange(0, self.parent.GameOptions['height']):
                self.lstNodes[(x, y)] = Node(self, (x, y))
        self.scr_dim = self.glo.dsp_window_width, self.glo.dsp_window_height - 20
        if self.glo.dsp_window_width / self.settings['width'] > (
                    self.glo.dsp_window_height - 20) / self.settings['height']:
            self.scr_dim = self.glo.dsp_window_height, self.glo.dsp_window_height - 20
        else:
            self.scr_dim = self.glo.dsp_window_width, self.glo.dsp_window_width - 20
            self.scr_dim = self.glo.dsp_window_width, self.glo.dsp_window_width - 20
        self.rect.size = self.scr_dim
        self.rect.center = self.glo.dsp_window_width / 2, (
            self.glo.dsp_window_height + 20) / 2
        self.scrRatio = [1.0 * self.rect.width / self.Surface.get_width(),
                         1.0 * self.rect.height / self.Surface.get_height()]

    def translate(self, screencoords):
        result = [0, 0]
        result[0] = (1.0 * (screencoords[0] - self.rect.left) / self.scrRatio[
            0] - 1) / (self.glo.dsp_render_res + 1) - 1
        result[1] = (1.0 * (screencoords[1] - self.rect.top) / self.scrRatio[
            1]) / (self.glo.dsp_render_res + 1) - 1
        if (self.rect.width / self.settings['width'] < 10 and self.rect.height /
            self.settings['height']) and (
                            1.0 > result[0] % 1 > .9 or .1 > result[
                    1] % 1 > .0):
            result = (-1, -1)
        result = math.ceil(result[0]), math.ceil(result[1])
        return tuple(result)

    def queueref(self, target):
        self.Surface.blit(*target.update())

    def update(self):
        if self.Over:
            self.glo.display.queue(
                pygame.transform.scale(self.Surface, (self.scr_dim)), self.rect)
            return
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            pygame.event.post(event)
            target = self.translate(event.pos)
            if not target in self.lstNodes: return
            if event.button == 1:
                if not self.boolactive:
                    Node.reqbombs = self.settings['bombs']
                    Node.reqNodes = len(self.lstNodes)
                    self.lstNodes[target].setup(True)
                    self.lstNodes[target].reveal()
                    self.boolactive = True
                else:
                    self.lstNodes[target].reveal()
            if event.button == 3 and self.boolactive:
                self.lstNodes[target].flag()
        # print self.Surface.get_size()
        self.glo.display.queue(
            pygame.transform.scale(self.Surface, (self.scr_dim)), self.rect)
        if self.Over:
            del self.lstNodes

    def GameOver(self, win=False):
        for x in self.lstNodes:
            t = self.lstNodes[x]
            if t.isbomb:
                t.reveal(True)
        self.Over = True
        if win:
            endtext = "You Won"
            Colour = "green"
        else:
            endtext = "Game Over"
            Colour = "darkred"
        self.Surface.blit(*self.glo.display.render(endtext, Colour, "nodefont",
                                                   centerx=self.Surface.get_width() / 2,
                                                   centery=self.Surface.get_height() / 2))
        Node.activenodes = 0
        Node.bombnodes = 0
        Node.safebombs = 0
        Node.reqbombs = 0
        Node.badflags = 0
        Node.reqNodes = 0
        Node.revNodes = 0


@ConfigGLO
class Node():
    activenodes = 0
    bombnodes = 0
    safebombs = 0
    reqbombs = 0
    badflags = 0
    reqNodes = 0
    revNodes = 0

    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.rect = pygame.Rect(1 + pos[0] * (self.glo.dsp_render_res + 1),
                                1 + pos[1] * (self.glo.dsp_render_res + 1),
                                self.glo.dsp_render_res,
                                self.glo.dsp_render_res)
        self.issetup = False
        self.isbomb = None
        self.isrevealed = False
        self.flagged = False
        self.Surface = pygame.Surface(self.rect.size)
        self.Surface.fill(self.glo.display.lightgrey)
        pygame.draw.rect(self.Surface, self.glo.display.darkgrey, (
            1, 1, self.glo.dsp_render_res - 2, self.glo.dsp_render_res - 2), 1)
        self.parent.queueref(self)

    def update(self):
        return self.Surface, self.rect

    def setup(self, IsStart=False):
        if self.issetup: return
        if self.isbomb is None and not self.reqbombs == self.bombnodes:
            self.isbomb = random.randint(0,
                                         self.reqNodes - self.activenodes) <= self.reqbombs - self.bombnodes + 1
        if self.isbomb:
            Node.bombnodes += 1
        # print self.bombnodes,self.reqbombs
        self.issetup = True
        Node.activenodes += 1
        if IsStart:
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    target = self.pos[0] + x, self.pos[1] + y
                    if not target in self.parent.lstNodes: continue
                    target = self.parent.lstNodes[target]
                    target.isbomb = False
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                target = self.pos[0] + x, self.pos[1] + y
                if not target in self.parent.lstNodes: continue
                target = self.parent.lstNodes[target]
                target.setup()

    def reveal(self, eg=False):
        if self.flagged:
            if not eg: return
            if self.isbomb:
                self.Surface.fill((0, 0, 255))
                self.Surface.blit(
                    *self.glo.display.render("F", "red", "nodefont",
                                             centery=self.glo.dsp_render_res / 2,
                                             centerx=self.glo.dsp_render_res / 2))
                self.parent.queueref(self)
                return
        if self.isbomb:
            self.Surface.fill((255, 0, 0))
            self.parent.queueref(self)
            if not eg: return self.parent.GameOver()
            return
        nearby = 0
        self.isrevealed = True
        Node.revNodes += 1
        if self.revNodes + self.safebombs == self.reqNodes:
            self.parent.GameOver(True)
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                # print x,y
                if x == 0 and y == 0: continue
                targetc = self.pos[0] + x, self.pos[1] + y
                # print targetc
                if targetc in self.parent.lstNodes:
                    target = self.parent.lstNodes[targetc]
                    #	print 'OrNode:',self,'TarNode:',target
                    if target.isbomb: nearby += 1
        if not nearby > 0:
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    targetc = self.pos[0] + x, self.pos[1] + y
                    if not targetc in self.parent.lstNodes: continue
                    target = self.parent.lstNodes[targetc]
                    if not target.isrevealed:
                        target.reveal()
        self.Surface.fill(self.glo.display.grey)
        if nearby > 0:
            self.Surface.blit(
                *self.glo.display.render(str(nearby), "red", "nodefont",
                                         centery=self.glo.dsp_render_res / 2,
                                         centerx=self.glo.dsp_render_res / 2))
        self.parent.queueref(self)

    def flag(self):
        if self.isrevealed: return
        if not self.flagged:
            self.flagged = True
            if self.isbomb:
                Node.safebombs += 1
            else:
                Node.badflags += 1
            self.Surface.fill(self.glo.display.lightgrey)
            pygame.draw.rect(self.Surface, self.glo.display.darkgrey, (
                1, 1, self.glo.dsp_render_res - 2, self.glo.dsp_render_res - 2),
                             1)
            self.Surface.blit(*self.glo.display.render("F", "red", "nodefont",
                                                       centery=self.glo.dsp_render_res / 2,
                                                       centerx=self.glo.dsp_render_res / 2))
        else:
            if self.isbomb:
                Node.safebombs -= 1
            else:
                Node.badflags -= 1
            self.flagged = False
            self.Surface.fill(self.glo.display.lightgrey)
            pygame.draw.rect(self.Surface, self.glo.display.darkgrey, (
                1, 1, self.glo.dsp_render_res - 2, self.glo.dsp_render_res - 2),
                             1)
        self.parent.queueref(self)

    def __repr__(self):
        return `self.pos, self.isbomb, self.issetup, self.isrevealed`
