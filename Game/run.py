# Import
from sys import exit
from mouvement import *
from initialisations import *
from mise_a_jour_pages import *
from gestion_evenements import *

# Game loop principal
while True:
    match variables_jeu["level_actu"]:
        case -2 : # Page fin
            for event in pygame.event.get():
                gestion_evenements_end(event)
            mise_a_jour_page_end()

        case -1 : # Accueil
            for event in pygame.event.get():
                gestion_evenements_accueil(event)
            mise_a_jour_page_accueil()

        case 0 : # Choix niveaux
            for event in pygame.event.get():
                gestion_evenements_choix_niveau(event)
            mise_a_jour_page_choix_niveau()

        case _: # Niveaux
            if entites["Joueur"].is_finish():
                reset_fin_niveau()
                
            for event in pygame.event.get():
                gestion_evenements_level(event)
            # Traite l'envoie d'une liste d'éléments
            elem_actuel = traiter_envoie(variables_jeu, elements, entites)

            mise_a_jour_page_level(elem_actuel)