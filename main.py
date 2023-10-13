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
  p.set_color('white')
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


  # what to do if we are not swinging our sword
  if p.get_is_swinging() == False:
    p.move(mouse_pos)
    p.update()
    player_alpha = math.degrees(methods.get_alpha(p.x, p.y,mouse_pos))
    p.image_rot = pygame.transform.rotate(p.image, player_alpha - 90)
    p.image_rot_rect = p.image_rot.get_rect(center = (p.get_x(), p.get_y()))
    
    s.update()

    resting_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),mouse_pos)) - 60
    # the alpha for not swinging we subtracted 60 from this value
    s.alpha = resting_alpha
    s.frame_val = 0


  #stop swinging after 40 frames
  elif time_diff >= 40:
    p.set_is_swinging(False)

  elif time_diff <= 15:
    # every frame we will rotate the original image, then recenter it

    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was)) - 60
    # the alpha for swinging we subtracted 60 from this value
    s.alpha = swing_alpha
    s.frame_val = time_diff * 8



    # SWING TRAIL HERE
    trail_alpha_frames = math.radians(swing_alpha + s.frame_val - 8)

    s.deg8_rot = pygame.transform.rotate(s.deg8, math.degrees(trail_alpha_frames))
    trail_x = s.rect.center[0] + math.cos(trail_alpha_frames) * globals.size/2
    trail_y = s.rect.center[1] - math.sin(trail_alpha_frames) * globals.size/2
    s.deg8_rot_rect = s.deg8_rot.get_rect(center = (trail_x,trail_y))

    globals.screen.blit(s.deg8_rot, s.deg8_rot_rect)


    trail_2_frames = math.radians(swing_alpha + s.frame_val - 16)

    s.deg8_rot = pygame.transform.rotate(s.deg8, math.degrees(trail_2_frames))
    trail_2_x = s.rect.center[0] + math.cos(trail_2_frames) * globals.size/2
    trail_2_y = s.rect.center[1] - math.sin(trail_2_frames) * globals.size/2

    s.deg8_rot_rect = s.deg8_rot.get_rect(center = (trail_2_x,trail_2_y))
    new_img = methods.paint(s.deg8_rot,(240, 240, 240, 255))
    globals.screen.blit(new_img, s.deg8_rot_rect)




    trail_3_frames = math.radians(swing_alpha + s.frame_val - 24)

    s.deg8_rot = pygame.transform.rotate(s.deg8, math.degrees(trail_3_frames))
    trail_3_x = s.rect.center[0] + math.cos(trail_3_frames) * globals.size/2
    trail_3_y = s.rect.center[1] - math.sin(trail_3_frames) * globals.size/2

    s.deg8_rot_rect = s.deg8_rot.get_rect(center = (trail_3_x,trail_3_y))
    new_img_3 = methods.paint(s.deg8_rot,(225, 225, 225, 255))
    globals.screen.blit(new_img_3, s.deg8_rot_rect)
    

    


  # make sword rest after a swing
  else:
    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was)) - 60
    # the alpha for just after swinging -60
    s.alpha = swing_alpha
    s.frame_val = 15 * 8




  s.image_rot = pygame.transform.rotate(s.image, s.alpha - 90 + s.frame_val)
  s.swing_mask = pygame.mask.from_surface(s.image_rot)




  # pop arc from center of player
  new_alpha = math.radians(s.alpha + s.frame_val)
  x = s.rect.center[0] + math.cos(new_alpha) * globals.size/2
  y = s.rect.center[1] - math.sin(new_alpha) * globals.size/2
  s.image_rot_rect = s.image_rot.get_rect(center = (x,y))



  if p.get_is_swinging():
    for thing in enemy_list:
      offset_x2 = thing.rect.left - s.image_rot_rect.left
      offset_y2 = thing.rect.top - s.image_rot_rect.top

      #this rectangle collision is messy
      if s.image.get_rect().colliderect(thing.enemy_surf.get_rect()) and s.swing_mask.overlap(thing.enemy_mask,(offset_x2,offset_y2)):
        thing.reset()
        # thing.kill(enemy_list)

  globals.screen.blit(s.image_rot, s.image_rot_rect)

  # this is checking player collision and then moving the enemies 
  for thing in enemy_list:
    offset_x = thing.rect.left - p.rect.left
    offset_y = thing.rect.top - p.rect.top
    if p.rect.colliderect(thing.rect) and p.player_mask.overlap(thing.enemy_mask,(offset_x,offset_y)):
      p.set_color('cyan')

    thing.move()
    thing.update()



  # RENDER YOUR GAME HERE


  pygame.draw.rect(globals.screen, "white", (0,0,globals.width+globals.size * 2,globals.height+globals.size * 2),globals.size)
  for thing in enemy_list:
    globals.screen.blit(thing.enemy_surf,thing.rect.topleft)
  globals.screen.blit(p.image_rot,p.image_rot_rect.topleft)
  # ^ walls, enemy, player


  # flip() the display to put your work on screen
  pygame.display.flip()

  globals.ticks += 1

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60) / 1000

pygame.quit()