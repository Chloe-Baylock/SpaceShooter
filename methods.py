import math, pygame, globals
from classes import enemy

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
    enemy_list.append(enemy_count[-1])

def paint(main_image, color):
  colored_image = pygame.Surface(main_image.get_size())
  colored_image.fill(color)

  copy_image = main_image.copy()
  copy_image.blit(colored_image,(0,0), special_flags = pygame.BLEND_MULT)
  return copy_image

# this function modifies things and returns nothing
def swing_trail(s, swing_alpha, delay, color):
  trail_alpha = math.radians(swing_alpha + s.frame_val - delay)
  mid = pop_arc(s, trail_alpha)
  s.deg8_rot = pygame.transform.rotate(s.deg8, math.degrees(trail_alpha))
  s.deg8_rot_rect = s.deg8_rot.get_rect(center = mid)
  colored = paint(s.deg8_rot, color)
  globals.screen.blit(colored, s.deg8_rot_rect)

def pop_arc(s, alpha):
  x = s.rect.center[0] + math.cos(alpha) * globals.size/2
  y = s.rect.center[1] - math.sin(alpha) * globals.size/2
  return (x,y)