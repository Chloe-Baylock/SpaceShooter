import pygame
import globals

class Swing (pygame.sprite.Sprite):
  def __init__(self, gamer):
    super().__init__()
    self.gamer = gamer
    self.surf = pygame.Surface((64,64))
    self.image = pygame.image.load('sprites/184pxswing.png').convert_alpha()
    self.rect = self.image.get_rect(center = self.gamer.get_center())
    self.swing_mask = pygame.mask.from_surface(self.image)

    self.image_rot = pygame.image.load('sprites/184pxswing.png').convert_alpha()
    self.image_rot_rect = self.image_rot.get_rect(center = (300, 300))

  def get_center(self):
    
    pass

  def update(self):
    self.rect = self.image.get_rect(center = (self.gamer.get_x() + globals.size/2, self.gamer.get_y() + globals.size/2))
