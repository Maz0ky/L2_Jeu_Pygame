import pygame

def initialiser_interface():
    """Création du bouton "Envoi"""
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Envoie", True, (255, 255, 255))
    button_rect = pygame.Rect(700, 360, 90, 40)

    return button_font, button_text, button_rect

def cree_surf_img(chemin: str, width, height, pos_x, pos_y):
    """Création des éléments fixes (mouvements)"""
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    return surf, rect, chemin 

def initaliser_elements():
    """Création des éléments de mouvements"""
    surf_1, rect_1, img1 = cree_surf_img('elem/left-arrow.png', 100, 100, 50, 300)
    surf_2, rect_2, img2 = cree_surf_img('elem/up-arrow.png', 100, 100, 100, 300)
    surf_3, rect_3, img3 = cree_surf_img('elem/right-arrow.png', 100, 100, 150, 300)
    elements_fixes = [(surf_1, rect_1, img1), (surf_2, rect_2, img2), (surf_3, rect_3, img3)]
    return elements_fixes

def eventss(event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect):
    """Gestion des évènements"""
    genere_liste_elements = False

    # Clic pour sélectionner une surface ou le bouton
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        # Vérification du clic sur le bouton Envoi
        if button_rect.collidepoint(mouse_pos):
            genere_liste_elements = True

        # Vérification des blocs fixes pour créer des blocs déplaçables si besoin
        for element in elements_fixes:
            if element[1].collidepoint(mouse_pos): # element[1] est sa surface
                new_surf, new_rect, new_img = cree_surf_img(element[2], element[1].width, element[1].height, element[1].x, element[1].y)
                elements_deplacables.append((new_surf, new_rect, new_img))
                selected_element = (new_surf, new_rect, new_img)
                mouse_offset = (mouse_pos[0] - new_rect.x, mouse_pos[1] - new_rect.y)
                break

        # Vérification des blocs déplaçables pour les déplacer si besoin
        for element in elements_deplacables:
            if element[1].collidepoint(mouse_pos) and event.button == 1:
                selected_element = element
                mouse_offset = (mouse_pos[0] - element[1].x, mouse_pos[1] - element[1].y)
                break

    # Relâchement du clic gauche : arrêt du déplacement
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        selected_element = None
    
    return elements_deplacables, mouse_offset, genere_liste_elements, selected_element

def interface_ajout_mouvements(screen, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_text, button_rect):
    """Gère le déplacement et met à jour la page"""
    
    # Déplacement de l'élément sélectionné avec la souris
    if selected_element is not None:
        mouse_pos = pygame.mouse.get_pos()
        selected_element[1].x = mouse_pos[0] - mouse_offset[0]
        selected_element[1].y = mouse_pos[1] - mouse_offset[1]

    # Mise à jour de l'affichage
    screen.fill((30, 30, 30))

    # Divise l'écran en deux sections
    pygame.draw.line(screen, (255, 255, 255), (800, 0), (800, 400), 5)

    # Met à jour les éléments sur la page
    for surf, rect, img in elements_fixes:
        screen.blit(surf, rect)

    for surf, rect, img in elements_deplacables:
        screen.blit(surf, rect)

    # Met à jour le bouton envoie
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    return selected_element, button_rect


def generer_liste_elements(elements_deplacables):
    """Trie et génère la liste d'éléments déplaçables"""
    elements_triee = sorted(elements_deplacables, key=lambda elem: elem[1].x)
    liste_elements = []
    for elem in elements_triee:
        if elem[2] == "elem/up-arrow.png":
            mouv = "j"
        elif elem[2] == "elem/right-arrow.png":
            mouv = "r"
        elif elem[2] == "elem/left-arrow.png":
            mouv = "l"
        temps = 10  # Temps par défaut pour chaque mouvement
        liste_elements.append({"mouvement": mouv, "temps": temps})
    return liste_elements
