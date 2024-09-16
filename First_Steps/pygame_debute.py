import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Two Steps Ahead")#titrew
clock = pygame.time.Clock()
test_font = pygame.font.Font('First_Steps/font/Pixeltype.ttf',50)

"""
test_surface = pygame.Surface((100,200))
test_surface.fill('Red')
"""


sky_surface = pygame.image.load('First_Steps/graphics/Sky.png').convert()
ground_surface = pygame.image.load('First_Steps/graphics/ground.png').convert()
text_surface = test_font.render('Big GG', False, 'Purple')

snail_surface = pygame.image.load('First_Steps/graphics/snail/snail1.png').convert_alpha() #convert = optimise les images
snail_x_pos = 600

player_surface = pygame.image.load('First_Steps/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surface,(0,0))#pose une surface sur l'ecran du jeu
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface, (350,50))
    snail_x_pos -= 4
    if snail_x_pos < -100 :    snail_x_pos = 800
    screen.blit(snail_surface, (snail_x_pos,250))
    screen.blit(player_surface, player_rect)
            
    pygame.display.flip()
    clock.tick(60) # max 60fps pour le jeu