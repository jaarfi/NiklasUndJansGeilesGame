import os, math, time, random, enum
import numpy as np
import pygame as pg
from shapely import affinity
import random
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, Point, LineString
from pygame.locals import *

class shellStates(enum.Enum):
    IDLE = 1
    FLYING = 2
    EXPLODING = 3

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

        NUMBEROFSHELLS = 1
        SPREAD = 0

    class LASER(enum.Enum):
        SPEED = 100
        GRAVITY = 0
        DAMAGE = 50
        RELOAD = 5
        SIZE = 7

        SEEKING = False
        NAME = "Laser Gun"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0
        SEEKDISTANCE = 0
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED= 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

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

        NUMBEROFSHELLS = 1
        SPREAD = 0

    class SEEKINGROCKET(enum.Enum):
        SPEED = 10
        GRAVITY = 0.05
        DAMAGE = 12
        RELOAD = 1
        SIZE = 10

        SEEKING = True
        NAME = "Seeking Rocket"
        FLYTIME = float("inf")
        TIMETILLSEEK = 0.5
        SEEKDISTANCE = 15
        SEEKINGGRAVITY = 10
        POSTLOCKONSPEED= 10

        NUMBEROFSHELLS = 1
        SPREAD = 0

    class SEEKINGMINE(enum.Enum):
        SPEED = 4
        GRAVITY = 0
        DAMAGE = 25
        RELOAD = 0.1
        SIZE = 10
        SEEKING = True
        NAME = "Skymine"

        FLYTIME = 1
        TIMETILLSEEK = 1
        SEEKDISTANCE = 100
        SEEKINGGRAVITY = 0
        POSTLOCKONSPEED = 3

        NUMBEROFSHELLS = 1
        SPREAD = 0

    #class SHOTGUN(enum.Enum):
        #SPEED = 30
        #GRAVITY = 0.05
        #DAMAGE = 3
        #RELOAD = 2
        #SIZE = 2

        #SEEKING = False
        #NAME = "Shotgun Shell"
        #FLYTIME = float("inf")
        #TIMETILLSEEK = 0
        #SEEKDISTANCE = 0
        #POSTLOCKONSPEED = 0

        #NUMBEROFSHELLS = 5
        #SPREAD = 10


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

class Map(CollisionObject):
    def __init__(self, polygon, gameinstance):
        color = pg.Color(35,133,85)
        super().__init__(polygon, gameinstance, color)

only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]
expl = []
for myfile in only_files:
    if "Explosion" in myfile:
        expl.append(pg.image.load("sprites/" + myfile))

class Explosion(CollisionObject):
    def draw(self, display):
        if len(expl) == int(self.internalFrame / len(expl)):
            return True
        display.blit(expl[int(self.internalFrame / len(expl))], (self.getCoords()[0] - 140, self.getCoords()[1] - 140))
        self.advanceFrameCounter()
        return False




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

class Shell(MovablePhysicsObject):
    def __init__(self, polygon,gameinstance,vector,shellType, tank):
        color = pg.Color(255,255,255)
        self.shellType = shellType
        self.shellState = shellStates.FLYING
        self.collisionPolygon = polygon
        super().__init__(polygon, gameinstance, vector, self.shellType.value.SPEED.value,color)
        self.remainingFlyingTime = self.shellType.value.FLYTIME.value * 60
        self.remainingTimeTillSeek = self.shellType.value.TIMETILLSEEK.value * 60
        self.gravity = self.shellType.value.GRAVITY.value
        self.seeking = False
        self.tank = tank
        self.explosion = 0

    def move(self):
        if self.shellState == shellStates.FLYING:
            oldCoords = self.getCoords()

            if self.seeking:
                seekedPlayer = 0
                distanceToSeekedPlayer = 99999999
                vectorToSeekedPlayer = 0
                for player in self.gameInstance.players:
                    vectorToPlayer = (self.getCoords()[0] - player.getCoords()[0], self.getCoords()[1] - player.getCoords()[1])
                    distanceToPlayer = math.sqrt(vectorToPlayer[0]*vectorToPlayer[0]+vectorToPlayer[1]*vectorToPlayer[1])
                    if distanceToPlayer < distanceToSeekedPlayer and distanceToPlayer < self.shellType.value.SEEKDISTANCE.value and player != self.tank:
                        seekedPlayer = player
                        vectorToSeekedPlayer = vectorToPlayer
                if seekedPlayer != 0:
                    self.color = Color(222, 23, 56)
                    self.speed = self.shellType.value.POSTLOCKONSPEED.value
                    vectorToSeekedPlayer = self.normalizeVector(vectorToSeekedPlayer)
                    self.changeVectorBy(-vectorToSeekedPlayer[0]*self.shellType.value.SPEED.value*0.004,-vectorToSeekedPlayer[1]*self.shellType.value.SPEED.value*0.004)

            self.physicsMove()
            self.changeVectorBy(0, self.gravity)
            newCoords = self.getCoords()
            if newCoords[0] > self.gameInstance.width or newCoords[0] < 0:
                self.safedelete()
            self.collisionPolygon = Polygon([
                (oldCoords[0],oldCoords[1]),
                (oldCoords[0]+self.shellType.value.SIZE.value, oldCoords[1]+self.shellType.value.SIZE.value),
                (newCoords[0]+self.shellType.value.SIZE.value, newCoords[1]+self.shellType.value.SIZE.value),
                (newCoords[0], newCoords[1])])

            for thing in self.gameInstance.collisionObjects:
                if thing.polygon.intersects(self.collisionPolygon) and thing != self and thing != self.tank:
                    thing.hit(self.shellType.value.DAMAGE.value)
                    self.explode()

            if self.remainingFlyingTime > 0:
                self.remainingFlyingTime -= 1
                self.speed -= self.shellType.value.SPEED.value/(self.shellType.value.FLYTIME.value*60)

            if self.speed <= 0:
                self.changeVectorTo((0,0))

            if self.remainingTimeTillSeek > 0:
                self.remainingTimeTillSeek -= 1

            if self.remainingTimeTillSeek <= 0:
                self.startSeeking()

    def draw(self, display):
        if self.shellState == shellStates.FLYING:
            pg.gfxdraw.filled_polygon(display, self.collisionPolygon.exterior.coords, self.color)
        if self.shellState == shellStates.EXPLODING:
            if self.explosion.draw(display):
                self.safedelete()


    def explode(self):
        self.explosion = Explosion(self.polygon, self.gameInstance)
        self.shellState = shellStates. EXPLODING

    def safedelete(self):
        if self in self.tank.shells:
            self.tank.shells.remove(self)

    def startSeeking(self):
        if self.shellType.value.SEEKING.value:
            self.gravity = self.shellType.value.SEEKINGGRAVITY.value

class Game(object):
    def __init__(self, width, heigth, display, font):
        self.width = width
        self.heigth = heigth
        self.display = display
        self.clock = pg.time.Clock()
        self.fps = 60
        self.font = font
        self.map = Map(Polygon(self.createMap(self.width, self.heigth)),self)
        self.players = []
        self.players.append(Tank(self))
        self.players.append(Tank(self))
        self.drawableObjects = []
        self.collisionObjects = []
        self.collisionObjects.append(self.map)
        for player in self.players:
            player.move(self.map)
            self.collisionObjects.append(player)
        for thing in self.collisionObjects:
            self.drawableObjects.append(thing)


    def startGame(self):
        while True:
            self.players[0].move(self.map)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    quit()
            self.display.fill((0, 0, 0))

            for toDraw in self.drawableObjects:
                toDraw.draw(self.display)

            pg.display.flip()
            self.clock.tick(self.fps)

    def createMap(self, width, height):
        map = [(0, height)]
        spacing = 4
        newpoint = (0,random.randint(int(height / 2),int(height * 4 / 6)))
        for i in range(0, spacing + 1):
            newpoint = (int(i * width / spacing), newpoint[1] + random.randint(-50, 50))
            while int(height / 2) < newpoint[1] < int(height * 4 / 6):
                newpoint = (int(i * width / spacing), newpoint[1] + random.randint(-50, 50))
            map.append(newpoint)
        map.append((width, height))
        return map


class Tank(MovablePhysicsObject):
    def __init__(self, gameinstance):
        color = pg.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        super().__init__(Polygon([(32,32), (32,62), (102,62), (102,32)]),gameinstance,[0,0],0, color)
        self.angle = 45
        tmpCoords = self.getCoords()
        self.firingVector = [math.cos(self.angle)*100, math.sin(self.angle)*100]
        self.shells = []
        self.mapLayer = Polygon([(32,32), (32,62), (102,62), (102,32)])
        self.timeToLoad = 0
        self.currentlySelectedShell = shellTypes.NORMAL
        self.life = 100
        self.groundedCorner = 1

    def move(self, map):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.changeVectorBy(-0.02, 0)
            self.speed = 3
            self.groundedCorner = 2
        elif key[pg.K_RIGHT]:
            self.changeVectorBy(0.02, 0)
            self.speed = 3
            self.groundedCorner = 1
        if key[pg.K_UP]:
            self.angle += 0.025
        if key[pg.K_DOWN]:
            self.angle -= 0.025
        for event in pg.event.get():
            if event.type == pg.KEYUP and event.key == pg.K_PERIOD:
                self.currentlySelectedShell = self.currentlySelectedShell.next()
        if key[pg.K_SPACE]:
            self.fireShell()
        if self.physicsMoveNewPolygon().exterior.coords[1][0] > 1 and self.physicsMoveNewPolygon().exterior.coords[2][0] < self.gameInstance.width -1:
            self.physicsMove()
        for shell in self.shells:
            shell.move()
        self.rotateToGround(map, self.groundedCorner)
        self.firingVector = [math.cos(self.angle)*100, math.sin(self.angle)*100]
        self.changeVectorTo([0,0])
        self.speed = 0
        if self.timeToLoad > 0:
            self.timeToLoad -= 1

    def fireShell(self):
        if self.timeToLoad <= 0:
            tmpCoords = self.getCoords()
            if self.currentlySelectedShell.value.NUMBEROFSHELLS.value > 1:
                for i in range(0,self.currentlySelectedShell.value.NUMBEROFSHELLS.value):
                    if i == 0:
                        self.angle -= self.currentlySelectedShell.value.SPREAD.value/2
                    self.angle += self.currentlySelectedShell.value.SPREAD.value*i/(self.currentlySelectedShell.value.NUMBEROFSHELLS.value-1)
                    self.firingVector = [math.cos(self.angle) * 100, math.sin(self.angle) * 100]
                    shellPolygon = Polygon([(tmpCoords[0], tmpCoords[1]+5), (tmpCoords[0]+5, tmpCoords[1]+5),(tmpCoords[0]+5, tmpCoords[1]),(tmpCoords[0], tmpCoords[1])])
                    self.shells.append(Shell(shellPolygon, self.gameInstance, self.firingVector, self.currentlySelectedShell, self))
            else:

                shellPolygon = Polygon([(tmpCoords[0], tmpCoords[1] + 5), (tmpCoords[0] + 5, tmpCoords[1] + 5),
                                        (tmpCoords[0] + 5, tmpCoords[1]), (tmpCoords[0], tmpCoords[1])])
                self.shells.append( Shell(shellPolygon, self.gameInstance, self.firingVector, self.currentlySelectedShell, self))
            self.timeToLoad = self.currentlySelectedShell.value.RELOAD.value * self.gameInstance.fps
        pass

    def firingAnimation(self):
        pass

    def hit(self, dmg):
        self.life = self.life - dmg

    def draw(self, display):
        print(self.angle)
        tmpCoords = (int(self.getCoords()[0]), int(self.getCoords()[1]))
        super().draw(display)
        pg.draw.line(display, self.color, (tmpCoords[0], tmpCoords[1]+50), (tmpCoords[0]+self.life, tmpCoords[1]+50), 10) #Die Hp Anzeige zeichnen
        pg.draw.line(display, self.color, (tmpCoords[0]-50, tmpCoords[1]), (tmpCoords[0]-50, tmpCoords[1]+self.timeToLoad), 10) #Die Hp Anzeige zeichnen
        pg.draw.line(display, self.color, (tmpCoords[0], tmpCoords[1]), (tmpCoords[0]+self.firingVector[0], tmpCoords[1]+self.firingVector[1]), 1) #Die Hp Anzeige zeichnen
        for shell in self.shells:
            shell.draw(display)
        textsurface = self.gameInstance.font.render(self.currentlySelectedShell.value.NAME.value, False, self.color)
        display.blit(textsurface, self.getCoords())

    def rotateToGround(self,map,corner):
        while not map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, 1)
        while map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, -2)
        if corner == 1:
            self.rotateTo(270, corner)
        elif corner == 2:
            self.rotateTo(90, corner)
        while not map.polygon.intersects(LineString([self.polygon.exterior.coords[1],self.polygon.exterior.coords[2]])):
            if corner == 1:
                self.rotateBy(1, corner)
            elif corner == 2:
                self.rotateBy(-1, corner)
        if corner == 1:
            self.rotateBy(-1, corner)
        elif corner == 2:
            self.rotateBy(1, corner)
