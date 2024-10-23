import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))  # Dimensions de la fenêtre
pygame.display.set_caption("Mon jeu")  # Nom de la fenêtre
clock = pygame.time.Clock()

# Listes pour stocker les éléments
elements_fixes = []  # Blocs fixes
elements_deplacables = []  # Blocs créés et déplaçables

# Fonction pour créer des surfaces
def cree_surf(color: str, width, height, pos_x, pos_y):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    rect = surf.get_rect(bottomright=(pos_x, pos_y))
    return surf, rect

# Création des blocs fixes
surf_1, rect_1 = cree_surf('yellow', 100, 200, 300, 400)
surf_2, rect_2 = cree_surf('purple', 100, 100, 100, 400)

# Ajouter les blocs fixes à la liste
elements_fixes.append((surf_1, rect_1))
elements_fixes.append((surf_2, rect_2))

selected_element = None  # Bloc sélectionné
mouse_offset = (0, 0)  # Décalage entre la souris et l'élément sélectionné


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # END
            pygame.quit()
            exit()

        # Clic de souris pour sélectionner une surface
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Vérification des blocs fixes
            for element in elements_fixes:
                if element[1].collidepoint(mouse_pos):  # Si on clique sur un bloc fixe
                    # Créer un nouveau bloc à la même position
                    new_surf, new_rect = cree_surf(element[0].get_at((0, 0)), element[1].width, element[1].height, element[1].x, element[1].y)
                    elements_deplacables.append((new_surf, new_rect))  # Ajouter à la liste des déplaçables
                    selected_element = (new_surf, new_rect)  # Sélectionner ce nouvel élément
                    mouse_offset = (mouse_pos[0] - new_rect.x, mouse_pos[1] - new_rect.y)
                    break  # On arrête de vérifier une fois qu'on a cliqué sur un élément fixe

            # Vérification des blocs déplaçables
            for element in elements_deplacables:
                if element[1].collidepoint(mouse_pos) and event.button == 1:  # Vérifie si on clique gauche sur un élément déplaçable
                    selected_element = element  # Surface sélectionnée
                    # Calcul du décalage entre la souris et le coin supérieur gauche de l'élément
                    mouse_offset = (mouse_pos[0] - element[1].x, mouse_pos[1] - element[1].y)
                    break  # On arrête de vérifier une fois qu'on a cliqué sur un élément déplaçable
        
        # Relâchement du clic gauche : on arrête de déplacer l'élément
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Relâcher uniquement si c'était le bouton gauche
                selected_element = None  # Libère la sélection de l'élément

    # Si un élément est sélectionné et que la souris bouge, on le déplace
    if selected_element is not None:
        mouse_pos = pygame.mouse.get_pos()
        # Met à jour la position de l'élément sélectionné en fonction de la position de la souris et du décalage initial
        selected_element[1].x = mouse_pos[0] - mouse_offset[0]
        selected_element[1].y = mouse_pos[1] - mouse_offset[1]

    # Remet l'écran à jour
    screen.fill((30, 30, 30))  # Remplit l'écran avec une couleur de fond

    # Dessiner tous les blocs fixes
    for surf, rect in elements_fixes:
        screen.blit(surf, rect)

    # Dessiner tous les blocs déplaçables
    for surf, rect in elements_deplacables:
        screen.blit(surf, rect)

    pygame.display.update()  # Maj de la fenêtre
    clock.tick(60)  # Notre boucle ne s'effectuera pas plus rapidemment que 60 fois par seconde
