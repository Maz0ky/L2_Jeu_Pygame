# Import
from mouvement import *
from gestion_page import *
from initialisations import *
from sys import exit

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

        case _:
            if entites["Joueur"].is_finish():
                match variables_jeu["level_actu"]:
                    case 5 :
                        variables_jeu["level_actu"] = -2

                    case level if level in range(1, variables_jeu["nb_level"]) :  # Vérifie si level_actu est entre 1 et 4
                        variables_jeu["levels_info"][level][3] = True
                        variables_jeu["level_actu"] = 0

                entites["Joueur"].reset()
                entites["Joueur"].respawn()
                elements["elem_deplacables"] = []
                variables_jeu["file_mvt"].clear()
                variables_jeu["nb_tentatives"] = 0
                variables_jeu["genere_lst_elements"] = False
                
            for event in pygame.event.get():
                gestion_evenements_level(event)

            # Traite l'envoie d'une liste d'éléments
            elem_actuel = traiter_envoie(variables_jeu, elements, entites)

            mise_a_jour_page_level(elem_actuel)