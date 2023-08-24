# Example file showing a basic pygame "game loop"
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class Player():
  def __init__(self):
    self.tick = 0
    self.x = 0
    self.y = 0
    self.velX = 0
    self.velY = 0
    self.accelX = 0
    self.accelY = 0

  def addTick(self, mousePos):
    if self.tick >= 0:
      self.tick = 0
      self.move(mousePos)
    else:
      self.tick += 1

  def move(self, mousePos):
    dirX = mousePos[0] - self.getX()
    dirY = mousePos[1] - self.getY()

    print((dirX, dirY))
    unitMove = self.unitVector((dirX,dirY))

    if (mousePos[0] and mousePos[1]):
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
    print(alpha)
    unitX = math.cos(alpha)
    unitY = math.sin(alpha)

    return ((unitX * 16, unitY * 16))
  
  # def move(self, direction):
  #   distance = 32
  #   match direction:
  #     case "LEFT":
  #       self.x -= distance
  #     case "RIGHT":
  #       self.x += distance
  #     case "UP":
  #       self.y -= distance
  #     case "DOWN":
  #       self.y += distance

  def accelerate(self, direction):
    match direction:
      case "LEFT":
        self.accelX = -1

      case "RIGHT":
        self.accelX = 1

      case "UP":
        self.accelY = -1

      case "DOWN":
        self.accelY = 1

  
  def decelerate(self):
    pass

  def velocity(self):
    pass

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
      # if event.type == pygame.KEYDOWN:
      #   match event.key:
      #     case pygame.K_a | pygame.K_LEFT:
      #       p.accelerate("LEFT")
      #     case pygame.K_d | pygame.K_RIGHT:
      #       p.accelerate("RIGHT")
      #     case pygame.K_w | pygame.K_UP:
      #       p.accelerate("UP")
      #     case pygame.K_s | pygame.K_DOWN:
      #       p.accelerate("DOWN")

  posTuple = pygame.mouse.get_pos()
  p.addTick(posTuple)
  # p.move(posTuple)

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  # RENDER YOUR GAME HERE
  pygame.draw.rect(screen, "white", (p.getX(), p.getY(), 64, 64))
  pygame.draw.rect(screen, "pink", (posTuple[0],posTuple[1], 64, 64))

  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits FPS to 60
  dt = clock.tick(60) / 1000

pygame.quit()