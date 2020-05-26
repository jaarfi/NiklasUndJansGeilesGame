from os import listdir
from os.path import isfile, join

import math
import pygame
import pygame.gfxdraw
import my_color as c
displaywidth = 800
displayheight = 600
half_w = int(displaywidth / 2)
half_h = int(displayheight / 2)

pygame.init()

screen = pygame.display.set_mode((displaywidth, displayheight), 0, 32)
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
                           front_w, 10, 2)

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


def drawrec(rec, color=(255, 0, 0), i=3):
    pygame.draw.circle(screen, color, rec.center, i)
    pygame.draw.circle(screen, color, rec.topleft, i)
    pygame.draw.circle(screen, color, rec.topright, i)
    pygame.draw.circle(screen, color, rec.bottomleft, i)
    pygame.draw.circle(screen, color, rec.bottomright, i)


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
    # TODO: elif für tutorial
    # TODO: elif für counter
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
    # cont_delay = 4
    rt = 0
    rot_speed = 2
    global fire
    # start_timer = cont_delay

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()
                    # start_timer = cont_delay

        screen.fill(c.white)
        player.draw(rt, -rt, fire)

        rt = (rt + rot_speed) % 360
        # rt = 0

        # while start_timer > 0:
        #    screen.fill(c.white)
        #    player.draw(rt, -rt, fire)
        #    draw_timer(start_timer)
        #    pygame.time.delay(750)
        #    start_timer -= 1
        pygame.display.flip()
        clock.tick(60)


def draw_timer(timer):
    # TODO shot durch richtige Bilder ersetzen
    countdown = tutorialSheets[timer]
    countdown_rect = pygame.Rect(displaywidth / 4, displayheight / 4, half_w, half_h)
    s_countdown = pygame.transform.scale(countdown, (countdown_rect.width, countdown_rect.height))
    screen.blit(s_countdown, countdown_rect)
    pygame.display.flip()


def pause_menu():
    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), (128, 128, 128, 128))
    pygame.display.flip()
    pause = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    tytel = pygame.Rect(pause.left + pause.width / 2 - 50, pause.top + 20, 100, 40)
    esc = pygame.Rect(pause.left + pause.width / 2 - 50, pause.bottom - 150, 100, 40)
    restart = pygame.Rect(pause.left + pause.width / 2 - 50, pause.bottom - 100, 100, 40)
    resume = pygame.Rect(pause.left + pause.width / 2 - 50, pause.bottom - 50, 100, 40)
    settings = pygame.Rect(pause.right - 50, pause.top + 10, 40, 40)

    while True:
        pygame.draw.rect(screen, (0, 0, 255), pause)

        mouse_pos = pygame.mouse.get_pos()

        set_btn = button_action(settings, mouse_pos, c.khaki, c.yellow)
        esc_btn = button_action(esc, mouse_pos, c.dark_green, c.green)
        re_btn = button_action(restart, mouse_pos, c.dark_green, c.green)
        end_btn = button_action(resume, mouse_pos, c.dark_green, c.green)

        draw_text(32, tytel, "Pause")
        draw_text(20, restart, "restart")
        draw_text(20, esc, "quit")
        draw_text(20, resume, "resume")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_r:
                    game()
                elif event.key == pygame.K_SPACE:
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                if set_btn:
                    setting()
                elif esc_btn:
                    menu()
                elif re_btn:
                    game()
                elif end_btn:
                    return

        pygame.display.update(pause)
        clock.tick(60)


def button_action(rect, mouse_pos, c_n, c_hover):
    if rect.right > mouse_pos[0] > rect.left and rect.top < mouse_pos[1] < rect.bottom:
        pygame.draw.rect(screen, c_hover, rect)
        if pygame.mouse.get_pressed() == (True, False, False):
            return True
    else:
        pygame.draw.rect(screen, c_n, rect)
        return False


def play_tutorial():
    # TODO Bilder laden
    sheet = 0
    tytel = pygame.Rect(displaywidth / 2 - 100, 20, 200, 40)
    nextp = pygame.Rect(displaywidth - 50, displayheight / 2, 40, 40)
    prevp = pygame.Rect(10, displayheight / 2, 40, 40)
    esc = pygame.Rect(10, 10, 40, 40)

    while True:
        screen.fill(c.white)
        mouse_pos = pygame.mouse.get_pos()

        nxt_btn = button_action(nextp, mouse_pos, c.dark_gray, c.gray)
        prv_btn = button_action(prevp, mouse_pos, c.dark_gray, c.gray)
        esc_btn = button_action(esc, mouse_pos, c.dark_red, c.red)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if nxt_btn:
                    if sheet + 1 == len(tutorialSheets):
                        sheet = 0
                    else:
                        sheet += 1
                elif prv_btn:
                    if sheet <= 0:
                        sheet = len(tutorialSheets) - 1
                    else:
                        sheet -= 1
                elif esc_btn:
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if sheet + 1 == len(tutorialSheets):
                        sheet = 0
                    else:
                        sheet += 1
                elif event.key == pygame.K_LEFT:
                    if sheet <= 0:
                        sheet = len(tutorialSheets) - 1
                    else:
                        sheet -= 1

                elif event.key == pygame.K_ESCAPE:
                    return

        s_sheet = pygame.transform.scale(tutorialSheets[sheet], (displaywidth, displayheight))
        screen.blit(s_sheet, (0, 0))

        # tytel text
        draw_text(32, tytel, "Tutorial")

        pygame.display.flip()
        clock.tick(60)


def setting(m=0):
    if m:
        pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), (128, 128, 128, 128))
        pygame.display.flip()

    global music_set, sound_set

    settings = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    tytel = pygame.Rect(settings.left + settings.width / 2 - 50, settings.top + 20, 100, 40)
    esc = pygame.Rect(settings.left + 10, settings.top + 10, 40, 40)
    music_txt = pygame.Rect(settings.left + settings.width / 2 - 75, settings.bottom - 150, 100, 40)
    sound_txt = pygame.Rect(settings.left + settings.width / 2 - 75, settings.bottom - 100, 100, 40)
    music_sym = pygame.Rect(music_txt.right + 10, music_txt.top, 40, 40)
    sound_sym = pygame.Rect(sound_txt.right + 10, sound_txt.top, 40, 40)

    while True:
        pygame.draw.rect(screen, (0, 0, 255), settings)

        mouse_pos = pygame.mouse.get_pos()

        mus_btn = button_action(music_sym, mouse_pos, c.dark_orange, c.orange)
        sou_btn = button_action(sound_sym, mouse_pos, c.dark_orange, c.orange)
        esc_btn = button_action(esc, mouse_pos, c.dark_red, c.red)

        draw_text(32, tytel, "Settings")
        draw_text(20, music_txt, "music")
        draw_text(20, sound_txt, "sound")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if mus_btn:
                    if music_set:
                        music_set = False
                    else:
                        music_set = True
                elif sou_btn:
                    if sound_set:
                        sound_set = False
                    else:
                        sound_set = True
                elif esc_btn:
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        if not music_set:
            pygame.draw.line(screen, c.red, music_sym.topleft, music_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, music_sym.topright, music_sym.bottomleft, 2)
        if not sound_set:
            pygame.draw.line(screen, c.red, sound_sym.topleft, sound_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, sound_sym.topright, sound_sym.bottomleft, 2)

        pygame.display.update(settings)
        clock.tick(60)


def text_objects(font=("freesansbold.ttf", 12), text="",  color=c.black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(px, rect, text):
    my_text_font = pygame.font.Font("freesansbold.ttf", px)
    text_surf, text_rect = text_objects(my_text_font, text)
    text_rect.center = rect.center
    screen.blit(text_surf, text_rect)


# ________________MENU________________
music_set = True
sound_set = True

move_right = False
speed = 10

fire = False
fire_count = 0
frame = 0


def menu():

    # TODO Bilder laden
    tytel = pygame.Rect(displaywidth / 2 - 50, displayheight / 2 - 20, 100, 40)
    start = pygame.Rect(displaywidth / 2 - 100, displayheight / 2 + 70, 200, 50)
    tutorial = pygame.Rect(displaywidth / 2 - 75, displayheight / 2 + 145, 150, 40)
    settings = pygame.Rect(displaywidth - 50, 10, 40, 40)

    btn_start = btn_scale(btn_gray_out, btn_gray_in, start)
    btn_tutorial = btn_scale(btn_gray_out, btn_gray_in, tutorial)

    while True:
        screen.fill(c.white)
        mouse_pos = pygame.mouse.get_pos()

        # sta_act = button_action(start, mouse_pos, c.dark_green, c.green)
        # tut_act = button_action(tutorial, mouse_pos, c.dark_blue, c.blue)
        set_act = button_action(settings, mouse_pos, c.khaki, c.yellow)

        sta_act = button_action2(start, mouse_pos, btn_start)
        tut_act = button_action2(tutorial, mouse_pos, btn_tutorial)

        draw_text(45, tytel, "NiklasUndJansGeilesGame")
        draw_text(20, start, "start")
        draw_text(16, tutorial, "tutorial")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game()
                elif event.key == pygame.K_s:
                    setting(1)
                elif event.key == pygame.K_t:
                    play_tutorial()

            if event.type == pygame.MOUSEBUTTONUP:
                if sta_act:
                    game()
                elif set_act:
                    setting(1)
                elif tut_act:
                    play_tutorial()

        pygame.display.flip()
        clock.tick(60)


def btn_scale1(btn, rect):
    btn[0] = pygame.transform.scale(btn[0], (rect.width, rect.height))
    btn[1] = pygame.transform.scale(btn[1], (rect.width, rect.height))
    return btn


def btn_scale(btn1, btn2, rect):
    btn1 = pygame.transform.scale(btn1, (rect.width, rect.height))
    btn2 = pygame.transform.scale(btn2, (rect.width, rect.height))
    return btn1, btn2


def button_action2(rect, mouse_pos, btn):
    if rect.right > mouse_pos[0] > rect.left and rect.top < mouse_pos[1] < rect.bottom:
        screen.blit(btn[1], rect.topleft)
        if pygame.mouse.get_pressed() == (True, False, False):
            return True
    else:
        screen.blit(btn[0], rect.topleft)
        return False


btn_gray_out = pygame.image.load("pics/btn/BTN_GRAY_RECT_OUT.png")
btn_gray_in = pygame.image.load("pics/btn/BTN_GRAY_RECT_IN.png")
btn_blue_out = pygame.image.load("pics/btn/BTN_BLUE_RECT_OUT.png")
btn_blue_in = pygame.image.load("pics/btn/BTN_BLUE_RECT_IN.png")
btn_orange_out = pygame.image.load("pics/btn/BTN_ORANGE_RECT_OUT.png")
btn_orange_in = pygame.image.load("pics/btn/BTN_ORANGE_RECT_IN.png")

menu()
