from os import listdir
from os.path import isfile, join

from baseClasses import *
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import pygame.gfxdraw

import my_color as c

displaywidth = 800
displayheight = 600
half_w = int(displaywidth / 2)
half_h = int(displayheight / 2)

pygame.init()

screen = pygame.display.set_mode((displaywidth, displayheight), 0, 32)
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
x = 200
y = 200

mc1 = c.black
mc2 = c.white

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

game = Game(displaywidth, displayheight, screen, myfont)


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
                    game.startGame()
                elif event.key == pygame.K_SPACE:
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                if set_btn:
                    setting()
                elif esc_btn:
                    menu()
                elif re_btn:
                    game.startGame()
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


def text_objects(font=("freesansbold.ttf", 12), text="", color=c.black):
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
    start = pygame.Rect(displaywidth / 2 - 125, displayheight / 2 + 70, 250, 50)
    tutorial = pygame.Rect(displaywidth / 2 - 100, displayheight / 2 + 145, 200, 40)
    settings = pygame.Rect(displaywidth - 50, 10, 40, 40)

    while True:
        screen.fill(c.white)
        mouse_pos = pygame.mouse.get_pos()

        sta_act = button_action(start, mouse_pos, c.dark_green, c.green)
        tut_act = button_action(tutorial, mouse_pos, c.dark_blue, c.blue)
        set_act = button_action(settings, mouse_pos, c.khaki, c.yellow)

        draw_text(45, tytel, "NiklasUndJansGeilesGame")
        draw_text(20, start, "start")
        draw_text(16, tutorial, "tutorial")

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
