import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

player_surf = pygame.Surface((50,50))
player_surf.fill("red")
player_rect = player_surf.get_rect(center = (300,300))
player_mask = pygame.mask.from_surface(player_surf)

obstacle_surf = pygame.Surface((400,400))
obstacle_surf.fill("cyan")
obstacle_rect = obstacle_surf.get_rect(center = (300,300))
obstacle_mask = pygame.mask.from_surface(obstacle_surf)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    
  screen.fill('gray')

  if pygame.mouse.get_pos():
    player_rect.center = pygame.mouse.get_pos()

  screen.blit(obstacle_surf,obstacle_rect)
  screen.blit(player_surf, player_rect)
  
  offset_x = obstacle_rect.left - player_rect.left
  offset_y = obstacle_rect.top - player_rect.top

  if player_mask.overlap(obstacle_mask,(offset_x,offset_y)):
    player_surf.fill('purple')
  else:
    player_surf.fill('red')

  pygame.display.update()
  clock.tick(60)
