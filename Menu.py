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

txt_n = int(displayheight / 30)
txt_m = int(displayheight / 20)
txt_t = int(displayheight / 13)

clock = pygame.time.Clock()

back_sound = pygame.mixer.music.load(config["music"]["epic"])
pygame.mixer.music.set_volume(0.1)
music_set = True
if music_set:
    pygame.mixer.music.play(-1)

sound_set = True


def get_all_theme():
    """
    :desc: ließt die Farben aller Themes aus "config.json".
    :return: 2-dimensionales Array mit Farb-Tupeln
    """
    with open('config.json', 'r') as c:
        config = json.load(c)
    t = []
    for i in range(3):
        t.append([])
        for j in range(3):
            t[i].append(tuple(config["theme"][str(i)][str(j)]))
    return t


def get_theme():
    """
    :return: aktuelle verwendetes Theme
    """
    with open('config.json', 'r') as c:
        config = json.load(c)
    t = []
    for i in range(3):
        t.append(tuple(config["theme"][str(config["settings"]["theme"])][str(i)]))
    return t


def set_theme(index):
    """
    :desc: setzt ein neues Theme das verwendet werden soll.
    :param index: Nummer des gewählten Themes
    :return:
    """
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

"""
laden aller benötigten Icons und Bilder 
"""
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
        """
        :param pos: (x, y)-Position
        :param txt: Text der in dem Button angezeigt werden soll
        :param width: Breite
        :param height: Höhe
        :param bri: Dicke des Rahmens
        :shd: Schatten unter dem Button
        """
        self.pos = pos
        self.txt = txt
        self.bri = bri
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.shd = displayheight * 0.0075

    def draw_button(self, mouse_pos, cc):
        """
        :desc: Zeichnet den Button, seinen Schatten und dessen Text. Steht die Maus über dem Button,
         wird dieser verschoben gezeichent.
        :param mouse_pos: Position der Maus
        :param cc: Farben für Rahmen, Schatten und Innen
        :return: -True: wenn der Button gehovert und die linke Maustaste gedrückt wird(Button wird angeklickt)
                 -False: sonst
        """
        press_rect = pygame.Rect(self.rect.left + self.shd, self.rect.top + self.shd, self.rect.width, self.rect.height)

        if self.rect.right > mouse_pos[0] > self.rect.left and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pygame.draw.rect(screen, cc[2], press_rect)
            pygame.draw.rect(screen, cc[0], press_rect, self.bri)
            draw_text(self.txt[0], press_rect, self.txt[1], cc[0])
            if pygame.mouse.get_pressed() == (True, False, False):
                return True
        else:
            pygame.draw.rect(screen, cc[1], press_rect)
            pygame.draw.rect(screen, cc[2], self.rect)
            pygame.draw.rect(screen, cc[0], self.rect, self.bri)
            draw_text(self.txt[0], self.rect, self.txt[1], cc[0])
            return False


class CubicButton(Button):
    """
    :desc: erzeugt einen quadratischen Button mit evtl. Icons.
    """
    def __init__(self, pos, pic_, txt=(0, ""), widhei=displayheight / 15, bri=2):
        """
        :param pos: (x, y)-Position
        :param pic_: Icon
        :param txt: Text wird hier nicht benutzt
        :param widhei: Breite und Höhe
        :param bri: Dicke des Rahmens
        :pic_w: Breite für Icons
        :pic: skaliertes Icon
        """
        super().__init__(pos, txt, widhei, widhei, bri)
        self.pic_w = int(self.width / 1.2)
        self.pic = self.scale_pic(pic_)

    def scale_pic(self, pic_):
        """
        :desc: wenn Button ein Icon haben soll wird es auf die richtige Größe skaliert.
        :param pic_: Icon
        :return: skaliertes Icon
        """
        if pic_:
            pic = pygame.transform.scale(pic_, (self.pic_w, self.pic_w))
            return pic

    def rect_pic(self, rect):
        """
        :desc: Um das Icon an der richtigen Stelle anzuzeigen, wird ein Quadrat erzeugt welches in der Mitte
         des Button liegt.
        :param rect: Quadrat des Button
        :return: Quadrat für Icon
        """
        v = int((rect.width - self.pic_w) / 2)
        rect = pygame.Rect(rect.left + v, rect.top + v, self.pic_w, self.pic_w)
        return rect

    def draw_button(self, mouse_pos, cc):
        """
        :desc: Zeichnet den Button und seinen Schatten. Steht die Maus über dem Button, wird dieser verschoben gezeichent
        Wird dem Button noch ein Icon übergeben wird dieses mit gezeichnet.
        :param mouse_pos: Position der Maus
        :param cc: Farben für Rahmen, Schatten und Innen
        :return: -True: wenn der Button gehovert und die linke Maustaste gedrückt wird(Button wird angeklickt)
                 -False: sonst
        """
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
    """Erzeugt einen mittel großen Button"""
    def __init__(self, pos, txt=(20, ""), width=displaywidth / 5, height=displayheight / 15, bri=2):
        super().__init__(pos, txt, width, height, bri)


class BigButton(Button):
    """Erzeugt einen großen Button"""
    def __init__(self, pos, txt=(20, ""), width=displaywidth / 4, height=displayheight / 13, bri=3):
        super().__init__(pos, txt, width, height, bri)


def draw_theme(btn, mouse_pos, cc):
    """
    :desc: Zeichnet für die Auswahl der Themes Button in der jeweiligen Farbe.
    :param btn: Button
    :param mouse_pos: Mausposition
    :param cc: Farben des Themes
    :return: -True: wenn der Button gehovert und die linke Maustaste gedrückt wird(Button wird angeklickt)
             -False: sonst
    """
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
    """
    :desc: Zeichen eines Pausen-Menus wenn das Spiel pausiert wird. Besitzt fünf Buttons:
        - "esc", "quit": Zum Hauptmenu zurückkehren
        - "restart": <c>
        - "resume": Zurück zum pausierten Spiel
        - "settings": Zu den Einstellungen
    Die Buttons werden erzeugt und dargestellt. In der While-Schleife werden permanent die Mause bzw. Tastatureingaben
    der Benutzer abgefragt. Wird ein Button gedrückt und wieder losgelassen, wird dessen Aktion ausgeführt. Die Aktionen
    können ebenfalls durch Tasten ausgelöst werden.
    :return: None
    """
    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
    pygame.display.flip()

    pause = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)
    tytel = pygame.Rect(pause.left + pause.width / 4, pause.top + pause.height / 8, pause.width / 2, pause.height / 9)

    esc = CubicButton((pause.left + btn_cu[0] / 2, pause.top + btn_cu[1] / 2), bigx[0])
    settings = CubicButton((pause.right - btn_cu[0] * 1.5, pause.top + btn_cu[1] / 2), sett[1])
    ex = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 4.5), (txt_n, "quit"))
    re = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 3), (txt_n, "restart"))
    res = MedButton((pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1] * 1.5), (txt_n, "resume"))

    while True:
        draw_panel(pause)

        mouse_pos = pygame.mouse.get_pos()

        esc_btn = esc.draw_button(mouse_pos, theme[::-1])
        set_btn = settings.draw_button(mouse_pos, theme[::-1])
        ex_btn = ex.draw_button(mouse_pos, theme[::-1])
        re_btn = re.draw_button(mouse_pos, theme[::-1])
        res_btn = res.draw_button(mouse_pos, theme[::-1])

        draw_text(txt_m, tytel, "Pause", theme[::-1][0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_r:
                    game_start()
                elif event.key == pygame.K_s:
                    setting()
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
    """
    :desc: Zeichen eines Tutorials. Besitzt drei Buttons:
        - "next": Springen zur nächsten Tutorialseite
        - "previous": Zur vorherigen springen
        - "esc": Tutorial beenden
    Die Buttons werden erzeugt und dargestellt. In der While-Schleife werden permanent die Mause bzw. Tastatureingaben
    der Benutzer abgefragt. Wird ein Button gedrückt und wieder losgelassen, wird dessen Aktion ausgeführt. Die Aktionen
    können ebenfalls durch Tasten ausgelöst werden. Die Tutorial-Informationen stehen auf Bilder, welche dargestellt
    werden.
    :return: None
    """
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
        draw_text(txt_m, tytel, "Tutorial", theme[0])

        pygame.display.flip()
        clock.tick(60)


def draw_panel(frame):
    """
    :desc: Zeichnet für das übergebene Menu, Hintergrund, Rahmen und Schatten
    :param frame: Rechteck des darzustellenden Menu
    :return: None
    """
    b1 = displayheight / 160
    b2 = displayheight / 114
    pygame.draw.rect(screen, theme[1], (frame.left + displayheight * 0.0075, frame.top + displayheight * 0.0075,
                                        frame.width, frame.height))
    pygame.draw.rect(screen, theme[2], frame)
    pygame.draw.rect(screen, theme[1], (frame.left + b1, frame.top + b1, frame.width - b1 * 2, frame.height - b1 * 2))
    pygame.draw.rect(screen, theme[0], (frame.left + b2, frame.top + b2, frame.width - b2 * 2, frame.height - b2 * 2))


def setting(m=0):
    """
    :desc: Zeichnet die Einstellungen. Besitzt einen Button:
        - "esc": Schließen der Einstellungen
    Einstellungen:
        - Music: Ein/Aus der Hintergrundmusik
        - Sound: Ein/Aus der Spieler Sounds
        (nur aus Hauptmenu abrufbar):
        - Theme: Auswahl der zur Verfügung stehenden Themes

    Der Button, bzw. die Buttons für die Einstellungen werden erzeugt und dargestellt. In der While-Schleife werden
    permanent die Mause bzw. Tastatureingaben der Benutzer abgefragt. Wird eine Einstellung angeklickt wird diese
    übernommen. Bei Musik und Sound werden globale Variablen benutzt. Eine Änderung des Themes wird in "config.json"
    gespeichert.
    :param m: Aufrufer Kennung (m=1, wenn aus Hauptmenu aufgerufen)
    :return: None
    """
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

        draw_text(txt_m, tytel, "Settings", theme[::-1][0])
        draw_text(txt_n, music_txt, "music", theme[::-1][0])
        draw_text(txt_n, sound_txt, "sound", theme[::-1][0])

        if m:
            draw_text(txt_n, theme_txt, "theme", theme[::-1][0])
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
            # des wird so dargestellt weils gut aussieht
            screen.blit(check[0], music_sym.rect_pic(music_sym.rect))
        if sound_set:
            screen.blit(check[0], sound_sym.rect_pic(sound_sym.rect))

        pygame.display.flip()
        clock.tick(60)


def text_objects(font=(config["settings"]["font"], txt_n), text="", color=theme[0]):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(px, rect, text, color=theme[0]):
    """
    :desc: Bildet ein Rechteck, in welchem der Text angezeigt wird
    :param px: Schriftgröße
    :param rect: Rechteck, welches die Position des Textes angibt
    :param text: Text
    :param color: Textfarbe
    :return: None
    """
    my_text_font = pygame.font.Font(config["settings"]["font"], px)
    text_surf, text_rect = text_objects(my_text_font, text, color)
    text_rect.center = rect.center
    screen.blit(text_surf, text_rect)


def game_start():
    """
    :desc: erzeugt eine neue Runde des Spiels
    :return: None
    """
    game = Game(displaywidth, displayheight, screen, pygame.font.SysFont(config["settings"]["font"], txt_n), theme)
    game.startGame()


def victory(player):
    """
    :desc: Zeichnet ein Endscreen. Besitzt zwei Buttons:
        - "quit": Zum Hauptmenu zurückkehren
        - "revenge": Startet eine neue Runde
    Die Buttons werden erzeugt und dargestellt. In der While-Schleife werden permanent die Mause bzw. Tastatureingaben
    der Benutzer abgefragt. Wird ein Button gedrückt und wieder losgelassen, wird dessen Aktion ausgeführt. Die Aktionen
    können ebenfalls durch Tasten ausgelöst werden. In dem Fenster wird zudem noch der Spieler spieler der gewonnen hat
    angezeigt.
    :param player: Nummer des Siegers
    :return: None
    """

    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
    pygame.display.flip()

    vic = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)
    tytel = pygame.Rect(vic.left + vic.width / 4, vic.top + vic.height / 8, vic.width / 2,
                        vic.height / 9)

    ex = MedButton((vic.left + vic.width / 2 - btn_mid[0] / 2, vic.bottom - btn_mid[1] * 3.5), (20, "quit"))
    re = MedButton((vic.left + vic.width / 2 - btn_mid[0] / 2, vic.bottom - btn_mid[1] * 2), (20, "revenge"))

    winner = "Player" + str(player) + " Victory"

    while True:
        draw_panel(vic)

        mouse_pos = pygame.mouse.get_pos()

        ex_btn = ex.draw_button(mouse_pos, theme[::-1])
        re_btn = re.draw_button(mouse_pos, theme[::-1])

        draw_text(txt_m, tytel, winner, theme[::-1][0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_r:
                    game_start()

            if event.type == pygame.MOUSEBUTTONUP:
                if ex_btn:
                    menu()
                elif re_btn:
                    game_start()

        pygame.display.flip()
        clock.tick(60)


def menu():
    """
     :desc: Zeichnet das Hauptmenu. Besitzt drei Buttons:
        - "start": Startet das Spiel
        - "turorial": Öffnet das Tutrial
        - "Settings": Öffnet die Einstellungen
    Die Buttons werden erzeugt und dargestellt. In der While-Schleife werden permanent die Mause bzw. Tastatureingaben
    der Benutzer abgefragt. Wird ein Button gedrückt und wieder losgelassen, wird dessen Aktion ausgeführt. Die Aktionen
    können ebenfalls durch Tasten ausgelöst werden.
    :return: None
    """
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, displayheight / 2 - btn_big[1] / 2, btn_big[0], btn_big[1])

    start = BigButton((displaywidth / 2 - btn_big[0] / 2, displayheight / 2 + btn_big[1] * 1.5), (txt_n, "start"))
    tutor = MedButton((displaywidth / 2 - btn_mid[0] / 2, displayheight / 2 + btn_big[1] * 3), (txt_n, "tutorial"))
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

        draw_text(txt_t, tytel, "NiklasUndJansGeilesGame", theme[2])

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
