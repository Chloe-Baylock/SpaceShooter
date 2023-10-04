import pygame

class Swing (pygame.sprite.Sprite):
  def __init__(self, gamer):
    super().__init__()
    self.gamer = gamer
    self.image = pygame.image.load('sprites/sword2.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.swing_mask = pygame.mask.from_surface(self.image)

    self.image_rot = pygame.image.load('sprites/sword2.png').convert_alpha()
    self.image_rot_rect = self.image_rot.get_rect(center = (300, 300))

    self.mouse_was = (0,0)


    # self.anim_1_image = pygame.image.load('sprites/swing_anim_1.png')

  def get_center(self):
    pass

  def update(self):
    self.rect.center = (self.gamer.get_x(), self.gamer.get_y())
