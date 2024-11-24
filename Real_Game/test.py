"""
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,672))
clock = pygame.time.Clock()
fps = 60

J = pygame.Surface((50,50))
J.fill('red')
J_rect = J.get_rect()

block = pygame.Surface((60,30))
block.fill('blue')
block_rect = block.get_rect()
block_rect.x = 200
block_rect.y = 100
collisiond,collisionb = False, False

while True:
    deltatime = clock.tick(60) * .001 * fps #stabilise les frames de l'image à 60 fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and not collisiond:
        J_rect.x += 5
    if keys[pygame.K_q]:
        J_rect.x -= 5
    if keys[pygame.K_z]:
        J_rect.y -= 5
    if keys[pygame.K_s] and not collisionb:
        J_rect.y += 5
    
    collisiond = J_rect.collidepoint(block_rect.topleft) or J_rect.collidepoint(block_rect.bottomleft) 
    if collisiond:
        J_rect.x = block_rect.x - J_rect.width
    
    collisionb = J_rect.collidepoint(block_rect.topleft) or J_rect.collidepoint(block_rect.topright)
    if collisionb:
        J_rect.x = block_rect.top
    
    screen.blit(J,J_rect)
    screen.blit(block,block_rect)
    
    pygame.display.flip() #update tout l'ecran


# Gestion de la gravité

def gestion_gravitee(player_rect, player_gravity):
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
        player_gravity = 0
    else:
        player_gravity += 0.5
    return player_rect, player_gravity
"""
import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from mouvement import *

RIGHT,LEFT,BOTTOM,TOP = 0,1,2,3
class Tile(pygame.sprite.Sprite):
    #sera toutes les tuiles construisant la map
    def __init__(self, pos, surf, groups):
        super().__init__(groups)#utilise une classe parenté de pygame pour creer les groupes dans les sprite
        self.image = pygame.transform.scale(surf,(32,32))
        self.rect = self.image.get_rect(topleft = pos)
    
    def get_rect(self):
        return self.rect

class Solid_Block(Tile):
    #classe des blocks collisionables
    def __init__(self, pos, surf, groups):
        super().__init__(pos = pos, surf = surf, groups = groups)
    
    def udate(self, player):
        if self.rect.colliderect(player.get_rect()):
            pass
            

class Fatal_Block(Tile):
    #classe des blocks fatals
    def __init__(self, pos, surf, groups):
        super().__init__(pos = pos, surf = surf, groups = groups)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Real_Game/Tuile/Image/Sprite_Player_72x72/tile011.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.blocked = [False for i in range(4)]#represente les 4 sens où le joueur peut être bloqué(right,left,bottom,top)
        
        #______affichage_____
        #self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, True

        self.vitesse = pygame.math.Vector2(0,0)
        #self.force = pygame.math.Vector2(0,0) 
    
    def show(self):
        screen.blit(self.image, self.rect)
        
    def get_rect(self):
        return self.rect
        
    def update(self,b_grp):     
        
        self.collisionx(b_grp)
        self.collisiony(b_grp)
        self.applique_vitesse()
        
        
        
    def applique_vitesse(self):
        self.rect.x  += self.vitesse.x
        self.rect.y  += self.vitesse.y
        self.vitesse.x = 0
        self.gravity()
        
    def jump(self):
        if self.on_ground :
            self.is_jumping, self.on_ground = True, False
            self.vitesse.y = -20
    
    def gravity(self):
        if self.is_jumping :
            self.vitesse.y += 1
    
    def get_hit(self, sprite_grp):
        return pygame.sprite.spritecollide(self,sprite_grp,False)
    
    def collisionx(self, sprite_grp):
        collision = self.get_hit(sprite_grp)
        for block in collision:
            if (self.vitesse.x > 0 and 
                (self.rect.collidepoint(block.rect.topleft) or 
                   self.rect.collidepoint(block.rect.bottomleft))):#si touche un block de la droiteq
                self.rect.x = block.rect.x - self.rect.width
            elif (self.vitesse.x < 0 and 
                  (self.rect.collidepoint(block.rect.topright) or 
                   self.rect.collidepoint(block.rect.bottomright))):#si touche un block de la gauche
                self.rect.x = block.rect.right
    
    def collisiony(self, sprite_grp):
        #self.on_ground = False
        #self.rect.bottom += 1
        collision = self.get_hit(sprite_grp)
        for block in collision:
            if (self.vitesse.y > 0):#si touche un block du bas
                self.is_jumping = False
                self.on_ground = True
                self.vitesse.y = 0
                self.rect.bottom = block.rect.y
            elif (self.vitesse.y < 0):#si touche un block du haut
                self.vitesse.y = 0
                self.rect.y = block.rect.bottom + self.rect.height
        
    # def collisiondroite(self,group_col:list):
    #     i = 0
    #     res = False
    #     while not res and i < len(group_col):
    #         block = group_col[i].get_rect()
    #         if self.rect.collidepoint(add_list_int(block.topleft,(0,6))) or self.rect.collidepoint(add_list_int(block.bottomleft,(0,-6))):#(self.rect.right >= block.left and not self.rect.right > block.right) and not( self.rect.bottom < block.top or self.rect.top > block.bottom):
    #             #verfie dans un premier temps que la collision s'effectue bien à droite et ensuite que le bloque est bien à la hauteur du joueur
    #             res = True
    #             self.rect.x = block.x - self.rect.width
    #         i+=1
    #     self.blocked[RIGHT] = res
    
    # def collisiongauche(self,group_col):
    #     i = 0
    #     res = False
    #     while not res and i < len(group_col):
    #         block = group_col[i].get_rect()
    #         if self.rect.collidepoint(add_list_int(block.topright,(0,6))) or self.rect.collidepoint(add_list_int(block.bottomright,(0,-6))):#if (self.rect.left <= block.right and not self.rect.left < block.left) and not( self.rect.bottom < block.top or self.rect.top > block.bottom):
    #             res = True
    #             self.rect.x = block.x + block.width
    #         i+=1
    #     self.blocked[LEFT] = res
    
    def collisionbas(self,group_col):
        i = 0
        res = False
        while not res and i < len(group_col):
            block = group_col[i].get_rect()
            if self.rect.collidepoint(add_list_int(block.topleft,(6,0))) or self.rect.collidepoint(add_list_int(block.topright,(-6,0))):#(self.rect.bottom >= block.top and not self.rect.bottom > block.bottom) and not( self.rect.right < block.left or self.rect.left > block.right):
                res = True
                self.rect.y = block.y - self.rect.height
            i+=1
        self.blocked[BOTTOM] = res
        
    def move(self,sens:str):
        assert sens in ('j','l','r','d'), "Doit appartenir à un mouvement connu"
        match sens:
            case 'r':
                if not self.blocked[RIGHT]:#s'il n'y a pas de block à droite
                    self.vitesse.x = 4
            case 'l':
                if not self.blocked[LEFT]:#s'il n'y a pas de block à droite
                    self.vitesse.x = -4
            case 'j':
                if not self.blocked[TOP]:
                    self.jump()
       
    #ne pas oublier d'importer la classe File_mouv dans le dossier                 
    def move_from_File(self, File: File_mouv):
        sens = File.get_mouv()["mouvement"]
        if File.est_ecoule():#si le temps du premier mouvement est terminé passe au suivant
            File.defiler_mouv()
            sens = File.get_mouv()
        File.defiler_temps()
        self.move(sens)
        return File
    
    def teleport_player(self,co):
        self.rect.x = co[0]
        self.rect.y = co[1]

def add_list_int(list1,list2):
    assert len(list1) == len(list2), "les deux tableaux ne s'additionnent pas"
    res = []
    for i in range(len(list1)):
        res += [list1[i] + list2[i]]
    return res
        
pygame.init()
screen = pygame.display.set_mode((800,672))
clock = pygame.time.Clock()
fps = 60
size_tileset = 32
map = load_pygame('Real_Game/map/map_test.tmx')
sprite_group = pygame.sprite.Group()#groupe regroupant toutes les tuiles de la map
block_group = pygame.sprite.Group()

def creer_tuile(tuiles, attribut:str=''):
    for x,y,surf in tuiles:#creer une tuile
            pos = (x * size_tileset, y * size_tileset)
            match attribut:
                case 'block':
                    block = Solid_Block(pos = pos, surf = surf, groups = sprite_group)
                    block_group.add(block)
                case 'fatal':
                    Fatal_Block(pos = pos, surf = surf, groups = sprite_group)
                case _:
                    Tile(pos = pos, surf = surf, groups = sprite_group)

# parcours toutes les couches
for layer in map.visible_layers:
    if layer.name == 'Block':
        creer_tuile(layer.tiles(),'block')
    elif layer.name == 'Deathful':
        creer_tuile(layer.tiles(),'fatal')
    elif hasattr(layer,'data'):#si la couche a des données alors
        creer_tuile(layer.tiles())
            
Joueur = Player((0,640))

while True:
    deltatime = clock.tick(60) * .001 * fps #stabilise les frames de l'image à 60 fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
            
        
    sprite_group.draw(screen)
    Joueur.show()
    Joueur.update(block_group)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        Joueur.move('r')
    if keys[pygame.K_q]:
        Joueur.move('l')
    if keys[pygame.K_z] or keys[pygame.K_SPACE]:
        Joueur.move('j')
    
    pygame.display.flip() #update tout l'ecran
    