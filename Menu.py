from classes.Game import *
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import pygame.gfxdraw

import my_color as c
import config

screen = config.display

displaywidth = config.displaywidth
displayheight = config.displayheight
half_w = int(displaywidth / 2)
half_h = int(displayheight / 2)

btn_big = displaywidth / 4, displayheight / 12, 3
btn_mid = displaywidth / 5, displayheight / 15, 2
btn_small = displaywidth / 8, displayheight / 15, 2
btn_cu = displayheight / 15, displayheight / 15, 2

shadow = displayheight * 0.0075

pygame.init()

# screen = pygame.display.set_mode((displaywidth, displayheight), 0, 32)
# TODO dass font nicht hier sein muss
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

game = Game(displaywidth, displayheight, screen, myfont)

theme = [c.black, (100, 100, 100, 100), c.white]
# theme = [c.blue, (128, 128, 128, 128), c.orange]
rev_theme = theme[::-1]

# _________________________________________________________________
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

only_p = [files for files in listdir("pics/btn") if isfile(join("pics/btn", files))]
bigx = []
check = []
play = []
sett = []
# ToDO responsive skale
for myfile in only_p:
    if "BIGX" in myfile:
        bigx.append(pygame.image.load("pics/btn/" + myfile))
    elif "CHECK" in myfile:
        img = pygame.image.load("pics/btn/" + myfile)
        check.append(pygame.transform.scale(img, (int(btn_cu[0]/1.2), int(btn_cu[0]/1.2))))
    elif "PLAY" in myfile:
        play.append(pygame.image.load("pics/btn/" + myfile))
    elif "SETT" in myfile:
        sett.append(pygame.image.load("pics/btn/" + myfile))


# sett = pygame.image.load("pics/btn/SYMB_SETTINGS_s.png")


class Button:
    def __init__(self, pos, cc, txt, width, height, bri):
        self.pos = pos
        self.cc = cc
        self.txt = txt
        self.bri = bri
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.shd = displayheight * 0.0075

    def draw_button(self, mouse_pos):
        pres_rect = pygame.Rect(self.rect.left + self.shd, self.rect.top + self.shd, self.rect.width, self.rect.height)

        if self.rect.right > mouse_pos[0] > self.rect.left and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pygame.draw.rect(screen, self.cc[2], pres_rect)
            pygame.draw.rect(screen, self.cc[0], pres_rect, self.bri)
            draw_text(self.txt[0], pres_rect, self.txt[1], self.cc[0])
            if pygame.mouse.get_pressed() == (True, False, False):
                return True
        else:
            pygame.draw.rect(screen, self.cc[1], pres_rect)
            pygame.draw.rect(screen, self.cc[2], self.rect)
            pygame.draw.rect(screen, self.cc[0], self.rect, self.bri)
            draw_text(self.txt[0], self.rect, self.txt[1], self.cc[0])
            return False


class CubicButton(Button):
    def __init__(self, pos, cc, pic_, txt=(0, ""), widhei=displayheight / 15, bri=2):
        super().__init__(pos, cc, txt, widhei, widhei, bri)
        self.pic_w = int(self.width/1.2)
        self.pic = self.scale_pic(pic_)

    def scale_pic(self, pic_):
        if pic_:
            pic = pygame.transform.scale(pic_, (self.pic_w, self.pic_w))
            return pic

    def rect_pic(self, rect):
        v = int((rect.width-self.pic_w)/2)
        rect = pygame.Rect(rect.left + v, rect.top + v, self.pic_w, self.pic_w)
        return rect

    def draw_button(self, mouse_pos):
        pres_rect = pygame.Rect(self.rect.left + self.shd, self.rect.top + self.shd, self.rect.width, self.rect.height)

        if self.rect.right > mouse_pos[0] > self.rect.left and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pygame.draw.rect(screen, self.cc[2], pres_rect)
            pygame.draw.rect(screen, self.cc[0], pres_rect, self.bri)
            if self.pic is not None:
                screen.blit(self.pic, self.rect_pic(pres_rect))
            if pygame.mouse.get_pressed() == (True, False, False):
                return True
        else:
            pygame.draw.rect(screen, self.cc[1], pres_rect)
            pygame.draw.rect(screen, self.cc[2], self.rect)
            pygame.draw.rect(screen, self.cc[0], self.rect, self.bri)
            if self.pic is not None:
                screen.blit(self.pic, self.rect_pic(self.rect))
            return False


class MedButton(Button):
    def __init__(self, pos, cc, txt=(20, ""), width=displaywidth / 5, height=displayheight / 15, bri=2):
        super().__init__(pos, cc, txt, width, height, bri)


class BigButton(Button):
    def __init__(self, pos, cc, txt=(20, ""), width=displaywidth / 4, height=displayheight / 13, bri=3):
        super().__init__(pos, cc, txt, width, height, bri)


def pause_menu():
    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
    pygame.display.flip()

    pause = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)
    tytel = pygame.Rect(pause.left + pause.width / 4, pause.top + pause.height / 8, pause.width / 2, pause.height / 9)

    esc = CubicButton((pause.left + btn_cu[0] / 2, pause.top + btn_cu[1] / 2), theme[::-1], bigx[0])
    settings = CubicButton((pause.right - btn_cu[0] * 1.5, pause.top + btn_cu[1] / 2), theme[::-1], sett[1])
    ex = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 4.5), theme[::-1],
                   (20, "quit"))
    re = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 3), theme[::-1],
                   (20, "restart"))
    res = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 1.5), theme[::-1],
                    (20, "resume"))

    while True:
        draw_panel(pause)

        mouse_pos = pygame.mouse.get_pos()

        esc_btn = esc.draw_button(mouse_pos)
        set_btn = settings.draw_button(mouse_pos)
        ex_btn = ex.draw_button(mouse_pos)
        re_btn = re.draw_button(mouse_pos)
        res_btn = res.draw_button(mouse_pos)

        draw_text(32, tytel, "Pause", rev_theme[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_r:
                    game.startGame()
                elif event.key == pygame.K_SPACE:
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                if set_btn:
                    setting()
                elif ex_btn:
                    menu()
                elif re_btn:
                    game.startGame()
                elif res_btn or esc_btn:
                    return

        pygame.display.update((pause.left, pause.top, pause.width + shadow, pause.height + shadow))
        clock.tick(60)


def play_tutorial():
    # TODO Bilder laden
    sheet = 0
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, 20, btn_big[0], btn_big[1])

    nextp = CubicButton((displaywidth - btn_cu[0] * 1.5, displayheight / 2), theme, play[1])
    prevp = CubicButton((btn_cu[0] / 2, displayheight / 2), theme, play[0])
    esc = CubicButton((btn_cu[0] / 2, btn_cu[1] / 2), theme, bigx[0])

    while True:
        screen.fill(theme[2])
        mouse_pos = pygame.mouse.get_pos()


        nxt_btn = nextp.draw_button(mouse_pos)
        prv_btn = prevp.draw_button(mouse_pos)
        esc_btn = esc.draw_button(mouse_pos)

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
        draw_text(32, tytel, "Tutorial", theme[0])

        pygame.display.flip()
        clock.tick(60)


def draw_panel(frame):
    b1 = displayheight / 160
    b2 = displayheight / 114
    pygame.draw.rect(screen, theme[1], (frame.left + shadow, frame.top + shadow, frame.width, frame.height))
    pygame.draw.rect(screen, theme[2], frame)
    pygame.draw.rect(screen, theme[1], (frame.left + b1, frame.top + b1, frame.width - b1 * 2, frame.height - b1 * 2))
    pygame.draw.rect(screen, theme[0], (frame.left + b2, frame.top + b2, frame.width - b2 * 2, frame.height - b2 * 2))


def setting(m=0):
    if m:
        pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
        pygame.display.flip()

    global music_set, sound_set

    settings = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    tytel = pygame.Rect(settings.left + settings.width / 4, settings.top + settings.height * 0.125,
                        settings.width / 2, settings.height / 9)

    music_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0] * 0.75,
                            settings.bottom - btn_small[1] * 3.75,
                            btn_small[0], btn_small[1])
    sound_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0] * 0.75,
                            settings.bottom - btn_small[1] * 2.5,
                            btn_small[0], btn_small[1])

    music_sym = CubicButton((music_txt.right + btn_cu[0] / 2, music_txt.top), theme[::-1], None)
    sound_sym = CubicButton((sound_txt.right + btn_cu[0] / 2, sound_txt.top), theme[::-1], None)
    esc = CubicButton((settings.left + btn_cu[0] / 2, settings.top + btn_cu[1] / 2), theme[::-1], bigx[0])



    while True:
        draw_panel(settings)
        mouse_pos = pygame.mouse.get_pos()

        mus_btn = music_sym.draw_button(mouse_pos)
        sou_btn = sound_sym.draw_button(mouse_pos)
        esc_btn = esc.draw_button(mouse_pos)

        draw_text(32, tytel, "Settings", rev_theme[0])
        draw_text(20, music_txt, "music", rev_theme[0])
        draw_text(20, sound_txt, "sound", rev_theme[0])

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

        if music_set:
            screen.blit(check[0], music_sym.rect_pic(music_sym.rect))
        if sound_set:
            screen.blit(check[0], sound_sym.rect_pic(sound_sym.rect))

        pygame.display.flip()
        # pygame.display.update((settings.left, settings.top, settings.width+shadow, settings.height+shadow))
        clock.tick(60)


def text_objects(font=("freesansbold.ttf", 12), text="", color=c.black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(px, rect, text, color=c.black):
    my_text_font = pygame.font.Font("freesansbold.ttf", px)
    text_surf, text_rect = text_objects(my_text_font, text, color)
    text_rect.center = rect.center
    screen.blit(text_surf, text_rect)


# ________________MENU________________
music_set = True
sound_set = True


def menu():
    # TODO Bilder laden
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, displayheight / 2 - btn_big[1] / 2, btn_big[0], btn_big[1])

    start = BigButton((displaywidth / 2 - btn_big[0] / 2, displayheight / 2 + btn_big[1] * 1.5), theme, (20, "start"))
    tutor = MedButton((displaywidth / 2 - btn_mid[0] / 2, displayheight / 2 + btn_big[1] * 3), theme, (20, "tutorial"))
    settings = CubicButton((displaywidth - btn_cu[0] * 1.5, btn_cu[0] / 2), theme, sett[0])

    while True:
        screen.fill(theme[2])
        mouse_pos = pygame.mouse.get_pos()

        # sta_act = button_action3(start, mouse_pos, theme, btn_big[2], start_txt)
        sta_act = start.draw_button(mouse_pos)
        tut_act = tutor.draw_button(mouse_pos)
        set_act = settings.draw_button(mouse_pos)

        draw_text(45, tytel, "NiklasUndJansGeilesGame", theme[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.startGame()
                elif event.key == pygame.K_s:
                    setting(1)
                elif event.key == pygame.K_t:
                    play_tutorial()

            if event.type == pygame.MOUSEBUTTONUP:
                if sta_act:
                    game.startGame()
                elif set_act:
                    setting(1)
                elif tut_act:
                    play_tutorial()

        pygame.display.flip()
        clock.tick(60)

# menu()
