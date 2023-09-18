import pygame, random
import globals



class Enemy():
  def __init__(self):
    self.x = random.randint(1, globals.width/globals.size)
    self.y = random.randint(1, globals.height/globals.size)

    self.enemy_surf = pygame.Surface((globals.size, globals.size))
    self.enemy_rect = self.enemy_surf.get_rect(center = (300,300))
    self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)

    self.color = "dark green"
    self.enemy_surf.fill(self.color)

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y
  
  def center(self):
    return ((self.get_x() - globals.size/2, self.get_y() - globals.size/2))

  def reset(self):
    self.x = random.randint(1, globals.width/globals.size)
    self.y = random.randint(1, globals.height/globals.size)