from classes.Shell import *

class Game(object):
    def __init__(self, width, heigth, display, font, colorScheme):
        self.width = width
        self.height = heigth
        self.display = display
        self.clock = pg.time.Clock()
        self.fps = 60
        self.font = font
        self.players = []
        self.players.append(Tank(self, 1))
        self.players.append(Tank(self, 2))
        self.drawableObjects = []
        self.collisionObjects = []
        self.map = 0
        self.colorScheme = colorScheme


    def startGame(self):
        self.map = Map(Polygon(self.createMap(self.width, self.height)), self)
        self.collisionObjects.append(self.map)
        for player in self.players:
            player.move(self.map)
            self.collisionObjects.append(player)
        for thing in self.collisionObjects:
            self.drawableObjects.append(thing)
        while True:
            #self.players[0].move(self.map)
            for player in self.players:
                pass
                player.move(self.map)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    quit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        Menu.pause_menu()
            self.display.fill(self.colorScheme[0])

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


class Map(CollisionObject):
    def __init__(self, polygon, gameinstance):
        color = gameinstance.colorScheme[2]
        super().__init__(polygon, gameinstance, color)

