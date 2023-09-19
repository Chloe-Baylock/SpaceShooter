import pygame, math
import globals, methods
from classes import *

# # people recommend against from... import* therefore I am doing this
# #---
# import classes
# from os.path import dirname, basename, isfile, join
# modules = classes.classes(join(dirname(__file__), "*.py"))
# __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
# #---

# I unfortunately cannot quite understand this. ^


# TODO:
# make enemy move



pygame.init()
clock = pygame.time.Clock()
running = True

p = player.Player()
e = enemy.Enemy()
e_2 = enemy.Enemy()
s = swing.Swing(p)

e_2.enemy_surf.fill("purple")

ls = [e, e_2]

swing_group = pygame.sprite.Group()
swing_group.add(s)

while running:

  mouse_pos = pygame.mouse.get_pos()
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        p.set_is_swinging(not p.is_swinging)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          e.reset()
        if event.key == pygame.K_a:
          print(e.get_x())
          print(e.point_x)
        if event.key == pygame.K_s:
          print(e.get_y())
          print(e.point_y)
        if event.key == pygame.K_ESCAPE:
          running = False


  # fill the screen with a color to wipe away anything from last frame
  globals.screen.fill("gray")

  if p.get_is_swinging():

    s.image_rot = pygame.transform.rotate(s.image,math.degrees(methods.get_alpha(p.get_center()[0], p.get_center()[1],mouse_pos)) - 90)
    
    # pop arc from center of player
    units = methods.unit_vector(p.get_center()[0],p.get_center()[1],mouse_pos)
    x = s.rect.center[0] + units[0] * globals.size/2
    y = s.rect.center[1] + units[1] * globals.size/2

    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))
    s.swing_mask = pygame.mask.from_surface(s.image_rot)

    for thing in ls:
      offset_x2 = thing.get_x() - s.image_rot_rect.left
      offset_y2 = thing.get_y() - s.image_rot_rect.top
      if s.swing_mask.overlap(thing.enemy_mask,(offset_x2,offset_y2)):
        thing.reset()
        p.set_is_swinging(False)

    globals.screen.blit(s.image_rot, s.image_rot_rect)
  else:
    e.enemy_surf.fill('dark green')
    p.move(mouse_pos)
    s.update()

  for thing in ls:
    thing.move()
    

  offset_x = e.get_x() - p.get_x()
  offset_y = e.get_y() - p.get_y()


  if p.player_mask.overlap(e.enemy_mask,(offset_x,offset_y)):
    p.player_surf.fill('cyan')
  else:
    p.player_surf.fill('white')

  # RENDER YOUR GAME HERE
  pygame.draw.rect(globals.screen, "white", (0,0,globals.width+globals.size * 2,globals.height+globals.size * 2),globals.size)
  for thing in ls:
    globals.screen.blit(thing.enemy_surf,(thing.get_x(),thing.get_y()))
  globals.screen.blit(p.player_surf,(p.get_x(),p.get_y()))
  # ^ walls, enemy, player, enemy point



  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60) / 1000

pygame.quit()