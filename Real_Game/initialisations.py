# Import
import os
import pygame
from mouvement import *
from entites import *
from init_boutons import *

BASE_DIR = os.path.dirname(__file__)

pygame.init()
pygame.display.set_caption("Zeta Jeu de la muerta")

pos_start = (800,640)
Joueur = Player(pos_start)

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
    "start" : bt_img("elem", "start.png", 200, 200, pygame_screen["screen"].get_width()/2, pygame_screen["screen"].get_height()*5/6, BASE_DIR),
    "retour_from_end" : bt_img("elem", "replay.png", 200, 200, pygame_screen["screen"].get_width()/2 + 40, pygame_screen["screen"].get_height()/2 + 150, BASE_DIR),

    "retour_de_choixlvl" : bt_txt("Retour accueil", 20, 20),
    "retour_de_page" : bt_txt("Retour menu choix level", 20, 20),

    "envoi" : bt_txt("Envoie", 690, 620),
    "reset" : bt_txt("Effacer", 690, 560)
}

def init_level(chemin, taille, width, height):
    level_surf = pygame.image.load(chemin).convert_alpha()
    level_surf = pygame.transform.scale(level_surf, taille)
    level_rect = level_surf.get_rect(midtop=(pygame_screen["screen"].get_width()*width, pygame_screen["screen"].get_height()*height))
    return level_surf, level_rect

level_1_surf, level_1_rect = init_level(os.path.join(BASE_DIR, "elem", "level_1.png"), (90, 90), 6/33, 10/27)
level_2_surf, level_2_rect = init_level(os.path.join(BASE_DIR, "elem", "level_2.png"), (130, 130), 12/41, 2/25)
level_3_surf, level_3_rect = init_level(os.path.join(BASE_DIR, "elem", "level_3.png"), (170, 170), 288/411, 1/15)
level_4_surf, level_4_rect = init_level(os.path.join(BASE_DIR, "elem", "level_4.png"), (210, 210), 85/100, 16/36)
level_5_surf, level_5_rect = init_level(os.path.join(BASE_DIR, "elem", "level_5.png"), (250, 250), 49/100, 6/15)

level_1_survol, level_2_survol, level_3_survol, level_4_survol, level_5_survol = False, False, False, False, False
level_1_accessible, level_2_accessible, level_3_accessible, level_4_accessible, level_5_accessible  = True, False, False, False, False

levels_info = [[level_1_surf, level_1_rect, level_1_survol, level_1_accessible], [level_2_surf, level_2_rect, level_2_survol, level_2_accessible], 
               [level_3_surf, level_3_rect, level_3_survol, level_3_accessible], [level_4_surf, level_4_rect, level_4_survol, level_4_accessible], 
               [level_5_surf, level_5_rect, level_5_survol, level_5_accessible]]

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
surf_1, rect_1, img1, nom1 = cree_surf_img(os.path.join(BASE_DIR, "elem", "left-arrow.png"), "left-arrow", 80, 80, 40 , 572)
surf_5, rect_5, img5, nom5 = cree_surf_img(os.path.join(BASE_DIR, "elem", "up-left-arrow.png"), "up-left-arrow", 60, 60, 180, 580)
surf_2, rect_2, img2, nom2 = cree_surf_img(os.path.join(BASE_DIR, "elem", "up-arrow.png"), "up-arrow", 80, 80, 270, 572)
surf_6, rect_6, img6, nom6 = cree_surf_img(os.path.join(BASE_DIR, "elem", "up-right-arrow.png"), "up-right-arrow", 60, 60, 370, 580)
surf_3, rect_3, img3, nom3 = cree_surf_img(os.path.join(BASE_DIR, "elem", "right-arrow.png"), "right-arrow", 80, 80, 480, 572)
surf_4, rect_4, img4, nom4 = cree_surf_img(os.path.join(BASE_DIR, "elem", "pause.png"), "pause", 55, 65, 610, 582)

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

background_image_accueil = pygame.image.load(os.path.join(BASE_DIR, "elem", "accueil_background.png"))
background_image_menu = pygame.image.load(os.path.join(BASE_DIR, "elem", "menu_background.png"))
background_image_end = pygame.image.load(os.path.join(BASE_DIR, "elem", "end_background.png")).convert_alpha()