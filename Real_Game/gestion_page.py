# Import
import pygame
from pygame.locals import *
from initialisations import *
from chargement_map import *

# Gestion des évènements

def gestion_evenement_base(event):
    if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def gestion_evenements_end(event):
    gestion_evenement_base(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if boutons["retour_from_end"][1].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0
    
def gestion_evenements_accueil(event):
    gestion_evenement_base(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if boutons["start"][1].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0

def gestion_evenements_choix_niveau(event):
    gestion_evenement_base(event)
    mouse_pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if boutons["retour_de_choixlvl"][2].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = -1
        else:
            for i in range(0, variables_jeu["nb_level"]):
                if variables_jeu["levels_info"][i][1].collidepoint(mouse_pos) and variables_jeu["levels_info"][i][3]:
                    entites["Joueur"] = Player()
                    entites["Joueur"].update_pos_start(variables_jeu["levels_info"][i][4])
                    variables_jeu["level_actu"] = i + 1
                    charge_map(i)
                    
    if event.type == pygame.MOUSEMOTION:  # Détecte les mouvements de la souris
        for i in range(0, variables_jeu["nb_level"]):
            if variables_jeu["levels_info"][i][1].collidepoint(mouse_pos):
                variables_jeu["levels_info"][i][2] = True  # Active l'effet de survol
            else:
                variables_jeu["levels_info"][i][2] = False

def gestion_evenements_level(event):
    
    """Gestion des évènements"""
    gestion_evenement_base(event)
    variables_jeu["genere_lst_elements"] = False # Indique si l'on doit envoyer la liste

    # Clic pour sélectionner une surface ou le bouton
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        if boutons["retour_de_page"][2].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0
        
        # Vérification des blocs fixes pour créer des blocs déplaçables si besoin
        for element in elements["elem_fixes"]:
            if element[1].collidepoint(mouse_pos): # element[1] est sa surface
                new_surf, new_rect, new_img, new_nom = cree_surf_img(element[2], element[3], element[1].width, element[1].height, element[1].x, element[1].y)
                temps_default = 21
                elements["elem_deplacables"].append([new_surf, new_rect, new_img, new_nom, temps_default])
                variables_jeu["elem_select"] = (new_surf, new_rect, new_img, new_nom)
                variables_jeu["mouse_offset"] = (mouse_pos[0] - new_rect.x, mouse_pos[1] - new_rect.y)
                break

        # Vérification des blocs déplaçables pour les déplacer si besoin
        for element in elements["elem_deplacables"]:
            if element[1].x < -20 or element[1].x > 720:
                elements["elem_deplacables"].remove(element)
                break

            if element[1].collidepoint(mouse_pos):
                if event.button == 1: # event.button == 1 désigne le clique gauche
                    variables_jeu["elem_select"] = element
                    variables_jeu["mouse_offset"] = (mouse_pos[0] - element[1].x, mouse_pos[1] - element[1].y)
                    break

                if event.button == 3:  # Clic droit
                    # Afficher un menu contextuel
                    menu["menu_visible"] = True
                    menu["element_concerne"] = element
                    affiche_menu()
                    break

    if menu["menu_visible"]:
        affiche_menu()
        # Gestion du menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Gestion du menu
            if menu["menu_rect"].collidepoint(mouse_pos):
                # Supprimer l'élément sélectionné si "Supprimer" est cliqué
                if menu["option_supprimer"].get_rect(topleft=(menu["menu_rect"].x, menu["menu_rect"].y)).collidepoint(mouse_pos):
                    elements["elem_deplacables"].remove(menu["element_concerne"])
                    menu["menu_visible"] = False
                
                # Modifier le temps si "Modifier le temps" est cliqué
                if menu["option_temps"].get_rect(topleft=(menu["menu_rect"].x, menu["menu_rect"].y + 40)).collidepoint(mouse_pos):
                    # Champ pour saisir le temps
                    affiche_menu_temps()
                    
                    menu["menu_visible"] = False
                    menu["menu_temps_visible"] = True
        
    if menu["menu_temps_visible"]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if menu["option_moins_moins"].get_rect(topleft=(menu["menu_temps_rect"].x - 20, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][4] -= 10
                if menu["element_concerne"][4] < 0:
                    menu["element_concerne"][4] = 0
                affiche_menu_temps()
              
            if menu["option_moins"].get_rect(topleft=(menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][4] -= 1
                if menu["element_concerne"][4] < 0:
                    menu["element_concerne"][4] = 0
                affiche_menu_temps()
                
            if menu["option_plus"].get_rect(topleft=(menu["menu_temps_rect"].x + 85, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][4] += 1
                affiche_menu_temps()

            if menu["option_plus_plus"].get_rect(topleft=(menu["menu_temps_rect"].x + 115, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][4] += 10
                affiche_menu_temps()

            if menu["option_fermer_temps"].get_rect(topleft=(menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + -20)).collidepoint(mouse_pos):
                menu["menu_temps_visible"] = False
                

    # Relâchement du clic gauche : arrêt du déplacement
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        variables_jeu["elem_select"] = None

    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        # Vérification du clic sur le bouton Envoi
        if boutons["envoi"][2].collidepoint(mouse_pos):
            for element in elements["elem_deplacables"]:
                if element[1].y > 520:
                    elements["elem_deplacables"].remove(element)
                    break

            if variables_jeu["click_again"] == True:
                variables_jeu["click_again"] = False
                entites["Joueur"].respawn()
                variables_jeu["genere_lst_elements"] = True
                variables_jeu["nb_tentatives"] += 1

        # Vérification du clic sur le bouton Reset
        if boutons["reset"][2].collidepoint(mouse_pos):
            variables_jeu["genere_lst_elements"] = False
            variables_jeu["file_mvt"].clear()
            elements["elem_deplacables"] = []
    
    # Déplacement de l'élément sélectionné avec la souris
    if variables_jeu["elem_select"] is not None:
        mouse_pos = pygame.mouse.get_pos()
        variables_jeu["elem_select"][1].x = mouse_pos[0] - variables_jeu["mouse_offset"][0]
        variables_jeu["elem_select"][1].y = mouse_pos[1] - variables_jeu["mouse_offset"][1]

# Les menus de la partie création de liste

def affiche_menu():
    """Affiche un menu contextuel pour l'élément sélectionné."""
    font = pygame.font.Font(None, 36)
    # Création des options de menu
    menu["option_supprimer"] = font.render("Supprimer", True, (255, 255, 255))
    menu["option_temps"] = font.render("Modifier temps", True, (255, 255, 255))

    # Position du menu contextuel
    menu["menu_rect"] = pygame.Rect(350, 320, 200, 80)

def affiche_menu_temps():
    font = pygame.font.Font(None, 36)
    # Création des options de menu
    menu["option_moins_moins"] = font.render("--", True, (255, 255, 255))
    menu["option_moins"]  = font.render("-", True, (255, 255, 255))
    menu["option_de_temps"] = font.render(str(menu["element_concerne"][4]), True, (255, 255, 255))
    menu["option_plus"] = font.render("+", True, (255, 255, 255))
    menu["option_plus_plus"] = font.render("++", True, (255, 255, 255))
    menu["option_fermer_temps"]  = font.render("Fermer", True, (255, 255, 255))

    # Position du menu contextuel
    menu["menu_temps_rect"] = pygame.Rect(350, 320, 0, 0)
    
# Mise à jour de la page

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

def levels_verifications(niveau):
    """Pour rendre la vérification des niveaux plus compacte"""
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

def mise_a_jour_page_choix_niveau():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    pygame_screen["screen"].blit(backgrounds["menu"], (0, 0))

    for i in range(0, variables_jeu["nb_level"]):
        levels_verifications(i + 1)

    boutons["retour_de_choixlvl"][2].width += 20 ; boutons["retour_de_choixlvl"][2].height += 20
    pygame.draw.ellipse(pygame_screen["screen"],(211, 211, 211), boutons["retour_de_choixlvl"][2])
    boutons["retour_de_choixlvl"][2].x += 10 ; boutons["retour_de_choixlvl"][2].y += 10
    pygame_screen["screen"].blit(boutons["retour_de_choixlvl"][1], boutons["retour_de_choixlvl"][2])
    boutons["retour_de_choixlvl"][2].width -= 20 ; boutons["retour_de_choixlvl"][2].height -= 20
    boutons["retour_de_choixlvl"][2].x -= 10 ; boutons["retour_de_choixlvl"][2].y -= 10

    mise_a_jour_page_base_fin()

def mise_a_jour_page_level(elem_actuel):
    """Met à jour la page"""

    screen = pygame_screen["screen"]

    mise_a_jour_page_base_debut()

    # Séparation des deux interfaces
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

    # Met à jour le bouton envoie
    boutons["envoi"][2].width += 20 ; boutons["envoi"][2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), boutons["envoi"][2])
    boutons["envoi"][2].x += 10 ; boutons["envoi"][2].y += 10
    screen.blit(boutons["envoi"][1], boutons["envoi"][2])
    boutons["envoi"][2].width -= 20 ; boutons["envoi"][2].height -= 20
    boutons["envoi"][2].x -= 10 ; boutons["envoi"][2].y -= 10

    # Met à jour le bouton reset
    boutons["reset"][2].width += 20 ; boutons["reset"][2].height += 20
    pygame.draw.ellipse(screen, (211, 211, 211), boutons["reset"][2])
    boutons["reset"][2].x += 10 ; boutons["reset"][2].y += 10
    screen.blit(boutons["reset"][1], boutons["reset"][2])
    boutons["reset"][2].width -= 20 ; boutons["reset"][2].height -= 20
    boutons["reset"][2].x -= 10 ; boutons["reset"][2].y -= 10

    # Met à jour le bouton retour menu choix niveau
    boutons["retour_de_page"][2].width += 20 ; boutons["retour_de_page"][2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), boutons["retour_de_page"][2])
    boutons["retour_de_page"][2].x += 10 ; boutons["retour_de_page"][2].y += 10
    screen.blit(boutons["retour_de_page"][1], boutons["retour_de_page"][2])
    boutons["retour_de_page"][2].width -= 20 ; boutons["retour_de_page"][2].height -= 20
    boutons["retour_de_page"][2].x -= 10 ; boutons["retour_de_page"][2].y -= 10

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

    # Partie map

    sprite_group.draw(screen)
    entites["Joueur"].show(screen)
    entites["Joueur"].update(block_group, fatal_group, end_group)
    if entites["Joueur"].is_dead():
        variables_jeu["file_mvt"].clear()
        entites["Joueur"].respawn()
        
    mise_a_jour_page_base_fin()