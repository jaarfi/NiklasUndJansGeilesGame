import os, math, time, random
from os import listdir
from os.path import isfile, join

import pygame as pg
import pygame.gfxdraw
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




class Tank(object):

    '''
    Mock
    '''

    def __init__(self):
        self.rect = pg.Rect(32, 32, 16, 16)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

    def getCoords(self):
        return (self.rect.x,self.rect.y)


class Map(object):

    '''
    Placeholder
    '''
    def __init__(self):
        self.polygon = createMap(displaywidth,displayheigth)

    def draw(self,display):
        pg.gfxdraw.filled_polygon(display, map.polygon, (255, 255, 255))




def createMap(width,height):
  '''
  Placeholder
  :param width: Die Breite der Map die herzustellen ist
  :param height: Die Höhe der Map die herzustellen ist
  :return: ein Array aus Tupeln, die den Koordinaten des Polygons der Map entsprechen
  '''
  map = [(0,height)]
  spacing = 10
  for i in range(0,spacing+1):
    map.append((int(i * width/spacing), random.randint(int(height/3), int(height*2/3))))
  map.append((width, height))
  return map

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


def explosion_tank(coords):
    global dead
    dead = False
    #expl_sound.play()
    #clock.tick(1)
    for i in range(8):
        map.draw(display)
        display.blit(expl[i], (coords[0] - 140, coords[1] - 140))

        clock.tick(10)
        pg.display.update()

    map.draw(display)


# __________________________________________________


bullet = pg.Rect(300, 100, 80, 80)
b_image = pg.image.load("pics/Heavy_Shell.png")
b_s_image = pg.transform.scale(b_image, (80, 80))


def rotate():
    pass


# ___________________________________________________


prev_x, prev_y = 0, 0
first = True
dead = True
x = 0
angle = 0

map = Map()
player = Tank()

# Spielschleife
while True:

    key = pg.key.get_pressed()
    if key[pg.K_LEFT]:
        player.move(-2, 0)
    if key[pg.K_RIGHT]:
        player.move(2, 0)
    if key[pg.K_SPACE]:
        explosion_tank(player.getCoords())

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            quit()

    display.fill((0, 0, 0))
    map.draw(display)
    pg.draw.rect(display, (255, 200, 0), player.rect)

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


    pg.display.flip()
    clock.tick(60)
'''
    if y < 500 or x < 100:
        pg.draw.circle(display, c.cyan, (int(prev_x), int(prev_y)), 5)

        if int(x) % 15 == 0:
            pg.draw.circle(display, c.grey, (int(prev_x), int(prev_y)), 2)

        prev_x, prev_y = x, y

        pg.draw.circle(display, c.black, (int(x), int(y)), 5)
        x += 5

    # explosion
        explosion_tank()
'''



