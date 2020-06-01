#Drive Sound: "Sound effects obtained from https://www.zapsplat.com"
#Fire Sound: "Sound effects obtained from https://www.zapsplat.com"
#Explosion Sound: "Sound effects obtained from https://www.zapsplat.com"

import json
from classes.Animation import *

with open('config.json', 'r') as c:
    config = json.load(c)


class Shell(MovablePhysicsObject):
    def __init__(self, polygon,gameinstance,vector,shellType, tank):
        color = pg.Color(255, 255, 255)
        self.shellType = shellType
        self.shellState = shellStates.FLYING
        self.collisionPolygon = polygon
        super().__init__(polygon, gameinstance, vector, self.shellType.value.SPEED.value,color)
        self.remainingFlyingTime = self.shellType.value.FLYTIME.value * 60
        self.remainingTimeTillSeek = self.shellType.value.TIMETILLSEEK.value * 60
        self.gravity = self.shellType.value.GRAVITY.value
        self.seeking = False
        self.tank = tank
        self.explosions = []
        self.gameInstance.collisionObjects.append(self)
        self.basetexture = pg.image.load(self.shellType.value.textureLocation.value)
        self.texture = self.basetexture
        self.rotation = math.degrees(math.asin(self._normalizedDirectionalVector[0]))
        self.ex_sound = pg.mixer.Sound(config["sound/explosion.wav"])

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
                    self.color = (222, 23, 56)
                    self.speed = self.shellType.value.POSTLOCKONSPEED.value
                    vectorToSeekedPlayer = self.normalizeVector(vectorToSeekedPlayer)
                    self.changeVectorBy(-vectorToSeekedPlayer[0]*self.shellType.value.POSTLOCKONSPEED.value*0.2, -vectorToSeekedPlayer[1]*self.shellType.value.POSTLOCKONSPEED.value*0.2)
                    self.speed += self.shellType.value.POSTLOCKONACCELERATION.value

            self.physicsMove()
            self.changeVectorBy(0, self.gravity)
            self.rotation = math.degrees(math.asin(self._normalizedDirectionalVector[0]))
            if self._normalizedDirectionalVector[1] > 0:
                self.texture = pg.transform.rotate(self.basetexture, self.rotation)
            else:
                self.texture = pg.transform.rotate(self.basetexture, -self.rotation)
            newCoords = self.getCoords()
            self.collisionPolygon = Polygon([
                (oldCoords[0], oldCoords[1]),
                (oldCoords[0]+self.shellType.value.SIZE.value, oldCoords[1]+self.shellType.value.SIZE.value),
                (newCoords[0]+self.shellType.value.SIZE.value, newCoords[1]+self.shellType.value.SIZE.value),
                (newCoords[0], newCoords[1])])

            for thing in self.gameInstance.collisionObjects:
                if thing.polygon.intersects(self.collisionPolygon) and thing != self and thing != self.tank and not thing in self.tank.shells:
                    thing.hit(self.shellType.value.DAMAGE.value)
                    intersection = self.collisionPolygon.intersection(thing.polygon)
                    self.explode(intersection)


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

            if newCoords[0] > self.gameInstance.width or newCoords[0] < 0 and self.shellState != shellStates.EXPLODING:
                self.safedelete()

    def draw(self, display):
        if self.shellState == shellStates.FLYING:
            #pg.gfxdraw.filled_polygon(display, self.collisionPolygon.exterior.coords, self.color)
            pos = (self.getCoords()[0] - (self.texture.get_width() / 2),
                   self.getCoords()[1] - (self.texture.get_height() / 2))
            display.blit(self.texture, pos)
        if self.shellState == shellStates.EXPLODING:
            delete = False
            for explosion in self.explosions:
                delete = delete or explosion.draw(display)
            if delete:
                self.safedelete()

    def explode(self, poly):
        if Menu.sound_set:
            self.ex_sound.set_volume(0.2)
            self.ex_sound.play()
        self.explosions.append(Animation(poly, self.gameInstance, expl, self.shellType.value.EXPLOSIONTIME.value,
                                         self.shellType.value.EXPLOSIONSIZE.value, self.explosions))
        self.shellState = shellStates.EXPLODING

    def safedelete(self):
        if self in self.tank.shells:
            self.tank.shells.remove(self)
        if self in self.gameInstance.collisionObjects:
            self.gameInstance.collisionObjects.remove(self)

    def startSeeking(self):
        if self.shellType.value.SEEKING.value:
            self.gravity = self.shellType.value.SEEKINGGRAVITY.value
            self.seeking = True


class Tank(MovablePhysicsObject):
    def __init__(self, gameinstance, playernumber):

        if playernumber == 1:
            self.config = playerControls.FIRST
        else:
            self.config = playerControls.SECOND

        color = self.config.value.Color.value
        super().__init__(Polygon([(2,38),(21,57),(87,58),(103,45),(103,15),(76,17),(76,0),(34,0),(35,16),(18,16)]),gameinstance,[0,0],0, color)
        if playernumber == 1:
            startpos = (self.gameInstance.width-50,0)
        else:
            startpos = (50,50)
        self.moveTo(startpos)
        self.angle = -90
        self.firingVector = [math.cos(math.radians(self.angle))*75, math.sin(math.radians(self.angle))*75]
        self.shells = []
        self.timeToLoad = 0
        self.currentlySelectedShell = shellTypes.NORMAL
        self.life = 100
        self.groundedCorner = 1
        self.keydown = False
        self.texture = pg.image.load(self.config.value.TextureLocation.value)
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.cannonTexture = pg.image.load(self.config.value.WeaponLocation.value)
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.animations = []
        self.soundFire = pg.mixer.Sound(config["sound"]["shoot"])
        self.soundDrive = pg.mixer.Sound(config["sound"]["drive"])
        self.drive = False

    def move(self, map):
        self.drive = False
        key = pg.key.get_pressed()
        if key[self.config.value.LEFT.value]:
            self.changeVectorBy(-0.02, 0)
            self.speed = 3
            self.groundedCorner = 2

            if Menu.sound_set:
                self.drive = True

        elif key[self.config.value.RIGHT.value]:
            self.changeVectorBy(0.02, 0)
            self.speed = 3
            self.groundedCorner = 1

            if Menu.sound_set:
               self.drive = True

        if self.drive:
            self.soundDrive.set_volume(0.1)
            self.soundDrive.play(-1)
        else:
            self.soundDrive.stop()

        if key[self.config.value.UP.value]:
            self.angle += 1
        if key[self.config.value.DOWN.value]:
            self.angle -= 1
        if key[self.config.value.CYCLE.value]:
            self.keydown = True
        elif self.keydown:
            self.keydown = False
            if self.timeToLoad <= 0:
                self.currentlySelectedShell = self.currentlySelectedShell.next()
        if self.physicsMoveNewPolygon().exterior.coords[1][0] > 1 and self.physicsMoveNewPolygon().exterior.coords[2][0] < self.gameInstance.width -1:
            self.physicsMove()
        for shell in self.shells:
            shell.move()
        self.firingVector = [math.cos(math.radians(self.angle))*75, math.sin(math.radians(self.angle))*75]
        self.rotateToGround(map, self.groundedCorner,self.speed)
        self.changeVectorTo([0, 0])
        self.speed = 0
        if key[self.config.value.FIRE.value]:
            self.fireShell()
        if self.timeToLoad > 0:
            self.timeToLoad -= 1

    def fireShell(self):
        if self.timeToLoad <= 0:
            tmpCoords = self.getCoords()
            if Menu.sound_set:
                self.soundFire.set_volume(0.4)
                self.soundFire.play()

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


    def hit(self, dmg):
        self.life = self.life - dmg

    def draw(self, display):
        tmpCoords = (int(self.getCoords()[0]), int(self.getCoords()[1]))
        #super().draw(display)

        if self.config == playerControls.FIRST:
            pg.draw.line(display, self.color, (self.gameInstance.width - 250, self.gameInstance.height - 30),(self.gameInstance.width - 250 + self.life * 2, self.gameInstance.height - 30), 30)  # Die Hp Anzeige zeichnen
        else:
            pg.draw.line(display, self.color, (50, self.gameInstance.height - 30),(50 +self.life * 2, self.gameInstance.height - 30), 30)  # Die Hp Anzeige zeichnen
        for shell in self.shells:
            shell.draw(display)

        for animation in self.animations:
            animation.draw(display)

        pos = (self.getCoords()[0] - (self.cannonTexture.get_width() / 2),
               self.getCoords()[1] - (self.cannonTexture.get_height() / 2))

        display.blit(self.cannonTexture,pos)
        pos = (self.getCoords()[0] - (self.texture.get_width() / 2),
               self.getCoords()[1] - (self.texture.get_height() / 2))
        display.blit(self.texture,pos)

        textsurface = self.gameInstance.font.render(self.currentlySelectedShell.value.NAME.value, False, self.color)
        if self.config == playerControls.FIRST:
            display.blit(textsurface, (self.gameInstance.width - 250, self.gameInstance.height - 90))
            textsurface = self.gameInstance.font.render(str(self.timeToLoad/self.gameInstance.fps)[:4], False, self.color)
            display.blit(textsurface, (self.gameInstance.width - 250, self.gameInstance.height - 120))
        else:
            display.blit(textsurface, (50, self.gameInstance.height - 90))
            textsurface = self.gameInstance.font.render(str(self.timeToLoad/self.gameInstance.fps)[:4], False, self.color)
            display.blit(textsurface, (50, self.gameInstance.height - 120))
        self.advanceFrameCounter()


    def rotateToGround(self,map,corner,moved):
        while not map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, 1)
        while map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, -2)

        if moved and not self.internalFrame % (self.gameInstance.fps/15):
            tempdust = []
            for i in range(len(dust)):
                tempdust.append(pg.transform.rotate(dust[i], self.rotation))
            self.animations.append(Animation(Polygon([self.polygon.exterior.coords[corner],self.polygon.exterior.coords[corner],self.polygon.exterior.coords[corner]]), self.gameInstance, tempdust,3/15, 1, self.animations))


        while not map.polygon.intersects(LineString([self.polygon.exterior.coords[1],self.polygon.exterior.coords[2]])):
            if corner == 1:
                self.rotateBy(1, corner)
            elif corner == 2:
                self.rotateBy(-1, corner)
        while map.polygon.intersects(LineString([self.polygon.exterior.coords[1],self.polygon.exterior.coords[2]])):
            if corner == 1:
                self.rotateBy(-1, corner)
            elif corner == 2:
                self.rotateBy(1, corner)

        self.texture = pg.image.load(self.config.value.TextureLocation.value)
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.texture = pg.transform.rotate(self.texture, -self.rotation)
        self.cannonTexture = pg.image.load(self.config.value.WeaponLocation.value)
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -self.angle)
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -180)
