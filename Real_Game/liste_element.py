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

def cree_surf_img(chemin: str, width, height, pos_x, pos_y):
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    img = chemin
    return surf, rect, img 

# Création du bouton envoie 
button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Envoie", True, (255, 255, 255))
button_rect = pygame.Rect(700, 350, 90, 40)

# Eléments de mouvements
surf_1, rect_1, img1 = cree_surf_img('elem/left-arrow.png', 100, 100, 0, 300)
surf_2, rect_2, img2 = cree_surf_img('elem/up-arrow.png', 100, 100, 90, 300)
surf_3, rect_3, img3 = cree_surf_img('elem/right-arrow.png', 100, 100, 180, 300)
elements_fixes.append((surf_1, rect_1, img1))
elements_fixes.append((surf_2, rect_2, img2))
elements_fixes.append((surf_3, rect_3, img3))

selected_element = None  # Bloc sélectionné
mouse_offset = (0, 0)  # Décalage entre la souris et l'élément sélectionné

def obtenir_position_x(element):
    return element[1].x #Position x de élément déplaçable

def generer_liste_elements():
    elements_triee = sorted(elements_deplacables, key=obtenir_position_x) # Je Trie les éléments de gauche à droite en fonction de leur position x
    liste_elements = []
    for elem in elements_triee:
        if elem[2] == "elem/up-arrow.png":
            mouv = "j"
        elif elem[2] == "elem/right-arrow.png":
            mouv = "r"
        elif elem[2] == "elem/left-arrow.png":
            mouv = "l"
        
        temps = 10
            
        liste_elements.append([mouv, temps])
    print("Liste des éléments dans l'ordre de gauche à droite :", liste_elements)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # END
            pygame.quit()
            exit()

        # Clic de souris pour sélectionner une surface
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Vérification du clic sur le bouton Envoi
            if button_rect.collidepoint(mouse_pos):
                generer_liste_elements()  # Génére et affiche la liste des éléments déplaçables

            # Vérification des blocs fixes
            for element in elements_fixes:
                if element[1].collidepoint(mouse_pos):  # Si on clique sur un bloc fixe
                    # Créer un nouveau bloc à la même position
                    new_surf, new_rect, new_img = cree_surf_img(element[2], element[1].width, element[1].height, element[1].x, element[1].y)
                    elements_deplacables.append((new_surf, new_rect, new_img))  # Ajouter à la liste des déplaçables
                    selected_element = (new_surf, new_rect, new_img)  # Sélectionner ce nouvel élément
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
    for surf, rect, img in elements_fixes:
        screen.blit(surf, rect)

    # Dessiner tous les blocs déplaçables
    for surf, rect, img in elements_deplacables:
        screen.blit(surf, rect)

    # Dessin du bouton envoie
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    pygame.display.update()  # Maj de la fenêtre
    clock.tick(60)  # Notre boucle ne s'effectuera pas plus rapidemment que 60 fois par seconde