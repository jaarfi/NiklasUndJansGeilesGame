import math, enum, json
import pygame as pg
from pygame import gfxdraw
from shapely import affinity
import random
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, Point, LineString
from pygame.locals import *
import Menu

with open('config.json', 'r') as c:
    config = json.load(c)


class shellStates(enum.Enum):   #Ein Enum in welchem Status sich die Shell befindet
    IDLE = 1
    FLYING = 2
    EXPLODING = 3

class playerControls(enum.Enum):    #Ein Enum, der genutzt wird um die Einstellungen fürr Spieler 1 und Spieler 2 zu speichern

    class FIRST(enum.Enum):
        RIGHT = pg.K_RIGHT
        LEFT = pg.K_LEFT
        DOWN = pg.K_DOWN
        UP = pg.K_UP
        CYCLE = pg.K_PERIOD
        FIRE = pg.K_COMMA

        TextureLocation = config["pics"]["tank"]["first"]["hull"]
        WeaponLocation = config["pics"]["tank"]["first"]["weapon"]
        Color = tuple(config["pics"]["tank"]["first"]["color"])

    class SECOND(enum.Enum):
        RIGHT = pg.K_d
        LEFT = pg.K_a
        DOWN = pg.K_w
        UP = pg.K_s
        CYCLE = pg.K_q
        FIRE = pg.K_e

        TextureLocation = config["pics"]["tank"]["second"]["hull"]
        WeaponLocation = config["pics"]["tank"]["second"]["weapon"]
        Color = tuple(config["pics"]["tank"]["second"]["color"])


class shellTypes(enum.Enum):    #Jede Art von Waffe hat ihre eigene Klasse in diesem ENUM bekommen

    class NORMAL(enum.Enum):    #In dieser Klasse werden alle wichtigen Werte gespeichert
        SPEED = 30              #Die Geschwindigkeit der Shell
        GRAVITY = 0.05          #Wie stark sie ovn der Schwerkraft beeinflusst wird
        DAMAGE = 15             #Wieviel Schaden sie bei einem Treffer verursacht
        RELOAD = 2              #Wielange sie nachladen muss
        SIZE = 5                #Wie groß die Hitbox der Shell ist

        SEEKING = False         #Ob es eine von Selbst suchende Shell ist
        NAME = "Normal Shell"   #Der Name in schönerem Text
        FLYTIME = float("inf")  #Wielange die Shell fliegt
        TIMETILLSEEK = 0        #Wielange bis sie ein Ziel sucht
        SEEKDISTANCE = 0        #Auf welche Distanz sie ein Ziel sucht
        SEEKINGGRAVITY = 0      #Wie stark sie während dem Suchen von der Schwerkraft beeinflusst wird
        POSTLOCKONSPEED = 0     #Wie schnell sie ist, osbald sie ein Ziel gefunden hat
        POSTLOCKONACCELERATION = 0  #Wie stark sie nach Zielfindung beschleunigt

        NUMBEROFSHELLS = 1      #Wieviele Shells bei Feuern geschossen werden
        SPREAD = 0              #In welchem Winkel diese gefeuert werden

        textureLocation = config["pics"]["shell"]["normal"]

        EXPLOSIONSIZE = 0.7     #Wie Groß die Epxlosion ist (rein visuell)
        EXPLOSIONTIME = 1       #Wie lange die Explosion angezeigt wird

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
        POSTLOCKONSPEED = 0
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = config["pics"]["shell"]["sniper"]

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
        POSTLOCKONSPEED = 0
        POSTLOCKONACCELERATION = 0

        NUMBEROFSHELLS = 1
        SPREAD = 0

        textureLocation = config["pics"]["shell"]["machine gun"]

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

        textureLocation = config["pics"]["shell"]["gravitron"]

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

        textureLocation = config["pics"]["shell"]["skymine"]

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

        textureLocation = config["pics"]["shell"]["shotgun"]

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

        textureLocation = config["pics"]["shell"]["flak"]

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
    '''
    Die grundlegendste Klasse, ein Objekt welches gezeichnet wird

    In der Klassenhierarchie des Projektes stellt ein DrawableObject jedes Object dar, welches gezeichnet werden kann.
    Hierbei werden grundlegende Funktionen bereit gestellt, die ein solches Objekt benötigt.
    '''

    def __init__(self, polygon, gameinstance, color=pg.Color(0,0,0)):
        '''
        Initiator

        :param polygon: ein shapely Polygon, welches die Umrandung des Objektes repräsentiert
        :param gameinstance: ein object der Klasse Game, um es den Klassen zu ermöglichen, auf alle Parameter dessen zuzugreifen
        :param color: eine Pygame Color, in welcher das Object gezeichnet wird, Standardwert = (0,0,0)
        '''
        self.gameInstance = gameinstance
        self.polygon = polygon
        self.internalFrame = 0                  #Ein interner Framecounter, um Animationen zu realisieren
        self.color = color
        self.rotation = 0                       #Die Rotation dieses Object

    def draw(self, display):
        '''
        Eine grundlegende draw Funktion, malt das Polygon des Objektes auf die Oberfläche Display

        :param display: Oberfläche auf die gemalt werden soll
        :return: none
        '''
        pg.gfxdraw.filled_polygon(display, self.polygon.exterior.coords, self.color)

    def advanceFrameCounter(self, numberofframes=1):
        '''
        Frame counter hochzählen

        :param numberofframes: Standard ist um 1 zu inkrementieren, man kann aber auch eine andere Zahl angeben
        :return: none
        '''
        self.internalFrame += int(numberofframes)

    def resetFrameCounter(self):
        '''
        Frame counter zurücksetzen

        :return: none
        '''
        self.internalFrame = 0

    def getCoords(self):
        '''
        Gibt die Koordinaten des Mittelpunktes zurück, dieser muss nicht zwingend im Polygon liegen

        :return: Koordinaten des Mittelpunktes als Tupel von zwei Integern
        '''
        return int(list(self.polygon.centroid.coords)[0][0]), int(list(self.polygon.centroid.coords)[0][1])

    def moveTo(self, coords):
        '''
        Das Object an eine bestimmte Stelle Bewegen

        :param coords: Koordinaten der neuen Stelle
        :return: none
        '''
        coordsDifference = (coords[0] - self.getCoords()[0], coords[1]- self.getCoords()[1])        #Man kann Polygone nicht direkt an eine Stelle vershcieben, sondern nur um einen Wert, dieser wird hier errechnet
        self.polygon = affinity.translate(self.polygon, coordsDifference[0], coordsDifference[1])

    def moveBy(self, dx, dy):
        '''
        Das Objekt um einen Offset verschieben

        :param dx: verschiebung X-Achse
        :param dy: Vershciebung Y-Achse
        :return: none
        '''
        self.polygon = affinity.translate(self.polygon, dx, dy)

    def rotateTo(self, degree, corner):
        '''
        Das Polyogn in eine bestimmte Position rotieren

        :param degree: zu wieviel grad es rotieren soll, angabe in °
        :param corner: um welche Ecke das Polygon rotieren soll, muss ein Integer mit der Nummer der Ecke sein
        :return: none
        '''
        degreediff = degree - self.rotation
        self.rotateBy(degreediff, corner)           #Man kann nur um einen Offset rotieren, dieser wird errechnet und ruft iene andere Funktion auf

    def rotateBy(self, degree, corner):
        '''
        Das Polygon um einen Offset rotieren

        :param degree: um wieviel grad es rotieren soll, angabe in °
        :param corner: um welche Ecke das Polygon rotieren soll, muss ein Integer mit der Nummer der Ecke sein
        :return: none
        '''
        if 0 < corner < len(self.polygon.exterior.coords):
            self.polygon = affinity.rotate(self.polygon,degree, self.polygon.exterior.coords[corner])
            self.rotation += degree
            if self.rotation > 360:                    #Falls die Rotation größer als 360° ist, sol les diese darauf zurücksetzen
                self.rotation -= 360
            if self.rotation < 0:
                self.rotation += 360


class CollisionObject(DrawableObject):
    '''
    Ein CollisionObject kann sich selbst nicht bewegen, stellt alerdings eine möglichkeit uzr Kollision dar

    Diese Klasse vererbt DrawableObject, da jedes CollisionObject in unserem Spiel auch gezeichnet wird.
    Die Klasse wird momentan nur von der Map genutzt
    '''
    def colliding(self, PhysicsObject):
        '''
        Gibt zurück, ob das Objekt mit einem Anderen Objekt kollidiert

        :param PhysicsObject: Das andere Object
        :return: ob die Objekte kollidieren
        '''
        return self.polygon.intersects(PhysicsObject.polygon)

    def hit(self, dmg):
        '''
        Jedes CollisionObject kann getroffen werden und muss eine Funktion hierfür bereitstellen

        :param dmg: not used
        :return: none
        '''
        pass        #Als default wird bei einem Hit nichts gemacht

class MovablePhysicsObject(CollisionObject):
    '''
    Ein MovablePhysicsObject besitzt einen Vektor, in wessen Richtung er sich bewegen kann

    Diese Klasse Vererbt CollisionObject, da jedes Physics object kollidierbar ist.
    Ein MovablePhysicsObject bietet die Möglichkeit das Object in Richtung eines Vektors zu bewegen
    '''
    def __init__(self, polygon, gameinstance, directionalvector, speed, color=(0, 0, 0)):
        '''
        Initiator

        :param polygon: ein shapely Polygon, welches die Umrandung des Objektes repräsentiert
        :param gameinstance: ein object der Klasse Game, um es den Klassen zu ermöglichen, auf alle Parameter dessen zuzugreifen
        :param directionalvector: ein Richtungsvektor, der die Bewegungsrichtung des Objektes repräsentiert
        :param speed: Die Geschwindigkeit mit der sich das Objekt bewegt
        :param color: eine Pygame Color, in welcher das Object gezeichnet wird, Standardwert = (0,0,0)
        '''
        super().__init__(polygon, gameinstance, color)
        self._normalizedDirectionalVector = directionalvector       #Der Vektor wird gespeichert..
        self._normalizeVector()                                     #.. und danach Normalisiert
        self.speed = speed

    def normalizeVector(self, vector):
        '''
        Normalisieren eines Vektors (Die Länge des Vektors wird auf 1 gesetzt)

        :param vector: zu normalisierender Vektor
        :return: none
        '''
        vectorLength = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
        if vectorLength:
            vector = [vector[0] / vectorLength, vector[1] / vectorLength]           #Normalisieren, Mathe Kram halt
        return vector

    def _normalizeVector(self):
        '''
        Normalisieren des eigenen Vektors ohne Überabe und Rückgabe Parameter

        :return: none
        '''
        self._normalizedDirectionalVector = self.normalizeVector(self._normalizedDirectionalVector)

    def changeVectorTo(self, vector):
        '''
        Ändern des Vektors auf einen anderen

        :param vector: neuer Vektor
        :return: none
        '''
        self._normalizedDirectionalVector = [vector[0], vector[1]]
        self._normalizeVector()

    def changeVectorBy(self, dx, dy):
        '''
        Ändern des Vektors um einen Offset

        :param dx: Offset X-Achse
        :param dy: Offset Y-Achse
        :return: none
        '''
        self._normalizedDirectionalVector = [self._normalizedDirectionalVector[0] + dx,
                                             self._normalizedDirectionalVector[1] + dy]
        self._normalizeVector()

    def physicsMoveNewPolygon(self):
        '''
        Rückgabe des Polygons, das es sein würde, wenn man PhysicsMove anwendet

        :return: neues Polygon
        '''
        denormalizedVector = [self._normalizedDirectionalVector[0] * self.speed,
                              self._normalizedDirectionalVector[1] * self.speed]
        return affinity.translate(self.polygon, denormalizedVector[0], denormalizedVector[1])

    def physicsMove(self):
        '''
        Object in Richtung des Vektors mit der Geschwindigkeit bewegen

        :return: none
        '''
        denormalizedVector = [self._normalizedDirectionalVector[0] * self.speed,
                              self._normalizedDirectionalVector[1] * self.speed]
        self.polygon = affinity.translate(self.polygon, denormalizedVector[0], denormalizedVector[1])

