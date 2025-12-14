import pygame
from pygame.locals import *
from initialisations import *
from chargement_map import *

# Sous fonction

def levels_verifications(niveau):
    """Affiche les niveaux sur le menu des niveaux en fonction de si ils sont accessibles ou non"""
    indice = niveau - 1
    if variables_jeu["levels_info"][indice][3]:
        if variables_jeu["levels_info"][indice][2]:
            level_scaled_rect = variables_jeu["levels_info"][indice][1].inflate(variables_jeu["levels_info"][indice][1].width * 0.2, variables_jeu["levels_info"][indice][1].height * 0.2)
            pygame.draw.circle(pygame_screen["screen"], (240, 240, 240), level_scaled_rect.center, max(level_scaled_rect.width, level_scaled_rect.height) // 2 + 40)
            pygame_screen["screen"].blit(pygame.transform.scale(variables_jeu["levels_info"][indice][0], level_scaled_rect.size), level_scaled_rect)
        else:
            pygame.draw.circle(pygame_screen["screen"], (240, 240,240), variables_jeu["levels_info"][indice][1].center, max(variables_jeu["levels_info"][indice][1].width, variables_jeu["levels_info"][indice][1].height) // 2 + 40)
            pygame_screen["screen"].blit(variables_jeu["levels_info"][indice][0], variables_jeu["levels_info"][indice][1])
    else:
        if niveau != 1: 
            pygame_screen["screen"].blit(variables_jeu["levels_info"][indice][0], variables_jeu["levels_info"][indice][1])
            overlay = pygame.Surface((pygame_screen["screen"].get_width(), pygame_screen["screen"].get_height()), pygame.SRCALPHA)  # Surface transparente
            pygame.draw.circle(overlay, (100, 40, 40, 240), variables_jeu["levels_info"][indice][1].center, max(variables_jeu["levels_info"][indice][1].width, variables_jeu["levels_info"][indice][1].height) // 2 + 40)  # Cercle semi-transparent
            pygame_screen["screen"].blit(overlay, (0, 0))

# Mise a jour pages

def mise_a_jour_page_base_debut():
    # Mise à jour de l'affichage
    pygame_screen["screen"].fill((30, 30, 30))

def mise_a_jour_page_base_fin():
    pygame.display.flip()  # Met à jour l'écran
    pygame_screen["clock"].tick(pygame_screen["fps"]) * .001 * pygame_screen["fps"]  # Limite à 60 FPS

def mise_a_jour_page_end():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    pygame_screen["screen"].blit(backgrounds["fin"], (0, 0))
    pygame_screen["screen"].blit(boutons["retour_from_end"][0], boutons["retour_from_end"][1])

    mise_a_jour_page_base_fin()

def mise_a_jour_page_accueil():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    pygame_screen["screen"].blit(backgrounds["accueil"], (0, 0))
    pygame_screen["screen"].blit(boutons["start"][0], boutons["start"][1])

    mise_a_jour_page_base_fin()

def mise_a_jour_page_choix_niveau():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    pygame_screen["screen"].blit(backgrounds["menu"], (0, 0))

    for i in range(0, variables_jeu["nb_level"]):
        levels_verifications(i + 1)

    # Met à jour le bouton de retour depuis le choix des niveaux
    rect = boutons["retour_de_choixlvl"][2]
    ellipse_rect = pygame.Rect(rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20)
    pygame.draw.ellipse(pygame_screen["screen"], (211, 211, 211), ellipse_rect)
    pygame_screen["screen"].blit(boutons["retour_de_choixlvl"][1], rect)

    mise_a_jour_page_base_fin()

def mise_a_jour_page_level(elem_actuel):
    """Met à jour la page"""

    screen = pygame_screen["screen"]

    mise_a_jour_page_base_debut()

    # Calculer la largeur totale de la map
    map_largeur = max(tile.rect.right for tile in tuiles_map["sprite_group"])  # Récupérer la largeur réelle de la map
    map_hauteur = max(tile.rect.bottom for tile in tuiles_map["sprite_group"])

    # Mise à jour de la caméra
    pygame_screen["camera"].update(entites["Joueur"], map_largeur, map_hauteur)

    for tile in tuiles_map["sprite_group"]:
        pos_x, pos_y = pygame_screen["camera"].apply(tile).topleft # Récupérer la position modifiée
        screen.blit(tile.image, (pos_x, pos_y))


    # Affichage du joueur
    entites["Joueur"].show(screen, pygame_screen)
    entites["Joueur"].update(tuiles_map["block_group"], tuiles_map["fatal_group"], tuiles_map["end_group"], tuiles_map)
    if entites["Joueur"].is_dead():
        variables_jeu["file_mvt"].clear()
        entites["Joueur"].respawn()
    
    # Interface de gauche
    pygame.draw.rect(screen, (232,195,158), Rect(0, 0, 800, 800))
    
    # Met à jour les éléments sur la page
    for surf, rect, img, nom in elements["elem_fixes"]:
        screen.blit(surf, rect)

    for surf, rect, img, nom, tps in elements["elem_deplacables"]:
        if elem_actuel == None or surf != elem_actuel[1][0]:
            screen.blit(surf, rect)
        else:
            surf = pygame.transform.scale(surf, (int(rect.width * 1.4), int(rect.height * 1.4)))
            rect = surf.get_rect(center=rect.center)
            screen.blit(surf, rect)            

    for ligne in elements["separation_mouvements"]:
        start_pos, end_pos, width = ligne
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, width)

    # Met à jour le bouton reset, menu de choix de niveau et envoi
    for key in ["reset", "retour_de_page", "envoi"]:
        rect = boutons[key][2]
        ellipse_rect = pygame.Rect(rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20)
        pygame.draw.ellipse(pygame_screen["screen"], (211, 211, 211), ellipse_rect)
        pygame_screen["screen"].blit(boutons[key][1], rect)

    nb_tentatives_surf = pygame.font.Font(None,36).render(f"Tentatives : {variables_jeu["nb_tentatives"]}",True,(0,0,0))
    screen.blit(nb_tentatives_surf, (620,10))

    # Met à jour le menu si il est affiché
    if menu["menu_visible"]:
        screen.blit(menu["option_supprimer"], (menu["menu_rect"].x + 10, menu["menu_rect"].y + 10))
        screen.blit(menu["option_temps"], (menu["menu_rect"].x + 10, menu["menu_rect"].y + 40))

    if menu["menu_temps_visible"]:
        screen.blit(menu["option_moins_moins"], (menu["menu_temps_rect"].x - 20, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_moins"], (menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_de_temps"], (menu["menu_temps_rect"].x + 40, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_plus"], (menu["menu_temps_rect"].x + 85, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_plus_plus"], (menu["menu_temps_rect"].x + 115, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_fermer_temps"], (menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y - 20))
        
    mise_a_jour_page_base_fin()