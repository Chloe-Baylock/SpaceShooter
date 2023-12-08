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
    self.alpha = 0

    self.frame_val = 0
    # this tells the game where to put the sword

    self.deg8 = pygame.image.load('sprites/deg8.png').convert_alpha()
    self.deg8_rot = pygame.image.load('sprites/deg8.png').convert_alpha()
    self.deg8_rot_rect = self.deg8_rot.get_rect(center = (300,300))

    self.is_hold = False
    self.hold_alpha = 0
    self.hold_rot = None
    self.hold_rect = None


  def get_center(self):
    pass

  def update(self):
    self.rect.center = (self.gamer.get_x(), self.gamer.get_y())
