# Example file showing a basic pygame "game loop"
import pygame
import random
import math



# pygame setup

width = 1088
height = 736
size = 32
# things move by 32's

# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
DISPLAYSURF = pygame.display.set_mode((width + size*2, height + size*2))
# screen = pygame.display.set_mode((width, height))

pygame.init()
clock = pygame.time.Clock()
running = True




def unitVector (yourX,yourY,mousePos):
  xVec = mousePos[0] - yourX
  yVec = mousePos[1] - yourY
  hypotenuse = math.sqrt(xVec ** 2 + yVec ** 2)

  if (xVec == 0):
    #no division by 0
    return ((0,0))

  unitX = xVec/hypotenuse
  unitY = yVec/hypotenuse

  return ((unitX, unitY))

def getAlpha(yourX, yourY, mousePos):
  x = mousePos[0] - yourX
  y = -1 * (mousePos[1] - yourY)

  alpha = math.atan2(y,x)

  return alpha

class Player():
  def __init__(self):
    self.x = size
    self.y = size
    self.player_surf = pygame.Surface((size, size))
    self.player_rect = self.player_surf.get_rect(center = (300, 300))
    self.player_mask = pygame.mask.from_surface(self.player_surf)

    self.color = 'white'
    self.player_surf.fill(self.color)

    self.weapon = "fire"
    self.swingImage = pygame.Surface((40,40))
    self.isSwinging = False

  def move(self, mousePos):
    dirX = mousePos[0] - self.getX()
    dirY = mousePos[1] - self.getY()

    if abs(dirX) <= size/4 and abs(dirY) <= size/4:
      return
      # if already super close don't move

    unitMove = unitVector(self.getX(), self.getY(),mousePos)

    if (mousePos[0] and mousePos[1]):
      #check that it is not empty
      newX = self.getX() + unitMove[0] * size/4
      newY = self.getY() + unitMove[1] * size/4

      self.setX(newX)
      self.setY(newY)

  def setX(self, val):
    self.x = val

  def setY(self, val):
    self.y = val

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  def get_center(self):
    return ((self.getX() + size/2, self.getY() + size/2))

  def swing(self, weapon):
    self.isSwinging = True
  
  def swingBody(self, mousePos):
    unitV = unitVector(self.getX(),self.getY(), mousePos)
    alpha = getAlpha(self.getX(), self.getY(), mousePos)

      # direction from Player in singles
      # translate to Player position

    res = []
    res.append(
    (unitV[0] * 4 + self.getX()/size,
    unitV[1] * 4 + self.getY()/size)
    )

    return res


  def getIsSwinging(self):
    return p.isSwinging

  def setIsSwinging(self, val):
    p.isSwinging = val

class Enemy():
  def __init__(self):
    self.x = width/size
    self.x = random.randint(1, width/size)
    self.y = random.randint(1, height/size)

    self.enemy_surf = pygame.Surface((size, size))
    self.enemy_rect = self.enemy_surf.get_rect(center = (300,300))
    self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)

    self.color = "dark green"
    self.enemy_surf.fill(self.color)

  def getX(self):
    return self.x

  def getY(self):
    return self.y
  
  def center(self):
    return ((self.getX() - size/2, self.getY() - size/2))

  def reset(self):
    self.x = random.randint(1, width/size)
    self.y = random.randint(1, height/size)
    

class Swing (pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((64,64))
    self.image = pygame.image.load('sprites/semicircle.png').convert_alpha()
    self.rect = self.image.get_rect(center = p.get_center())
    self.swing_mask = pygame.mask.from_surface(self.image)

    self.image_rot = pygame.image.load('sprites/semicircle.png').convert_alpha()
    self.image_rot_rect = self.image_rot.get_rect(center = (300, 300))

  def update(self):
    self.rect = self.image.get_rect(center = (p.getX() + size/2, p.getY() + size/2))


p = Player()
e = Enemy()
s = Swing()

swing_group = pygame.sprite.Group()
swing_group.add(s)

while running:

  mousePosition = pygame.mouse.get_pos()
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      p.setIsSwinging(not p.isSwinging)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          e.reset()
        if event.key == pygame.K_a:
          pass
        if event.key == pygame.K_ESCAPE:
          running = False


  # fill the screen with a color to wipe away anything from last frame
  DISPLAYSURF.fill("gray")

  if p.getIsSwinging():
    # swing_group.draw(DISPLAYSURF)

    s.image_rot = pygame.transform.rotate(s.image,math.degrees(getAlpha(p.get_center()[0], p.get_center()[1],mousePosition)) - 90)
    
    # pop arc from center of player
    units = unitVector(p.get_center()[0],p.get_center()[1],mousePosition)
    x = s.rect.center[0] + units[0] * size/2
    y = s.rect.center[1] + units[1] * size/2

    s.image_rot_rect = s.image_rot.get_rect(center = (x,y))
    s.swing_mask = pygame.mask.from_surface(s.image_rot)

    offset_x2 = e.getX() * size - s.image_rot_rect.left
    offset_y2 = e.getY() * size - s.image_rot_rect.top
    if s.swing_mask.overlap(e.enemy_mask,(offset_x2,offset_y2)):
      e.enemy_surf.fill('orange')
    else:
      e.enemy_surf.fill('red')

    DISPLAYSURF.blit(s.image_rot, s.image_rot_rect)
  else:
    e.enemy_surf.fill('dark green')
    p.move(mousePosition)
    s.update()

  offset_x = e.getX() * size - p.getX()
  offset_y = e.getY() * size - p.getY()


  if p.player_mask.overlap(e.enemy_mask,(offset_x,offset_y)):
    p.player_surf.fill('cyan')
  else:
    p.player_surf.fill('white')



  # RENDER YOUR GAME HERE
  pygame.draw.rect(DISPLAYSURF, "white", (0,0,width+size * 2,height+size * 2),size)
  DISPLAYSURF.blit(e.enemy_surf,(e.getX() * size,e.getY() * size))
  DISPLAYSURF.blit(p.player_surf,(p.getX(),p.getY()))

  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits Fsize to 60
  dt = clock.tick(60) / 1000

pygame.quit()