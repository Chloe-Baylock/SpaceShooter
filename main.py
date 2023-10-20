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
# sword drawn later with everything else
# combo counter
# sound effect
# enemy spawning

pygame.init()
clock = pygame.time.Clock()
running = True


p = player.Player()
s = swing.Swing(p)

enemy_snake = snake.Snake()
enemy_count = [enemy_snake]
enemy_list = [enemy_snake]
splat_list = []

print(enemy_snake.color)
print(enemy_snake.x)

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
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        p.is_holding_down = True
        if p.is_swinging == False:
          p.set_is_swinging(True)
          p.swing_start = globals.ticks
          s.mouse_was = mouse_pos
    if event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        p.is_holding_down = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          # e.spawn()
          pass
        if event.key == pygame.K_a:
          print(pygame.time.get_ticks())
        if event.key == pygame.K_s:
          pass
        if event.key == pygame.K_ESCAPE:
          running = False


  globals.screen.fill("gray")
  p.set_color('white')


  time_diff = globals.ticks - p.swing_start
  # counts frames since beginning of swing

  # generate enemies over time
  if pygame.time.get_ticks() >= globals.run_time + 5000:
    methods.make_enemies(3, enemy_count, enemy_list)
    globals.run_time += 5000

  # swing trail here
  if p.get_is_swinging() == True and time_diff <= 19:
    # check timediff vals in function
    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was)) - 60
    methods.swing_trail(s, swing_alpha, time_diff - 1, (240,240,240,255))
    methods.swing_trail(s, swing_alpha, time_diff - 2, (230,230,230,255))
    methods.swing_trail(s, swing_alpha, time_diff - 3, (220,220,220,255))
    methods.swing_trail(s, swing_alpha, time_diff - 4, (210,210,210,255))


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
    for thing in enemy_list:
      thing.is_invincible = False

    # if holding left click, swing again
    if p.is_holding_down == True:
      p.set_is_swinging(True)
      p.swing_start = globals.ticks

  elif time_diff <= 15:
    # every frame we will rotate the original image, then recenter it

    swing_alpha = math.degrees(methods.get_alpha(p.get_x(), p.get_y(),s.mouse_was)) - 60
    # the alpha for swinging we subtracted 60 from this value
    s.alpha = swing_alpha
    s.frame_val = time_diff * 8




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
        if thing.is_invincible == False:
          (damage, did_crit) = p.damage_roll()
          thing.hp -= damage
          thing.is_invincible = True

          font = pygame.font.SysFont("Arial", 30)  
          if did_crit == True:
            font = pygame.font.SysFont("Arial", 40)  

          if did_crit == True:
            text_surf = font.render(str(damage), True, (255, 0, 0, 255))
          else:
            text_surf = font.render(str(damage), True, (255, 255, 0, 255))

          text_surf_rect = text_surf.get_rect(center = thing.get_xy())
          p.damages.append([text_surf, text_surf_rect, pygame.time.get_ticks()])
          if thing.hp > 0:
            per = thing.hp/thing.max_hp
            thing.enemy_surf.fill(methods.color_grad(per))
          elif thing.hp <= 0:
            thing.hp = thing.max_hp
            # thing.spawn()
            splat_list.append([thing, pygame.time.get_ticks()])
            thing.kill(enemy_list)

  globals.screen.blit(s.image_rot, s.image_rot_rect)

  # splat
  for x in splat_list:
    (thing , time) = x
    t = pygame.time.get_ticks() - time
    if t > 1000:
      splat_list.remove(x)
      # thing.spawn()
      # thing.update()
      # enemy_list.append(thing)
      pass
    else:
      thing.splat_rect.center = (thing.get_xy())

  # this is checking player collision and then moving the enemies 
  for thing in enemy_list:
    offset_x = thing.rect.left - p.rect.left
    offset_y = thing.rect.top - p.rect.top
    if p.rect.colliderect(thing.rect) and p.player_mask.overlap(thing.enemy_mask,(offset_x,offset_y)):
      p.set_color('cyan')

    thing.move()
    thing.update()


  # because we set color after the rotated image, we have to paint it one more time each frame.
  player_image = methods.paint(p.image_rot, p.color)



  # RENDER YOUR GAME HERE

  for (thing, time) in splat_list:
    globals.screen.blit(thing.splat_img, thing.splat_rect)

  # enemy health bars
  bar_width = 6
  for thing in enemy_list:
    bar_xi = thing.get_x() - 30
    bar_xf = thing.get_x() + 30
    bar_yi = thing.get_y() + globals.size
    bar_yf = thing.get_y() + globals.size
    percent_hp = thing.hp / thing.max_hp
    bar_length = bar_xf - bar_xi
    curr_health_x = bar_xi + percent_hp * bar_length
    pygame.draw.line(globals.screen, "black", (bar_xi - 2,bar_yi), (bar_xf + 2,bar_yf), bar_width + 4)
    pygame.draw.line(globals.screen, "red", (bar_xi,bar_yi), (bar_xf, bar_yf), bar_width)
    pygame.draw.line(globals.screen, "green", (bar_xi,bar_yi), (curr_health_x, bar_yf), bar_width)
    # border, max, curr


    globals.screen.blit(thing.enemy_surf,thing.rect.topleft)
    pygame.draw.rect(globals.screen,"black",thing.rect, 1)
    # draw enemy then enemy outline


  pygame.draw.rect(globals.screen, "white", (0,0,globals.width+globals.size * 2,globals.height+globals.size * 2),globals.size)
  globals.screen.blit(player_image,p.image_rot_rect.topleft)
  # ^ walls, player


  # damage text
  for text_ls in p.damages:
    [text, text_rect, time] = text_ls
    tick_diff = pygame.time.get_ticks() - time
    if (tick_diff < 600):
      y_val = text_rect.top - (1.5 + 2 * tick_diff/800) * globals.size
      globals.screen.blit(text, (text_rect.left, y_val))
    else:
      p.damages.remove(text_ls)


  # flip() the display to put your work on screen
  pygame.display.flip()

  globals.ticks += 1

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60) / 1000

pygame.quit()