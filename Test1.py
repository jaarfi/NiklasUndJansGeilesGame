import os, math, time, random
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon


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
        self.shellInAir = False
        self.rect = pg.Rect(32, 32, 16, 16)
        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]
        self.angle = 45
        self.shell = Shell()

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
        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]

    def getCoords(self):
        return (self.rect.x,self.rect.y)

    def fireShell(self):
        self.shellInAir = True

    def shellFiring(self, frame):
        if frame == 60:
            self.shellInAir = False
        if self.shellInAir:
            explosion_tank(self.getCoords(), frame)

    def draw(self, display):
        pg.draw.rect(display, (255, 200, 0), player.rect)
        if self.shellInAir:
            self.shell.draw(display)
        else:
            pg.draw.line(display, (255, 50, 0), player.getCoords(), (player.getCoords()[0]+int(math.sin(-self.angle)*150), player.getCoords()[1]+int(math.cos(-self.angle)*150)))
        print(player.getCoords()[0]+int(math.sin(self.angle)/50), player.getCoords()[1]+int(math.cos(self.angle)/50))

class Shell(object):
    def __init__(self):
        self.rect = pg.Rect(32, 32, 16, 16)
        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]
        self.directionVector = (0,0)

    def draw(self,display):
        pg.draw.rect(display, (155, 100, 0), player.rect)



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
    map.append((int(i * width/spacing), random.randint(int(height/2), int(height*4/6))))
  map.append((width, height))
  return map

beta = 65
v_0 = 75


def parabola(beth, v0, x_value):
    y_value = -math.tan(math.radians(beth)) * x_value + (9.81 * x_value ** 2) / (
            2 * (v0 * 100) * (math.cos(math.radians(beth)) ** 2)) + 500
    return int(y_value)


# _________________________________________________
# sprite preparation
only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]

expl = []

for myfile in only_files:
    if "Explosion" in myfile:
        expl.append(pg.image.load("sprites/" + myfile))

expl_sound = pg.mixer.Sound("sound/läsch_explosion.wav")


def explosion_tank(coords, frame):
    global dead
    dead = False
    expl_sound.play()
    #clock.tick(1)
    display.blit(expl[int(frame/8)], (coords[0] - 140, coords[1] - 140))



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
frameCounterForAnimations = 0

# Spielschleife
while True:

    if frameCounterForAnimations == 60:
        frameCounterForAnimations = 0
    else:
        frameCounterForAnimations += 1

    key = pg.key.get_pressed()
    if key[pg.K_LEFT] and player.getCoords()[0] > 2:
        player.move(-2, 0)
    if key[pg.K_RIGHT] and player.getCoords()[0] < displaywidth - 18:
        player.move(2, 0)
    if key[pg.K_UP] :
        player.angle = player.angle - 0.1
    if key[pg.K_DOWN] :
        player.angle = player.angle + 0.1
    player.move(0, 200)
    if key[pg.K_SPACE] and not player.shellInAir:
        player.fireShell()
        frameCounterForAnimations = 0

    while Polygon(map.polygon).intersects(Polygon(player.polygon)):
        player.move(0, -1)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            quit()

    display.fill((0, 0, 0))
    map.draw(display)
    player.draw(display)


    player.shellFiring(frameCounterForAnimations)
    '''
    if angle == 359:
        angle = 0
        bs_image = pg.transform.rotate(b_s_image, angle)
    else:
        bs_image = pg.transform.rotate(b_s_image, angle)
        angle += 1
    display.blit(bs_image, bullet)

    y = parabola(beta, v_0, x) + 20
    ''
    # ____________line zeichnen__________
    if first:
        first = False
        prev_x, prev_y = x, y
        continue
    '''

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



