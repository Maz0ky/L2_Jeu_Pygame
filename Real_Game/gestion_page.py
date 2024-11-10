# Import
import pygame
from pygame.locals import *
from Initialisations import *

# Gestion des évènements

def gestion_evenements(screen, event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, click_again, player_rect, player_surf):
    """Gestion des évènements"""

    if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    genere_liste_elements = False # Indique si l'on doit envoyer la liste
    # Clic pour sélectionner une surface ou le bouton
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()


        # Vérification des blocs fixes pour créer des blocs déplaçables si besoin
        for element in elements_fixes:
            if element[1].collidepoint(mouse_pos): # element[1] est sa surface
                new_surf, new_rect, new_img = cree_surf_img(element[2], element[1].width, element[1].height, element[1].x, element[1].y)
                temps_default = 10
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
                    menu_visible = True
                    element_concerne = element
                    menu_rect, option_supprimer, option_temps = affiche_menu(screen, menu_rect)
                    break
        

    if menu_visible:
        menu_rect, option_supprimer, option_temps = affiche_menu(screen, menu_rect)
        # Gestion du menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Gestion du menu
            if menu_rect.collidepoint(mouse_pos):
                # Supprimer l'élément sélectionné si "Supprimer" est cliqué
                if option_supprimer.get_rect(topleft=(menu_rect.x + 10, menu_rect.y + 10)).collidepoint(mouse_pos):
                    elements_deplacables.remove(element_concerne)
                    menu_visible = False
                
                # Modifier le temps si "Modifier le temps" est cliqué
                if option_temps.get_rect(topleft=(menu_rect.x + 10, menu_rect.y + 40)).collidepoint(mouse_pos):
                    # Champ pour saisir le temps
                    nouveau_temps = int(input("Entrez le nouveau temps : "))
                    for element in elements_deplacables:
                        if element == element_concerne:
                            element[3] = nouveau_temps # Mise à jour du temps dans les données de l'élément
                            break
                    menu_visible = False

    # Relâchement du clic gauche : arrêt du déplacement
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        selected_element = None

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
    # Vérification du clic sur le bouton Envoi
        if button_rect.collidepoint(mouse_pos):
            if click_again == True:
                click_again = False
                player_rect = player_surf.get_rect(midbottom=(880, 300))
                genere_liste_elements = True
    
    # Déplacement de l'élément sélectionné avec la souris
    if selected_element is not None:
        mouse_pos = pygame.mouse.get_pos()
        selected_element[1].x = mouse_pos[0] - mouse_offset[0]
        selected_element[1].y = mouse_pos[1] - mouse_offset[1]

    return elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, player_rect, click_again

def affiche_menu(screen, menu_rect):
    """Affiche un menu contextuel pour l'élément sélectionné."""
    font = pygame.font.Font(None, 36)
    # Création des options de menu
    option_supprimer = font.render("Supprimer", True, (255, 255, 255))
    option_temps = font.render("Modifier le temps", True, (255, 255, 255))
    
    # Position du menu contextuel
    menu_rect = pygame.Rect(350, 320, 200, 80)
    pygame.draw.rect(screen, (50, 50, 50), menu_rect)  # Fond du menu contextuel
    pygame.draw.rect(screen, (200, 200, 200), menu_rect, 2)  # Bordure du menu contextuel
    
    return menu_rect, option_supprimer, option_temps


# Mise à jour de la page

def mise_a_jour_page(screen, elements_fixes, elements_deplacables, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, player_surf, player_rect, clock, fps):
    """Met à jour la page"""

    # Mise à jour de l'affichage
    screen.fill((30, 30, 30))

    pygame.draw.rect(screen, (232,195,158), Rect(0, 0, 800, 672))

    # Met à jour les éléments sur la page
    for surf, rect, img in elements_fixes:
        screen.blit(surf, rect)

    for surf, rect, img, tps in elements_deplacables:
        screen.blit(surf, rect)

    # Met à jour le bouton envoie
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Afficher le joueur
    screen.blit(player_surf, player_rect)
    
    # Met à jour le menu si il est affiché
    if menu_visible:
        screen.blit(option_supprimer, (menu_rect.x + 10, menu_rect.y + 10))
        screen.blit(option_temps, (menu_rect.x + 10, menu_rect.y + 40))

    pygame.display.flip()  # Met à jour l'écran
    clock.tick(fps)  # Limite à 60 FPS
    return button_rect, menu_visible, menu_rect, option_supprimer, option_temps