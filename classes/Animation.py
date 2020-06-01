from classes.baseClasses import *

only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]  #Alle Files für die Animationen laden
expl = []
for myfile in only_files:
    if "Explosion" in myfile:
        expl.append(pg.image.load("sprites/" + myfile))
fireShots = []
for myfile in only_files:
    if "Fire_Shots_Shot_A" in myfile:
        fireShots.append(pg.image.load("sprites/" + myfile))

dust = []
only_files2 = [files for files in listdir("pics/sprites") if isfile(join("pics/sprites", files))]
for myfile in only_files2:
    if "Smoke" in myfile:
        dust.append(pg.image.load("pics/sprites/" + myfile))


class Animation(CollisionObject):
    '''
    Eine Klasse um Animationen zu spawnen und (halbwegs) unabhängig von den Callern zu machen

    Die Animation wird erstellt, und wird sich sobald sie "fertig" ist selbst aus dem Animationen Array des Callers löschen
    '''
    def __init__(self, polygon, gameinstance, sprites, duration, size, callerArray):
        '''
        Initiator

        :param polygon: Ein Polygon, welches hauptsächlich für die Position benötigt wird
        :param gameinstance: Eine Instanz von Game
        :param sprites: ein Array an pg Images, die die Sprites der Animation sind
        :param duration: Wie lange die Animation gezeichnet werden soll in sekunden
        :param size: Multiplikations Faktor für die Größe der Animation
        :param callerArray: das Array des callers, in welchem sich die Animation befindet.
        '''
        super().__init__(polygon,gameinstance)
        self.duration = duration * 60
        newSprites = []
        for sprite in sprites:
            newSprites.append(pg.transform.scale(sprite,(int(sprite.get_width() * size), int(sprite.get_width() * size)))) #Die Sprites werden in die korrekte Größe skaliert
        self.sprites = newSprites
        self.callerArray = callerArray


    def draw(self, display):
        '''
        Zeichenfunktion der Animation
        
        :param display: Display auf welches gezeichnet wird
        :return: True, falls die Animation vorbei ist, False falls noch nicht
        '''''
        if math.floor(self.internalFrame/self.duration*len(self.sprites)) >= len(self.sprites): #Falls alle Frames gezeichnet wurden
            if self in self.callerArray:
                self.callerArray.remove(self)
            return True
        display.blit(self.sprites[math.floor(self.internalFrame/self.duration*len(self.sprites))],
                     (self.getCoords()[0] - self.sprites[0].get_width()/2,
                      self.getCoords()[1] - self.sprites[0].get_height()/2))
        self.advanceFrameCounter()
        return False
