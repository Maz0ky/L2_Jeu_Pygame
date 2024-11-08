import pygame
from mouvement import *
from liste_element import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1600, 400))  # Nouvelle taille de fenêtre
pygame.display.set_caption("Zeta Jeu de la muerta")

clock = pygame.time.Clock()
fps = 60
speed = 10

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(880, 300))  # Position initiale du joueur
player_gravity = 0

# Initialisation de la file des mouvements
ex_tab_mouv = File_mouv([])
# ex_tab_mouv = File_mouv([{"mouvement": "r", "temps": 30}, {"mouvement": "l", "temps": 3},
#                         {"mouvement": "j", "temps": 4}, {"mouvement": "l", "temps": 23}])

def bouge(mouv, rect):
    global player_gravity
    if mouv == "r":  # Droite
        rect.right += speed
    elif mouv == "l":  # Gauche
        rect.right -= speed
    elif mouv == "j":  # Saut
        player_gravity = -15

def traite_mouv(File: File_mouv, rect):
    mouv = File.get_mouv()["mouvement"]
    if File.est_ecoule():
        File.defiler_mouv()
        mouv = File.get_mouv()
    File.defiler_temps()
    bouge(mouv, rect)


### [liste_element]
# Variables de configuration initiale (générales pour une exécution persistante)

elements_fixes, elements_deplacables, selected_element, mouse_offset = initialiser_interface() # Initialisation de divers élements
button_font, button_text, button_rect = initialiser_bouton_envoi()  # Initialisation de l'interface avec les éléments
menu_visible, menu_rect, option_supprimer, option_temps, element_concerne = initialiser_menu() # Initialisation du menu (suppression et temps)
### [liste_element]

# Game loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                player_gravity = -15

        ### [liste_element]
        elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne = eventss(screen, event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne)
        ### [liste_element]

    screen.blit(sky_surf, (0, 0))  # Affichage de l'arrière-plan
    screen.blit(ground_surf, (0, 300))  # Affichage du sol
    
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
        player_gravity = 0
    else:
        player_gravity += 0.5
    
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    #     player_rect.right += speed
    # if keys[pygame.K_LEFT] or keys[pygame.K_q]:
    #     player_rect.right -= speed
    
    # Si des mouvements sont dans la file, on les traite
    if not ex_tab_mouv.est_vide():
        
        traite_mouv(ex_tab_mouv, player_rect)

    ### [liste_element]
    # Récupérer et appliquer les mouvements générés par l'interface
    selected_element, button_rect, menu_visible, menu_rect, option_supprimer, option_temps = interface_ajout_mouvements(screen, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps)
    if genere_liste_elements:  # Si des mouvements sont générés
        liste_mouvements = generer_liste_elements(elements_deplacables)  # Retourne la liste des mouvements pour l'utiliser dans Code 3
        print("Mouvements générés :", liste_mouvements)
        for mouvement in liste_mouvements:
            ex_tab_mouv.enfiler_mouv(mouvement)  # Ajoute à la file des mouvements
    ### [liste_element]

    # Afficher le joueur
    screen.blit(player_surf, player_rect)
    
    pygame.display.flip()  # Met à jour l'écran
    clock.tick(fps)  # Limite à 60 FPS