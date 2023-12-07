import pygame, random
import globals, methods



class Enemy():
  def __init__(self):
    self.x = 0
    self.y = 0

    self.speed = 3

    self.enemy_surf = pygame.Surface((globals.size, globals.size))
    self.rect = self.enemy_surf.get_rect(center = (self.x,self.y))
    self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)

    self.color = (0, 255, 0, 255)


    self.enemy_surf.fill(self.color)
    self.point_x = random.randint(1, globals.width)
    self.point_y = random.randint(1, globals.height)

    self.max_hp = 10
    self.hp = self.max_hp
    self.is_invincible = False

    self.splat_img = pygame.image.load('sprites/splat.png').convert_alpha()
    self.splat_rect = self.splat_img.get_rect(center = (300,300))

    self.particle_effect = pygame.image.load('sprites/particle_effect.png').convert_alpha()
    self.new_particle_effect = pygame.image.load('sprites/particle_effect.png').convert_alpha()

    self.particle_x = 0
    self.particle_y = 0


  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_xy(self):
    return (self.x,self.y)

  def set_x(self, val):
    self.x = val

  def set_y(self, val):
    self.y = val
  
  def get_center(self):
    return ((self.get_x() + globals.size/2, self.get_y() + globals.size/2))

  def spawn(self):
    side = random.randint(1, 4)
    self.x = random.randint(-globals.size, globals.width)
    self.y = random.randint(-globals.size, globals.height)
    if side == 1:
      self.y = -globals.size
    if side == 2:
      self.x = globals.width + globals.size
    if side == 3:
      self.y = globals.height + globals.size
    if side == 4:
      self.x = -globals.size
    
    self.point_x = random.randint(1, globals.width)
    self.point_y = random.randint(1, globals.height)

    self.enemy_surf.fill(self.color)
    self.is_invincible = False

  def move(self):
    unit_vec = methods.unit_vector(self.get_x(), self.get_y(), ((self.point_x,self.point_y)))
    if (abs(self.get_x() - self.point_x) <= self.speed and abs(self.get_y() - self.point_y) <= self.speed):
      # when you arrive, go somewhere else
      self.point_x = random.randint(1, globals.width)
      self.point_y = random.randint(1, globals.height)
    else:
      self.set_x(unit_vec[0] * self.speed + self.get_x())
      self.set_y(unit_vec[1] * self.speed + self.get_y())

  def kill(self, enemy_type, enemy_list):
    enemy_list.remove((self, enemy_type))

  def update(self):
    self.rect.center = (self.get_xy())