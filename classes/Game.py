from classes.Shell import *

class Game(object):
    '''
    Eine Klasse für das Spiel

    Diese Klasse bietet die Möglichkeit, eine Spielinstanz zu erzeugen und auf dieser das Spiel auszuführen.
    Indem man dieses Spiel an die anderenn Klassen weitergibt, können diese auf alle Attribute des Spiels, wie die Breite
    und Höhe weitergeben.
    '''
    def __init__(self, width, heigth, display, font, colorScheme):
        '''
        Initiator

        :param width: Breite des Spielfensters in Pixel
        :param heigth: Höhe des Spielfensters in Pixel
        :param display: Das Display, auf welchem alles gezeichnet wird
        :param font: ein pygame Font objekt, um auch Schrift anzeigen zu können
        :param colorScheme: Ein Array an Farben, welche himmer und Bodenfarbe bestimmen
        '''
        self.width = width
        self.height = heigth
        self.display = display
        self.clock = pg.time.Clock()        #Die Clock, um das Spiel in der richtigen Geschwindigkeit laufen zu lassen.
        self.fps = 60                       #Die Anzahl der FPS
        self.font = font
        self.players = []
        self.players.append(Tank(self, 1))
        self.players.append(Tank(self, 2))
        self.drawableObjects = []
        self.collisionObjects = []
        self.map = 0                        #Die Map wird erst bei Spielbeginn erstellt , nicht hier
        self.colorScheme = colorScheme


    def startGame(self):
        '''
        Das Spiel starten.

        :return: none
        '''
        self.collisionObjects = []
        self.map = Map(Polygon(self.createMap(self.width, self.height)), self)  #Die Map wird erstellt
        self.collisionObjects.append(self.map)
        for player in self.players:
            player.move(self.map)
            self.collisionObjects.append(player)
        for thing in self.collisionObjects:
            self.drawableObjects.append(thing)
        while True:
            #self.players[0].move(self.map)
            for player in self.players:
                player.move(self.map)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    quit()
                if event.type == KEYUP:                 #Wenn Escapegedrückt wird wird das Optionen Fenster geöffnet
                    if event.key == K_ESCAPE:
                        Menu.pause_menu()
            self.display.fill(self.colorScheme[0])      #Den Hintergrund zeichnen

            for toDraw in self.drawableObjects:         #Alle Objekte zeichnen
                toDraw.draw(self.display)

            pg.display.flip()
            self.clock.tick(self.fps)                   #Mit FPS ticken und dann in den nächsten Frame springen

    def createMap(self, width, height):
        '''
        Erstellt eine Map, welche als Untergrund für die Panzer agiert

        :param width: Breite der Map
        :param height: Höhe der Map
        :return: die Map als Polygon
        '''
        map = [(0, height)]
        spacing = 4
        newpoint = (0,random.randint(int(height / 2),int(height * 4 / 6)))                  #Die Map wird immer zufällig erstellt
        for i in range(0, spacing + 1):
            newpoint = (int(i * width / spacing), newpoint[1] + random.randint(-50, 50))    #Die Punkte müssen in einem gewissen Rahmen sein
            while int(height / 2) < newpoint[1] < int(height * 4 / 6):
                newpoint = (int(i * width / spacing), newpoint[1] + random.randint(-50, 50))
            map.append(newpoint)
        map.append((width, height))
        return map


class Map(CollisionObject):
    '''
    Die Klasse Für die Map

    Wird eigentlich nicht benötigt, ist aber zu stressig zu ändern
    '''
    def __init__(self, polygon, gameinstance):
        '''
        Initiator

        Siehe Collisionobject, ist ja eigentlich genau das gleiche
        :param polygon:
        :param gameinstance:
        '''
        color = gameinstance.colorScheme[2]
        super().__init__(polygon, gameinstance, color)

