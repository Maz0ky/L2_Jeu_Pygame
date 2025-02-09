# Import
import os
import pygame
from mouvement import *
from entites import *
from init_boutons import *

pygame.init()
pygame.display.set_caption("Zeta Jeu de la muerta")

entite = {
    "Joueur" : Player()
}

variables_jeu = {
    "level_actu" : -1,
    "nb_tentatives" : 0,
    "nb_level" : 5
}

pygame_screen = {
    "fps" : 60,
    "clock" : pygame.time.Clock(),
    "screen" : pygame.display.set_mode((1600, 672))
}

boutons = {
    # [surf, rect]
    "start" : bt_img("elem", "start.png", 200, 200, pygame_screen["screen"].get_width()/2, pygame_screen["screen"].get_height()*5/6),
    "retour_from_end" : bt_img("elem", "replay.png", 200, 200, pygame_screen["screen"].get_width()/2 + 40, pygame_screen["screen"].get_height()/2 + 150),

    # [font, text, rect]
    "retour_de_choixlvl" : bt_txt("Retour accueil", 20, 20),
    "retour_de_page" : bt_txt("Retour menu choix level", 20, 20),

    # [font, text, rect]
    "envoi" : bt_txt("Envoie", 690, 620),
    "reset" : bt_txt("Effacer", 690, 560)
}

def init_level(repertoire, nom, taille, width, height, pos_start_x, pos_start_y):
    lvl_surf = pygame.image.load(os.path.join(os.path.dirname(__file__), repertoire, nom)).convert_alpha()
    lvl_surf = pygame.transform.scale(lvl_surf, taille)
    lvl_rect = lvl_surf.get_rect(midtop=(pygame_screen["screen"].get_width()*width, pygame_screen["screen"].get_height()*height))
    pos_start = (pos_start_x, pos_start_y)
    return lvl_surf, lvl_rect, pos_start

lvl_1_surf, lvl_1_rect, lvl_1_pos_start = init_level("elem", "level_1.png", (90, 90), 6/33, 10/27, 800, 640)
lvl_2_surf, lvl_2_rect, lvl_2_pos_start = init_level("elem", "level_2.png", (130, 130), 12/41, 2/25, 800, 640)
lvl_3_surf, lvl_3_rect, lvl_3_pos_start = init_level("elem", "level_3.png", (170, 170), 288/411, 1/15, 800, 640)
lvl_4_surf, lvl_4_rect, lvl_4_pos_start = init_level("elem", "level_4.png", (210, 210), 85/100, 16/36, 800, 640)
lvl_5_surf, lvl_5_rect, lvl_5_pos_start = init_level("elem", "level_5.png", (250, 250), 49/100, 6/15, 800, 640)

lvl_1_survol, lvl_2_survol, lvl_3_survol, lvl_4_survol, lvl_5_survol = False, False, False, False, False
lvl_1_accessible, lvl_2_accessible, lvl_3_accessible, lvl_4_accessible, lvl_5_accessible  = True, False, False, False, False

levels_info = [[lvl_1_surf, lvl_1_rect, lvl_1_survol, lvl_1_accessible, lvl_1_pos_start], [lvl_2_surf, lvl_2_rect, lvl_2_survol, lvl_2_accessible, lvl_2_pos_start], 
               [lvl_3_surf, lvl_3_rect, lvl_3_survol, lvl_3_accessible, lvl_3_pos_start], [lvl_4_surf, lvl_4_rect, lvl_4_survol, lvl_4_accessible, lvl_4_pos_start], 
               [lvl_5_surf, lvl_5_rect, lvl_5_survol, lvl_5_accessible, lvl_5_pos_start]]

# Initialisation des éléments de bases

elements_deplacables = []
selected_element = None # Correspond à l'élément séléctionné
mouse_offset = (0, 0)
click_again = True # Indique si l'on peut cliquer à nouveau
file_mouvement = File_mouv([]) # Initialisation de la file des mouvements
genere_liste_elements = False

barres_separations_interface = lignes_info = [((0, 180), (800, 180), 3), ((0, 360), (800, 360), 3), ((0, 540), (800, 540), 3)]

def cree_surf_img(chemin: str, nom, width, height, pos_x, pos_y):
    """Création des éléments fixes (mouvements)"""
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    return surf, rect, chemin, nom

"""Création des éléments de mouvements"""
surf_1, rect_1, img1, nom1 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "left-arrow.png"), "left-arrow", 80, 80, 40 , 572)
surf_5, rect_5, img5, nom5 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-left-arrow.png"), "up-left-arrow", 60, 60, 180, 580)
surf_2, rect_2, img2, nom2 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-arrow.png"), "up-arrow", 80, 80, 270, 572)
surf_6, rect_6, img6, nom6 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-right-arrow.png"), "up-right-arrow", 60, 60, 370, 580)
surf_3, rect_3, img3, nom3 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "right-arrow.png"), "right-arrow", 80, 80, 480, 572)
surf_4, rect_4, img4, nom4 = cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "pause.png"), "pause", 55, 65, 610, 582)

elements_fixes = [(surf_1, rect_1, img1, nom1), (surf_2, rect_2, img2, nom2), (surf_3, rect_3, img3, nom3), 
                  (surf_4, rect_4, img4, nom4), (surf_5, rect_5, img5, nom5), (surf_6, rect_6, img6, nom6)]

# Initialisation du menu (suppression et temps)

menu_visible = False # Indique si le menu (temps et suppression) doit être affiché
menu_temps_visible = False # Indique si le menu temps doit être affiché
element_concerne = None
menu_rect, option_supprimer, option_temps = None, None, None # A l'état "None" puisque Faux par défaut
option_fermer_temps, option_moins, option_moins_moins, option_plus, option_plus_plus, menu_temps_rect, option_de_temps = None, None, None, None, None, None, None

menu = {"menu_visible" : menu_visible, "menu_rect" : menu_rect, "option_supprimer" : option_supprimer, "option_temps" : option_temps, 
        "element_concerne" : element_concerne, "menu_temps_visible" : menu_temps_visible, "menu_temps_rect" : menu_temps_rect, 
        "option_de_temps" : option_de_temps, "option_fermer_temps" : option_fermer_temps, "option_moins" : option_moins, 
        "option_moins_moins" : option_moins_moins, "option_plus" : option_plus, "option_plus_plus" : option_plus_plus}

background_image_accueil = pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "accueil_background.png"))
background_image_menu = pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "menu_background.png"))
background_image_end = pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "end_background.png")).convert_alpha()