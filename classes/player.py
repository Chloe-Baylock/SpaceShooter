import pygame, math
import globals, methods

class Player():
  def __init__(self):
    self.x = globals.size/2
    self.y = globals.size/2
    self.original_image = pygame.image.load('sprites/circle.png').convert_alpha()
    self.image = pygame.image.load('sprites/circle.png').convert_alpha()
    self.player_surf = pygame.Surface(self.image.get_size())
    self.rect = self.image.get_rect(center = (self.x, self.y))
    self.player_mask = pygame.mask.from_surface(self.player_surf)

    self.color = 'white'
    self.player_surf.fill(self.color)

    self.weapon = "fire"
    self.swing_image = pygame.Surface((40,40))
    self.is_swinging = False

    self.swing_start = math.inf

  def move(self, mousePos):
    dirX = mousePos[0] - self.get_x()
    dirY = mousePos[1] - self.get_y()

    if abs(dirX) <= globals.size/4 and abs(dirY) <= globals.size/4:
      if abs(dirX) <= 1 and abs(dirY) <= 1:
        return
      else:
        val = 1
      return
      # if already super close don't move
    else:
      val = globals.size/4

    unitMove = methods.unit_vector(self.get_x(), self.get_y(),mousePos)

    if (mousePos[0] and mousePos[1]):
      #check that it is not empty
      newX = self.get_x() + unitMove[0] * val
      newY = self.get_y() + unitMove[1] * val

      self.set_x(newX)
      self.set_y(newY)

  def set_x(self, val):
    self.x = val

  def set_y(self, val):
    self.y = val

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_top_left(self):
    return ((self.get_x() - globals.size/2, self.get_y() - globals.size/2))

  def swing(self, weapon):
    self.isSwinging = True
  
  def swing_body(self, mousePos):
    unitV = methods.unit_vector(self.get_x(),self.get_y(), mousePos)

      # direction from Player in singles
      # translate to Player position

    res = []
    res.append(
    (unitV[0] * 4 + self.get_x()/globals.size,
    unitV[1] * 4 + self.get_y()/globals.size)
    )

    return res

  def get_is_swinging(self):
    return self.is_swinging

  def set_is_swinging(self, val):
    self.is_swinging = val

  def set_color(self, color):
    if color != self.color:
      self.image = methods.paint(self.original_image, color)
      self.color = color

  def update(self):
    self.rect.center = (self.get_x(),self.get_y())