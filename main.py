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
# swing animation
# update hitbox with animation
# become a circle instead of a square
# combo counter
# sound effect
# fix rectangle collision mess
# enemy death splat for a few seconds
# enemy spawning


pygame.init()
clock = pygame.time.Clock()
running = True


p = player.Player()
s = swing.Swing(p)

enemy_count = []
enemy_list = []

methods.make_enemies(4, enemy_count, enemy_list)


swing_group = pygame.sprite.Group()
swing_group.add(s)
# I do not understand sprite groups just yet


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
          # e.reset()
          pass
        if event.key == pygame.K_a:
          pass
        if event.key == pygame.K_s:
          pass
        if event.key == pygame.K_ESCAPE:
          running = False

  globals.screen.fill("gray")

  if p.get_is_swinging():

    s.image_rot = pygame.transform.rotate(s.image,math.degrees(methods.get_alpha(p.get_center()[0], p.get_center()[1],mouse_pos)) - 90)
    
    # pop arc from center of player
    units = methods.unit_vector(p.get_center()[0],p.get_center()[1],mouse_pos)
    x = s.rect.center[0] + units[0] * globals.size/2
    y = s.rect.center[1] + units[1] * globals.size/2

    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))
    s.swing_mask = pygame.mask.from_surface(s.image_rot)

    for thing in enemy_list:
      offset_x2 = thing.get_x() - s.image_rot_rect.left
      offset_y2 = thing.get_y() - s.image_rot_rect.top

      #this rectangle collision is messy
      if s.image.get_rect().colliderect(thing.enemy_surf.get_rect()):
        if s.swing_mask.overlap(thing.enemy_mask,(offset_x2,offset_y2)):
          thing.reset()
          # thing.kill(enemy_list)
          p.set_is_swinging(False)

    globals.screen.blit(s.image_rot, s.image_rot_rect)
  else:
    p.move(mouse_pos)
    s.update()

  for thing in enemy_list:
    thing.move()
    


  for thing in enemy_list:
    offset_x = thing.get_x() - p.get_x()
    offset_y = thing.get_y() - p.get_y()
    if p.player_mask.overlap(thing.enemy_mask,(offset_x,offset_y)):
      p.player_surf.fill('cyan')
      break
    else:
      p.player_surf.fill('white')

  # RENDER YOUR GAME HERE
  pygame.draw.rect(globals.screen, "white", (0,0,globals.width+globals.size * 2,globals.height+globals.size * 2),globals.size)
  for thing in enemy_list:
    globals.screen.blit(thing.enemy_surf,(thing.get_x(),thing.get_y()))
  globals.screen.blit(p.player_surf,(p.get_x(),p.get_y()))
  # ^ walls, enemy, player, enemy point


  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60) / 1000

pygame.quit()