# Import
import pygame
from Initialisations import *
from mouvement import *
from gestion_page import *
from sys import exit

# Gestion de la fenêtre
pygame.init()
screen = pygame.display.set_mode((1600, 400))  # Nouvelle taille de fenêtre
pygame.display.set_caption("Zeta Jeu de la muerta")
clock = pygame.time.Clock()
fps = 60

# Initialisation
elements_fixes, elements_deplacables, selected_element, mouse_offset, click_again, button_font, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, ex_tab_mouv, player_surf, player_rect, player_gravity, speed = init()

# Game loop principal
while True:
    # Gestion évenements
    for event in pygame.event.get():
        elements_deplacables, mouse_offset, genere_liste_elements, selected_element, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, player_rect, click_again = gestion_evenements(screen, event, elements_fixes, elements_deplacables, selected_element, mouse_offset, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, element_concerne, click_again, player_rect, player_surf)
    
    # Gestion de la gravitée
    player_rect, player_gravity = gestion_gravitee(player_rect, player_gravity)

    # Traite l'envoie d'une liste d'éléments
    genere_liste_elements, player_gravity, click_again = traiter_envoie(genere_liste_elements, elements_deplacables, player_gravity, click_again, ex_tab_mouv, player_rect, speed)

    # Mise à jour de la page
    button_rect, menu_visible, menu_rect, option_supprimer, option_temps = mise_a_jour_page(screen, elements_fixes, elements_deplacables, button_text, button_rect, menu_visible, menu_rect, option_supprimer, option_temps, player_surf, player_rect, clock, fps)
    
    