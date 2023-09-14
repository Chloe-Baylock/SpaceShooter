import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

player_surf = pygame.Surface((50,50))
player_surf.fill("red")
player_rect = player_surf.get_rect(center = (300,300))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    
  screen.fill('white')

  if pygame.mouse.get_pos():
    player_rect.center = pygame.mouse.get_pos()

  screen.blit(player_surf, player_rect)
  pygame.display.update()
  clock.tick(60)



# player_mask = pygame.mask.from_surface(player_surf)
# obstacle_mask = pygame.mask.from_surface(obstacle_surf)