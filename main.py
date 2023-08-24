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
    self.velX = 0
    self.velY = 0
    self.accelX = 0
    self.accelY = 0

  def move(self, mousePos):
    dirX = mousePos[0] - self.getX()
    dirY = mousePos[1] - self.getY()

    if abs(dirX) <= pixelSize and abs(dirY) <= pixelSize:
      print('yes')
      return

    unitMove = self.unitVector((dirX,dirY))

    if (mousePos[0] and mousePos[1]):
      #check that it is not empty
      newX = unitMove[0] + self.getX()
      newY = unitMove[1] + self.getY()

      self.setX(newX * 1)
      self.setY(newY * 1)
      
  def unitVector(self, direction):
    x = direction[0]
    y = direction[1]

    if (y == 0):
      return
    
    alpha = math.atan(y/x)
    if (x < 0 and y < 0):
      alpha += math.pi
    elif (x < 0 and y > 0):
      alpha += math.pi
    unitX = math.cos(alpha)
    unitY = math.sin(alpha)

    return ((unitX * pixelSize, unitY * pixelSize))

  def setX(self, val):
    self.x = val

  def setY(self, val):
    self.y = val

  def getX(self):
    return self.x

  def getY(self):
    return self.y
    


    
p = Player()
  


while running:
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

  mousePosition = pygame.mouse.get_pos()
  p.move(mousePosition)

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  # RENDER YOUR GAME HERE
  pygame.draw.rect(screen, "white", (p.getX(), p.getY(), 64, 64))
  pygame.draw.rect(screen, "pink", (mousePosition[0],mousePosition[1], 64, 64))

  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits FPS to 60
  dt = clock.tick(60) / 1000

pygame.quit()