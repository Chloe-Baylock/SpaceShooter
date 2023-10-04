import math, pygame
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