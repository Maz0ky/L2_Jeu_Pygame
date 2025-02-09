import os
import pygame

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