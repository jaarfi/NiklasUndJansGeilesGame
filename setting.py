
def work_setting():
    # TODO Bilder laden
    global music_set, sound_set

    esc = pygame.Rect(10, 10, 40, 40)
    tytel = pygame.Rect(displaywidth / 2 - 100, 20, 200, 40)

    music = pygame.Rect(displaywidth / 2 - 50, displayheight / 2, 200, 40)
    music_txt = pygame.Rect(music.left, music.top, 50, 40)
    music_sym = pygame.Rect(music.left + music_txt.width + 5, music.top, 40, 40)
    sound = pygame.Rect(displaywidth / 2 - 50, displayheight / 2 + 60, 200, 40)
    sound_txt = pygame.Rect(sound.left, sound.top, 50, 40)
    sound_sym = pygame.Rect(sound.left + sound_txt.width + 5, sound.top, 40, 40)

    while True:
        screen.fill(c.white)
        pygame.draw.rect(screen, c.dark_orange, music_sym)
        pygame.draw.rect(screen, c.dark_orange, sound_sym)
        pygame.draw.rect(screen, c.dark_red, esc)

        mouse_pos = pygame.mouse.get_pos()

        if music_sym.right > mouse_pos[0] > music_sym.left and music_sym.top < mouse_pos[1] < music_sym.bottom:
            pygame.draw.rect(screen, c.orange, music_sym)
            music_s = True
        else:
            music_s = False
        if sound_sym.right > mouse_pos[0] > sound_sym.left and sound_sym.top < mouse_pos[1] < sound_sym.bottom:
            pygame.draw.rect(screen, c.orange, sound_sym)
            sound_s = True
        else:
            sound_s = False

        if esc.right > mouse_pos[0] > esc.left and esc.top < mouse_pos[1] < esc.bottom:
            pygame.draw.rect(screen, c.red, esc)
            if pygame.mouse.get_pressed() == (True, False, False):
                return

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
                if sound_s:
                    if sound_set:
                        sound_set = False
                    else:
                        sound_set = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        if not music_set:
            pygame.draw.line(screen, c.red, music_sym.topleft, music_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, music_sym.topright, music_sym.bottomleft, 2)
        if not sound_set:
            pygame.draw.line(screen, c.red, sound_sym.topleft, sound_sym.bottomright, 2)
            pygame.draw.line(screen, c.red, sound_sym.topright, sound_sym.bottomleft, 2)

        # setting text
        my_music_font = pygame.font.Font("freesansbold.ttf", 16)
        music_surf, music_rect = text_objects("Music", my_music_font)
        music_rect.center = music_txt.center
        screen.blit(music_surf, music_rect)
        sound_surf, sound_rect = text_objects("Sound", my_music_font)
        sound_rect.center = sound_txt.center
        screen.blit(sound_surf, sound_rect)

        # tytel text
        my_tytel_font = pygame.font.Font("freesansbold.ttf", 32)
        tytel_surf, tytel_rect = text_objects("Settings", my_tytel_font)
        tytel_rect.center = tytel.center
        screen.blit(tytel_surf, tytel_rect)

        pygame.display.flip()
        clock.tick(60)

def setting():
    esc = pygame.Rect(10, 10, 40, 40)
    tytel = pygame.Rect(displaywidth / 2 - 100, 20, 200, 40)


    while True:
        screen.fill(c.white)
        pygame.draw.rect(screen, c.dark_red, esc)

        mouse_pos = pygame.mouse.get_pos()

        if esc.right > mouse_pos[0] > esc.left and esc.top < mouse_pos[1] < esc.bottom:
            pygame.draw.rect(screen, c.red, esc)
            if pygame.mouse.get_pressed() == (True, False, False):
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        setting_draw()

        # tytel text
        my_tytel_font = pygame.font.Font("freesansbold.ttf", 32)
        tytel_surf, tytel_rect = text_objects("Settings", my_tytel_font)
        tytel_rect.center = tytel.center
        screen.blit(tytel_surf, tytel_rect)
        pygame.display.flip()
        clock.tick(60)


def setting_draw():
    # TODO Bilder laden
    global music_set, sound_set

    music = pygame.Rect(displaywidth / 2 - 50, displayheight / 2, 200, 40)
    music_txt = pygame.Rect(music.left, music.top, 50, 40)
    music_sym = pygame.Rect(music.left + music_txt.width + 5, music.top, 40, 40)
    sound = pygame.Rect(displaywidth / 2 - 50, displayheight / 2 + 60, 200, 40)
    sound_txt = pygame.Rect(sound.left, sound.top, 50, 40)
    sound_sym = pygame.Rect(sound.left + sound_txt.width + 5, sound.top, 40, 40)

    #while True:
    pygame.draw.rect(screen, c.dark_orange, music_sym)
    pygame.draw.rect(screen, c.dark_orange, sound_sym)

    mouse_pos = pygame.mouse.get_pos()

    if music_sym.right > mouse_pos[0] > music_sym.left and music_sym.top < mouse_pos[1] < music_sym.bottom:
        pygame.draw.rect(screen, c.orange, music_sym)

        music_hover = True
    else:
        music_hover = False
    if sound_sym.right > mouse_pos[0] > sound_sym.left and sound_sym.top < mouse_pos[1] < sound_sym.bottom:
        pygame.draw.rect(screen, c.orange, sound_sym)
        sound_hover = True
    else:
        sound_hover = False


        if music_hover:
            if music_set:
                music_set = False
            else:
                music_set = True
        if sound_hover:
            if sound_set:
                sound_set = False
            else:
                sound_set = True

    if not music_set:
        pygame.draw.line(screen, c.red, music_sym.topleft, music_sym.bottomright, 2)
        pygame.draw.line(screen, c.red, music_sym.topright, music_sym.bottomleft, 2)
    if not sound_set:
        pygame.draw.line(screen, c.red, sound_sym.topleft, sound_sym.bottomright, 2)
        pygame.draw.line(screen, c.red, sound_sym.topright, sound_sym.bottomleft, 2)

        # setting text
    my_music_font = pygame.font.Font("freesansbold.ttf", 16)
    music_surf, music_rect = text_objects("Music", my_music_font)
    music_rect.center = music_txt.center
    screen.blit(music_surf, music_rect)
    sound_surf, sound_rect = text_objects("Sound", my_music_font)
    sound_rect.center = sound_txt.center
    screen.blit(sound_surf, sound_rect)

    # pygame.display.flip()
    # clock.tick(60)