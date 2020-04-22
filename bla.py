import pygame

WIDTH = 500
HEIGHT = 500
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bild = pygame.image.load("pics/tank/tank_model_1.png")
s_bild = pygame.transform.scale(bild, (80, 45))
# r_bild = pygame.transform.rotate(s_bild,rot)

rec = pygame.Rect(200, 200, 80, 45)

rot = 0
rot_speed = 2

while True:
    # clear the screen every time before drawing new objects
    screen.fill((255, 255, 255))
    # check for the exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    rot = (rot + rot_speed) % 360

    r_bild = pygame.transform.rotate(s_bild, 45)

    pos = (rec.center[0]-(r_bild.get_width()/2), rec.center[1])
    screen.blit(r_bild, pos)
    pygame.draw.circle(screen, (255, 0, 0), rec.center, 3)
    pygame.draw.circle(screen, (255, 0, 0), rec.topleft, 3)
    pygame.draw.circle(screen, (255, 0, 0), rec.topright, 3)
    pygame.draw.circle(screen, (255, 0, 0), rec.bottomleft, 3)
    pygame.draw.circle(screen, (255, 0, 0), rec.bottomright, 3)

    pygame.display.flip()
    clock.tick(FPS)
