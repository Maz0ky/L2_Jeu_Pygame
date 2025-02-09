# Import
from mouvement import *
from gestion_page import *
from initialisations import *
from sys import exit

# Game loop principal
while True:

    if variables_jeu["level_actu"] == -2: # Page Fin

        for event in pygame.event.get():
            gestion_evenements_end(event)

        mise_a_jour_page_end()
    
    elif variables_jeu["level_actu"] == -1: # Accueil

        for event in pygame.event.get():
            gestion_evenements_accueil(event)

        mise_a_jour_page_accueil()

    elif variables_jeu["level_actu"] == 0: # Choix niveaux

        for event in pygame.event.get():
            gestion_evenements_choix_niveau(event)

        mise_a_jour_page_choix_niveau()

    else:
        if entite["Joueur"].is_finish():
            match variables_jeu["level_actu"]:
                case 5:
                    variables_jeu["level_actu"] = -2
                case level if level in range(1, variables_jeu["nb_level"]):  # Vérifie si level_actu est entre 1 et 4
                    levels_info[level][3] = True
                    variables_jeu["level_actu"] = 0

            variables_jeu["nb_tentatives"] = 0
            entite["Joueur"].respawn()
            entite["Joueur"].reset()
            genere_liste_elements = False
            file_mouvement.clear()
            elements_deplacables = []

        # [DEBUT] Gestion des évènements
        for event in pygame.event.get():
            genere_liste_elements, click_again, elements_deplacables = gestion_evenements_level(event, click_again, elements_deplacables)

        # [2] Traite l'envoie d'une liste d'éléments
        genere_liste_elements, click_again, elem_actuel = traiter_envoie(genere_liste_elements, elements_deplacables, click_again, file_mouvement, entite["Joueur"])

        # [FIN] Mise à jour de la page
        mise_a_jour_page_level(elem_actuel, elements_deplacables)