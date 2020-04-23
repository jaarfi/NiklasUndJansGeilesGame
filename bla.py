import pygame, math

WIDTH = 500
HEIGHT = 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Tank(object):
    def __init__(self):
        self.bild = pygame.image.load("pics/tank/tank_model_1.png")
        self.s_bild = pygame.transform.scale(self.bild, (80, 45))
        self.outer_rec = pygame.Rect(200, 200, self.s_bild.get_width(), self.s_bild.get_height())
        self.map_rec = self.buildRecMap()

    def buildRecMap(self, a=0):
        cos = abs(math.cos(math.radians(a)))+0.00001
        sin = abs(math.sin(math.radians(a)))+0.00001

        rec2width = ((self.outer_rec.topright[0] - self.outer_rec.topleft[0])/2) * sin
        rec2height = (self.outer_rec.bottomleft[1] - self.outer_rec.topleft[1]) * cos
        r = pygame.Rect(self.outer_rec.center[0] - rec2width / 2, self.outer_rec.center[1] - rec2height / 2,
                        rec2width, rec2height)
        return r

    def draw(self, rt):
        r_bild = pygame.transform.rotate(player.s_bild, rt)

        pos = (self.outer_rec.center[0] - (r_bild.get_width() / 2), self.outer_rec.center[1] - (r_bild.get_height() / 2))
        screen.blit(r_bild, pos)

        self.map_rec = self.buildRecMap(rt)
        drawrec(self.outer_rec)
        drawrec(self.map_rec, (255, 128, 0), 2)


def drawrec(rec, c=(255, 0, 0), i=3):
    pygame.draw.circle(screen, c, rec.center, i)
    pygame.draw.circle(screen, c, rec.topleft, i)
    pygame.draw.circle(screen, c, rec.topright, i)
    pygame.draw.circle(screen, c, rec.bottomleft, i)
    pygame.draw.circle(screen, c, rec.bottomright, i)


rt = 0
rot_speed = 1

player = Tank()

while True:
    # clear the screen every time before drawing new objects
    screen.fill((255, 255, 255))
    # check for the exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    rt = (rt + rot_speed) % 360
    # rt = 0

    player.draw(rt)

    pygame.display.flip()
    clock.tick(30)
