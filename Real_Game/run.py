import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Zeta Jeu de la muerta")
clock = pygame.time.Clock()

list_moving = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        
    pygame.display.flip() #update tout l'ecran
    clock.tick(60) # max 60fps pour le jeu