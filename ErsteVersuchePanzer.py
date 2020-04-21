import pygame
import pygame.gfxdraw
import random

class Tank(object):

  '''
  Mock
  '''

  def __init__(self):
    self.rect = pygame.Rect(32, 32, 16, 16)

  def move(self, dx, dy):
    # Move each axis separately. Note that this checks for collisions both times.
    if dx != 0:
      self.move_single_axis(dx, 0)
    if dy != 0:
      self.move_single_axis(0, dy)

  def move_single_axis(self, dx, dy):
    # Move the rect
    self.rect.x += dx
    self.rect.y += dy

class Map(object):

  '''
  Placeholder
  '''
  def __init__(self):
    self.polygon = createMap(960,540)



def createMap(width,height):
  '''
  Placeholder
  :param width: Die Breite der Map die herzutellen ist
  :param height: Die Höhe der Map die herzutellen ist
  :return: ein Array aus Tpeln die den Koordinaten des Polygons der Map entpsrechen
  '''
  map = [(0,height)]
  spacing = 10
  for i in range(0,spacing+1):
    print(i)
    map.append((int(i * width/spacing), random.randint(int(height/3), int(height*2/3))))
  map.append((width, height))
  print(map)
  return map

background_colour = (0,200,255)
(width, height) = (960, 540)
pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

map = Map()
player = Tank()
clock = pygame.time.Clock()


running = True
while running:
  clock.tick(60)
  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT]:
    player.move(-2, 0)
  if key[pygame.K_RIGHT]:
    player.move(2, 0)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False


  screen.fill((0, 0, 0))
  pygame.gfxdraw.filled_polygon(screen, map.polygon, (255, 255, 255))
  pygame.draw.rect(screen, (255, 200, 0), player.rect)
  pygame.display.flip()