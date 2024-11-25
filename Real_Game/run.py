# Import
import pygame
from initialisations import *
from mouvement import *
from gestion_page import *
from load_map import *
from sys import exit
from pytmx.util_pygame import load_pygame

# Gestion de la fenêtre
pygame.init()
screen = pygame.display.set_mode((1600, 672))  # Nouvelle taille de fenêtre
pygame.display.set_caption("Zeta Jeu de la muerta")
clock = pygame.time.Clock()
fps = 60

# Initialisation
level, start_surf, start_rect, button_retour_de_choixlvl, button_retour_de_page, levels_info = init_page_debut_et_fin(screen)
elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, bouton_envoi, genere_liste_elements, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, ex_tab_mouv, option_fermer_temps, option_moins, option_plus, menu_temps_rect, option_de_temps, menu_temps_visible = init_levels()

player_surf, player_rect, player_gravity, speed = None, None, None, None

# Code partie map
size_tileset = 32
map = load_pygame('Real_Game/map/map_test.tmx')
sprite_group = pygame.sprite.Group()#groupe regroupant toutes les tuiles de la map
block_group = pygame.sprite.Group()
# parcours toutes les couches
for layer in map.visible_layers:
    if layer.name == 'Block':
        block_group = creer_tuile(layer.tiles(), size_tileset, sprite_group, block_group, 'block')
    elif layer.name == 'Deathful':
        block_group = creer_tuile(layer.tiles(), size_tileset, sprite_group, block_group, 'fatal')
    elif hasattr(layer,'data'):#si la couche a des données alors
        block_group = creer_tuile(layer.tiles(), size_tileset, sprite_group, block_group)

Joueur = Player((800,640))

# Game loop principal
while True:
    if level == -1:

        # [DEBUT] Gestion des évènements
        for event in pygame.event.get():
            level = gestion_evenements_accueil(screen, event, level, start_rect)

        # [FIN] Mise à Jour de la page
        mise_a_jour_page_accueil(screen, clock, fps, start_surf, start_rect)

    if level == 0:

        # [DEBUT] Gestion des évènements
        for event in pygame.event.get():
            level = gestion_evenements_choix_niveau(screen, event, level, button_retour_de_choixlvl, levels_info)

        # [FIN] Mise à Jour de la page
        mise_a_jour_page_choix_niveau(screen, clock, fps, button_retour_de_choixlvl, levels_info)

    if level == 1:
        
        # [DEBUT] Gestion des évènements
        for event in pygame.event.get():
            elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, player_rect, click_again, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus, level = gestion_evenements_level_1(screen, event, level, elements_fixes, elements_deplacables, selected_element, mouse_offset, bouton_envoi, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, click_again, player_rect, player_surf, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus, button_retour_de_page, Joueur)

        # [1] Gestion de la gravitée à faire
        
        # [2] Traite l'envoie d'une liste d'éléments
        genere_liste_elements, click_again = traiter_envoie(genere_liste_elements, elements_deplacables, click_again, ex_tab_mouv, Joueur, block_group)

        # [FIN] Mise à jour de la page
        mise_a_jour_page_level_1(screen, elements_fixes, elements_deplacables, bouton_envoi, menu_visible, menu_rect, option_supprimer, option_temps, clock, fps, menu_temps_visible, option_moins, option_de_temps, option_plus, option_fermer_temps, menu_temps_rect, button_retour_de_page, sprite_group, Joueur, block_group)