# Import
import os
import pygame
from mouvement import *
from entites import *
from init_fonctions import *

pygame.init()
pygame.display.set_caption("Zeta Jeu de la muerta")

sprite = {
    "niveau_1" : "Shrek-1.png",
    "niveau_2" : "Shrek-1.png",
    "niveau_3" : "Shrek-1.png",
    "niveau_4" : "Shrek-1.png",
    "niveau_5" : "Shrek-1.png",    
}

entites = {
    "Joueur" : Player(sprite["niveau_1"])
}

pygame_screen = {
    "fps" : 60,
    "clock" : pygame.time.Clock(),
    "screen" : pygame.display.set_mode((1600, 672))
}

variables_jeu = {
    "level_actu" : -1,
    "nb_tentatives" : 0,
    "nb_level" : 5,

    "elem_select" : None, # Correspond à l'élément séléctionné
    "mouse_offset" : (0, 0),
    "click_again" : True, # Indique si l'on peut cliquer à nouveau
    "file_mvt" : File_mouv([]), # Initialisation de la file des mouvements
    "genere_lst_elements" : False,

    # [lvl_surf, lvl_rect, lvl_survol, lvl_accessible, pos_start]
    "levels_info" : [init_level(pygame_screen, "elem", "level_1.png", (90, 90), 6/33, 10/27, 801, 635), 
                   init_level(pygame_screen, "elem", "level_2.png", (130, 130), 12/41, 2/25, 801, 635), 
                   init_level(pygame_screen, "elem", "level_3.png", (170, 170), 288/411, 1/15, 801, 635), 
                   init_level(pygame_screen, "elem", "level_4.png", (210, 210), 85/100, 16/36, 801, 635), 
                   init_level(pygame_screen, "elem", "level_5.png", (250, 250), 49/100, 6/15, 801, 635)]
}

backgrounds = {
    "accueil" : pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "accueil_background.png")),
    "menu" : pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "menu_background.png")),
    "fin" : pygame.image.load(os.path.join(os.path.dirname(__file__), "elem", "end_background.png")).convert_alpha()
}

boutons = {
    # [surf, rect]
    "start" : bt_img("elem", "start.png", 200, 200, pygame_screen["screen"].get_width()/2, pygame_screen["screen"].get_height()*5/6),
    "retour_from_end" : bt_img("elem", "replay.png", 200, 200, pygame_screen["screen"].get_width()/2 + 40, pygame_screen["screen"].get_height()/2 + 150),

    # [font, text, rect]
    "retour_de_choixlvl" : bt_txt("Retour accueil", 20, 20),
    "retour_de_page" : bt_txt("Retour menu choix level", 20, 20),

    # [font, text, rect]
    "envoi" : bt_txt("Envoie", 700, 620),
    "reset" : bt_txt("Effacer", 700, 560)
}

menu = {
    "menu_visible" : False, # Indique si le menu (temps et suppression) doit être affiché
    "menu_rect" : None,
    "option_supprimer" : None,
    "option_temps" : None,
    "element_concerne" : None,
    "menu_temps_visible" : False, # Indique si le menu temps doit être affiché
    "menu_temps_rect" : None,
    "option_de_temps" : None,
    "option_fermer_temps" : None,
    "option_moins" : None,
    "option_moins_moins" : None,
    "option_plus" : None,
    "option_plus_plus" : None
}

elements = {
    # [surf, rect, chemin, nom]
    "elem_fixes" : [cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "left-arrow.png"), "left-arrow", 80, 80, 40 , 572),
                  cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-arrow.png"), "up-arrow", 80, 80, 270, 572),
                  cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "right-arrow.png"), "right-arrow", 80, 80, 480, 572),
                  cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "pause.png"), "pause", 55, 65, 610, 582),
                  cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-left-arrow.png"), "up-left-arrow", 60, 60, 180, 580),
                  cree_surf_img(os.path.join(os.path.dirname(__file__), "elem", "up-right-arrow.png"), "up-right-arrow", 60, 60, 370, 580)],
    "elem_deplacables" : [],

    # Barre de séparations des mouvements
    "separation_mouvements" : [((0, 180), (800, 180), 3), ((0, 360), (800, 360), 3), ((0, 540), (800, 540), 3)]
}

tuiles_map = {
    "sprite_group" : pygame.sprite.Group(), # groupe regroupant toutes les tuiles de la map
    "block_group" : pygame.sprite.Group(),
    "fatal_group" : pygame.sprite.Group(),
    "end_group" : pygame.sprite.Group(),
    "tileset_size" : 32
}