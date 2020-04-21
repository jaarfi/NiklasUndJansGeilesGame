import os, math, time, random
from os import listdir
from os.path import isfile, join

import pygame as pg
from pygame.locals import *

import my_color as c

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

pg.init()

# Fensterkonstanten
displaywidth = 800
displayheigth = 600
displayflags = 0
displaycolbit = 32

display = pg.display.set_mode((displaywidth, displayheigth), displayflags, displaycolbit)
clock = pg.time.Clock()


def mapdraw():
    display.fill(c.cyan)

    pg.draw.rect(display, c.khaki, (0, displayheigth - 100, displaywidth, 100))


mapdraw()
beta = 65
v_0 = 75


def parabola(beth, v0, x_value):
    y_value = -math.tan(math.radians(beth)) * x_value + (9.81 * x_value ** 2) / (
            2 * (v0 * 100) * (math.cos(math.radians(beth)) ** 2)) + 500
    return int(y_value)


def multV_0():
    for v0 in range(10, 100, 10):

        pr_x, pr_y = 0, 0
        fi = True

        for x in range(displaywidth):
            y = parabola(beta, v0, x)

            if fi:
                fi = False
                pr_x, pr_y = x, y
                continue

            pg.draw.line(display, c.dark_orange, (pr_x, pr_y), (int(x), int(y)), 2)
            pr_x, pr_y = x, y


def multBeta():
    for b in range(10, 80, 10):

        pre_x, pre_y = 0, 0
        firs = True

        for x in range(displaywidth):
            y = parabola(b, v_0, x)

            if firs:
                firs = False
                pre_x, pre_y = x, y
                continue

            pg.draw.line(display, c.dark_grey, (pre_x, pre_y), (int(x), int(y)), 2)
            pre_x, pre_y = x, y


# _________________________________________________
# sprite preparation
only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]

expl = []

for myfile in only_files:
    if "Explosion" in myfile:
        expl.append(pg.image.load("sprites/" + myfile))

expl_sound = pg.mixer.Sound("sound/läsch_explosion.wav")


def explosion_tank(x_cor=400, y_cor=400):
    global dead
    dead = False
    expl_sound.play()
    clock.tick(1)
    for i in range(8):
        mapdraw()
        display.blit(expl[i], (x_cor - 140, y_cor - 140))

        clock.tick(10)
        pg.display.update()

    mapdraw()


# __________________________________________________


bullet = pg.Rect(300, 100, 80, 80)
b_image = pg.image.load("pics/Effects/Heavy_Shell.png")
b_s_image = pg.transform.scale(b_image, (80, 80))


def rotate():
    pass


# ___________________________________________________


prev_x, prev_y = 0, 0
first = True
dead = True
x = 0
angle = 0
# Spielschleife
while True:

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            quit()
    mapdraw()

    """
    if angle == 359:
        angle = 0
        bs_image = pg.transform.rotate(b_s_image, angle)
    else:
        bs_image = pg.transform.rotate(b_s_image, angle)
        angle += 1
    display.blit(bs_image, bullet)
 """
    y = parabola(beta, v_0, x) + 20

    # ____________line zeichnen__________
    if first:
        first = False
        prev_x, prev_y = x, y
        continue
    
    
    if y < 500 or x < 100:
        pg.draw.circle(display, c.cyan, (int(prev_x), int(prev_y)), 5)

        if int(x) % 15 == 0:
            pg.draw.circle(display, c.grey, (int(prev_x), int(prev_y)), 2)

        prev_x, prev_y = x, y

        pg.draw.circle(display, c.black, (int(x), int(y)), 5)
        x += 5

    # explosion
        explosion_tank()

    pg.display.update()
    clock.tick(15)
