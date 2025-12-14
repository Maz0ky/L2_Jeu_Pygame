import os
import pygame
from entites import *
from initialisations import *
from pytmx.util_pygame import load_pygame

BASE_DIR = os.path.dirname(__file__)

def charge_map(num_map):
    mapa = load_pygame(os.path.join(BASE_DIR, "map", f"map_{num_map}.tmx"))
    # parcours toutes les couches
    tuiles_map["sprite_group"].empty()
    tuiles_map["block_group"].empty()
    tuiles_map["fatal_group"].empty()
    tuiles_map["end_group"].empty()

    for layer in mapa.visible_layers:
        if layer.name == 'Block':
            creer_tuile(layer.tiles(),'block')
        elif layer.name == 'Fatal':
            creer_tuile(layer.tiles(),'fatal')
        elif layer.name == 'End':
            creer_tuile(layer.tiles(), 'end')
        elif hasattr(layer,'data'):#si la couche a des données alors
            creer_tuile(layer.tiles(), tuiles_map["tileset_size"])

def creer_tuile(tuiles, attribut:str=''):

    for x, y, surf in tuiles: #creer une tuile
        pos = (x * tuiles_map["tileset_size"] + 800, y * tuiles_map["tileset_size"])
        match attribut:
            case 'block':
                block = Solid_Block(pos = pos, surf = surf, groups = tuiles_map["sprite_group"])
                tuiles_map["block_group"].add(block)
            case 'fatal':
                fatal = Fatal_Block(pos = pos, surf = surf, groups = tuiles_map["sprite_group"])
                tuiles_map["fatal_group"].add(fatal)
            case 'end':
                end = Finish_Block(pos = pos, surf = surf, groups = tuiles_map["sprite_group"])
                tuiles_map["end_group"].add(end)
            case _:
                Tile(pos = pos, surf = surf, groups = tuiles_map["sprite_group"])