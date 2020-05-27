from os import listdir
from os.path import isfile, join

from baseClasses import *
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import pygame.gfxdraw

import my_color as c
import start

screen = start.display

displaywidth = start.displaywidth
displayheight = start.displayheight
half_w = int(displaywidth / 2)
half_h = int(displayheight / 2)

btn_big = displaywidth / 4, displayheight / 12, 3
btn_mid = displaywidth / 5, displayheight / 15, 2
btn_small = displaywidth / 8, displayheight / 15, 2
btn_cu = displayheight / 15, displayheight / 15, 2

pygame.init()

# screen = pygame.display.set_mode((displaywidth, displayheight), 0, 32)
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

game = Game(displaywidth, displayheight, screen, myfont)

theme = [c.black, (128, 128, 128, 128), c.white]
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


def pause_menu():
    pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
    pygame.display.flip()
    pause = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    tytel = pygame.Rect(pause.left + pause.width / 4, pause.top + pause.height * 0.125,
                        pause.width / 2, pause.height / 9)
    esc = pygame.Rect(pause.left + btn_cu[0]/4, pause.top + btn_cu[1]/4, btn_cu[0], btn_cu[1])
    settings = pygame.Rect(pause.right - btn_cu[0]*1.25, pause.top + btn_cu[1]/4, btn_cu[0], btn_cu[1])
    ex = pygame.Rect(pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1]*4,
                     btn_mid[0], btn_mid[1])
    restart = pygame.Rect(pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1]*2.75,
                         btn_mid[0], btn_mid[1])
    resume = pygame.Rect(pause.left + pause.width / 2 - btn_mid[0] / 2, pause.bottom - btn_mid[1]*1.5,
                         btn_mid[0], btn_mid[1])

    restart_txt = (20, "restart")
    ex_txt = (20, "quit")
    resume_txt = (20, "resume")

    while True:
        pygame.draw.rect(screen, theme[0], pause)

        mouse_pos = pygame.mouse.get_pos()

        set_btn = button_action3(settings, mouse_pos, rev_theme, btn_cu[2])
        esc_btn = button_action3(esc, mouse_pos, rev_theme, btn_cu[2])
        ex_btn = button_action3(ex, mouse_pos, rev_theme, btn_mid[2], ex_txt)
        re_btn = button_action3(restart, mouse_pos, rev_theme, btn_mid[2], restart_txt)
        end_btn = button_action3(resume, mouse_pos, rev_theme, btn_mid[2], resume_txt)

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
                elif end_btn or esc_btn:
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
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, 20, btn_big[0], btn_big[1])
    nextp = pygame.Rect(displaywidth - btn_cu[0]*1.25, displayheight / 2, btn_cu[0], btn_cu[1])
    prevp = pygame.Rect(btn_cu[0]/4, displayheight / 2, btn_cu[0], btn_cu[1])
    esc = pygame.Rect(btn_cu[0]/4, btn_cu[1]/4, btn_cu[0], btn_cu[1])

    while True:
        screen.fill(theme[2])
        mouse_pos = pygame.mouse.get_pos()

        nxt_btn = button_action3(nextp, mouse_pos, theme, btn_cu[2])
        prv_btn = button_action3(prevp, mouse_pos, theme, btn_cu[2])
        esc_btn = button_action3(esc, mouse_pos, theme, btn_cu[2])

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


def setting(m=0):
    if m:
        pygame.gfxdraw.box(screen, (0, 0, displaywidth, displayheight), theme[1])
        pygame.display.flip()

    global music_set, sound_set

    settings = pygame.Rect(displaywidth / 5, displayheight / 5, displaywidth * 0.6, displayheight * 0.6)

    tytel = pygame.Rect(settings.left + settings.width / 4, settings.top + settings.height*0.125,
                        settings.width / 2, settings.height/9)
    esc = pygame.Rect(settings.left + btn_cu[0]*0.25, settings.top + btn_cu[1]*0.25, btn_cu[0], btn_cu[1])
    #music_txt = pygame.Rect(settings.left + settings.width / 2 - 75, settings.bottom - 150, 100, 40)
    music_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0]*0.75, settings.bottom - btn_small[1]*3.75,
                            btn_small[0], btn_small[1])
    sound_txt = pygame.Rect(settings.left + settings.width / 2 - btn_small[0]*0.75, settings.bottom - btn_small[1]*2.5,
                            btn_small[0], btn_small[1])
    music_sym = pygame.Rect(music_txt.right + btn_cu[0]*0.25, music_txt.top, btn_cu[0], btn_cu[1])
    sound_sym = pygame.Rect(sound_txt.right + btn_cu[0]*0.25, sound_txt.top, btn_cu[0], btn_cu[1])

    while True:
        pygame.draw.rect(screen, theme[0], settings)

        mouse_pos = pygame.mouse.get_pos()

        mus_btn = button_action3(music_sym, mouse_pos, rev_theme, btn_cu[2])
        sou_btn = button_action3(sound_sym, mouse_pos, rev_theme, btn_cu[2])
        esc_btn = button_action3(esc, mouse_pos, rev_theme, btn_cu[2])

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

        if not music_set:
            pygame.draw.line(screen, c.red, music_sym.topleft, music_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, music_sym.topright, music_sym.bottomleft, 2)
        if not sound_set:
            pygame.draw.line(screen, c.red, sound_sym.topleft, sound_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, sound_sym.topright, sound_sym.bottomleft, 2)

        pygame.display.update(settings)
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

move_right = False
speed = 10

fire = False
fire_count = 0
frame = 0


def button_action3(rect, mouse_pos, theme, bri, txt=(0, "")):
    pres_rect = pygame.Rect(rect.left + displayheight * 0.0075, rect.top + displayheight * 0.0075,
                            rect.width, rect.height)

    if rect.right > mouse_pos[0] > rect.left and rect.top < mouse_pos[1] < rect.bottom:
        pygame.draw.rect(screen, theme[2], pres_rect)
        pygame.draw.rect(screen, theme[0], pres_rect, bri)
        draw_text(txt[0], pres_rect, txt[1], theme[0])
        if pygame.mouse.get_pressed() == (True, False, False):
            return True
    else:
        pygame.draw.rect(screen, theme[1], pres_rect)
        pygame.draw.rect(screen, theme[2], rect)
        pygame.draw.rect(screen, theme[0], rect, bri)
        draw_text(txt[0], rect, txt[1], theme[0])
        return False


def menu(display):
    # TODO Bilder laden
    tytel = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, displayheight / 2 - btn_big[1] / 2, btn_big[0], btn_big[1])
    start = pygame.Rect(displaywidth / 2 - btn_big[0] / 2, displayheight / 2 + btn_big[1] * 1.5, btn_big[0], btn_big[1])
    tutorial = pygame.Rect(displaywidth / 2 - btn_mid[0] / 2, displayheight / 2 + btn_big[1] * 3, btn_mid[0],
                           btn_mid[1])
    settings = pygame.Rect(displaywidth - btn_cu[0] * 1.25, btn_cu[0] * 0.25, btn_cu[0], btn_cu[0])

    start_txt = (20, "start")
    tutorial_txt = (16, "tutorial")

    while True:
        screen.fill(theme[2])
        mouse_pos = pygame.mouse.get_pos()

        sta_act = button_action3(start, mouse_pos, theme, btn_big[2], start_txt)
        tut_act = button_action3(tutorial, mouse_pos, theme[::-1], btn_mid[2], tutorial_txt)
        set_act = button_action3(settings, mouse_pos, theme, btn_cu[2])

        draw_text(45, tytel, "NiklasUndJansGeilesGame", theme[0])
        # draw_text(20, start, "start", theme[0])
        # draw_text(16, tutorial, "tutorial", theme[::-1][0])

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
