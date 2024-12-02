# Import
import pygame
from mouvement import *

# [1] Initialisation du menu de début et de fin

# Note : condenser les options de temps + start surf, start rect + button retour de choix + de page + buton tout cour
def init_page_debut_et_fin(screen):
    level = niveau_actuel()
    start_surf, start_rect = page_accueil(screen)
    levels_info = boutons_levels(screen)
    button_retour_de_choixlvl = initialiser_bouton_retour_de_choixlvl()
    button_retour_de_page = initialiser_bouton_retour_de_page()
    return level, start_surf, start_rect, button_retour_de_choixlvl, button_retour_de_page, levels_info

# Initialisation du bouton de retour pour retourner à l'accueil depuis la page de choix des niveaux

def initialiser_bouton_retour_de_page():
    """Création du bouton Retour"""
    button_retour_de_page_font = pygame.font.Font(None, 36)
    button_retour_de_page_text = button_retour_de_page_font.render("Menu choix level", True, (0, 0, 0))
    button_retour_de_page_rect = pygame.Rect(20, 20, button_retour_de_page_text.get_width(), button_retour_de_page_text.get_height())
    button_retour_de_page = [button_retour_de_page_font, button_retour_de_page_text, button_retour_de_page_rect]
    return button_retour_de_page

# Initialisation du bouton de retour pour retourner à l'accueil depuis la page de choix des niveaux

def initialiser_bouton_retour_de_choixlvl():
    """Création du bouton Retour"""
    button_retour_de_choixlvl_font = pygame.font.Font(None, 36)
    button_retour_de_choixlvl_text = button_retour_de_choixlvl_font.render("Retour", True, (255, 255, 255))
    button_retour_de_choixlvl_rect = pygame.Rect(20, 20, button_retour_de_choixlvl_text.get_width(), button_retour_de_choixlvl_text.get_height())
    button_retour_de_choixlvl = button_retour_de_choixlvl_font, button_retour_de_choixlvl_text, button_retour_de_choixlvl_rect
    return button_retour_de_choixlvl

def niveau_actuel():
    level = 1
    return level

def page_accueil(screen):
    start_surf = pygame.image.load('Real_Game/elem/start.png').convert_alpha()
    start_surf = pygame.transform.scale(start_surf, (200, 200))
    start_rect = start_surf.get_rect(midbottom=(screen.get_width()/2, screen.get_height()*5/6))  # Position du bouton start
    return start_surf, start_rect

def boutons_levels(screen):
    level_1_surf = pygame.image.load('Real_Game/elem/level_1.png').convert_alpha()
    level_1_surf = pygame.transform.scale(level_1_surf, (200, 200))
    level_1_rect = level_1_surf.get_rect(midtop=(screen.get_width()/6, screen.get_height()/6))  # Position du bouton start

    level_2_surf = pygame.image.load('Real_Game/elem/level_2.png').convert_alpha()
    level_2_surf = pygame.transform.scale(level_2_surf, (200, 200))
    level_2_rect = level_2_surf.get_rect(midtop=(screen.get_width()*3/6, screen.get_height()/6))  # Position du bouton start

    level_3_surf = pygame.image.load('Real_Game/elem/level_3.png').convert_alpha()
    level_3_surf = pygame.transform.scale(level_3_surf, (200, 200))
    level_3_rect = level_3_surf.get_rect(midtop=(screen.get_width()*5/6, screen.get_height()/6))  # Position du bouton start

    level_1_survol, level_2_survol, level_3_survol = False, False, False
    level_1_accessible, level_2_accessible, level_3_accessible = True, False, False

    levels_info = [[level_1_surf, level_1_rect, level_1_survol, level_1_accessible], [level_2_surf, level_2_rect, level_2_survol, level_2_accessible], [level_3_surf, level_3_rect, level_3_survol, level_3_accessible]]
    return levels_info

# [2] Initialisations du niveau

def init_levels():
    elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, ex_tab_mouv, barres_separations_interface = initialisation_de_base()
    bouton_envoi, genere_liste_elements = initialiser_bouton_envoi()
    menu = initialisation_menu()
    return elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, bouton_envoi, genere_liste_elements, ex_tab_mouv, menu, barres_separations_interface

# Initialisation des éléments de bases

def initialisation_de_base():
    elements_fixes = initaliser_elements_fixes()
    elements_deplacables = []
    selected_element = None # Correspond à l'élément séléctionné
    mouse_offset = (0, 0)
    click_again = True # Indique si l'on peut cliquer à nouveau
    ex_tab_mouv = File_mouv([]) # Initialisation de la file des mouvements

    barres_separations_interface = lignes_info = [((0, 160), (800, 160), 3), ((0, 320), (800, 320), 3), ((0, 480), (800, 480), 3)]
    return elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, ex_tab_mouv, barres_separations_interface

def initaliser_elements_fixes():
    """Création des éléments de mouvements"""
    surf_1, rect_1, img1 = cree_surf_img('Real_Game/elem/left-arrow.png', 100, 100, 40 , 572)
    surf_2, rect_2, img2 = cree_surf_img('Real_Game/elem/up-arrow.png', 100, 100, 120, 572)
    surf_3, rect_3, img3 = cree_surf_img('Real_Game/elem/right-arrow.png', 100, 100, 200, 572)
    surf_4, rect_4, img4 = cree_surf_img('Real_Game/elem/pause.png', 70, 80, 310, 582)
    elements_fixes = [(surf_1, rect_1, img1), (surf_2, rect_2, img2), (surf_3, rect_3, img3), (surf_4, rect_4, img4)]
    return elements_fixes

def cree_surf_img(chemin: str, width, height, pos_x, pos_y):
    """Création des éléments fixes (mouvements)"""
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    return surf, rect, chemin

# Initialisation du bouton d'envoi

def initialiser_bouton_envoi():
    """Création du bouton Envoi"""
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Envoie", True, (0, 0, 0))
    button_rect = pygame.Rect(700, 632, button_text.get_width(), button_text.get_height())
    genere_liste_elements = False
    bouton_envoi =  button_font, button_text, button_rect
    return bouton_envoi, genere_liste_elements


# Initialisation du menu (suppression et temps)

def initialisation_menu():
    menu_visible = False # Indique si le menu (temps et suppression) doit être affiché
    menu_temps_visible = False # Indique si le menu temps doit être affiché
    element_concerne = None
    menu_rect, option_supprimer, option_temps = None, None, None # A l'état "None" puisque Faux par défaut
    option_fermer_temps, option_moins, option_plus, menu_temps_rect, option_de_temps = None, None, None, None, None
    menu = {"menu_visible" : menu_visible, "menu_rect" : menu_rect, "option_supprimer" : option_supprimer, "option_temps" : option_temps, "element_concerne" : element_concerne, "menu_temps_visible" : menu_temps_visible, "menu_temps_rect" : menu_temps_rect, "option_de_temps" : option_de_temps, "option_fermer_temps" : option_fermer_temps, "option_moins" : option_moins, "option_plus" : option_plus}
    return menu