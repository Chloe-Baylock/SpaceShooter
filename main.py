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
# player carries sword
# swing trail
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

methods.make_enemies(5, enemy_count, enemy_list)

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
        if p.is_swinging == False:
          p.set_is_swinging(True)
          p.swing_start = globals.ticks
          s.mouse_was = mouse_pos
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          # e.reset()
          pass
        if event.key == pygame.K_a:
          # print(p.rect)
          # print(s.rect)
          print(resting_alpha)
        if event.key == pygame.K_s:
          pass
        if event.key == pygame.K_ESCAPE:
          running = False

  globals.screen.fill("gray")

  time_diff = globals.ticks - p.swing_start
  # counts frames since beginning of swing

  # wet code

  if time_diff == 40:
    p.set_is_swinging(False)

  elif p.get_is_swinging() and time_diff <= 15:
    # every frame we will rotate the original image, then recenter it
    
    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was))
    s.image_rot = pygame.transform.rotate(s.image, swing_alpha - 90 - 60 + time_diff * 8)
    
    # pop arc from center of player
    swing_alpha_2 = math.radians(swing_alpha - 60 + time_diff * 8)
    x = s.rect.center[0] + math.cos(swing_alpha_2) * globals.size/2
    y = s.rect.center[1] - math.sin(swing_alpha_2) * globals.size/2
    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))
    s.swing_mask = pygame.mask.from_surface(s.image_rot)

    for thing in enemy_list:
      offset_x2 = thing.rect.left - s.image_rot_rect.left
      offset_y2 = thing.rect.top - s.image_rot_rect.top

      #this rectangle collision is messy
      if s.image.get_rect().colliderect(thing.enemy_surf.get_rect()):
        if s.swing_mask.overlap(thing.enemy_mask,(offset_x2,offset_y2)):
          thing.reset()
          # thing.kill(enemy_list)

    globals.screen.blit(s.image_rot, s.image_rot_rect.topleft)

    # new_image = methods.paint(s.image_rot,"cyan")
    # globals.screen.blit(new_image, s.image_rot_rect)
    # ^ this is a working way to color things

  elif p.get_is_swinging():
    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was))
    s.image_rot = pygame.transform.rotate(s.image, swing_alpha - 90 - 60 + 15 * 8)

    # pop arc from center of player
    swing_alpha_2 = math.radians(swing_alpha - 60 + 15 * 8)
    x = s.rect.center[0] + math.cos(swing_alpha_2) * globals.size/2
    y = s.rect.center[1] - math.sin(swing_alpha_2) * globals.size/2
    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))
    s.swing_mask = pygame.mask.from_surface(s.image_rot)

    for thing in enemy_list:
      offset_x2 = thing.rect.left - s.image_rot_rect.left
      offset_y2 = thing.rect.top - s.image_rot_rect.top

      #this rectangle collision is messy
      if s.image.get_rect().colliderect(thing.enemy_surf.get_rect()):
        if s.swing_mask.overlap(thing.enemy_mask,(offset_x2,offset_y2)):
          thing.reset()
          # thing.kill(enemy_list)

    globals.screen.blit(s.image_rot, s.image_rot_rect.topleft)
    

  else:
    p.move(mouse_pos)
    p.update()
    s.update()

    resting_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),mouse_pos))
    s.image_rot = pygame.transform.rotate(s.image, resting_alpha - 90 - 60)

    # pop arc from center of player
    resting_alpha_2 = math.radians(resting_alpha - 60)
    x = s.rect.center[0] + math.cos(resting_alpha_2) * globals.size/2
    y = s.rect.center[1] - math.sin(resting_alpha_2) * globals.size/2
    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))

    globals.screen.blit(s.image_rot, s.image_rot_rect)


    # globals.screen.blit(s.image_rot, s.rect)
    # i think i had to use s.image_rot_rect instead of s.rect

  for thing in enemy_list:
    thing.move()
    thing.update()
    


  for thing in enemy_list:
    offset_x = thing.rect.left - p.rect.left
    offset_y = thing.rect.top - p.rect.top
    
    if p.rect.colliderect(thing.rect):
      if p.player_mask.overlap(thing.enemy_mask,(offset_x,offset_y)):
        p.set_color('cyan')
        break
      else:
        p.set_color('white')
    else:
      p.set_color('white')

  # RENDER YOUR GAME HERE
  pygame.draw.rect(globals.screen, "white", (0,0,globals.width+globals.size * 2,globals.height+globals.size * 2),globals.size)
  for thing in enemy_list:
    globals.screen.blit(thing.enemy_surf,thing.rect.topleft)
  globals.screen.blit(p.image,p.rect.topleft)
  # ^ walls, enemy, player


  # flip() the display to put your work on screen
  pygame.display.flip()

  globals.ticks += 1

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60) / 1000

pygame.quit()