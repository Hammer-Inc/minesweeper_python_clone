import traceback as tb
import xml.etree.ElementTree as xml
import pygame, gc
from display import *

__all__ = [
    'ConfigGLO',
    'init',
    'pygame',
    'tb',
    'gc'
]


# contains editable settings.config values
class Settings():
    game_level_presets = {
        'Easy': {'width': 10, 'height': 10, 'bombs': 10},
        'Medium': {'width': 20, 'height': 20, 'bombs': 50},
        'Hard': {'width': 30, 'height': 30, 'bombs': 400},
        'Debug': {'width': 20, 'height': 10, 'bombs': 2}
    }

    def __init__(self):
        try:
            self.settings = xml.parse('settings.config')
        except Exception:
            self.settings = xml.parse('Defaults.xml')
            self.UpdateFile()
        finally:
            self.defaults = xml.parse('Defaults.xml')

    def __getattr__(self, name):
        try:
            return eval(self.settings.find(name).attrib['value'])
        except AttributeError:
            try:
                value = eval(self.defaults.find(name).attrib['value'])
                self.settings.append(self.defaults.find(name))
                self.UpdateFile()
                return value
            except AttributeError:
                return None

    def UpdateFile(self):
        self.settings.write('settings.config')


# contains all global items/functions
class Global():
    title = 'MineSweeper'
    background = (100, 100, 255)

    def __init__(self):
        self.settings = Settings()
        self.display = Display(self)

    def __getattr__(self, name):
        return eval('self.settings.' + name)


def init():
    global glo
    glo = Global()
    try:
        import states
        states.MainMenu()
    except Exception:
        tb.print_exc()
    pygame.quit()


def ConfigGLO(cls):
    cls.glo = glo
    return cls
