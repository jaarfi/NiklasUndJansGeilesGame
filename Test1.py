
from baseClasses import *

import pygame as pg
import pygame.gfxdraw
from pygame.locals import *

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

pg.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.

myfont = pygame.font.SysFont('Comic Sans MS', 30)
# Fensterkonstanten
displaywidth = 1080
displayheigth = 720
displayflags = 0
displaycolbit = 32

display = pg.display.set_mode((displaywidth, displayheigth), displayflags, displaycolbit)
clock = pg.time.Clock()


game = Game(displaywidth,displayheigth,display, myfont)
game.startGame()

