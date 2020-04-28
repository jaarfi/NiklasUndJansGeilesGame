import json
from os import listdir
from os.path import isfile, join

import pygame, math

from NiklasUndJansGeilesGame import my_color as c

displaywidth = 800
displayheight = 600

pygame.init()
screen = pygame.display.set_mode((displaywidth, displayheight))
clock = pygame.time.Clock()
x = 200
y = 200


class Tank(object):
    def __init__(self):
        self.bild = pygame.image.load("pics/tank/tank_model_1.png")
        self.wepon = pygame.image.load("pics/tank/tank_model_1_w1.png")
        self.s_bild = pygame.transform.scale(self.bild, (207, 117))
        self.s_wepon = pygame.transform.scale(self.wepon,
                                              (int(self.bild.get_width() * 3 / 2), int(self.bild.get_width() * 3 / 2)))
        self.outer_rec = pygame.Rect(x, y, self.s_bild.get_width(), self.s_bild.get_height())
        self.help1_rec = self.buildRec()
        self.wepon_rec = pygame.Rect(
            # self.outer_rec.topleft[0] + self.outer_rec.width / 2 - self.s_wepon.get_width() / 2,
            # self.outer_rec.topleft[1] + self.outer_rec.height / 4 - self.s_wepon.get_height() / 2 - 10,
            self.help1_rec.bottomleft[0] - self.s_wepon.get_width() / 2,
            self.help1_rec.bottomleft[1] - self.s_wepon.get_height() / 2,
            self.s_wepon.get_width(), self.s_wepon.get_height())
        # self.map_rec = self.buildRecMap()
        pygame.draw.polygon(self.s_bild, (255, 0, 0),
                            [(65, 0), (65, 30), (35, 30), (0, 75), (40, 117), (175, 117), (207, 95), (207, 30),
                             (155, 30), (155, 0), (104, 0), (104, 57), (103, 27), (103, 0)], 3)

    def buildRec(self, a=0):
        cos = abs(math.cos(math.radians(a))) + 0.00001
        sin = abs(math.sin(math.radians(a))) + 0.00001

        r = pygame.Rect(self.outer_rec.center[0], self.outer_rec.center[1],
                        -(self.outer_rec.height / 4 + 10) * cos, -(self.outer_rec.height / 4 + 10) * sin)

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
        self.wepon_rec = pygame.Rect(center_w[0] - self.wepon_rec.width / 2, center_w[1] - self.wepon_rec.height / 2,
                                     self.s_wepon.get_width(), self.s_wepon.get_height())

        front_w = (center_w[0] - int(self.s_wepon.get_width() / 2 * math.sin(math.radians(rt_w + 90))),
                   center_w[1] - int(self.s_wepon.get_height() / 2 * math.cos(math.radians(rt_w + 90))))
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

        # self.map_rec = self.buildRecMap(rt_t)
        self.help1_rec = self.buildRec(rt_t)
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

            s_shot = shot[int(fire_count)]

            shot_rec = pygame.Rect(coords[0] - int(s_shot.get_width() / 2) - 5,
                                   coords[1] - int(s_shot.get_height() / 2),
                                   s_shot.get_width(), s_shot.get_height())

            drawrec(shot_rec)
            r_shot = pygame.transform.rotate(s_shot, rt_s + 90)

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


player = Tank()

only_files = [files for files in listdir("sprites") if isfile(join("sprites", files))]
exhaust = []
shot = []
tutorialSheets = []

for myfile in only_files:
    if "Exhaust_02" in myfile:
        img = pygame.image.load("sprites/" + myfile)
        exhaust.append(pygame.transform.scale(img, (200, 200)))
    elif "Shot_A" in myfile:
        shot.append(pygame.image.load("sprites/" + myfile))
    # TODO: elif für tutorial Bilder
    elif "Explosion" in myfile:
        tutorialSheets.append(pygame.image.load("sprites/" + myfile))


def exhaust_(coords=tank_polygon.get("t4")):
    global frame
    if frame + 1 >= 9:
        frame = 0

    if move_right:
        screen.blit(exhaust[frame], coords)
        frame += 1

    pygame.display.update()


def game():
    rt = 0
    rot_speed = 2
    global fire

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
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_ESCAPE:
                    return

        rt = (rt + rot_speed) % 360
        # rt = 0
        player.draw(rt, -rt, fire)

        exhaust_()

        pygame.display.flip()
        clock.tick(60)


def play_tutorial():
    sheet = 0
    next_btn = pygame.Rect(displaywidth - 50, displayheight / 2, 40, 40)
    prev_btn = pygame.Rect(10, displayheight / 2, 40, 40)

    while True:
        screen.fill(c.white)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, c.dark_grey, next_btn)
        pygame.draw.rect(screen, c.dark_grey, prev_btn)

        if next_btn.right > mouse_pos[0] > next_btn.left and next_btn.top < mouse_pos[1] < next_btn.bottom:
            pygame.draw.rect(screen, c.grey, next_btn)
            next_s = True
        else:
            next_s = False
        if prev_btn.right > mouse_pos[0] > prev_btn.left and prev_btn.top < mouse_pos[1] < prev_btn.bottom:
            pygame.draw.rect(screen, c.grey, prev_btn)
            prev_s = True
        else:
            prev_s = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if next_s:
                    if sheet + 1 == len(tutorialSheets):
                        sheet = 0
                    else:
                        sheet += 1
                elif prev_s:
                    if sheet <= 0:
                        sheet = len(tutorialSheets) - 1
                    else:
                        sheet -= 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if sheet + 1 == len(tutorialSheets):
                        sheet = 0
                    else:
                        sheet += 1
                if event.key == pygame.K_LEFT:
                    if sheet <= 0:
                        sheet = len(tutorialSheets) - 1
                    else:
                        sheet -= 1

                if event.key == pygame.K_ESCAPE:
                    return

        s_sheet = pygame.transform.scale(tutorialSheets[sheet], (displaywidth, displayheight))
        screen.blit(s_sheet, (0, 0))

        pygame.display.flip()
        clock.tick(60)


def setting():
    global music_set
    # music = pygame.Rect(displaywidth-210, 10, 200, 40)
    music = pygame.Rect(displaywidth / 2 - 100, displayheight / 2, 200, 40)
    music_txt = pygame.Rect(music.left, music.top, 50, 40)
    music_sym = pygame.Rect(music.left + music_txt.width + 5, music.top, 40, 40)
    music_balken = pygame.Rect(music_sym.left + 5, music.top, 100, 40)

    while True:
        screen.fill(c.white)
        pygame.draw.rect(screen, c.dark_orange, music_sym)
        mouse_pos = pygame.mouse.get_pos()

        if music_sym.right > mouse_pos[0] > music_sym.left and music_sym.top < mouse_pos[1] < music_sym.bottom:
            pygame.draw.rect(screen, c.orange, music_sym)
            music_s = True
        else:
            music_s = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if music_s:
                    if music_set:
                        music_set = False
                    else:
                        music_set = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        if not music_set:
            pygame.draw.line(screen, c.red, music_sym.topleft, music_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, music_sym.topright, music_sym.bottomleft, 2)

        # tytel text
        my_music_font = pygame.font.Font("freesansbold.ttf", 16)
        music_surf, music_rect = text_objects("Music", my_music_font)
        music_rect.center = music_txt.center
        screen.blit(music_surf, music_rect)

        pygame.display.flip()
        clock.tick(60)


# def set_music():
#    global music_set
#
#    if music_set:
#        music_set = False
#    else:
#        music_set = True
#    print(music_set)
#    return


# ________________MENU________________
def text_objects(text="", font="", color=c.black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_menu(mouse_pos):
    tytel = pygame.Rect(displaywidth / 2 - 50, displayheight / 2 - 20, 100, 40)
    start = pygame.Rect(displaywidth / 2 - 150, displayheight / 2 + 70, 300, 50)
    tutorial = pygame.Rect(displaywidth / 2 - 125, displayheight / 2 + 145, 250, 40)
    settings = pygame.Rect(displaywidth - 50, 10, 40, 40)

    # Start-Button
    if start.right > mouse_pos[0] > start.left and start.top < mouse_pos[1] < start.bottom:
        pygame.draw.rect(screen, c.green, start)
        if pygame.mouse.get_pressed() == (True, False, False):
            game()
    else:
        pygame.draw.rect(screen, c.dark_green, start)

    # Tutorial-Button
    if tutorial.right > mouse_pos[0] > tutorial.left and tutorial.top < mouse_pos[1] < tutorial.bottom:
        pygame.draw.rect(screen, c.blue, tutorial)
        if pygame.mouse.get_pressed() == (True, False, False):
            play_tutorial()
    else:
        pygame.draw.rect(screen, c.dark_blue, tutorial)

    # Setting-Button
    if settings.right > mouse_pos[0] > settings.left and settings.top < mouse_pos[1] < settings.bottom:
        pygame.draw.rect(screen, c.yellow, settings)
        if pygame.mouse.get_pressed() == (True, False, False):
            setting()
            # set_music()
    else:
        pygame.draw.rect(screen, c.khaki, settings)

    # tytel text
    my_tytel_font = pygame.font.Font("freesansbold.ttf", 45)
    tytel_surf, tytel_rect = text_objects("NiklasUndJansGeilesGame", my_tytel_font)
    tytel_rect.center = tytel.center
    screen.blit(tytel_surf, tytel_rect)

    # start text
    my_start_font = pygame.font.Font("freesansbold.ttf", 20)
    start_surf, start_rect = text_objects("start", my_start_font)
    start_rect.center = start.center
    screen.blit(start_surf, start_rect)

    # tutorial text
    my_tutorial_font = pygame.font.Font("freesansbold.ttf", 16)
    tutorial_surf, tutorial_rect = text_objects("tutorial", my_tutorial_font)
    tutorial_rect.center = tutorial.center
    screen.blit(tutorial_surf, tutorial_rect)

    # settings text
    my_settings_font = pygame.font.Font("freesansbold.ttf", 14)
    settings_surf, settings_rect = text_objects("music", my_settings_font)
    settings_rect.center = settings.center
    screen.blit(settings_surf, settings_rect)
    settings_surf, settings_rect = text_objects("sound", my_settings_font)
    settings_rect.center = settings.center
    screen.blit(settings_surf, settings_rect)


music_set = True
sound_set = True

move_right = False
speed = 10

fire = False
fire_count = 0
frame = 0

while True:
    screen.fill(c.white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouse = pygame.mouse.get_pos()
    # setting(mouse)
    draw_menu(mouse)

    pygame.display.flip()
    clock.tick(30)
