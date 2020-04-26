import json
from os import listdir
from os.path import isfile, join

import pygame, math

WIDTH = 500
HEIGHT = 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
x = 200
y = 200


class Tank(object):
    def __init__(self):
        self.bild = pygame.image.load("pics/tank/tank_model_1.png")
        self.wepon = pygame.image.load("pics/tank/tank_model_1_w1.png")
        self.s_bild = pygame.transform.scale(self.bild, (207, 117))
        self.s_wepon = pygame.transform.scale(self.wepon, (int(self.bild.get_width()*3/2), int(self.bild.get_width()*3/2)))
        self.outer_rec = pygame.Rect(x, y, self.s_bild.get_width(), self.s_bild.get_height())
        self.help1_rec = self.buildRec()
        self.wepon_rec = pygame.Rect(
            # self.outer_rec.topleft[0] + self.outer_rec.width / 2 - self.s_wepon.get_width() / 2,
            # self.outer_rec.topleft[1] + self.outer_rec.height / 4 - self.s_wepon.get_height() / 2 - 10,
            self.help1_rec.bottomleft[0]-self.s_wepon.get_width()/2,
            self.help1_rec.bottomleft[1]-self.s_wepon.get_height()/2,
            self.s_wepon.get_width(), self.s_wepon.get_height())
        # self.map_rec = self.buildRecMap()
        pygame.draw.polygon(self.s_bild, (255, 0, 0),
                            [(65, 0), (65, 30), (35, 30), (0, 75), (40, 117), (175, 117), (207, 95), (207, 30),
                             (155, 30), (155, 0), (104, 0), (104, 57), (103, 27), (103, 0)], 3)

    def buildRec(self, a=0):
        cos = abs(math.cos(math.radians(a))) + 0.00001
        sin = abs(math.sin(math.radians(a))) + 0.00001

        r = pygame.Rect(self.outer_rec.center[0], self.outer_rec.center[1],
                        -(self.outer_rec.height/4+10)*cos, -(self.outer_rec.height/4+10)*sin)

        return r

    def buildRecMap(self, a=0):
        cos = abs(math.cos(math.radians(a))) + 0.00001
        sin = abs(math.sin(math.radians(a))) + 0.00001

        rec2width = ((self.outer_rec.topright[0] - self.outer_rec.topleft[0]) / 2) * sin
        rec2height = (self.outer_rec.bottomleft[1] - self.outer_rec.topleft[1]) * cos
        r = pygame.Rect(self.outer_rec.center[0] - rec2width / 2, self.outer_rec.center[1] - rec2height / 2,
                        rec2width, rec2height)
        return r


    def draw(self, rt_t, rt_w, fire):
        center_w = (self.outer_rec.center[0] - int((self.outer_rec.height / 4 + 10) * math.sin(math.radians(rt_t))),
                    self.outer_rec.center[1] - int((self.outer_rec.height / 4 + 10) * math.cos(math.radians(rt_t))))
        self.wepon_rec = pygame.Rect(center_w[0]-self.wepon_rec.width/2, center_w[1]-self.wepon_rec.height/2,
                                     self.s_wepon.get_width(), self.s_wepon.get_height())

        front_w = (center_w[0]-int(self.s_wepon.get_width()/2 * math.sin(math.radians(rt_w+90))),
                   center_w[1]-int(self.s_wepon.get_height()/2 * math.cos(math.radians(rt_w+90))))
        pygame.draw.circle(screen, (255, 128, 0),
                           (front_w), 10, 2)

        r_bild = pygame.transform.rotate(player.s_bild, rt_t)
        r_wepon = pygame.transform.rotate(player.s_wepon, rt_w)

        pos = (self.outer_rec.center[0] - (r_bild.get_width() / 2),
               self.outer_rec.center[1] - (r_bild.get_height() / 2))
        pos_w = (self.wepon_rec.center[0] - (r_wepon.get_width() / 2),
                 self.wepon_rec.center[1] - (r_wepon.get_height() / 2))

        screen.blit(r_wepon, pos_w)
        screen.blit(r_bild, pos)
        if fire:
            self.shoot(front_w, rt_w)

        # self.map_rec = self.buildRecMap(rt)
        self.help1_rec = self.buildRec(rt)
        drawrec(self.outer_rec)
        drawrec(self.wepon_rec, (0, 0, 255))
        # drawrec(self.help1_rec)

        # drawrec(self.map_rec, (255, 128, 0), 2)

        # screen.blit(self.bild, (0,0))
        # pygame.draw.polygon(screen, (0, 255, 255),
        #                    [(65, 0), (65, 30), (35, 30), (0, 75), (40, 117), (175, 117), (207, 95), (207, 30),
        #                     (155, 30), (155, 0), (111, 0), (111, 57), (110, 27), (110, 0)], 3)

    def shoot(self, coords, rt_s):
        global shot
        global fire
        global fire_count

        if fire_count >= 4:
            fire = False
            fire_count = 0
        else:

            s_shot = pygame.transform.scale(shot[int(fire_count)], (200, 200))

            shot_rec = pygame.Rect(coords[0]-int(s_shot.get_width()/2)-5, coords[1]-int(s_shot.get_height()/2),
                                   s_shot.get_width(), s_shot.get_height())

            drawrec(shot_rec)
            r_shot = pygame.transform.rotate(s_shot, rt_s+90)

            pos_s = (shot_rec.center[0] - (r_shot.get_width() / 2),
                     shot_rec.center[1] - (r_shot.get_height() / 2))
            screen.blit(r_shot, pos_s)
            fire_count += 0.5


tank_polygon = {
    "h3": (65, 0),
    "h2": (65, 30),
    "h1": (35, 30),
    "t1": (0, 75),
    "t2": (40, 117),
    "t3": (175, 117),
    "t4": (207, 95),
    "h4": (207, 30),
    "h5": (155, 30),
    "h6": (155, 0),
    "e1": (101, 0),
    "center": (101, 57),
    "canon": (100, 27),
    "e2": (100, 0)
}


def drawrec(rec, c=(255, 0, 0), i=3):
    pygame.draw.circle(screen, c, rec.center, i)
    pygame.draw.circle(screen, c, rec.topleft, i)
    pygame.draw.circle(screen, c, rec.topright, i)
    pygame.draw.circle(screen, c, rec.bottomleft, i)
    pygame.draw.circle(screen, c, rec.bottomright, i)


rt = 0
rot_speed = 2

player = Tank()

only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]
exhaust = []
shot = []

for myfile in only_files:
    if "Exhaust_02" in myfile:
        exhaust.append(pygame.image.load("sprites/" + myfile))
    elif "Shot_A" in myfile:
        shot.append(pygame.image.load("sprites/" + myfile))


def exhaust_(coords=tank_polygon.get("t4")):
    global frame
    if frame + 1 >= 9:
        frame = 0

    if move_right:
        screen.blit(exhaust[frame], coords)
        frame += 1

    pygame.display.update()


move_right = False
speed = 10

fire = False
fire_count = 0
frame = 0
while True:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                fire = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False

    rt = (rt + rot_speed) % 360
    # rt = 0
    player.draw(rt, -rt, fire)

    exhaust_()

    pygame.display.flip()
    clock.tick(60)
