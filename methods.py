import math

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
