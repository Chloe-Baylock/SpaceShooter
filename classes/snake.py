import pygame, random
import globals
from classes import enemy

# snake enemy that eats food on the ground to grow longer


class Snake(enemy.Enemy):
  def __init__(self):
    self.x = 0
    self.y = 0

    self.speed = 3

    self.enemy_surf = pygame.Surface((globals.size, globals.size))
    self.rect = self.enemy_surf.get_rect(center = (self.x,self.y))
    self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)

    self.color = (0, 0, 255, 255)
    # red, green, blue
    # 0, 200    = green
    # 255, 125  = bright orange
    # 255, 0    = bright red

    # green -> yellow -> red


    self.enemy_surf.fill(self.color)
    self.point_x = random.randint(1, globals.width)
    self.point_y = random.randint(1, globals.height)

    self.max_hp = 10
    self.hp = self.max_hp
    self.is_invincible = False

    self.splat_img = pygame.image.load('sprites/splat.png').convert_alpha()
    self.splat_rect = self.splat_img.get_rect(center = (300,300))