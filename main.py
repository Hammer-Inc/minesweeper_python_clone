import gc
import traceback as tb

import pygame

from display import *
from manager import Manager

__all__ = [
    'init',
    'pygame',
    'tb',
    'gc'
]


def init():
    Manager()
    try:
        import states
        states.MainMenu()
    except Exception:
        tb.print_exc()
    pygame.quit()


def ConfigGLO(cls):
    cls.glo = glo
    return cls
