# Example file showing a basic pygame "game loop"
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pixelSize = 16


class Player():
  def __init__(self):
    self.x = 0
    self.y = 0
    self.weapon = "greatSword"
    self.isSwinging = False

  def move(self, mousePos):
    dirX = mousePos[0] - self.getX()
    dirY = mousePos[1] - self.getY()

    if abs(dirX) <= pixelSize and abs(dirY) <= pixelSize:
      return

    unitMove = self.unitVector(mousePos)

    if (mousePos[0] and mousePos[1]):
      #check that it is not empty
      newX = unitMove[0] * pixelSize + self.getX()
      newY = unitMove[1] * pixelSize + self.getY()

      self.setX(newX * 1)
      self.setY(newY * 1)

  def unitVector(self, mousePos):
    x = mousePos[0] - self.getX()
    y = mousePos[1] - self.getY()
    c = math.sqrt(x ** 2 + y ** 2)

    if (x == 0):
      # no division by 0
      return ((0,0))

    unitX = x/c
    unitY = y/c

    return ((unitX, unitY))

  def setX(self, val):
    self.x = val

  def setY(self, val):
    self.y = val

  def getX(self):
    return self.x

  def getY(self):
    return self.y

  def swing(self, weapon):
    self.isSwinging = True
  
  def getIsSwinging(self):
    return p.isSwinging

  def setIsSwinging(self, val):
    p.isSwinging = val


    
p = Player()
  


while running:
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      p.setIsSwinging(True)

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  mousePosition = pygame.mouse.get_pos()
  if p.getIsSwinging():
    x = p.getX() + p.unitVector(mousePosition)[0] * pixelSize
    y = p.getY() + p.unitVector(mousePosition)[1] * pixelSize
    pygame.draw.rect(screen, "orange", (x,y, 64, 64))
  else:
    p.move(mousePosition)

  # RENDER YOUR GAME HERE
  pygame.draw.rect(screen, "white", (p.getX(), p.getY(), 64, 64))
  pygame.draw.rect(screen, "pink", (mousePosition[0],mousePosition[1], 64, 64))

  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits FPS to 60
  dt = clock.tick(60) / 1000

pygame.quit()