import pygame, math
import globals, methods
from classes import *


# TODO:
# gas enemy
# gas + base enemy collision
# make enemy art
# give animations
# snake enemy
# make sound effects
# sword drawn later with everything else

# Bug fixes
# s.frame_val is different on a kill?

pygame.init()
clock = pygame.time.Clock()
running = True


p = player.Player()
s = swing.Swing(p)

# enemy_snake = snake.Snake()
enemy_count = []
enemy_list = []
splat_list = []
particle_list = [] # list of enemies recently hit for particle effects

methods.make_enemies(5, enemy_count, enemy_list)
methods.make_smokey(enemy_count, enemy_list)

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
    s.fading_combo_ls = [s.curr_combo, pygame.time.get_ticks()]
    s.curr_combo = 0
    p.set_is_swinging(False)
    for thing in enemy_list:
      (target, enemy_type) = thing
      target.is_invincible = False

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
      (target, enemy_type) = thing
      offset_x2 = target.rect.left - s.image_rot_rect.left
      offset_y2 = target.rect.top - s.image_rot_rect.top

      #this rectangle collision is messy
      if s.image.get_rect().colliderect(target.enemy_surf.get_rect()) and s.swing_mask.overlap(target.enemy_mask,(offset_x2,offset_y2)):
        if target.is_invincible == False:
          target.particle_alpha = -(s.alpha + s.frame_val) - 90
          particle_list.append([target,pygame.time.get_ticks()])
          target.particle_x = target.get_x()
          target.particle_y = target.get_y()
          target.is_blinking = True
          # particles

          (damage, did_crit) = p.damage_roll()
          target.hp -= damage
          target.is_invincible = True

          s.curr_combo += 1
          s.max_combo = max(s.curr_combo, s.max_combo)

          font = pygame.font.SysFont("Arial", 30)  
          if did_crit == True:
            font = pygame.font.SysFont("Arial", 40)  

          if did_crit == True:
            text_surf = font.render(str(damage), True, (255, 0, 0, 255))
          else:
            text_surf = font.render(str(damage), True, (255, 255, 0, 255))

          text_surf_rect = text_surf.get_rect(center = target.get_xy())
          p.damages.append([text_surf, text_surf_rect, pygame.time.get_ticks()])
          if target.hp > 0:
            per = target.hp/target.max_hp
            if enemy_type == 'basic':
              col = methods.color_grad(per)
              target.enemy_surf.fill(col)
              target.color = col
          elif target.hp <= 0:
            target.hp = target.max_hp
            # target.spawn()
            splat_list.append([thing, pygame.time.get_ticks()])
            target.kill(enemy_type, enemy_list)
            p.kill_count += 1
            if p.kill_count % 50 == 0:
              p.damage += 1
              print(p.damage)
          

  globals.screen.blit(s.image_rot, s.image_rot_rect)

  # splat
  for x in splat_list:
    (thing , time) = x
    (target, enemy_type) = thing
    t = pygame.time.get_ticks() - time
    duration = 1000
    if enemy_type == 'smokey':
      duration = 5000
    if t > duration:
      splat_list.remove(x)
      if enemy_type == 'smokey':
        target.splat_switch = 0

      # target.spawn()
      # target.update()
      # enemy_list.append(thing)
      # UPDATE THIS COMMENTED CODE

      pass
    else:
      target.splat_rect.center = (target.get_xy())

  # this is checking player collision and then moving the enemies 
  for thing in enemy_list:
    (target, enemy_type) = thing
    offset_x = target.rect.left - p.rect.left
    offset_y = target.rect.top - p.rect.top
    if p.rect.colliderect(target.rect) and p.player_mask.overlap(target.enemy_mask,(offset_x,offset_y)):
      p.set_color('cyan')

    target.move()
    target.update()


  # because we set color after the rotated image, we have to paint it one more time each frame.
  player_image = methods.paint(p.image_rot, p.color)



  # RENDER YOUR GAME HERE

  for (thing, time) in splat_list:
    (target, enemy_type) = thing
    img = target.splat_img
    if enemy_type == 'smokey':
      time_diff = pygame.time.get_ticks() - time
      if time_diff < 500:
        target.splat_frame = 0
      elif time_diff < 1000:
        target.splat_frame = 1
      else:
        target.splat_frame = 2 + target.splat_switch % 2
        if time_diff > 1000 + target.splat_goal:
          target.splat_switch += 1
          target.splat_goal += 750
      globals.screen.blit(img, target.splat_rect, [target.splat_frame * 64, 0, 64, 64])
    elif enemy_type == 'basic':
      globals.screen.blit(img, target.splat_rect)


  for thing in particle_list:
    (target, time) = thing
    time_diff = pygame.time.get_ticks() - time

    if time_diff >= 500:
      particle_list.remove(thing)
    elif time_diff > 375:
      target.new_particle_effect.set_alpha(75)
    elif time_diff > 250:
      target.new_particle_effect = target.new_particle_effect_3
      target.new_particle_effect.set_alpha(150)
    elif time_diff > 125:
      target.new_particle_effect.set_alpha(200)
    else:
      target.new_particle_effect = target.particle_effect

    val = -time_diff * time_diff/2000 / 16 + time_diff/8
    particle_x = target.particle_x + val * math.cos(math.radians(target.particle_alpha))
    particle_y = target.particle_y + val * math.sin(math.radians(target.particle_alpha))
    target.new_particle_effect = methods.add_paint(target.new_particle_effect, (255,255,255))
    target.new_particle_effect = methods.paint(target.new_particle_effect, (0,0,255))
    
    globals.screen.blit(target.new_particle_effect, (particle_x, particle_y - globals.size/2))

  # enemy health bars
  bar_width = 6
  for thing in enemy_list:
    (target, enemy_type) = thing
    bar_xi = target.get_x() - 30
    bar_xf = target.get_x() + 30
    bar_yi = target.get_y() + globals.size
    bar_yf = target.get_y() + globals.size
    percent_hp = target.hp / target.max_hp
    bar_length = bar_xf - bar_xi
    curr_health_x = bar_xi + percent_hp * bar_length
    pygame.draw.line(globals.screen, "black", (bar_xi - 2,bar_yi), (bar_xf + 2,bar_yf), bar_width + 4)
    pygame.draw.line(globals.screen, "red", (bar_xi,bar_yi), (bar_xf, bar_yf), bar_width)
    pygame.draw.line(globals.screen, "green", (bar_xi,bar_yi), (curr_health_x, bar_yf), bar_width)
    # border, max, curr


    if enemy_type == 'smokey':
      globals.screen.blit(target.enemy_image,target.rect.topleft)
    elif enemy_type == 'basic' and target.is_blinking == True:
      white_surf = target.enemy_surf.copy()
      white_surf.fill((255,255,255))
      globals.screen.blit(white_surf,target.rect.topleft)
      pygame.draw.rect(globals.screen,"black",target.rect, 1)
      target.is_blinking = False
    else:
      globals.screen.blit(target.enemy_surf,target.rect.topleft)
      pygame.draw.rect(globals.screen,"black",target.rect, 1)
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

  # combo text
  font = pygame.font.SysFont("Arial", 30)
  text = f"Combo: {s.curr_combo}"
  text_surf = font.render(text, True, (0, 0, 0, 255))
  text_surf_rect = text_surf.get_rect()
  text_surf_rect.right = globals.width + globals.size - 4
  text_surf_rect.bottom = globals.height + globals.size
  globals.screen.blit(text_surf, text_surf_rect)

  [val, time] = s.fading_combo_ls
  if val > 0:
    tick_diff = pygame.time.get_ticks() - time
    if tick_diff < 1500:
      fade_font = pygame.font.SysFont("Arial", 45)
      fading_text_surf = fade_font.render(f"{val}", True, (0, 100, 255))
      fading_rect = fading_text_surf.get_rect()
      fading_rect.right = globals.width + globals.size - 20
      fading_rect.bottom = globals.height + globals.size - 20
      globals.screen.blit(fading_text_surf, (fading_rect.left, fading_rect.top - tick_diff/30))
      


  # flip() the display to put your work on screen
  pygame.display.flip()

  globals.ticks += 1

  # clock.tick(60)  # limits Fglobals.size to 60
  dt = clock.tick(60)
  # dt = clock.tick(60) / 1000

pygame.quit()