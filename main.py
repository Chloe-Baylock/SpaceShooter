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
  y = mousePos[1] - yourY

  
  if (x == 0):
    return

  alpha = math.atan(y/x)
  if x < 0:
    alpha += math.pi

  return alpha

class MainChar():
  def __init__(self):
    self.x = size
    self.y = size
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

  def center(self):
    return ((self.getX() - size/2, self.getY() - size/2))

  def swing(self, weapon):
    self.isSwinging = True
  
  def swingBody(self, mousePos):
    unitV = unitVector(self.getX(),self.getY(), mousePos)
    alpha = getAlpha(self.getX(), self.getY(), mousePos)

      # direction from MainChar in singles
      # translate to MainChar position


# if abs(alpha) < pi/2 add full to x
# if abs(alpha) < pi add full to y
# if abs(alpha) < 3pi/2 add full to x

# 0     -    1/2        1/8,2/8,3/8,4/8
    res = []
    res.append(
    (unitV[0] * 4 + self.getX()/size,
    unitV[1] * 4 + self.getY()/size)
    )


    # for k in range(0,4):
    #   for i in range(4, 8):
    #     res.append((round(unitV[0] * (i - k)) + round(self.getX()/size),
    #     round(unitV[1] * i) + round(self.getY()/size)))
         
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
    self.color = "lime"

  def getX(self):
    return self.x

  def getY(self):
    return self.y
  
  def center(self):
    return ((self.getX() - .5, self.getY() - .5))

  def reset(self):
    self.x = random.randint(1, width/size)
    self.y = random.randint(1, height/size)
    
p = MainChar()
e = Enemy()


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
          # print(p.swingBody(mousePosition))
          # print(e.getX())
          # print(e.getY())
          print(getAlpha(p.x,p.y,mousePosition))
        if event.key == pygame.K_ESCAPE:
          running = False


  # fill the screen with a color to wipe away anything from last frame
  DISPLAYSURF.fill("black")

  if p.getIsSwinging():
    alpha = -1 * getAlpha(p.getX(), p.getY(), mousePosition)
    myRectangle = pygame.Rect(p.getX() - size * 8, p.getY() - size * 8, size * 16, size * 16)
    # pygame.draw.rect(screen,"purple",myRectangle)
    pygame.draw.arc(DISPLAYSURF,"orange",myRectangle, alpha - (math.pi/9), alpha + (math.pi/9), size * 4)
    # pygame.draw.arc(screen,"orange",(x-64, y-64, 356, 356), alpha - (math.pi/6), alpha + (math.pi/6), 64)
    # x = p.swingBody(mousePosition)[0][0]
    # y = p.swingBody(mousePosition)[0][1]

    for ((x,y)) in p.swingBody(mousePosition):
      pygame.draw.rect(DISPLAYSURF, "purple",((x*size,y*size,size,size)))
    
    # pygame.draw.rect(DISPLAYSURF, "purple",((x*size,y*size,size,size)))
    if ((e.getX(), e.getY())) in p.swingBody(mousePosition):
      e.color = "gray"
    else:
      e.color = "lime"
  else:
    p.move(mousePosition)



  # RENDER YOUR GAME HERE
  pygame.draw.rect(DISPLAYSURF, "white", (p.center()[0], p.center()[1], size, size))
  pygame.draw.rect(DISPLAYSURF, e.color, (e.getX() *size, e.getY() * size, size, size))
  pygame.draw.rect(DISPLAYSURF, "white", (0,0,width+size * 2,height+size * 2),size)

  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits Fsize to 60
  dt = clock.tick(60) / 1000

pygame.quit()