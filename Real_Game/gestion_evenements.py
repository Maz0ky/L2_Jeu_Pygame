# Import
import pygame
from initialisations import *
from chargement_map import *

# Sous fonctions

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

# Gestion évènements

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

# Evenement de fin de niveau

def reset_fin_niveau():
    match variables_jeu["level_actu"]:
        case 5 :
            variables_jeu["level_actu"] = -2

        case level if level in range(1, variables_jeu["nb_level"]) :  # Vérifie si level_actu est entre 1 et 4
            variables_jeu["levels_info"][level][3] = True
            variables_jeu["level_actu"] = 0

    entites["Joueur"].reset()
    entites["Joueur"].respawn()
    elements["elem_deplacables"] = []
    variables_jeu["file_mvt"].clear()
    variables_jeu["nb_tentatives"] = 0
    variables_jeu["genere_lst_elements"] = False