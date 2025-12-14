import os
import pygame

# Boutons

def bt_txt(texte, pos_x, pos_y):
    font = pygame.font.Font(None, 36)
    text = font.render(texte, True, (0, 0, 0))
    rect = pygame.Rect(pos_x, pos_y, text.get_width(), text.get_height())
    return [font, text, rect]

def bt_img(repertoire, nom, taille_x, taille_y, pos_x, pos_y):
    surf = pygame.image.load(os.path.join(os.path.dirname(__file__), repertoire, nom)).convert_alpha()
    surf = pygame.transform.scale(surf, (taille_x, taille_y))
    rect = surf.get_rect(midbottom=(pos_x, pos_y))
    return [surf, rect]

# Niveaux

def init_level(pygame_screen, repertoire, nom, taille, width, height, pos_start_x, pos_start_y):
    lvl_surf = pygame.image.load(os.path.join(os.path.dirname(__file__), repertoire, nom)).convert_alpha()
    lvl_surf = pygame.transform.scale(lvl_surf, taille)
    lvl_rect = lvl_surf.get_rect(midtop=(pygame_screen["screen"].get_width()*width, pygame_screen["screen"].get_height()*height))
    pos_start = (pos_start_x, pos_start_y)
    lvl_survol = False
    lvl_accessible = nom == "level_1.png" # le level1 est accessible par default
    return [lvl_surf, lvl_rect, lvl_survol, lvl_accessible, pos_start]

# Elements

def cree_surf_img(chemin: str, nom, width, height, pos_x, pos_y):
    """Création des éléments fixes (mouvements)"""
    surf = pygame.image.load(chemin).convert_alpha()
    surf = pygame.transform.scale(surf, (width, height))
    rect = surf.get_rect(topleft=(pos_x, pos_y))
    return [surf, rect, chemin, nom]