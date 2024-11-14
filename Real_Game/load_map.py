import pygame
from sys import exit
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)#utilise une classe parenté de pygame pour creer les groupes dans les sprite
        self.image = pygame.transform.scale(surf,(32,32))
        self.rect = self.image.get_rect(topleft = pos)
    

class Player(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos = pos, surf = surf, groups = groups)
        self.image = pygame.transform.scale(surf,(48,48))


pygame.init()
screen = pygame.display.set_mode((800,672))
clock = pygame.time.Clock()
fps = 60
size_tileset = 32
tmx_data = load_pygame('Visi301_Mathieu_Teva/map/map_test.tmx')
sprite_group = pygame.sprite.Group()

# parcours toutes les couches
for layer in tmx_data.visible_layers:
    if hasattr(layer,'data'):#si la couche a des données alors
        for x,y,surf in layer.tiles():#creer une tuile
            pos = (x * size_tileset, y * size_tileset)
            Tile(pos = pos, surf = surf, groups = sprite_group)


for obj in tmx_data.objects:
    pos = obj.x,obj.y
    if obj.type in ('Player'):#if obj.image
        Player(pos = pos, surf = obj.image, groups = sprite_group)


#print(liste_block)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        
    screen.fill('black')
    sprite_group.draw(screen)
    pygame.display.flip() #update tout l'ecran
    clock.tick(fps) # max 60fps pour le jeu
