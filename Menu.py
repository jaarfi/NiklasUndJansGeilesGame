from classes.Game import *
import os
import pygame
import pygame.gfxdraw
import json

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

pygame.init()

with open('config.json', 'r') as c:
    config = json.load(c)

displaywidth = config["settings"]["displaywidth"]
displayheight = config["settings"]["displayheight"]
displayflags = config["settings"]["displayflags"]
displaycolbit = config["settings"]["displaycolbit"]

screen = pygame.display.set_mode((displaywidth, displayheight), displayflags, displaycolbit)
pygame.display.set_caption("NiklasUndJansGeilesGame")

half_w = int(displaywidth / 2)
half_h = int(displayheight / 2)

btn_big = displaywidth / 4, displayheight / 12, 3
btn_mid = displaywidth / 5, displayheight / 15, 2
btn_small = displaywidth / 8, displayheight / 15, 2
btn_cu = displayheight / 15, displayheight / 15, 2

shadow = displayheight * 0.0075


# screen = pygame.display.set_mode((displaywidth, displayheight), 0, 32)

clock = pygame.time.Clock()

back_sound = pygame.mixer.music.load("sound/music.wav.mid")
music_set = True
if music_set:
    pygame.mixer.music.play(-1)


def get_all_theme():
    with open('config.json', 'r') as c:
        config = json.load(c)
    t = []
    for i in range(3):
        t.append([])
        for j in range(3):
            t[i].append(tuple(config["theme"][str(i)][str(j)]))
    return t


def get_theme():
    with open('config.json', 'r') as c:
        config = json.load(c)
    t = []
    for i in range(3):
        t.append(tuple(config["theme"][str(config["settings"]["theme"])][str(i)]))
    return t


def set_theme(index):
    global theme
    with open('config.json', 'r+') as c:
        con = json.load(c)
        con["settings"]["theme"] = index
        c.seek(0)
        json.dump(con, c, indent=4)
        c.truncate()

    theme = get_theme()


theme = get_theme()
all_theme = get_all_theme()

# _________________________________________________________________
only_files = [files for files in listdir("pics/tutorial") if isfile(join("pics/tutorial", files))]
tutorialSheets = []

for myfile in only_files:
    if "tutorial" in myfile:
        img = pygame.image.load("pics/tutorial/" + myfile)
        tutorialSheets.append(pygame.transform.scale(img, (displayheight, displayheight)))

only_p = [files for files in listdir("pics/btn") if isfile(join("pics/btn", files))]
bigx = []
check = []
play = []
sett = []

for myfile in only_p:
    if "BIGX" in myfile:
        bigx.append(pygame.image.load("pics/btn/" + myfile))
    elif "CHECK" in myfile:
        img = pygame.image.load("pics/btn/" + myfile)
        check.append(pygame.transform.scale(img, (int(btn_cu[0] / 1.2), int(btn_cu[0] / 1.2))))
    elif "PLAY" in myfile:
        play.append(pygame.image.load("pics/btn/" + myfile))
    elif "SETT" in myfile:
        sett.append(pygame.image.load("pics/btn/" + myfile))


class Button:
    def __init__(self, pos, txt, width, height, bri):
        self.pos = pos
        self.txt = txt
        self.bri = bri
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.shd = displayheight * 0.0075

    def draw_button(self, mouse_pos, cc):
        pres_rect = pygame.Rect(self.rect.left + self.shd, self.rect.top + self.shd, self.rect.width, self.rect.height)

        if self.rect.right > mouse_pos[0] > self.rect.left and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pygame.draw.rect(screen, cc[2], pres_rect)
            pygame.draw.rect(screen, cc[0], pres_rect, self.bri)
            draw_text(self.txt[0], pres_rect, self.txt[1], cc[0])
            if pygame.mouse.get_pressed() == (True, False, False):
                return True
        else:
            pygame.draw.rect(screen, cc[1], pres_rect)
            pygame.draw.rect(screen, cc[2], self.rect)
            pygame.draw.rect(screen, cc[0], self.rect, self.bri)
            draw_text(self.txt[0], self.rect, self.txt[1], cc[0])
            return False


class CubicButton(Button):
    def __init__(self, pos, pic_, txt=(0, ""), widhei=displayheight / 15, bri=2):
        super().__init__(pos, txt, widhei, widhei, bri)
        self.pic_w = int(self.width / 1.2)
        self.pic = self.scale_pic(pic_)

    def scale_pic(self, pic_):
        if pic_:
            pic = pygame.transform.scale(pic_, (self.pic_w, self.pic_w))
            return pic

    def rect_pic(self, rect):
        v = int((rect.width - self.pic_w) / 2)
        rect = pygame.Rect(rect.left + v, rect.top + v, self.pic_w, self.pic_w)
        return rect

    def draw_button(self, mouse_pos, cc):
        pres_rect = pygame.Rect(self.rect.left + self.shd, self.rect.top + self.shd, self.rect.width, self.rect.height)

        if self.rect.right > mouse_pos[0] > self.rect.left and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pygame.draw.rect(screen, cc[2], pres_rect)
            pygame.draw.rect(screen, cc[0], pres_rect, self.bri)
            if self.pic is not None:
                screen.blit(self.pic, self.rect_pic(pres_rect))
            if pygame.mouse.get_pressed() == (True, False, False):
                return True
        else:
            pygame.draw.rect(screen, cc[1], pres_rect)
            pygame.draw.rect(screen, cc[2], self.rect)
            pygame.draw.rect(screen, cc[0], self.rect, self.bri)
            if self.pic is not None:
                screen.blit(self.pic, self.rect_pic(self.rect))
            return False


class MedButton(Button):
    def __init__(self, pos, txt=(20, ""), width=displaywidth / 5, height=displayheight / 15, bri=2):
        super().__init__(pos, txt, width, height, bri)


class BigButton(Button):
    def __init__(self, pos, txt=(20, ""), width=displaywidth / 4, height=displayheight / 13, bri=3):
        super().__init__(pos, txt, width, height, bri)


def draw_theme(btn, mouse_pos, cc):
    p_rect = pygame.Rect(btn.rect.left + btn.shd, btn.rect.top + btn.shd, btn.rect.width, btn.rect.height)

    if btn.rect.right > mouse_pos[0] > btn.rect.left and btn.rect.top < mouse_pos[1] < btn.rect.bottom:
        pygame.draw.rect(screen, cc[2], (p_rect.left, p_rect.top, p_rect.width, p_rect.height / 2))
        pygame.draw.rect(screen, cc[0], (p_rect.left, p_rect.centery, p_rect.width, p_rect.height / 2))
        if pygame.mouse.get_pressed() == (True, False, False):
            return True
    else:
        pygame.draw.rect(screen, cc[1], p_rect)
        pygame.draw.rect(screen, cc[2], (btn.rect.left, btn.rect.top, btn.rect.width, btn.rect.height / 2))
        pygame.draw.rect(screen, cc[0], (btn.rect.left, btn.rect.centery, btn.rect.width, btn.rect.height / 2))
    return False


def pause_menu():
    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
    pygame.display.flip()

    pause = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)
    tytel = pygame.Rect(pause.left + pause.width / 4, pause.top + pause.height / 8, pause.width / 2, pause.height / 9)

    esc = CubicButton((pause.left + btn_cu[0] / 2, pause.top + btn_cu[1] / 2), bigx[0])
    settings = CubicButton((pause.right - btn_cu[0] * 1.5, pause.top + btn_cu[1] / 2), sett[1])
    ex = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 4.5), (20, "quit"))
    re = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 3), (20, "restart"))
    res = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 1.5), (20, "resume"))

    while True:
        draw_panel(pause)

        mouse_pos = pygame.mouse.get_pos()

        esc_btn = esc.draw_button(mouse_pos, theme[::-1])
        set_btn = settings.draw_button(mouse_pos, theme[::-1])
        ex_btn = ex.draw_button(mouse_pos, theme[::-1])
        re_btn = re.draw_button(mouse_pos, theme[::-1])
        res_btn = res.draw_button(mouse_pos, theme[::-1])

        draw_text(32, tytel, "Pause", theme[::-1][0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_r:
                    game_start()
                elif event.key == pygame.K_SPACE:
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                if set_btn:
                    setting()
                elif ex_btn:
                    menu()
                elif re_btn:
                    game_start()
                elif res_btn or esc_btn:
                    return

        pygame.display.flip()
        clock.tick(60)


def tutorial():
    # TODO Bilder laden
    sheet = 0
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, 20, btn_big[0], btn_big[1])

    nextp = CubicButton((displaywidth - btn_cu[0] * 1.5, displayheight / 2), play[1])
    prevp = CubicButton((btn_cu[0] / 2, displayheight / 2), play[0])
    esc = CubicButton((btn_cu[0] / 2, btn_cu[1] / 2), bigx[0])

    while True:
        screen.fill(theme[2])
        mouse_pos = pygame.mouse.get_pos()

        nxt_btn = nextp.draw_button(mouse_pos, theme)
        prv_btn = prevp.draw_button(mouse_pos, theme)
        esc_btn = esc.draw_button(mouse_pos, theme)

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

        screen.blit(tutorialSheets[sheet], (displaywidth/2-tutorialSheets[sheet].get_width()/2,
                                            displayheight/2-tutorialSheets[sheet].get_height()/2))

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
    global music_set, sound_set
    fact = 0

    settings = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    if m:
        pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
        pygame.display.flip()
        fact = 2.5
        theme_rect = pygame.Rect(settings.left * 1.1, settings.bottom - settings.height * 0.4,
                                 settings.width - settings.left * 0.2, settings.height * 0.35)
        theme_txt = pygame.Rect(theme_rect.left, theme_rect.top, btn_small[0], btn_small[1])

        l = len(config["theme"])
        bx = [pygame.Rect(theme_rect.left, theme_rect.centery, 0, 0)]
        btn = []

        for i in range(1, l + 1):
            bx.append(pygame.Rect(bx[i - 1].right, bx[i - 1].top, theme_rect.width / l, btn_cu[1]))
            btn.append(CubicButton((bx[i].centerx - btn_cu[0] / 2, bx[i].centery - btn_cu[0] / 2), None))

    tytel = pygame.Rect(settings.left + settings.width / 4, settings.top + settings.height * 0.125,
                        settings.width / 2, settings.height / 9)
    music_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0] * 0.75,
                            settings.bottom - btn_small[1] * (4 + fact),
                            btn_small[0], btn_small[1])
    sound_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0] * 0.75,
                            settings.bottom - btn_small[1] * (2.5 + fact),
                            btn_small[0], btn_small[1])

    music_sym = CubicButton((music_txt.right + btn_cu[0] / 2, music_txt.top), None)
    sound_sym = CubicButton((sound_txt.right + btn_cu[0] / 2, sound_txt.top), None)
    esc = CubicButton((settings.left + btn_cu[0] / 2, settings.top + btn_cu[1] / 2), bigx[0])

    while True:
        draw_panel(settings)
        mouse_pos = pygame.mouse.get_pos()

        mus_btn = music_sym.draw_button(mouse_pos, theme[::-1])
        sou_btn = sound_sym.draw_button(mouse_pos, theme[::-1])
        esc_btn = esc.draw_button(mouse_pos, theme[::-1])

        draw_text(32, tytel, "Settings", theme[::-1][0])
        draw_text(20, music_txt, "music", theme[::-1][0])
        draw_text(20, sound_txt, "sound", theme[::-1][0])

        if m:
            draw_text(20, theme_txt, "theme", theme[::-1][0])
            theme_btn = []
            i = 0
            for a in btn:
                theme_btn.append(draw_theme(a, mouse_pos, all_theme[i]))
                i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if mus_btn:
                    if music_set:
                        music_set = False
                        pygame.mixer.music.stop()
                    else:
                        music_set = True
                        pygame.mixer.music.play(-1)
                elif sou_btn:
                    if sound_set:
                        sound_set = False
                    else:
                        sound_set = True
                elif esc_btn:
                    return
                if m:
                    i = 0
                    for b in theme_btn:
                        if b:
                            set_theme(i)
                            break
                        i += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        if music_set:
            screen.blit(check[0], music_sym.rect_pic(music_sym.rect))
        if sound_set:
            screen.blit(check[0], sound_sym.rect_pic(sound_sym.rect))

        pygame.display.flip()
        clock.tick(60)


def text_objects(font=(config["settings"]["font"], 12), text="", color=theme[0]):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(px, rect, text, color=theme[0]):
    my_text_font = pygame.font.Font(config["settings"]["font"], px)
    text_surf, text_rect = text_objects(my_text_font, text, color)
    text_rect.center = rect.center
    screen.blit(text_surf, text_rect)


def game_start():
    game = Game(displaywidth, displayheight, screen, pygame.font.SysFont(config["settings"]["font"], 30), theme)
    game.startGame()


# ________________MENU________________
sound_set = True


def victory(player):
    return


def menu():
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, displayheight / 2 - btn_big[1] / 2, btn_big[0], btn_big[1])

    start = BigButton((displaywidth / 2 - btn_big[0] / 2, displayheight / 2 + btn_big[1] * 1.5), (20, "start"))
    tutor = MedButton((displaywidth / 2 - btn_mid[0] / 2, displayheight / 2 + btn_big[1] * 3), (20, "tutorial"))
    settings = CubicButton((displaywidth - btn_cu[0] * 1.5, btn_cu[0] / 2), sett[1])

    while True:
        screen.fill(theme[0])
        pygame.gfxdraw.filled_polygon(screen, [(displaywidth, displayheight),
                                               (0, displayheight),
                                               (0, displayheight * 0.75),
                                               (displaywidth * 0.2, displayheight * 0.7),
                                               (displaywidth * 0.5, displayheight * 0.73),
                                               (displaywidth * 0.8, displayheight * 0.695),
                                               (displaywidth, displayheight * 0.5)], theme[2])
        mouse_pos = pygame.mouse.get_pos()

        sta_act = start.draw_button(mouse_pos, theme[::-1])
        tut_act = tutor.draw_button(mouse_pos, theme)
        set_act = settings.draw_button(mouse_pos, theme[::-1])

        draw_text(45, tytel, "NiklasUndJansGeilesGame", theme[2])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_start()
                elif event.key == pygame.K_s:
                    setting(1)
                elif event.key == pygame.K_t:
                    tutorial()

            if event.type == pygame.MOUSEBUTTONUP:
                if sta_act:
                    game_start()
                elif set_act:
                    setting(1)
                elif tut_act:
                    tutorial()

        pygame.display.flip()
        clock.tick(60)
