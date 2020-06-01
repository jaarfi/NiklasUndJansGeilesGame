#Drive Sound: "Sound effects obtained from https://www.zapsplat.com"
#Fire Sound: "Sound effects obtained from https://www.zapsplat.com"
#Explosion Sound: "Sound effects obtained from https://www.zapsplat.com"

import json
from classes.Animation import *


with open('config.json', 'r') as c:
    config = json.load(c)


class Shell(MovablePhysicsObject):
    '''
    Eine Klasse für die Shell, also die gefeuerte Granate eines Panzers

    '''
    def __init__(self, polygon,gameinstance,vector,shellType, tank):
        '''
        Initiator

        :param polygon: Das Polygon der Shell
        :param gameinstance: Eine Instant des Klasse Game
        :param vector: Der Vektor, in welche Richtung die Shell gefeuert wird
        :param shellType: Die Art der Shell, ist eine Klasse des shellStates Enum
        :param tank: Der Panzer zu dem die Shell gehört
        '''
        color = pg.Color(255, 255, 255)
        self.shellType = shellType
        self.shellState = shellStates.FLYING    #Da die Shell erst erzeugt wird, sobald sie fliegt, kann sie damit erzeugt werden
        self.collisionPolygon = polygon         #Das Collisionspolygon wird später benötigt und irgendeiner weise initialisiert werden
        super().__init__(polygon, gameinstance, vector, self.shellType.value.SPEED.value,color)
        self.remainingFlyingTime = self.shellType.value.FLYTIME.value * self.gameInstance.fps          #Wie lange die Shell fliegt in frames
        self.remainingTimeTillSeek = self.shellType.value.TIMETILLSEEK.value * self.gameInstance.fps
        self.gravity = self.shellType.value.GRAVITY.value
        self.seeking = False                    #Ob die Shell momentan ein Ziel sucht
        self.tank = tank
        self.explosions = []                    #Ein Array für die Explosionen, die die Shell erzeugt
        self.gameInstance.collisionObjects.append(self)         #Die Shell fügt sich zu dem collisionObject array hinzu, damit alles mit dieser shell kollidieren kann
        self.basetexture = pg.image.load(self.shellType.value.textureLocation.value)
        self.texture = self.basetexture
        self.rotation = math.degrees(math.asin(self._normalizedDirectionalVector[0]))
        self.ex_sound = pg.mixer.Sound(config["sound"]["explosion"])

    def move(self):
        '''
        Bewegen der Shell

        :return: none
        '''
        if self.shellState == shellStates.FLYING:   #Falls die shell fliegt, darf sie sich bewegen
            oldCoords = self.getCoords()            #Die Koordinaten vor dem bewegen werden zwischengespeichert

            if self.seeking:                        #Falls die Granate ein Ziel sucht, wird ausgerechnet welches
                seekedPlayer = 0
                distanceToSeekedPlayer = 99999999
                vectorToSeekedPlayer = 0
                for player in self.gameInstance.players:    #Die Distanz zu allen Spielern wird berechnet
                    if player != self.tank:
                        vectorToPlayer = (self.getCoords()[0] - player.getCoords()[0], self.getCoords()[1] - player.getCoords()[1])
                        distanceToPlayer = math.sqrt(vectorToPlayer[0]*vectorToPlayer[0]+vectorToPlayer[1]*vectorToPlayer[1])
                        if distanceToPlayer < distanceToSeekedPlayer and distanceToPlayer < self.shellType.value.SEEKDISTANCE.value:    #Der nächst gelegene Feindliche Panzer, der in Reichweite ist, wird als Ziel ausgesucht
                            seekedPlayer = player
                            vectorToSeekedPlayer = vectorToPlayer
                if seekedPlayer != 0:           #Falls ein Ziel gefunden wurde, wird der Vektor zu diesem berechnet
                    self.color = (222, 23, 56)
                    self.speed = self.shellType.value.POSTLOCKONSPEED.value
                    vectorToSeekedPlayer = self.normalizeVector(vectorToSeekedPlayer)
                    self.changeVectorBy(-vectorToSeekedPlayer[0]*self.shellType.value.POSTLOCKONSPEED.value*0.2, -vectorToSeekedPlayer[1]*self.shellType.value.POSTLOCKONSPEED.value*0.2)   #Der Flugvektor der Shell wird unter berücksichtigung des Zieles neu berechnet
                    self.speed += self.shellType.value.POSTLOCKONACCELERATION.value

            self.physicsMove()          #Die shell in richtung des Flugvektors bewegen
            self.changeVectorBy(0, self.gravity)    #Die Schwerkraft miteinberechnen, für den Parabelflug
            self.rotation = math.degrees(math.asin(self._normalizedDirectionalVector[0]))   #Die neue Rotation nach der Schwerkraft
            if self._normalizedDirectionalVector[1] > 0:
                self.texture = pg.transform.rotate(self.basetexture, self.rotation)     #Die Textur richtig rotieren
                self.texture = pg.transform.rotate(self.texture , 180)
            else:
                self.texture = pg.transform.rotate(self.basetexture, -self.rotation)

            #Berechnung, ob man ein Ziel getroffen hat:
            #Da manche Schells zu schnell sind, kann es passieren, dass sie innerhalb eines Frames von vor dem Panzer hinter
            #ihn gelangen, was dann nicht als Kollision zählen würde, weil das neue Polygon nicht mit dem Panzer Kollidiert.
            #Gelöst wurde das Porblem, indem ein Kollisionspolygon erzeugt wird, welches vom alten Polygon zum neuen verläuft.
            #Falls dieses Polygon ein Objekt übershcneidet, hat die Shell in diesem Zeitschritt das Objekt getroffen

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
                    self.explode(intersection)  #Falls es etwas trifft, das nicht der eigene Panzer oder die eigene Shell ist, explodiert die Shell
                    #Es wird die Intersection übergaben, damit in dessen mitte die Explosion gezeichnet wird, was die beste Methode ist, sie an die richtige Stelle zu malen ohne zu raycaste, was sehr kopmliziert wäre


            if self.remainingFlyingTime > 0:    #Manche Shells fliegen nicht unendlich lang und werden Abgebremst
                self.remainingFlyingTime -= 1
                self.speed -= self.shellType.value.SPEED.value/(self.shellType.value.FLYTIME.value*60)

            if self.speed <= 0:             #Falls eine Shell nicht mehr fliegt wird ihr speed auf 0 gesetzt
                self.changeVectorTo((0,0))
                if not self.shellType.value.SEEKING.value:  #Falls die Shell nicht noch im nachhinein einen Panzer sucht, wird sie gelöscht
                    self.safedelete()

            if self.remainingTimeTillSeek > 0:
                self.remainingTimeTillSeek -= 1

            if self.remainingTimeTillSeek <= 0:
                self.startSeeking()

            if newCoords[0] > self.gameInstance.width or newCoords[0] < 0 and self.shellState != shellStates.EXPLODING:
                self.safedelete()           #Die shell löschen falls sie aus dem Bildschirmrand rausgeht

    def draw(self, display):
        '''
        Zeichenfunktion der Shell

        :param display: das Display auf welches gezeichnet wird
        :return:
        '''
        if self.shellState == shellStates.FLYING:
            pos = (self.getCoords()[0] - (self.texture.get_width() / 2),
                   self.getCoords()[1] - (self.texture.get_height() / 2))
            display.blit(self.texture, pos)     #Wenn die shell fliegt, wird sie auf das display geblittet
        if self.shellState == shellStates.EXPLODING:
            delete = False
            for explosion in self.explosions:   #Falls sie explodiert, werden alle Explosionen gezeichnet
                delete = explosion.draw(display) #Falls diese Explosionen vorbei sind, kann sich die shell löschen
            if delete:
                self.safedelete()

    def explode(self, poly):
        '''
        Die Shell explodieren lassen

        :param poly: Die Explosion braucht ein Polygon, in dessen Mittelpuntk sie gezeichnet werden kann
        :return:
        '''
        if Menu.sound_set:      #sound abspielen, wenn das Häkchen gesetzt wurde
            self.ex_sound.set_volume(0.2)
            self.ex_sound.play()
        self.explosions.append(Animation(poly, self.gameInstance, expl, self.shellType.value.EXPLOSIONTIME.value,
                                         self.shellType.value.EXPLOSIONSIZE.value, self.explosions))    #Eine Explosion erzeugen und anzeigen lassen
        self.shellState = shellStates.EXPLODING         #Den Status ändern

    def safedelete(self):
        '''
        Vllt unnötige Funktion um die Shell aus allen Arrays zu löschen, in denen sie ist

        :return: none
        '''
        if self in self.tank.shells:
            self.tank.shells.remove(self)
        if self in self.gameInstance.collisionObjects:
            self.gameInstance.collisionObjects.remove(self)

    def startSeeking(self):
        '''
        Anfangen, ein ziel zu suchen

        :return: none
        '''
        if self.shellType.value.SEEKING.value:
            self.gravity = self.shellType.value.SEEKINGGRAVITY.value
            self.seeking = True


class Tank(MovablePhysicsObject):
    '''
    Der Tank hat eine eigene Klasse bekommen
    '''
    def __init__(self, gameinstance, playernumber):
        '''
        Initiator

        :param gameinstance: instanz von Game
        :param playernumber: Welche Spielernumemr der Panzer ist
        '''

        if playernumber == 1:       #Die Richtigen Configs laden
            self.config = playerControls.FIRST
        else:
            self.config = playerControls.SECOND

        color = self.config.value.Color.value
        super().__init__(Polygon([(2,38),(21,57),(87,58),(103,45),(103,15),(76,17),(76,0),(34,0),(35,16),(18,16)]),gameinstance,[0,0],0, color)
        if playernumber == 1:   #Die spieler an unterschiedlichen Stellen Spawnen lassen
            startpos = (self.gameInstance.width-50,0)
        else:
            startpos = (50,50)
        self.moveTo(startpos)
        self.angle = -90    #Der Winkel zum feuern
        self.firingVector = [math.cos(math.radians(self.angle))*75, math.sin(math.radians(self.angle))*75]
        self.shells = []
        self.timeToLoad = 0
        self.currentlySelectedShell = shellTypes.NORMAL
        self.life = 100
        self.groundedCorner = 1 #Es gibt eine Ecke des Polyogns, die immer als Anker fundiert, um den Panzer gescheit zu rotieren
        self.keydown = False    #Braucht man, um zu testen, ob ein Key losgelassen wurde
        self.texture = pg.image.load(self.config.value.TextureLocation.value)
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.cannonTexture = pg.image.load(self.config.value.WeaponLocation.value)
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.animations = []
        self.soundFire = pg.mixer.Sound(config["sound"]["shoot"])
        self.soundDrive = pg.mixer.Sound(config["sound"]["drive"])
        self.drive = False
        self.playerNumber = playernumber

    def move(self, map):
        '''
        Den Panzer bewegen

        :param map: Das Polygon des Untergrundes, auf dem man sich bewegt
        :return: none
        '''
        self.drive = False
        key = pg.key.get_pressed()
        if key[self.config.value.LEFT.value]: #Bei Tastendurck den Vektor manipulieren und Speed setzen
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
        elif self.keydown:          #Die Shell wechseln, sobald man die Taste loslässt
            self.keydown = False
            if self.timeToLoad <= 0:
                self.currentlySelectedShell = self.currentlySelectedShell.next()
        if self.physicsMoveNewPolygon().exterior.coords[1][0] > 1 and self.physicsMoveNewPolygon().exterior.coords[2][0] < self.gameInstance.width -1:
            #Erst muss getestet werden, ob der Panzer fahren darf oder aus dem Spielfeld fallen würde
            self.physicsMove()
        for shell in self.shells:
            shell.move()
        self.firingVector = [math.cos(math.radians(self.angle))*75, math.sin(math.radians(self.angle))*75]
        self.rotateToGround(map, self.groundedCorner,self.speed)    #Den Panzer auf den Boden setzen und ihm entsprechend rotieren
        self.changeVectorTo([0, 0])
        self.speed = 0
        if key[self.config.value.FIRE.value]:
            self.fireShell()
        if self.timeToLoad > 0:
            self.timeToLoad -= 1

    def fireShell(self):
        '''
        Eine Shell schießen

        :return: none
        '''
        if self.timeToLoad <= 0:    #Falls geladen wurde darf man schießen
            tmpCoords = self.getCoords()
            if Menu.sound_set:
                self.soundFire.set_volume(0.4)
                self.soundFire.play()

            if self.currentlySelectedShell.value.NUMBEROFSHELLS.value > 1:                  #Falls es sich um eine Shell mit mehreren Projektielen handelt, werden diese alle erzeugt
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
            self.timeToLoad = self.currentlySelectedShell.value.RELOAD.value * self.gameInstance.fps    #Man muss nachladen


    def hit(self, dmg):
        '''
        Der Panzer wird getroffen und ihm werden dmg HP abgezoge, sind die HP nun < 0, verliert er

        :param dmg: Schadensmenge
        :return: none
        '''
        self.life = self.life - dmg
        if self.life < 0:
            self.soundDrive.stop()
            Menu.victory(self.playerNumber)

    def draw(self, display):
        '''
        Zeichenfunktion des Panzers

        :param display: Das Dispaly auf welches gezecihnet wird
        :return: none
        '''

        if self.config == playerControls.FIRST:
            #Je nach Spielernummer die Werte in eine andere Ecke schreiben
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

        textsurface = self.gameInstance.font.render(self.currentlySelectedShell.value.NAME.value, False, self.color)    #Nachladestatus und ausgewählte Munition anzeigen
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
        '''
        Funktion, um den Panzer de mBoden anzupassen

        :param map: Das Polygon des Bodens
        :param corner: Die Ecke, die grundiert ist
        :param moved: ob sich der Panzer bewegt hat
        :return: none
        '''

        #Die Gewählte Ecke auf den Boden bringen
        while not map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, 1)
        while map.polygon.contains(Point(self.polygon.exterior.coords[corner])):
            self.moveBy(0, -2)

        if moved and not self.internalFrame % (self.gameInstance.fps/15):
            #Lustigen stuab aufwirbeln wenn der Panzer fährt
            tempdust = []
            for i in range(len(dust)):
                tempdust.append(pg.transform.rotate(dust[i], self.rotation))
            self.animations.append(Animation(Polygon([self.polygon.exterior.coords[corner],self.polygon.exterior.coords[corner],self.polygon.exterior.coords[corner]]), self.gameInstance, tempdust,3/15, 1, self.animations))


        #Den Panzer rotieren, bis er6 komplett auf dem boden ist
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

        #Die Texturen rotieren
        self.texture = pg.image.load(self.config.value.TextureLocation.value)
        self.texture = pg.transform.scale(self.texture, (104, 59))
        self.texture = pg.transform.rotate(self.texture, -self.rotation)
        self.cannonTexture = pg.image.load(self.config.value.WeaponLocation.value)
        self.cannonTexture = pg.transform.scale(self.cannonTexture,(int(self.texture.get_width() * 3 / 2), int(self.texture.get_width() * 3 / 2)))
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -self.angle)
        self.cannonTexture = pg.transform.rotate(self.cannonTexture, -180)
