# Import
import pygame
from initialisations import *
from mouvement import *
from gestion_page import *
from sys import exit

# Gestion de la fenêtre
pygame.init()
screen = pygame.display.set_mode((1600, 672))  # Nouvelle taille de fenêtre
pygame.display.set_caption("Zeta Jeu de la muerta")
clock = pygame.time.Clock()
fps = 60

# Initialisation
level, start_surf, start_rect, level_1_surf, level_1_rect, level_2_surf, level_2_rect, level_3_surf, level_3_rect = init_page_debut_et_fin(screen)
elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, button_font, button_text, button_rect, genere_liste_elements, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, ex_tab_mouv, player_surf, player_rect, player_gravity, speed, option_fermer_temps, option_moins, option_plus, menu_temps_rect, option_de_temps, menu_temps_visible = init_levels()

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
            level = gestion_evenements_choix_niveau(screen, event, level, level_1_rect, level_2_rect, level_3_rect)

        # [FIN] Mise à Jour de la page
        mise_a_jour_page_choix_niveau(screen, clock, fps, level_1_surf, level_1_rect, level_2_surf, level_2_rect, level_3_surf, level_3_rect)

    if level == 1:

        # [DEBUT] Gestion des évènements
        for event in pygame.event.get():

            elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, player_rect, click_again, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus = gestion_evenements_level_1(screen, event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, click_again, player_rect, player_surf, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus)
        
        # [1] Gestion de la gravitée
        player_rect, player_gravity = gestion_gravitee(player_rect, player_gravity)

        # [2] Traite l'envoie d'une liste d'éléments
        genere_liste_elements, player_gravity, click_again = traiter_envoie(genere_liste_elements, elements_deplacables, player_gravity, click_again, ex_tab_mouv, player_rect, speed)

        # [FIN] Mise à jour de la page
        button_rect, menu_visible, menu_rect, option_supprimer, option_temps, menu_temps_rect, option_moins, option_de_temps, option_plus, option_fermer_temps = mise_a_jour_page_level_1(screen, elements_fixes, elements_deplacables, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, player_surf, player_rect, clock, fps, menu_temps_visible, option_moins, option_de_temps, option_plus, option_fermer_temps, menu_temps_rect)