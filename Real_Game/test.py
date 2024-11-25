import pygame
from sys import exit
from pytmx.util_pygame import load_pygame
from mouvement import *

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
        
        #______affichage_____
        #self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.on_ground = False

        self.vitesse = pygame.math.Vector2(0,0)
        #self.force = pygame.math.Vector2(0,0) 
    
    def show(self,screen):
        screen.blit(self.image, self.rect)
        
    def get_rect(self):
        return self.rect
        
    def update(self,b_grp):
        self.collisionx(b_grp)
        self.collisiony(b_grp)
        self.applique_vitesse(b_grp)
           
    def applique_vitesse(self,b_grp):
        self.rect.x  += self.vitesse.x
        self.check_on_ground(b_grp)
        self.rect.y  += self.vitesse.y
        self.vitesse.x = 0
        self.gravity()
    
    def check_on_ground(self,b_grp):
        collision = self.get_hit(b_grp)
        if not(collision):
            self.on_ground = False
        
    def jump(self):
        if self.on_ground :
            self.on_ground = False
            self.vitesse.y = -10
    
    def gravity(self):
        if not self.on_ground :
            self.vitesse.y += 0.5
    
    def get_hit(self, sprite_grp):
        return pygame.sprite.spritecollide(self,sprite_grp,False)
    
    def collisionx(self, sprite_grp):
        collision = self.get_hit(sprite_grp)
        for block in collision:
            if (self.vitesse.x > 0 and self.rect.collidepoint(block.rect.midleft)):#si touche un block de la droiteq
                self.rect.x = block.rect.x - self.rect.width
            elif (self.vitesse.x < 0 and self.rect.collidepoint(block.rect.midright)):#si touche un block de la gauche
                self.rect.x = block.rect.right
    
    def collisiony(self, sprite_grp):
        collision = self.get_hit(sprite_grp)
        for block in collision:
            if (self.vitesse.y > 0 and self.rect.collidepoint(block.rect.midtop)):#si touche un block du bas
                self.on_ground = True
                self.vitesse.y = 0
                self.rect.bottom = block.rect.y + 1
            elif (self.vitesse.y < 0 and self.rect.collidepoint(block.rect.midbottom)):#si touche un block du haut
                self.vitesse.y = 0
                self.rect.y = block.rect.bottom
        
    def move(self,sens:str):
        assert sens in ('j','l','r','p'), "Doit appartenir à un mouvement connu"
        match sens:
            case 'r':
                self.vitesse.x = 4
            case 'l':
                self.vitesse.x = -4
            case 'j':
                self.jump()
       
    #ne pas oublier d'importer la classe File_mouv dans le dossier                 
    def move_from_File(self, File):
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
    Joueur.show(screen)
    Joueur.update(block_group)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        Joueur.move('r')
    if keys[pygame.K_q]:
        Joueur.move('l')
    if keys[pygame.K_z] or keys[pygame.K_SPACE]:
        Joueur.move('j')
    
    pygame.display.flip() #update tout l'ecran
    