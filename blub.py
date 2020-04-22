import math


def angle_tank(p):
    """
    :param p: polygon from map
    :param coords: coordination of tank bottom
    :return: angle
    """

    """
    if p is None:
        p = [(0, 2), (2, 0)]
    b_a = (p[0][0] - p[1][0], p[1][0] - p[1][1])
    b_c = (-p[1][0], -p[1][1])
    tetha = math.acos((b_a[0] * b_c[0] + b_a[1] * b_c[1]) /
                      (math.sqrt(b_a[0] * b_a[0] + b_a[1] * b_a[1]) * math.sqrt(b_c[0] * b_c[0] + b_c[1] * b_c[1])))
    tetha = math.degrees(tetha)

    if p[0][0] < p[1][0]:
        tetha += 270
    else:
        tetha += 0
    """
    angles = []

    for i in range(len(p)-1):
        b_a = (p[i][0] - p[i+1][0], p[i+1][0] - p[i+1][1])
        b_c = (-p[i+1][0], -p[i+1][1])
        tetha = int(math.degrees(math.acos((b_a[0] * b_c[0] + b_a[1] * b_c[1]) /
                      (math.sqrt(b_a[0] * b_a[0] + b_a[1] * b_a[1]) *
                       math.sqrt(b_c[0] * b_c[0] + b_c[1] * b_c[1])))))

        if p[i][i] < p[i+1][i]:
            tetha += 270

        angles.append(tetha)




import pygame as py

# define constants
WIDTH = 500
HEIGHT = 500
FPS = 30

# define colors
BLACK = (0 , 0 , 0)
GREEN = (0 , 255 , 0)

# initialize pygame and create screen
py.init()
screen = py.display.set_mode((WIDTH , HEIGHT))
# for setting FPS
clock = py.time.Clock()

rot = 0
rot_speed = 2

# define a surface (RECTANGLE)
image_orig = py.Surface((100, 100))
# for making transparent background while rotating an image
# image_orig.set_colorkey(BLACK)
# fill the rectangle / surface with green color
image_orig.fill(GREEN)
# creating a copy of orignal image for smooth rotation
image = image_orig.copy()
image.set_colorkey(BLACK)
# define rect for placing the rectangle at the desired position
rect = image.get_rect()
rect.center = (WIDTH / 2, HEIGHT / 2)
# keep rotating the rectangle until running is set to False

bild = py.image.load("pics/tank/tank_model_1.png")
s_bild = py.transform.scale(bild, (100, 100))


running = True
while running:
    # set FPS
    clock.tick(FPS)
    # clear the screen every time before drawing new objects
    screen.fill(BLACK)
    # check for the exit
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # making a copy of the old center of the rectangle
    old_center = rect.center
    # defining angle of the rotation
    rot = (rot + rot_speed) % 360
    # rotating the orignal image
    bld = py.transform.rotate(s_bild, rot)
    new_image = py.transform.rotate(image_orig, rot)
    rect = new_image.get_rect()
    # set the rotated rectangle to the old center
    rect.center = old_center
    # drawing the rotated rectangle to the screen
    screen.blit(new_image, rect)
    screen.blit(bild, rect)
    # flipping the display after drawing everything
    py.display.flip()

py.quit()
