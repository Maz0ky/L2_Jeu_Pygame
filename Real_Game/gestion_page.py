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
        if retour_from_end_rect.collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0
    
def gestion_evenements_accueil(event):
    gestion_evenement_base(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0

def gestion_evenements_choix_niveau(event):
    gestion_evenement_base(event)
    mouse_pos = pygame.mouse.get_pos()
    Joueur = None

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_retour_de_choixlvl[2].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = -1
        else:
            for i in range(0, variables_jeu["nb_level"]):
                if levels_info[i][1].collidepoint(mouse_pos) and levels_info[i][3]:
                    charge_map(i)
                    Joueur = Player(pos_start)
                    variables_jeu["level_actu"] = i + 1

    if event.type == pygame.MOUSEMOTION:  # Détecte les mouvements de la souris
        for i in range(0, variables_jeu["nb_level"]):
            if levels_info[i][1].collidepoint(mouse_pos):
                levels_info[i][2] = True  # Active l'effet de survol
            else:
                levels_info[i][2] = False

def gestion_evenements_level(event, elements_fixes, elements_deplacables, selected_element, mouse_offset, bouton_envoi, click_again, player_rect, button_retour_de_page):
    """Gestion des évènements"""
    gestion_evenement_base(event)
    genere_liste_elements = False # Indique si l'on doit envoyer la liste

    # Clic pour sélectionner une surface ou le bouton
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        if button_retour_de_page[2].collidepoint(mouse_pos):
            variables_jeu["level_actu"] = 0
        
        # Vérification des blocs fixes pour créer des blocs déplaçables si besoin
        for element in elements_fixes:
            if element[1].collidepoint(mouse_pos): # element[1] est sa surface
                new_surf, new_rect, new_img, new_nom = cree_surf_img(element[2], element[3], element[1].width, element[1].height, element[1].x, element[1].y)
                temps_default = 21
                elements_deplacables.append([new_surf, new_rect, new_img, new_nom, temps_default])
                selected_element = (new_surf, new_rect, new_img, new_nom)
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
                    elements_deplacables.remove(menu["element_concerne"])
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
        selected_element = None

    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        # Vérification du clic sur le bouton Envoi
        if bouton_envoi[2].collidepoint(mouse_pos):
            for element in elements_deplacables:
                if element[1].y > 520:
                    elements_deplacables.remove(element)
                    break

            if click_again == True:
                click_again = False
                Joueur.respawn()
                genere_liste_elements = True
                variables_jeu["nb_tentatives"] += 1

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

    return elements_deplacables, mouse_offset, genere_liste_elements, selected_element, player_rect, click_again

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
    screen.fill((30, 30, 30))

def mise_a_jour_page_base_fin():
    pygame.display.flip()  # Met à jour l'écran
    clock.tick(variables_jeu["fps"]) * .001 * variables_jeu["fps"]  # Limite à 60 FPS

def mise_a_jour_page_end():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    screen.blit(background_image_end, (0, 0))
    screen.blit(retour_from_end_surf, retour_from_end_rect)

    mise_a_jour_page_base_fin()

def mise_a_jour_page_accueil():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    screen.blit(background_image_accueil, (0, 0))
    screen.blit(start_surf, start_rect)

    mise_a_jour_page_base_fin()

def levels_verifications(niveau):
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

def mise_a_jour_page_choix_niveau():
    """Met à jour la page"""

    mise_a_jour_page_base_debut()
    
    screen.blit(background_image_menu, (0, 0))

    for i in range(0, variables_jeu["nb_level"]):
        levels_verifications(i + 1)

    button_retour_de_choixlvl[2].width += 20 ; button_retour_de_choixlvl[2].height += 20
    pygame.draw.ellipse(screen,(211, 211, 211), button_retour_de_choixlvl[2])
    button_retour_de_choixlvl[2].x += 10 ; button_retour_de_choixlvl[2].y += 10
    screen.blit(button_retour_de_choixlvl[1], button_retour_de_choixlvl[2])
    button_retour_de_choixlvl[2].width -= 20 ; button_retour_de_choixlvl[2].height -= 20
    button_retour_de_choixlvl[2].x -= 10 ; button_retour_de_choixlvl[2].y -= 10

    mise_a_jour_page_base_fin()

def mise_a_jour_page_level(elements_fixes, elements_deplacables, bouton_envoi, button_retour_de_page, barres_separations_interface, file_mouvement, elem_actuel):
    """Met à jour la page"""

    mise_a_jour_page_base_debut()

    # Séparation des deux interfaces
    pygame.draw.rect(screen, (232,195,158), Rect(0, 0, 800, 800))
    
    # Met à jour les éléments sur la page
    for surf, rect, img, nom in elements_fixes:
        screen.blit(surf, rect)

    for surf, rect, img, nom, tps in elements_deplacables:
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
    Joueur.show(screen)
    Joueur.update(block_group, fatal_group, end_group)
    if Joueur.is_dead():
        file_mouvement.clear()
        Joueur.respawn()
        
    mise_a_jour_page_base_fin()