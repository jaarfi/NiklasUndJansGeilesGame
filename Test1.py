import os, math, time, random, enum
import numpy as np
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


class shellStates(enum.Enum):
    IDLE = 1
    FLYING = 2
    EXPLODING = 3

class colors(enum.Enum):
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    cyan = (0, 255, 255)
    khaki = (255, 246, 143)
    grey = (127, 127, 127)

    light_grey = (200, 200, 200)

    dark_grey = (50, 50, 50)
    dark_orange = (255, 140, 0)

    springgreen = (0, 255, 127)

class Tank(object):

    '''
    Mock
    '''

    def __init__(self):
        self.shellInAir = False
        self.rect = pg.Rect(32, 32, 50, 30)
        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]
        self.angle = 45
        self.shootingVector = (int(math.sin(-self.angle)*150), int(math.cos(-self.angle)*150))
        self.shell = Shell()
        self.life = 100
        self.color =  list(np.random.random(3) * 256)

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
        self.shootingVector = (int(math.sin(-self.angle)*150), int(math.cos(-self.angle)*150))

    def getCoords(self):
        return (self.rect.x,self.rect.y)

    def fireShell(self):
        if self.shell.state == shellStates.IDLE:
            self.shell.fireShell(self.shootingVector, self.getCoords())

    def firingAnimation(self, listOfObjects, frame):
        listCopy = list.copy(listOfObjects)
        listCopy.remove(self)
        self.shell.collisionCheck(listCopy)
        if self.shell.state == shellStates.FLYING:
            pass

    def hit(self):
        self.life = self.life-20

    def draw(self, display):
        print(self,self.rect)
        pg.draw.rect(display, self.color, self.rect)
        pg.draw.line(display, self.color, (self.rect.x, self.rect.y-10), (self.rect.x+self.life, self.rect.y-10))
        self.shell.draw(display)
        if self.shell.state == shellStates.IDLE:
            pg.draw.line(display, (255, 50, 0), (self.rect.x, self.rect.y),(self.rect.x+self.shootingVector[0], self.rect.y+self.shootingVector[1]))

class Shell(object):
    def __init__(self):
        self.rect = pg.Rect(-1, -1, 0, 0)
        self.polygon = [(-1,-1),(-1,-2),(-2,-1)]        #store out of bounds
        self.directionVector = (0, 0)
        self.state = shellStates.IDLE
        self.explodeFrameCounter = 0

    def draw(self,display):
        self.move()
        if (self.state == shellStates.FLYING):
            pg.draw.rect(display, (155, 100, 0), self.rect)
        elif (self.state == shellStates.EXPLODING):
            self.explodeFrameCounter = self.explodeFrameCounter + 1
            if explosion_tank(self.rect.center,self.explodeFrameCounter):
                self.state = shellStates.IDLE
                self.move((-1,-1))
                self.explodeFrameCounter = 0

    def move(self, coords=(0, 0)):
        if self.state == shellStates.FLYING:
            if coords == (0,0):
                self.rect.x = self.rect.x + int(self.directionVector[0]/15)
                self.rect.y = self.rect.y + int(self.directionVector[1]/15)
                self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]
                self.directionVector = (self.directionVector[0],self.directionVector[1] + 5)
        elif coords != (0,0):
            self.rect.x = coords[0]
            self.rect.y = coords[1]
            self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]

        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]

    def collisionCheck(self, listOfObjects):
        if self.state == shellStates.FLYING:
            for collision in listOfObjects:
                if Polygon(self.polygon).intersects(Polygon(collision.polygon)):
                    self.dy = -4
                    self.state=shellStates.EXPLODING
                    collision.hit()

    def fireShell(self, shootingVector, startpoint):
        self.directionVector = shootingVector
        self.rect = pg.Rect(startpoint[0], startpoint[1], 10, 10)
        self.state = shellStates.FLYING
        self.polygon = [self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright]



class Map(object):

    '''
    Placeholder
    '''
    def __init__(self):
        self.polygon = createMap(displaywidth,displayheigth)

    def draw(self,display):
        pg.gfxdraw.filled_polygon(display, map.polygon, (255, 255, 255))

    def hit(self):
        pass


def drawAllObjects(arrayOfObjects, display):
    for toDraw in arrayOfObjects:
        toDraw.draw(display)

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
    #expl_sound.play()
    #clock.tick(1)
    print(frame)
    if len(expl)==int(frame/len(expl)):
        return True
    display.blit(expl[int(frame/len(expl))], (coords[0] - 140, coords[1] - 140))
    return False



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
players = []
players.append(Tank())
players[0].move(100,100)
players.append(Tank())
print(players[0]==players[1])
listOfObjects = []
listOfObjects.append(map)
for player in players:
    listOfObjects.append(player)
frameCounterForAnimations = 0

# Spielschleife
while True:

    if frameCounterForAnimations == 60:
        frameCounterForAnimations = 0
    else:
        frameCounterForAnimations += 1

    key = pg.key.get_pressed()
    if key[pg.K_LEFT] and players[0].getCoords()[0] > 2:
        players[0].move(-2, 0)
    if key[pg.K_RIGHT] and players[0].getCoords()[0] < displaywidth - 18:
        players[0].move(2, 0)
    if key[pg.K_UP] :
        players[0].angle = players[0].angle - 0.025
    if key[pg.K_DOWN] :
        players[0].angle = players[0].angle + 0.025
    if key[pg.K_SPACE] and players[0].shell.state == shellStates.IDLE:
        players[0].fireShell()
        frameCounterForAnimations = 0

    players[0].move(0, 100)
    players[1].move(0, 100)
    while Polygon(map.polygon).intersects(Polygon(players[0].polygon)):
        players[0].move(0, -1)
    while Polygon(map.polygon).intersects(Polygon(players[1].polygon)):
        players[1].move(0, -1)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            quit()

    display.fill((0, 0, 0))
    drawAllObjects(listOfObjects, display)
    print("\n")

    players[0].firingAnimation(listOfObjects, frameCounterForAnimations)
    players[1].firingAnimation(listOfObjects, frameCounterForAnimations)
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



