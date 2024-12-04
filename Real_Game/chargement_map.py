import pygame
from load_map import *
from pytmx.util_pygame import load_pygame

sprite_group = pygame.sprite.Group()#groupe regroupant toutes les tuiles de la map
block_group = pygame.sprite.Group()
fatal_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
SIZE_TILESET = 32

def charge_map(num_map):
    global sprite_group, block_group, fatal_group, end_group, SIZE_TILESET

    mapa = load_pygame("Real_Game/map/map_" + str(num_map) + ".tmx")
    # parcours toutes les couches
    for layer in mapa.visible_layers:
        if layer.name == 'Block':
            creer_tuile(layer.tiles(),'block')
        elif layer.name == 'Fatal':
            creer_tuile(layer.tiles(),'fatal')
        elif layer.name == 'End':
            creer_tuile(layer.tiles(), 'end')
        elif hasattr(layer,'data'):#si la couche a des données alors
            creer_tuile(layer.tiles(), SIZE_TILESET)

def creer_tuile(tuiles, attribut:str=''):
    for x ,y ,surf in tuiles: #creer une tuile
        pos = (x * SIZE_TILESET + 800, y * SIZE_TILESET)
        match attribut:
            case 'block':
                block = Solid_Block(pos = pos, surf = surf, groups = sprite_group)
                block_group.add(block)
            case 'fatal':
                fatal = Fatal_Block(pos = pos, surf = surf, groups = sprite_group)
                fatal_group.add(fatal)
            case 'end':
                end = Finish_Block(pos = pos, surf = surf, groups = sprite_group)
                end_group.add(end)
            case _:
                Tile(pos = pos, surf = surf, groups = sprite_group)