import Menu
import pygame as pg

myfont = pg.font.SysFont('Comic Sans MS', 30)
# Fensterkonstanten
displaywidth = 800
displayheight = 600
displayflags = 0
displaycolbit = 32

display = pg.display.set_mode((displaywidth, displayheight), displayflags, displaycolbit)

Menu.menu(display)
