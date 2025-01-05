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

def gestion_evenements_end(event, level, end_rect):
    gestion_evenement_base(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if end_rect.collidepoint(mouse_pos):
            level = 0
    return level

def gestion_evenements_accueil(event, level, start_rect):
    gestion_evenement_base(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            level = 0
    return level

def gestion_evenements_choix_niveau(event, level, button_retour_de_choixlvl, levels_info):
    gestion_evenement_base(event)
    mouse_pos = pygame.mouse.get_pos()
    Joueur = None

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos_start = (800,640)
        if button_retour_de_choixlvl[2].collidepoint(mouse_pos):
            level = -1
        elif levels_info[0][1].collidepoint(mouse_pos):
            
            charge_map(0)
            Joueur = Player(pos_start)
            level = 1
        elif levels_info[1][1].collidepoint(mouse_pos) and levels_info[1][3]:
            
            charge_map(1)
            Joueur = Player(pos_start)
            level = 2
        elif levels_info[2][1].collidepoint(mouse_pos) and levels_info[2][3]:
            
            charge_map(2)
            Joueur = Player(pos_start)
            level = 3
        elif levels_info[3][1].collidepoint(mouse_pos) and levels_info[3][3]:
            
            charge_map(3)
            Joueur = Player(pos_start)
            level = 4
        elif levels_info[4][1].collidepoint(mouse_pos) and levels_info[4][3]:
            
            charge_map(4)
            Joueur = Player(pos_start)
            level = 5
    
    if event.type == pygame.MOUSEMOTION:  # Détecte les mouvements de la souris
        if levels_info[0][1].collidepoint(mouse_pos):
            levels_info[0][2] = True  # Active l'effet de survol
        else:
            levels_info[0][2] = False
        if levels_info[1][1].collidepoint(mouse_pos):
            levels_info[1][2] = True  # Active l'effet de survol
        else:
            levels_info[1][2] = False
        if levels_info[2][1].collidepoint(mouse_pos):
            levels_info[2][2] = True  # Active l'effet de survol
        else:
            levels_info[2][2] = False
        if levels_info[3][1].collidepoint(mouse_pos):
            levels_info[3][2] = True  # Active l'effet de survol
        else:
            levels_info[3][2] = False
        if levels_info[4][1].collidepoint(mouse_pos):
            levels_info[4][2] = True  # Active l'effet de survol
        else:
            levels_info[4][2] = False
    return level, Joueur

def gestion_evenements_level(screen, event, level, elements_fixes, elements_deplacables, selected_element, mouse_offset, bouton_envoi, click_again, player_rect, player_surf, button_retour_de_page, Joueur, menu):
    """Gestion des évènements"""
    gestion_evenement_base(event)
    genere_liste_elements = False # Indique si l'on doit envoyer la liste

    # Clic pour sélectionner une surface ou le bouton
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        if button_retour_de_page[2].collidepoint(mouse_pos):
            level = 0
        
        # Vérification des blocs fixes pour créer des blocs déplaçables si besoin
        for element in elements_fixes:
            if element[1].collidepoint(mouse_pos): # element[1] est sa surface
                new_surf, new_rect, new_img = cree_surf_img(element[2], element[1].width, element[1].height, element[1].x, element[1].y)
                temps_default = 21
                elements_deplacables.append([new_surf, new_rect, new_img, temps_default])
                selected_element = (new_surf, new_rect, new_img)
                mouse_offset = (mouse_pos[0] - new_rect.x, mouse_pos[1] - new_rect.y)
                break

        # Vérification des blocs déplaçables pour les déplacer si besoin
        for element in elements_deplacables:
            if element[1].x < -20 or element[1].x > 720:
                elements_deplacables.remove(element)
                break

            if element[1].collidepoint(mouse_pos):
                if event.button == 1: # event.button == 1 désigne le clique gauche
                    selected_element = element
                    mouse_offset = (mouse_pos[0] - element[1].x, mouse_pos[1] - element[1].y)
                    break

                if event.button == 3:  # Clic droit
                    # Afficher un menu contextuel
                    menu["menu_visible"] = True
                    menu["element_concerne"] = element
                    menu["menu_rect"], menu["option_supprimer"], menu["option_temps"] = affiche_menu(screen, menu["menu_rect"])
                    break

    if menu["menu_visible"]:
        menu["menu_rect"], menu["option_supprimer"], menu["option_temps"] = affiche_menu(screen, menu["menu_rect"])
        # Gestion du menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Gestion du menu
            if menu["menu_rect"].collidepoint(mouse_pos):
                # Supprimer l'élément sélectionné si "Supprimer" est cliqué
                if menu["option_supprimer"].get_rect(topleft=(menu["menu_rect"].x, menu["menu_rect"].y)).collidepoint(mouse_pos):
                    elements_deplacables.remove(menu["element_concerne"])
                    menu["menu_visible"] = False
                
                # Modifier le temps si "Modifier le temps" est cliqué
                if menu["option_temps"].get_rect(topleft=(menu["menu_rect"].x, menu["menu_rect"].y + 40)).collidepoint(mouse_pos):
                    # Champ pour saisir le temps
                    menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"] = affiche_menu_temps(screen, menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"])
                    
                    menu["menu_visible"] = False
                    menu["menu_temps_visible"] = True
        
    if menu["menu_temps_visible"]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if menu["option_moins"].get_rect(topleft=(menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][3] -= 1
                menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"] = affiche_menu_temps(screen, menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"])
                
            if menu["option_moins"].get_rect(topleft=(menu["menu_temps_rect"].x + 85, menu["menu_temps_rect"].y + 10)).collidepoint(mouse_pos):
                menu["element_concerne"][3] += 1
                menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"] = affiche_menu_temps(screen, menu["menu_temps_rect"], menu["element_concerne"][3], menu["option_fermer_temps"], menu["option_moins"], menu["option_plus"], menu["option_de_temps"])

            if menu["option_fermer_temps"].get_rect(topleft=(menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + -20)).collidepoint(mouse_pos):
                menu["menu_temps_visible"] = False
                

    # Relâchement du clic gauche : arrêt du déplacement
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        selected_element = None

    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        # Vérification du clic sur le bouton Envoi
        if bouton_envoi[2].collidepoint(mouse_pos):
            if click_again == True:
                click_again = False
                Joueur.respawn()
                genere_liste_elements = True
        # Vérification du clic sur le bouton Reset
        if bouton_reset[2].collidepoint(mouse_pos):
            genere_liste_elements = False
            file_mouvement.clear()
            elements_deplacables = []
    
    # Déplacement de l'élément sélectionné avec la souris
    if selected_element is not None:
        mouse_pos = pygame.mouse.get_pos()
        selected_element[1].x = mouse_pos[0] - mouse_offset[0]
        selected_element[1].y = mouse_pos[1] - mouse_offset[1]

    return elements_deplacables, mouse_offset, genere_liste_elements, selected_element, player_rect, click_again, level

# Les menus de la partie création de liste

def affiche_menu(screen, menu_rect):
    """Affiche un menu contextuel pour l'élément sélectionné."""
    font = pygame.font.Font(None, 36)
    # Création des options de menu
    option_supprimer = font.render("Supprimer", True, (255, 255, 255))
    option_temps = font.render("Modifier temps", True, (255, 255, 255))

    # Position du menu contextuel
    menu_rect = pygame.Rect(350, 320, 200, 80)
    
    return menu_rect, option_supprimer, option_temps

def affiche_menu_temps(screen, menu_temps_rect, temps, option_fermer_temps, option_moins, option_plus, option_de_temps):
    font = pygame.font.Font(None, 36)
    # Création des options de menu
    option_moins  = font.render("-", True, (255, 255, 255))
    option_de_temps = font.render(str(temps), True, (255, 255, 255))
    option_plus = font.render("+", True, (255, 255, 255))
    option_fermer_temps  = font.render("Fermer", True, (255, 255, 255))

    # Position du menu contextuel
    menu_temps_rect = pygame.Rect(350, 320, 0, 0)
    
    return menu_temps_rect, temps, option_fermer_temps, option_moins, option_plus, option_de_temps

# Mise à jour de la page

def mise_a_jour_page_base_debut(screen):
    # Mise à jour de l'affichage
    screen.fill((30, 30, 30))

def mise_a_jour_page_base_fin(clock, fps):
    pygame.display.flip()  # Met à jour l'écran
    clock.tick(fps) * .001 * fps  # Limite à 60 FPS

def mise_a_jour_page_end(screen, clock, fps, retour_from_end_surf, retour_from_end_rect):
    """Met à jour la page"""

    mise_a_jour_page_base_debut(screen)
    
    screen.blit(background_image_end, (0, 0))
    screen.blit(retour_from_end_surf, retour_from_end_rect)

    mise_a_jour_page_base_fin(clock, fps)

def mise_a_jour_page_accueil(screen, clock, fps, start_surf, start_rect):
    """Met à jour la page"""

    mise_a_jour_page_base_debut(screen)
    
    screen.blit(background_image_accueil, (0, 0))
    screen.blit(start_surf, start_rect)

    mise_a_jour_page_base_fin(clock, fps)

def levels_verifications(screen, levels_info, niveau):
    """Pour rendre la vérification des niveaux plus compacte"""
    indice = niveau - 1
    if levels_info[indice][3]:
        if levels_info[indice][2]:
            level_scaled_rect = levels_info[indice][1].inflate(levels_info[indice][1].width * 0.2, levels_info[indice][1].height * 0.2)
            pygame.draw.circle(screen, (240, 240, 240), level_scaled_rect.center, max(level_scaled_rect.width, level_scaled_rect.height) // 2 + 40)
            screen.blit(pygame.transform.scale(levels_info[indice][0], level_scaled_rect.size), level_scaled_rect)
        else:
            pygame.draw.circle(screen, (240, 240,240), levels_info[indice][1].center, max(levels_info[indice][1].width, levels_info[indice][1].height) // 2 + 40)
            screen.blit(levels_info[indice][0], levels_info[indice][1])
    else:
        if niveau != 1: 
            screen.blit(levels_info[indice][0], levels_info[indice][1])
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)  # Surface transparente
            pygame.draw.circle(overlay, (100, 40, 40, 240), levels_info[indice][1].center, max(levels_info[indice][1].width, levels_info[indice][1].height) // 2 + 40)  # Cercle semi-transparent
            screen.blit(overlay, (0, 0))

def mise_a_jour_page_choix_niveau(screen, clock, fps, button_retour_de_choixlvl, levels_info):
    """Met à jour la page"""

    mise_a_jour_page_base_debut(screen)
    
    screen.blit(background_image_menu, (0, 0))

    levels_verifications(screen, levels_info, 1)
    levels_verifications(screen, levels_info, 2)
    levels_verifications(screen, levels_info, 3)
    levels_verifications(screen, levels_info, 4)
    levels_verifications(screen, levels_info, 5)

    button_retour_de_choixlvl[2].width += 20 ; button_retour_de_choixlvl[2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), button_retour_de_choixlvl[2])
    button_retour_de_choixlvl[2].x += 10 ; button_retour_de_choixlvl[2].y += 10
    screen.blit(button_retour_de_choixlvl[1], button_retour_de_choixlvl[2])
    button_retour_de_choixlvl[2].width -= 20 ; button_retour_de_choixlvl[2].height -= 20
    button_retour_de_choixlvl[2].x -= 10 ; button_retour_de_choixlvl[2].y -= 10

    mise_a_jour_page_base_fin(clock, fps)

def mise_a_jour_page_level(screen, elements_fixes, elements_deplacables, bouton_envoi, clock, fps, button_retour_de_page, Joueur, menu, barres_separations_interface, file_mouvement, elem_actuel):
    """Met à jour la page"""

    mise_a_jour_page_base_debut(screen)

    # Séparation des deux interfaces
    pygame.draw.rect(screen, (232,195,158), Rect(0, 0, 800, 800))
    
    # Met à jour les éléments sur la page
    for surf, rect, img in elements_fixes:
        screen.blit(surf, rect)

    for surf, rect, img, tps in elements_deplacables:
        if elem_actuel == None or surf != elem_actuel[1][0]:
            screen.blit(surf, rect)
        else:
            surf = pygame.transform.scale(surf, (int(rect.width * 1.4), int(rect.height * 1.4)))
            rect = surf.get_rect(center=rect.center)
            screen.blit(surf, rect)            

    for ligne in barres_separations_interface:
        start_pos, end_pos, width = ligne
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, width)

    # Met à jour le bouton envoie
    bouton_envoi[2].width += 20 ; bouton_envoi[2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), bouton_envoi[2])
    bouton_envoi[2].x += 10 ; bouton_envoi[2].y += 10
    screen.blit(bouton_envoi[1], bouton_envoi[2])
    bouton_envoi[2].width -= 20 ; bouton_envoi[2].height -= 20
    bouton_envoi[2].x -= 10 ; bouton_envoi[2].y -= 10

    # Met à jour le bouton reset
    bouton_reset[2].width += 20 ; bouton_reset[2].height += 20
    pygame.draw.ellipse(screen, (211, 211, 211), bouton_reset[2])
    bouton_reset[2].x += 10 ; bouton_reset[2].y += 10
    screen.blit(bouton_reset[1], bouton_reset[2])
    bouton_reset[2].width -= 20 ; bouton_reset[2].height -= 20
    bouton_reset[2].x -= 10 ; bouton_reset[2].y -= 10

    # Met à jour le bouton retour menu choix niveau
    button_retour_de_page[2].width += 20 ; button_retour_de_page[2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), button_retour_de_page[2])
    button_retour_de_page[2].x += 10 ; button_retour_de_page[2].y += 10
    screen.blit(button_retour_de_page[1], button_retour_de_page[2])
    button_retour_de_page[2].width -= 20 ; button_retour_de_page[2].height -= 20
    button_retour_de_page[2].x -= 10 ; button_retour_de_page[2].y -= 10

    
    # Met à jour le menu si il est affiché
    if menu["menu_visible"]:
        screen.blit(menu["option_supprimer"], (menu["menu_rect"].x + 10, menu["menu_rect"].y + 10))
        screen.blit(menu["option_temps"], (menu["menu_rect"].x + 10, menu["menu_rect"].y + 40))

    if menu["menu_temps_visible"]:
        screen.blit(menu["option_moins"], (menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_de_temps"], (menu["menu_temps_rect"].x + 40, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_plus"], (menu["menu_temps_rect"].x + 85, menu["menu_temps_rect"].y + 10))
        screen.blit(menu["option_fermer_temps"], (menu["menu_temps_rect"].x + 10, menu["menu_temps_rect"].y - 20))

    # Partie map

    sprite_group.draw(screen)
    Joueur.show(screen)
    Joueur.update(block_group, fatal_group, end_group)
    if Joueur.is_dead():
        file_mouvement.clear()
        Joueur.respawn()
        
    mise_a_jour_page_base_fin(clock, fps)