import os, math, time, random, enum
import numpy as np
from shapely import affinity
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon
from NiklasUndJansGeilesGame import my_color as c

import pygame as pg
import pygame.gfxdraw
from pygame.locals import *


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
    '''
    Es gibt Momentan 3 States, in denen sich eine Shell befinden kann. Sie ist entweder nicht in Benutzung(Idle), fliegt(Flying), oder explodiert(exploding).
    '''
    IDLE = 1
    FLYING = 2
    EXPLODING = 3

class Tank(object):

    '''
    Bei den Tanks handelt es sich um die Panzer der Spieler. Ein Tank wird dargestellt durch ein Rechteck und bietet unterschiedliche Funktionen, die von der Spiellogik aufgerufen werden
    '''

    def __init__(self):
        '''
        Initiator der Tank Klasse
        '''
        self.rect = pg.Rect(32, 32, 50, 30)                                                                             #Das Rechteck welches den Panzer präsentiert
        self.polygon = Polygon([self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright])             #Das Polygon, welches dem Rechteck entspricht, wird benötigt zur Kollisionsberechnung
        self.angle = 45                                                                                                 #Der Abschusswinkel
        self.shootingVector = (int(math.sin(-self.angle)*150), int(math.cos(-self.angle)*150))                          #Der Vektor, in welchem die Shell losgeschossen werden soll. Wird auch zur Zielanzeige verwendet
        self.shell = Shell()                                                                                            #Jeder Tank hat eine Shell. Diese wird später unterschiedliche Typen annehmen können (Spread, Fire.. ?)
        self.life = 100                                                                                                 #Die aktuellen Hitpoint die der Tank noch hat
        self.color = list(np.random.random(3) * 256)                                                                   #Dem Tank wird eine zufällige Farbe zugewiesen, um die spieler auseinander zu halten
        self.dx = 0
        self.dy = 0
        self.da = 0

    def premove(self, key):
        if key[pg.K_LEFT] and self.getCoords()[0] > 2:
            self.dx = self.dx - 2
        if key[pg.K_RIGHT] and players[0].getCoords()[0] < displaywidth - 18:
            self.dx = self.dx + 2
        if key[pg.K_UP]:
            self.da = self.da - 0.025
        if key[pg.K_DOWN]:
            self.da = self.da + 0.025
        if key[pg.K_SPACE] and self.shell.state == shellStates.IDLE:
            self.fireShell()

    def move(self, map):
        '''
        Bewegt den Panzer um die dx in der horizontalen Ebene und nach dy in der Vertikalen
        :param dx: Horizontale Bewegung
        :param dy: Vertikale Bewegung
        :param map: Der Untergrund auf dem sich der Panzer bewegen soll
        :return: None
        '''
        self.rect.x += self.dx
        self.rect.y = displayheigth
        self.polygon = Polygon([self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright])
        while self.polygon.intersects(map.polygon):
            self.rect.y -= 1
            self.polygon = Polygon([self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright])  # Das Polygon besteht aus den Ecken des Rechtecks und muss bei jeder Bewegung geupdatet werden
        self.angle += self.da
        #TODO AUSLAGERN
        self.shootingVector = (int(math.sin(-self.angle) * 150), int(math.cos(-self.angle) * 150))                      #Der Vektor muss regelmäßig geupdatet werden, hier macht es momentan am meisten sinn
        self.dx = 0
        self.da = 0

    def getCoords(self):
        '''
        :return: Koordinaten des Mittelpunktes
        '''
        return (self.rect.center)

    def fireShell(self):
        '''
        Wird aufgerufen sobald geschossen wird und teilt dies der Shell mit
        :return: None
        '''
        if self.shell.state == shellStates.IDLE:                                                                        #Falls die Shell bereits im Flug ist oder Explodiert, darf sie nicht erneut gefeuert werden
            self.shell.fireShell(self.shootingVector, self.getCoords())                                                 #Die Shell feuern, mit dem Richtungsvektor und dem Ortsvektor

    def firingAnimation(self, listOfObjects):
        '''
        Diese Funktion berechnet die Animationen bzw. teilt der Shell mit diese zu berechnen. Hierzu gehören Kollisionschecks
        :param listOfObjects: Eine Liste an Objekten, mit denen die Shell kollidieren kann. (Darf auch feuernden Tank beinhalten, deiser wird programmatisch entfernt)
        :return: None
        '''
        listCopy = list.copy(listOfObjects)                                                                             #Eine Kopie der Liste wird erstellt, um diese zu manipulieren
        if listCopy.__contains__(self):                                                                                 #Falls die Liste den feuernden Tank beinhaltet, ...
            listCopy.remove(self)                                                                                       #... wird dieser entfernt. Wird dies nicht getan, explodiert die Shell sofort, da sie im Tank gespawnt wird
        self.shell.collisionCheck(listCopy)                                                                             #Die Shell wird auf Kollision mit den Objekten überprüft

    def hit(self):
        '''
        Wird der Tank gehittet, verliert er HP
        :return: None
        '''
        self.life = self.life-20                                                                                        #20HP Fix momentan, wird abhängig von Shell sein

    def draw(self, display):
        '''
        Alles was zum Panzer gehört wird gezeichnet
        :param display: Das Display auf welches gezeichnet werden soll
        :return: None
        '''
        pg.draw.rect(display, self.color, self.rect)                                                                    #Der Spieler Selbst wird gezeichnet
        pg.draw.line(display, self.color, (self.rect.x, self.rect.center[1]+50), (self.rect.x+self.life, self.rect.center[1]+50), 10) #Die Hp Anzeige zeichnen
        self.shell.draw(display)                                                                                        #Der Shell sagen, sie soll Zeichnen was sie muss
        if self.shell.state == shellStates.IDLE:                                                                        #Falls die Shell Idle ist, man also feuern kann..
            pg.draw.line(display, (255, 50, 0), self.rect.center,(self.rect.center[0]+self.shootingVector[0], self.rect.center[1]+self.shootingVector[1]))#... wird eine Zielgerade gezeichnet

class Shell(object):
    '''
    Bei der Shell handelt es sich um ddas Geschoss des Tanks
    '''
    def __init__(self):
        '''
        Initiator der Shell Klasse
        '''
        #Viele der Attribut benötigen einen Startwert und können nicht mit 0 initialisiert werden
        self.rect = pg.Rect(-1, -1, 0, 0)                                                                               #Das Rechteck der Shell wird auserhalb der Map erstellt, um nicht mit etwas zu kollidieren und da man die genauen Koordinaten noch nicht weis
        self.polygon = Polygon([(-1,-1),(-1,-2),(-2,-1)])                                                               #Auch das Polygon der Shell wird mit Werten initialisiert, die während des Spieles nicht auftreten
        self.directionVector = (0, 0)
        self.state = shellStates.IDLE                                                                                   #Bei Generierung der Shell sit sie Idle, da sie noch vor dem Feuern generiert wird
        self.explodeFrameCounter = 0                                                                                    #Der Framecounter iwrd benötigt, um die Explosion richtig abzuspielen


    def draw(self,display):
        '''
        Zeichnet die wichtigen Teile der Shell
        :param display: Das Display auf welches gezeichnet wird
        :return: None
        '''
        self.move()                                                                                                     #Vor dem Malen wird die Position des Geschosses neu berechnet
        if (self.state == shellStates.FLYING):                                                                          #Die Shell wird nur gezeichnet wenn sie fliegt (Bei IDLE unbenutzt, bei EXPLODING schon kaputt)
            pg.draw.rect(display, (155, 100, 0), self.rect)
        elif (self.state == shellStates.EXPLODING):                                                                     #Falls die Shell am Explodieren ist muss die Explosionsanimation gezeichnet werden
            self.explodeFrameCounter = self.explodeFrameCounter + 1                                                     #Der Framecounter zählt hoch. Da draw jeden Frame aufgerufen wird, zählt es jeden seit Explosionsbeginn mit
            if explosion_tank(self.rect.center, self.explodeFrameCounter):                                              #Die Explosion wird abhängig von den Frames seit Beginn gezeichnet. Da explosion_tank True zurückgibt, falls sie komplett animiert wurde...
                self.state = shellStates.IDLE                                                                           #... Können die Werte der Shell zurückgesetzt werden, sobald sie voll explodiert ist
                self.move((-1,-1))
                self.explodeFrameCounter = 0


    def move(self, coords=(0, 0)):
        '''
        Bewegt die Shell um ihren eigens berechneten Wert. Werden Koordinaten angebeben, wird sie an die Stelle teleportiert
        :param coords: Optionale Angabe, falls die Shell an eine Bestimmte Stelle teleportiert werden soll
        :return: None
        '''
        if self.state == shellStates.FLYING:                                                                            # Falls die Shell am Fliegen ist, berechnet sie ihre Bewegung Selbst
            if coords == (0,0):
                self.rect.x = self.rect.x + int(self.directionVector[0]/15)
                self.rect.y = self.rect.y + int(self.directionVector[1]/15)
                self.directionVector = (self.directionVector[0], self.directionVector[1] + 5)                            #Der Y-Teil des Richtungvektors wird neu berechnet, um der Shell einen Parabelflug zu ermöglichen
        elif coords != (0, 0):                                                                                           #Teleportation bei Angabe von Koordinaten
            self.rect.x = coords[0]
            self.rect.y = coords[1]

        self.polygon = Polygon([self.rect.bottomleft, self.rect.topleft, self.rect.topright,self.rect.bottomright])              # Polygon muss geupdatet werden

    def collisionCheck(self, listOfObjects):
        '''
        Testet alle Objekte durch, ob die Shell mit ihnen Kollidiert
        :param listOfObjects: Liste der Kollidierbaren Objekte
        :return: None
        '''
        if self.state == shellStates.FLYING:                                                                            #Nur Falls die Shell fliegt kann sie Kollidieren
            for collision in listOfObjects:                                                                             #Für jedes Objekt wird einzeln geprüft
                if self.polygon.intersects(collision.polygon):                                        #Falls es mit dem Objekt kollidiert...
                    self.state=shellStates.EXPLODING                                                                    #... wrid der State gesetzt...
                    collision.hit()                                                                                     #... und dem Objekt mitgeteilt, dass es getroffen wurde
            if displaywidth < self.rect.x or self.rect.x < 0:
                self.state = shellStates.IDLE

    def fireShell(self, shootingVector, startpoint):
        '''
        Die Shell wird gefeuert
        :param shootingVector: Der Richtungsvektor in welchem sie fliegen soll
        :param startpoint: der Startpunkt der Shell
        :return: None
        '''
        self.directionVector = shootingVector                                                                           #Da die Werte jetzt wichtig sind, werden sie zu den richtigen gesetzt
        self.rect = pg.Rect(startpoint[0], startpoint[1], 10, 10)                                                       #Das Rechtek wird in dem Startpunkt gezeichnet
        self.state = shellStates.FLYING
        self.polygon = Polygon([self.rect.bottomleft, self.rect.topleft, self.rect.topright, self.rect.bottomright])


class Map(object):

    '''
    Eine Klasse um die Spielwelt zu repräsentieren
    '''
    def __init__(self):
        '''
        Initiator der Map
        '''
        self.polygon = Polygon(createMap(displaywidth,displayheigth))                                                   #eine externe Funktion wird aufgerufen um die Map zu generieren

    def draw(self, display):
        '''
        Malen der Map
        :param display: Das Display auf welches gemalt werden soll
        :return: None
        '''
        pg.gfxdraw.filled_polygon(display, map.polygon.exterior.coords, (255, 255, 255))                                                #Ein großes Polygon wird gezeichnet, welches dem Untergrund enspricht

    def hit(self):                                                                                                      #Muss definiert werden, da Map hittable ist, macht aber nichts
        pass


def drawAllObjects(arrayOfObjects, display):
    '''
    Ein funktion um das Malen mehrer Objekte zu ermölglichen
    :param arrayOfObjects: Ein Array der Objekte, die zu malen sind. Alle müssen eine .draw() Funktion besitzen
    :param display: Das Display auf welches die Objekte gemalt werden
    :return: None
    '''
    for toDraw in arrayOfObjects:
        toDraw.draw(display)

def createMap(width,height):
  '''
  Diese Funktion wird genutzt, um ein Array zu generieren, welches aus den Punkten eines Polygons besteht. Hier wird eine Map generiert, die den Untergrund der Spielfäche stellt
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
    '''
    Animation der Explosion
    :param coords: Die Koordinaten, an welchen Die Epxlosion stattfindet
    :param frame: Der aktuelle Frame der Animation. Wird benötigt um die Explosion "asynchron" zu malen
    :return: Boolean: Ist die Explosion beendet?
    '''
    #expl_sound.play()
    #clock.tick(1)
    if len(expl) == int(frame/len(expl)):
        return True
    display.blit(expl[int(frame/len(expl))], (coords[0] - 140, coords[1] - 140))
    return False



# __________________________________________________

def text_objects(text="", font="", color=c.black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def draw_menu(mouse):
    display.fill(c.white)
    global menu

    if ((displaywidth / 2) - 150) < mouse[0] < ((displaywidth / 2) + 150) and ((displayheigth / 2) + 50) < mouse[1] < (
            (displayheigth / 2) + 100):
        pg.draw.rect(display, c.green, ((displaywidth / 2) - 150, (displayheigth / 2) + 50, 300, 50))
        if pg.mouse.get_pressed() == (True, False, False):
            menu = False
    else:
        pg.draw.rect(display, c.dark_green, ((displaywidth / 2) - 150, (displayheigth / 2) + 50, 300, 50))

    # tytel text
    my_tytel_font = pg.font.Font("freesansbold.ttf", 45)
    TextSurf, TextRect = text_objects("NiklasUndJansGeilesGame", my_tytel_font)
    TextRect.center = ((displaywidth / 2), (displayheigth / 2))
    display.blit(TextSurf, TextRect)

    # box test
    my_box_font = pg.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects("start", my_box_font)
    TextRect.center = ((displaywidth / 2), (displayheigth / 2) + 75)
    display.blit(TextSurf, TextRect)


# ___________________________________________________


prev_x, prev_y = 0, 0
first = True
dead = True
x = 0
angle = 0

map = Map()
players = []
players.append(Tank())
players[0].move(map)
players.append(Tank())
print(players[0]==players[1])
listOfObjects = []
listOfObjects.append(map)
for player in players:
    listOfObjects.append(player)
frameCounerForPlayerPass = 0
activePlayer = players[0]
menu = True

# Spielschleife
while True:
    # print(frameCounerForPlayerPass)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            quit()

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                menu = True

    if menu:
        draw_menu(pg.mouse.get_pos())
    else:

        if frameCounerForPlayerPass == 360:
            frameCounerForPlayerPass = 0
            if activePlayer == players[0]:
                activePlayer = players[1]
            if activePlayer == players[1]:
                activePlayer = players[0]
        else:
            frameCounerForPlayerPass += 1

        keys = pg.key.get_pressed()

        activePlayer.premove(keys)
        for player in players:
            player.move(map)


        display.fill((0, 0, 0))
        drawAllObjects(listOfObjects, display)
        pg.draw.circle(display, c.yellow, (60, 600), 15, 5)

        activePlayer.firingAnimation(listOfObjects)

    pg.display.flip()
    clock.tick(60)



