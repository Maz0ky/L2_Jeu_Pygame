# Import
import pygame
from Initialisations import *
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
elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, button_font, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, ex_tab_mouv, player_surf, player_rect, player_gravity, speed, option_fermer_temps, option_moins, option_plus, menu_temps_rect, option_de_temps, menu_temps_visible = init()

# Game loop principal
while True:
    # Gestion évenements
    for event in pygame.event.get():
        elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, player_rect, click_again, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus = gestion_evenements(screen, event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, click_again, player_rect, player_surf, menu_temps_rect, option_de_temps, menu_temps_visible, option_fermer_temps, option_moins, option_plus)
    
    # Gestion de la gravitée
    player_rect, player_gravity = gestion_gravitee(player_rect, player_gravity)

    # Traite l'envoie d'une liste d'éléments
    genere_liste_elements, player_gravity, click_again = traiter_envoie(genere_liste_elements, elements_deplacables, player_gravity, click_again, ex_tab_mouv, player_rect, speed)

    # Mise à jour de la page
    button_rect, menu_visible, menu_rect, option_supprimer, option_temps, menu_temps_rect, option_moins, option_de_temps, option_plus, option_fermer_temps = mise_a_jour_page(screen, elements_fixes, elements_deplacables, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, player_surf, player_rect, clock, fps, menu_temps_visible, option_moins, option_de_temps, option_plus, option_fermer_temps, menu_temps_rect)