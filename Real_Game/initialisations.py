# Import
import pygame
from mouvement import *

pygame.init()
screen = pygame.display.set_mode((1600, 672))
pygame.display.set_caption("Zeta Jeu de la muerta")
clock = pygame.time.Clock()
fps = 60
pos_start = (800,640)

level = -1

nb_tentatives = 0

# Initialisation du bouton de retour pour retourner à l'accueil depuis la page de choix des niveaux
"""Création du bouton Retour"""
button_retour_de_page_font = pygame.font.Font(None, 36)
button_retour_de_page_text = button_retour_de_page_font.render("Retour menu choix level", True, (0, 0, 0))
button_retour_de_page_rect = pygame.Rect(20, 20, button_retour_de_page_text.get_width(), button_retour_de_page_text.get_height())
button_retour_de_page = [button_retour_de_page_font, button_retour_de_page_text, button_retour_de_page_rect]

# Initialisation du bouton de retour pour retourner à l'accueil depuis la page de choix des niveaux

"""Création du bouton Retour"""
button_retour_de_choixlvl_font = pygame.font.Font(None, 36)
button_retour_de_choixlvl_text = button_retour_de_choixlvl_font.render("Retour accueil", True, (0, 0, 0))
button_retour_de_choixlvl_rect = pygame.Rect(20, 20, button_retour_de_choixlvl_text.get_width(), button_retour_de_choixlvl_text.get_height())
button_retour_de_choixlvl = button_retour_de_choixlvl_font, button_retour_de_choixlvl_text, button_retour_de_choixlvl_rect
button_retour_de_choixlvl

start_surf = pygame.image.load('Real_Game/elem/start.png').convert_alpha()
start_surf = pygame.transform.scale(start_surf, (200, 200))
start_rect = start_surf.get_rect(midbottom=(screen.get_width()/2, screen.get_height()*5/6))  # Position du bouton start

def init_level(screen, chemin, taille, width, height):
    level_surf = pygame.image.load(chemin).convert_alpha()
    level_surf = pygame.transform.scale(level_surf, taille)
    level_rect = level_surf.get_rect(midtop=(screen.get_width()*width, screen.get_height()*height))
    return level_surf, level_rect

level_1_surf, level_1_rect = init_level(screen, 'Real_Game/elem/level_1.png', (90, 90), 6/33, 10/27)
level_2_surf, level_2_rect = init_level(screen, 'Real_Game/elem/level_2.png', (130, 130), 12/41, 2/25)
level_3_surf, level_3_rect = init_level(screen, 'Real_Game/elem/level_3.png', (170, 170), 288/411, 1/15)
level_4_surf, level_4_rect = init_level(screen, 'Real_Game/elem/level_4.png', (210, 210), 85/100, 16/36)
level_5_surf, level_5_rect = init_level(screen, 'Real_Game/elem/level_5.png', (250, 250), 49/100, 6/15)

level_1_survol, level_2_survol, level_3_survol, level_4_survol, level_5_survol = False, False, False, False, False
level_1_accessible, level_2_accessible, level_3_accessible, level_4_accessible, level_5_accessible  = True, False, False, False, False

levels_info = [[level_1_surf, level_1_rect, level_1_survol, level_1_accessible], [level_2_surf, level_2_rect, level_2_survol, level_2_accessible], [level_3_surf, level_3_rect, level_3_survol, level_3_accessible], [level_4_surf, level_4_rect, level_4_survol, level_4_accessible], [level_5_surf, level_5_rect, level_5_survol, level_5_accessible]]



# Initialisation des éléments de bases

elements_deplacables = []
selected_element = None # Correspond à l'élément séléctionné
mouse_offset = (0, 0)
click_again = True # Indique si l'on peut cliquer à nouveau
file_mouvement = File_mouv([]) # Initialisation de la file des mouvements

barres_separations_interface = lignes_info = [((0, 180), (800, 180), 3), ((0, 360), (800, 360), 3), ((0, 540), (800, 540), 3)]

def cree_surf_img(chemin: str, width, height, pos_x, pos_y):
    """Création des éléments fixes (mouvements)"""
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    return surf, rect, chemin

"""Création des éléments de mouvements"""
surf_1, rect_1, img1 = cree_surf_img('Real_Game/elem/left-arrow.png', 80, 80, 40 , 572)
surf_5, rect_5, img5 = cree_surf_img('Real_Game/elem/up-left-arrow.png', 60, 60, 180, 580)
surf_2, rect_2, img2 = cree_surf_img('Real_Game/elem/up-arrow.png', 80, 80, 270, 572)
surf_6, rect_6, img6 = cree_surf_img('Real_Game/elem/up-right-arrow.png', 60, 60, 370, 580)
surf_3, rect_3, img3 = cree_surf_img('Real_Game/elem/right-arrow.png', 80, 80, 480, 572)
surf_4, rect_4, img4 = cree_surf_img('Real_Game/elem/pause.png', 55, 65, 610, 582)
elements_fixes = [(surf_1, rect_1, img1), (surf_2, rect_2, img2), (surf_3, rect_3, img3), (surf_4, rect_4, img4), (surf_5, rect_5, img5), (surf_6, rect_6, img6)]

# Initialisation du bouton d'envoi

"""Création du bouton Envoi"""
button_font = pygame.font.Font(None, 36)
button_text = button_font.render("Envoie", True, (0, 0, 0))
button_rect = pygame.Rect(690, 620, button_text.get_width(), button_text.get_height())
genere_liste_elements = False
bouton_envoi = button_font, button_text, button_rect

# Initialisation du bouton reset

"""Création du bouton Reset"""
button_r_font = pygame.font.Font(None, 36)
button_r_text = button_r_font.render("Effacer", True, (0, 0, 0))
button_r_rect = pygame.Rect(690, 560, button_r_text.get_width(), button_r_text.get_height())
bouton_reset = button_r_font, button_r_text, button_r_rect

# Initialisation du menu (suppression et temps)

menu_visible = False # Indique si le menu (temps et suppression) doit être affiché
menu_temps_visible = False # Indique si le menu temps doit être affiché
element_concerne = None
menu_rect, option_supprimer, option_temps = None, None, None # A l'état "None" puisque Faux par défaut
option_fermer_temps, option_moins, option_moins_moins, option_plus, option_plus_plus, menu_temps_rect, option_de_temps = None, None, None, None, None, None, None
menu = {"menu_visible" : menu_visible, "menu_rect" : menu_rect, "option_supprimer" : option_supprimer, "option_temps" : option_temps, "element_concerne" : element_concerne, "menu_temps_visible" : menu_temps_visible, "menu_temps_rect" : menu_temps_rect, "option_de_temps" : option_de_temps, "option_fermer_temps" : option_fermer_temps, "option_moins" : option_moins, "option_moins_moins" : option_moins_moins, "option_plus" : option_plus, "option_plus_plus" : option_plus_plus}

retour_from_end_surf = pygame.image.load('Real_Game/elem/replay.png').convert_alpha()
retour_from_end_surf = pygame.transform.scale(retour_from_end_surf, (200, 200))
retour_from_end_rect = retour_from_end_surf.get_rect(midbottom=(screen.get_width()/2 + 40, screen.get_height()/2 + 150))  # Position du bouton start

background_image_accueil = pygame.image.load("Real_Game/elem/accueil_background.png")
background_image_menu = pygame.image.load("Real_Game/elem/menu_background.png")
background_image_end = pygame.image.load("Real_Game/elem/end_background.png").convert_alpha()

player_surf, player_rect, player_gravity, speed = None, None, None, None