import math, enum
import pygame as pg
from shapely import affinity
import random
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, Point, LineString
from pygame.locals import *
import Menu

class shellStates(enum.Enum):
    IDLE = 1
    FLYING = 2
    EXPLODING = 3

class playerControls(enum.Enum):

    class FIRST(enum.Enum):
        RIGHT = pg.K_RIGHT
        LEFT = pg.K_LEFT
        DOWN = pg.K_DOWN
        UP = pg.K_UP
        CYCLE = pg.K_PERIOD
        FIRE = pg.K_COMMA

        TextureLocation = "pics/tank/tank_1_b.png"
        WeaponLocation = "pics/tank/wapon_1_b.png"
        Color = pg.Color(32, 137, 235)

    class SECOND(enum.Enum):
        RIGHT = pg.K_d
        LEFT = pg.K_a
        DOWN = pg.K_w
        UP = pg.K_s
        CYCLE = pg.K_q
        FIRE = pg.K_e

        TextureLocation = "pics/tank/tank_1_g.png"
        WeaponLocation = "pics/tank/wapon_1_g.png"
        Color = pg.Color(164,226,68)

class shellTypes(enum.Enum):

    class NORMAL(enum.Enum):
        SPEED = 30
        GRAVITY = 0.05
        DAMAGE = 15
        RELOAD = 2
        SIZE = 5

        SEEKING = False
        NAME = "Normal Shell"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED = 0
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = "pics/sprites/Medium_Shell.png"

        EXPLOSIONSIZE = 0.7
        EXPLOSIONTIME = 1

    class SNIPER(enum.Enum):
        SPEED = 100
        GRAVITY = 0
        DAMAGE = 49
        RELOAD = 5
        SIZE = 7

        SEEKING = False
        NAME = "Sniper Gun"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED= 0
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = "pics/sprites/Sniper_Shell.png"

        EXPLOSIONSIZE = 1
        EXPLOSIONTIME = 1

    class MACHINEGUN(enum.Enum):
        SPEED = 100
        GRAVITY = 0
        DAMAGE = 3
        RELOAD = 0.02
        SIZE = 2

        SEEKING = False
        NAME = "Machine Gun"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED= 0
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = "pics/sprites/Light_Shell.png"

        EXPLOSIONSIZE = 0.2
        EXPLOSIONTIME = 0.5

    class GRAVITRONROCKET(enum.Enum):
        SPEED = 10
        GRAVITY = 0.05
        DAMAGE = 12
        RELOAD = 1
        SIZE = 10

        SEEKING = True
        NAME = "Gravitron Rocket"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0.5
        SEEKDISTANCE = 1500
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED = 10
        POSTLOCKONACCELERATION = 1

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = "pics/sprites/Heavy_Shell.png"

        EXPLOSIONSIZE = 0.8
        EXPLOSIONTIME = 1

    class SEEKINGMINE(enum.Enum):
        SPEED = 15
        GRAVITY = 0
        DAMAGE = 11
        RELOAD = 3
        SIZE = 10
        SEEKING = True
        NAME = "Skymine"

        FLYTIME = 1
        TIMETILLSEEK = 1
        SEEKDISTANCE = 200
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED = 20
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = "pics/sprites/Granade_Shell.png"

        EXPLOSIONSIZE = 0.7
        EXPLOSIONTIME = 1

    class SHOTGUN(enum.Enum):
        SPEED = 30
        GRAVITY = 0.05
        DAMAGE = 3
        RELOAD = 2
        SIZE = 2

        SEEKING = False
        NAME = "Shotgun Shell"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        POSTLOCKONSPEED = 0

        NUMBEROFSHELLS = 5
        SPREAD = 10

        textureLocation = "pics/sprites/Granade_Shell.png"

        EXPLOSIONSIZE = 0.7
        EXPLOSIONTIME = 1

    class FLAK(enum.Enum):
        SPEED = 30
        GRAVITY = 0
        DAMAGE = 0
        RELOAD = 2
        SIZE = 2

        SEEKING = False
        NAME = "Flak"
        FLYTIME = 0.3
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        POSTLOCKONSPEED = 0

        NUMBEROFSHELLS = 10
        SPREAD = 45

        textureLocation = "pics/sprites/Light_Shell.png"

        EXPLOSIONSIZE = 0.2
        EXPLOSIONTIME = 0.2


    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]

class DrawableObject(object):
    def __init__(self, polygon, gameinstance, color=pg.Color(0,0,0)):
        self.gameInstance = gameinstance
        self.polygon = polygon
        self.internalFrame = 0
        self.color = color
        self.rotation = 0

    def draw(self, display):
        pg.gfxdraw.filled_polygon(display, self.polygon.exterior.coords, self.color)

    def advanceFrameCounter(self, numberofframes=1):
        self.internalFrame += numberofframes

    def resetFrameCounter(self):
        self.internalFrame = 0

    def getCoords(self):
        return int(list(self.polygon.centroid.coords)[0][0]), int(list(self.polygon.centroid.coords)[0][1])

    def moveTo(self, coords):
        coordsDifference = (coords[0] - self.getCoords()[0], coords[1]- self.getCoords()[1])
        self.polygon = affinity.translate(self.polygon, coordsDifference[0], coordsDifference[1])

    def moveBy(self, dx, dy):
        self.polygon = affinity.translate(self.polygon, dx, dy)

    def rotateTo(self, degree, corner):
        degreediff = degree - self.rotation
        self.rotateBy(degreediff, corner)

    def rotateBy(self, degree, corner):
        self.polygon = affinity.rotate(self.polygon,degree, self.polygon.exterior.coords[corner])
        self.rotation += degree
        if self.rotation > 360:
            self.rotation -= 360
        if self.rotation < 0:
            self.rotation += 360

class CollisionObject(DrawableObject):
    def colliding(self, PhysicsObject):
        return self.polygon.intersects(PhysicsObject.polygon)

    def hit(self, dmg):
        pass

class MovablePhysicsObject(CollisionObject):
    def __init__(self, polygon, gameinstance, directionalvector, speed, color=pg.Color(0,0,0)):
        super().__init__(polygon,gameinstance,color)
        self._normalizedDirectionalVector = directionalvector
        self._normalizeVector()
        self.speed = speed

    def normalizeVector(self, vector):
        vectorLength = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        if vectorLength:
            vector = [vector[0]/vectorLength, vector[1]/vectorLength]
        return vector

    def _normalizeVector(self):
        self._normalizedDirectionalVector = self.normalizeVector(self._normalizedDirectionalVector)

    def changeVectorTo(self, vector):
        self._normalizedDirectionalVector = [vector[0], vector[1]]
        self._normalizeVector()

    def changeVectorBy(self, dx, dy):
        self._normalizedDirectionalVector = [self._normalizedDirectionalVector[0] + dx, self._normalizedDirectionalVector[1] + dy]
        self._normalizeVector()

    def physicsMoveNewPolygon(self):
        denormalizedVector = [self._normalizedDirectionalVector[0]*self.speed, self._normalizedDirectionalVector[1]*self.speed]
        return affinity.translate(self.polygon, denormalizedVector[0], denormalizedVector[1])

    def physicsMove(self):
        denormalizedVector = [self._normalizedDirectionalVector[0]*self.speed, self._normalizedDirectionalVector[1]*self.speed]
        self.polygon = affinity.translate(self.polygon, denormalizedVector[0], denormalizedVector[1])

