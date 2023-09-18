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
    

class Swing (pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image_original = pygame.image.load('sprites/semicircle.png').convert_alpha()
    self.rect = self.image_original.get_rect(center = (300, 300))
    self.swing_mask = pygame.mask.from_surface(self.image_original)

    self.image_new = pygame.image.load('sprites/semicircle.png').convert_alpha()
    self.image_new_rect = self.image_original.get_rect(center = (300,300))


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
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False
        if event.key == pygame.K_a:
          s.image_new = pygame.transform.rotate(s.image_original, 45)
          s.image_new_rect = s.image_new.get_rect(center = (300,300))
        if event.key == pygame.K_s:
          s.image_new = pygame.transform.rotate(s.image_original, 90)
          s.image_new_rect = s.image_new.get_rect(center = (300,300))
        if event.key == pygame.K_d:
          s.image_new = pygame.transform.rotate(s.image_original, 135)
          s.image_new_rect = s.image_new.get_rect(center = (300,300))
          # if math.degrees(getAlpha(p.getX(), p.getY(), mousePosition)) > s.rot:
            # s.surf = pygame.transform.rotate(s.surf,90)

  # fill the screen with a color to wipe away anything from last frame
  
  #get mouse position
  pos = pygame.mouse.get_pos()

  #calculate turret angle
  x_dist = pos[0] - 300
  y_dist = -(pos[1] - 300)#-ve because pygame y coordinates increase down the screen
  angle = math.degrees(math.atan2(y_dist, x_dist))
  
  s.image_new = pygame.transform.rotate(s.image_original, angle - 90)
  s.image_new_rect = s.image_new.get_rect(center = (300, 300))

  DISPLAYSURF.fill("gray")
  DISPLAYSURF.blit(s.image_new,s.image_new_rect)


  # RENDER YOUR GAME HERE
  # pygame.draw.rect(DISPLAYSURF, "white", (p.center()[0], p.center()[1], size, size))
  # pygame.draw.rect(DISPLAYSURF, e.color, (e.getX() *size, e.getY() * size, size, size))
  pygame.draw.rect(DISPLAYSURF, "white", (0,0,width+size * 2,height+size * 2),size)


  # flip() the display to put your work on screen
  pygame.display.flip()

  # clock.tick(60)  # limits Fsize to 60
  dt = clock.tick(60) / 1000

pygame.quit()