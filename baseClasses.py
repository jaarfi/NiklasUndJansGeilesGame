import os, math, time, random, enum
import numpy as np
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

        TextureLocation = "pics/tank/tank_model_1.png"

    class SECOND(enum.Enum):
        RIGHT = pg.K_d
        LEFT = pg.K_a
        DOWN = pg.K_w
        UP = pg.K_s
        CYCLE = pg.K_q
        FIRE = pg.K_e

        TextureLocation = "pics/tank/tank_model_2_1_b.png"

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
        POSTLOCKONACCELERATION = 0

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
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

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

    class SEEKINGMINE(enum.Enum):
        SPEED = 15
        GRAVITY = 0
        DAMAGE = 25
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
        self.gameInstance.collisionObjects.append(self)

    def move(self):
        if self.shellState == shellStates.FLYING:
            oldCoords = self.getCoords()

            if self.seeking:
                seekedPlayer = 0
                distanceToSeekedPlayer = 99999999
                vectorToSeekedPlayer = 0
                for player in self.gameInstance.players:
                    if player != self.tank:
                        vectorToPlayer = (self.getCoords()[0] - player.getCoords()[0], self.getCoords()[1] - player.getCoords()[1])
                        distanceToPlayer = math.sqrt(vectorToPlayer[0]*vectorToPlayer[0]+vectorToPlayer[1]*vectorToPlayer[1])
                        if distanceToPlayer < distanceToSeekedPlayer and distanceToPlayer < self.shellType.value.SEEKDISTANCE.value:
                            seekedPlayer = player
                            vectorToSeekedPlayer = vectorToPlayer
                if seekedPlayer != 0:
                    self.color = Color(222, 23, 56)
                    self.speed = self.shellType.value.POSTLOCKONSPEED.value
                    vectorToSeekedPlayer = self.normalizeVector(vectorToSeekedPlayer)
                    self.changeVectorBy(-vectorToSeekedPlayer[0]*self.shellType.value.POSTLOCKONSPEED.value*0.2,-vectorToSeekedPlayer[1]*self.shellType.value.POSTLOCKONSPEED.value*0.2)
                    self.speed += self.shellType.value.POSTLOCKONACCELERATION.value

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
                if thing.polygon.intersects(self.collisionPolygon) and thing != self and thing != self.tank and not thing in self.tank.shells:
                    thing.hit(self.shellType.value.DAMAGE.value)
                    self.explode()

            if self.remainingFlyingTime > 0:
                self.remainingFlyingTime -= 1
                self.speed -= self.shellType.value.SPEED.value/(self.shellType.value.FLYTIME.value*60)

            if self.speed <= 0:
                self.changeVectorTo((0,0))
                if not self.shellType.value.SEEKING.value:
                    self.safedelete()

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
        if self in self.gameInstance.collisionObjects:
            self.gameInstance.collisionObjects.remove(self)

    def startSeeking(self):
        if self.shellType.value.SEEKING.value:
            self.gravity = self.shellType.value.SEEKINGGRAVITY.value
            self.seeking = True

class Game(object):
    def __init__(self, width, heigth, display, font):
        self.width = width
        self.heigth = heigth
        self.display = display
        self.clock = pg.time.Clock()
        self.fps = 60
        self.font = font
        self.players = []
        self.players.append(Tank(self,1))
        self.players.append(Tank(self,2))
        self.drawableObjects = []
        self.collisionObjects = []
        self.map = 0


    def startGame(self):
        self.map = Map(Polygon(self.createMap(self.width, self.heigth)),self)
        self.collisionObjects.append(self.map)
        for player in self.players:
            player.move(self.map)
            self.collisionObjects.append(player)
        for thing in self.collisionObjects:
            self.drawableObjects.append(thing)
        while True:
            self.players[0].move(self.map)
            for player in self.players:
                pass
                #player.move(self.map)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    quit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        Menu.pause_menu()
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
    def __init__(self, gameinstance, playernumber):
        color = pg.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        super().__init__(Polygon([(2,38),(21,57),(87,58),(103,45),(103,15),(76,17),(76,0),(34,0),(35,16),(18,16)]),gameinstance,[0,0],0, color)
        self.angle = -45
        self.firingVector = [math.cos(math.radians(self.angle))*100, math.sin(math.radians(self.angle))*100]
        self.shells = []
        self.timeToLoad = 0
        self.currentlySelectedShell = shellTypes.NORMAL
        self.life = 100
        self.groundedCorner = 1
        self.texture = pg.image.load("pics/tank/tank_model_1.png")
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.cannonTexture = pg.image.load("pics/tank/tank_model_1_w1.png")
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.keydown = False
        if playernumber == 1:
            self.config = playerControls.FIRST
        else:
            self.config = playerControls.SECOND

    def move(self, map):
        key = pg.key.get_pressed()
        if key[self.config.value.LEFT.value]:
            self.changeVectorBy(-0.02, 0)
            self.speed = 3
            self.groundedCorner = 2
        elif key[self.config.value.RIGHT.value]:
            self.changeVectorBy(0.02, 0)
            self.speed = 3
            self.groundedCorner = 1
        if key[self.config.value.UP.value]:
            self.angle += 1
        if key[self.config.value.DOWN.value]:
            self.angle -= 1
        if key[self.config.value.CYCLE.value]:
            self.keydown = True
        elif self.keydown:
            self.keydown = False
            self.currentlySelectedShell = self.currentlySelectedShell.next()
        if key[self.config.value.FIRE.value]:
            self.fireShell()
        if self.physicsMoveNewPolygon().exterior.coords[1][0] > 1 and self.physicsMoveNewPolygon().exterior.coords[2][0] < self.gameInstance.width -1:
            self.physicsMove()
        for shell in self.shells:
            shell.move()
        self.rotateToGround(map, self.groundedCorner)
        self.firingVector = [math.cos(math.radians(self.angle))*100, math.sin(math.radians(self.angle))*100]
        self.changeVectorTo([0,0])
        self.speed = 0
        if self.timeToLoad > 0:
            self.timeToLoad -= 1

    def fireShell(self):
        if self.timeToLoad <= 0:
            tmpCoords = self.getCoords()
            if self.currentlySelectedShell.value.NUMBEROFSHELLS.value > 1:
                self.angle -= self.currentlySelectedShell.value.SPREAD.value/2
                for i in range(0,self.currentlySelectedShell.value.NUMBEROFSHELLS.value):
                    self.angle += self.currentlySelectedShell.value.SPREAD.value/(self.currentlySelectedShell.value.NUMBEROFSHELLS.value-1)
                    self.firingVector = [math.cos(math.radians(self.angle))*100, math.sin(math.radians(self.angle))*100]
                    shellPolygon = Polygon([(tmpCoords[0], tmpCoords[1]+5), (tmpCoords[0]+5, tmpCoords[1]+5),(tmpCoords[0]+5, tmpCoords[1]),(tmpCoords[0], tmpCoords[1])])
                    self.shells.append(Shell(shellPolygon, self.gameInstance, self.firingVector, self.currentlySelectedShell, self))
                self.angle -= self.currentlySelectedShell.value.SPREAD.value/2
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
        tmpCoords = (int(self.getCoords()[0]), int(self.getCoords()[1]))
        #super().draw(display)
        pg.draw.line(display, self.color, (tmpCoords[0], tmpCoords[1]+50), (tmpCoords[0]+self.life, tmpCoords[1]+50), 10) #Die Hp Anzeige zeichnen
        pg.draw.line(display, self.color, (tmpCoords[0]-50, tmpCoords[1]), (tmpCoords[0]-50, tmpCoords[1]+self.timeToLoad), 10) #Die Hp Anzeige zeichnen
        #pg.draw.line(display, self.color, (tmpCoords[0], tmpCoords[1]), (tmpCoords[0]+self.firingVector[0], tmpCoords[1]+self.firingVector[1]), 1) #Die Hp Anzeige zeichnen
        for shell in self.shells:
            shell.draw(display)

        pos = (self.getCoords()[0] - (self.cannonTexture.get_width() / 2),
               self.getCoords()[1] - (self.cannonTexture.get_height() / 2))
        display.blit(self.cannonTexture,pos)
        pos = (self.getCoords()[0] - (self.texture.get_width() / 2),
               self.getCoords()[1] - (self.texture.get_height() / 2))
        display.blit(self.texture,pos)

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

        self.texture = pg.image.load(self.config.value.TextureLocation.value)
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.texture = pg.transform.rotate(self.texture, -self.rotation)
        self.cannonTexture = pg.image.load("pics/tank/tank_model_1_w1.png")
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -self.angle)
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -180)
