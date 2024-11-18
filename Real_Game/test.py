import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,672))
clock = pygame.time.Clock()
fps = 60

J = pygame.Surface((50,50))
J.fill('red')
J_rect = J.get_rect()
while True:
    deltatime = clock.tick(60) * .001 * fps #stabilise les frames de l'image à 60 fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        print("hop")
        J_rect.x += 5
    if keys[pygame.K_q]:
        J_rect.x -= 5
    if keys[pygame.K_z]:
        J_rect.y += 5
    if keys[pygame.K_s]:
        J_rect.y -= 5
        
    screen.blit(J,J_rect)
    pygame.display.flip() #update tout l'ecran