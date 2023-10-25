import math, pygame, globals
from classes import *

def unit_vector (your_x,your_y,mousePos):
  x_vector = mousePos[0] - your_x
  y_vector = mousePos[1] - your_y
  hypotenuse = math.sqrt(x_vector ** 2 + y_vector ** 2)

  unit_x = x_vector/hypotenuse
  unit_y = y_vector/hypotenuse

  return ((unit_x, unit_y))

def get_alpha(your_x, your_y, mousePos):
  x = mousePos[0] - your_x
  y = -1 * (mousePos[1] - your_y)

  alpha = math.atan2(y,x)

  return alpha

def make_enemies(num_to_make, enemy_count, enemy_list):
  for x in range(num_to_make):
    enemy_count.append(len(enemy_count))
    enemy_count[-1] = enemy.Enemy()
    enemy_list.append((enemy_count[-1], 'basic'))
    (target, enemy_type) = enemy_list[-1]
    target.spawn()


# i want to pass in a list of specs, then ... the list to give the specs to the smokey
def make_smokey(enemy_count, enemy_list):
  enemy_count.append(len(enemy_count))
  enemy_count[-1] = smokey.Smokey()
  # put specs here ^

  enemy_list.append((enemy_count[-1], 'smokey'))
  (target, enemy_type) = enemy_list[-1]
  target.spawn()


def paint(main_image, color):
  colored_image = pygame.Surface(main_image.get_size())
  colored_image.fill(color)

  copy_image = main_image.copy()
  copy_image.blit(colored_image,(0,0), special_flags = pygame.BLEND_MULT)
  return copy_image

def swing_trail(s, swing_alpha, timer, color):
  if timer >= 0 and timer <= 14:
    trail_alpha = math.radians(swing_alpha + timer * 8)
    mid = pop_arc(s, trail_alpha)
    copy = pygame.transform.rotate(s.deg8, math.degrees(trail_alpha))
    copy_rect = copy.get_rect(center = mid)
    colored_copy = paint(copy, color)
    globals.screen.blit(colored_copy, copy_rect)

def pop_arc(s, alpha):
  x = s.rect.center[0] + math.cos(alpha) * globals.size/2
  y = s.rect.center[1] - math.sin(alpha) * globals.size/2
  return (x,y)

# using LCH colors 
def color_grad(per):
  if per > .9:
    return ((0, 255, 0, 255))
  elif per > .8:
    return ((111, 237, 0, 255))
  elif per > .7:
    return ((152, 219, 0, 255))
  elif per > .6:
    return ((182, 199, 0, 255))
  elif per > .5:
    return ((205, 178, 0, 255))
  elif per > .4:
    return ((223, 155, 0, 255))
  elif per > .3:
    return ((238, 130, 0, 255))
  elif per > .2:
    return ((248, 102, 0, 255))
  elif per > .1:
    return ((254, 68, 0, 255))
  elif per > 0:
    return ((255, 0, 0, 255))
  print('error negative percent')

# rgb(0, 255, 0)
# rgb(111, 237, 0)
# rgb(152, 219, 0)
# rgb(182, 199, 0)
# rgb(205, 178, 0)
# rgb(223, 155, 0)
# rgb(238, 130, 0)
# rgb(248, 102, 0)
# rgb(254, 68, 0)
# rgb(255, 0, 0)


def spawn_food():
  red_surf = pygame.Surface(globals.size,globals.size)
  red_rect = red_surf.get_rect(center = (300, 300))
  globals.screen.blit(red_surf, red_rect)
  pass