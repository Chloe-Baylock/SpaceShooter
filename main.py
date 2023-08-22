# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class Player():
  def __init__(self):
    self.x = 0
    self.y = 0
  
  def move(self, direction):
    distance = 32
    match direction:
      case "LEFT":
        self.x -= distance
      case "RIGHT":
        self.x += distance
      case "UP":
        self.y -= distance
      case "DOWN":
        self.y += distance

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
      if event.type == pygame.KEYDOWN:
        match event.key:
          case pygame.K_a | pygame.K_LEFT:
            p.move("LEFT")
          case pygame.K_d | pygame.K_RIGHT:
            p.move("RIGHT")
          case pygame.K_w | pygame.K_UP:
            p.move("UP")
          case pygame.K_s | pygame.K_DOWN:
            p.move("DOWN")

  # fill the screen with a color to wipe away anything from last frame
  screen.fill("black")

  # RENDER YOUR GAME HERE
  pygame.draw.rect(screen, "white", (p.getX(), p.getY(), 64, 64))

  # flip() the display to put your work on screen
  pygame.display.flip()

  clock.tick(60)  # limits FPS to 60

pygame.quit()