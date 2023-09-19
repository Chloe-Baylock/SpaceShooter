import pygame, random
import globals, methods



class Enemy():
  def __init__(self):
    self.x = random.randint(1, globals.width/globals.size)
    self.y = random.randint(1, globals.height/globals.size)

    self.speed = 3

    self.enemy_surf = pygame.Surface((globals.size, globals.size))
    self.enemy_rect = self.enemy_surf.get_rect(center = (300,300))
    self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)

    self.color = "dark green"
    self.enemy_surf.fill(self.color)
    self.point_x = random.randint(1, globals.width)
    self.point_y = random.randint(1, globals.height)

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def set_x(self, val):
    self.x = val

  def set_y(self, val):
    self.y = val
  
  def center(self):
    return ((self.get_x() - globals.size/2, self.get_y() - globals.size/2))

  def reset(self):
    self.x = random.randint(1, globals.width)
    self.y = random.randint(1, globals.height)
    
    self.point_x = random.randint(1, globals.width)
    self.point_y = random.randint(1, globals.height)

  def move(self):
    unit_vec = methods.unit_vector(self.get_x(), self.get_y(), ((self.point_x,self.point_y)))
    if (abs(self.get_x() - self.point_x) <= self.speed and abs(self.get_y() - self.point_y) <= self.speed):
      return
    else:
      self.set_x(unit_vec[0] * self.speed + self.get_x())
      self.set_y(unit_vec[1] * self.speed + self.get_y())