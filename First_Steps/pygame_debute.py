import pygame
from sys import exit

path_for_files = "Visi301_Mathieu_Teva/First_Steps"

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Two Steps Ahead")#titrew
clock = pygame.time.Clock()
test_font = pygame.font.Font(path_for_files + '/font/Pixeltype.ttf',50)


"""
test_surf = pygame.surf((100,200))
test_surf.fill('Red')
"""


sky_surf = pygame.image.load(path_for_files + '/graphics/Sky.png').convert()
ground_surf = pygame.image.load(path_for_files + '/graphics/ground.png').convert()
text_surf = test_font.render('Big GG', False, 'Purple')

snail_surf = pygame.image.load(path_for_files + '/graphics/snail/snail1.png').convert_alpha() #convert = optimise les images
snail_rect = snail_surf.get_rect(bottomright = (600, 300))

player_surf = pygame.image.load(path_for_files + '/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300)) #assigne un rect à player un sprite où le midbottom sera aux co 80 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(sky_surf,(0,0))#pose une surface sur l'ecran du jeu
    screen.blit(ground_surf,(0,300))
    screen.blit(text_surf, (350,50))
    
    # snail_x_pos -= 4
    snail_rect.x -= 4
    if snail_rect.right < 0 :    snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)
    
    player_rect.left += 1
    screen.blit(player_surf, player_rect)
            
    pygame.display.flip() #update tout l'ecran
    clock.tick(60) # max 60fps pour le jeu