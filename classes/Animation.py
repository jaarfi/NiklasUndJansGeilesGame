from classes.baseClasses import *

only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]
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
    def __init__(self, polygon, gameinstance, sprites, duration, size, callerArray):
        super().__init__(polygon,gameinstance)
        self.duration = duration * 60
        newSprites = []
        for sprite in sprites:
            newSprites.append(pg.transform.scale(sprite,(int(sprite.get_width() * size), int(sprite.get_width() * size))))

        self.sprites = newSprites
        self.callerArray = callerArray
    def draw(self, display):
        if math.floor(self.internalFrame/self.duration*len(self.sprites)) >= len(self.sprites):
            if self in self.callerArray:
                self.callerArray.remove(self)
            return True
        display.blit(self.sprites[math.floor(self.internalFrame/self.duration*len(self.sprites))], (self.getCoords()[0] - self.sprites[0].get_width()/2, self.getCoords()[1] - self.sprites[0].get_height()/2))
        self.advanceFrameCounter()
        return False
