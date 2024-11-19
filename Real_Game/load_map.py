import pygame

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
        self.image = pygame.image.load("Tuile/Image/Sprite_Player_72x72/tile011.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
        self.blocked = [False for i in range(4)]#represente les 4 sens où le joueur peut être bloqué(right,left,bottom,top)
        
        #______affichage_____
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False

        self.pos =  pygame.math.Vector2(pos)
        self.vitesse = pygame.math.Vector2(5,5)
        self.force = pygame.math.Vector2(0,0)
        self.RIGHT, self.LEFT, self.BOTTOM, self.TOP = 0,1,2,3
    
    def show(self, screen):
        screen.blit(self.image, (self.rect.x+800, self.rect.y))
        
    def get_rect(self):
        return self.rect
        
    def update(self, block_group):
        group_collision = pygame.sprite.spritecollide(self,block_group,False)
        
        self.collisiondroite(group_collision)
        self.collisiongauche(group_collision)
        self.collisionbas(group_collision)
        if len(group_collision)>1:
            print(group_collision)
    
    def collisiondroite(self,group_col:list):
        i = 0
        res = False
        while not res and i < len(group_col):
            block = group_col[i].get_rect()
            print(block.topleft)
            if self.rect.collidepoint(add_list(block.topleft,(0,1))) or self.rect.collidepoint(block.bottomleft):#(self.rect.right >= block.left and not self.rect.right > block.right) and not( self.rect.bottom < block.top or self.rect.top > block.bottom):
                #verfie dans un premier temps que la collision s'effectue bien à droite et ensuite que le bloque est bien à la hauteur du joueur
                res = True
                self.rect.right = block.left
            i+=1
        self.blocked[self.RIGHT] = res
    
    def collisiongauche(self,group_col):
        i = 0
        res = False
        while not res and i < len(group_col):
            block = group_col[i].get_rect()
            if (self.rect.left <= block.right and not self.rect.left < block.left) and not( self.rect.bottom < block.top or self.rect.top > block.bottom):
                res = True
                self.rect.left = block.right
            i+=1
        self.blocked[self.LEFT] = res
    
    def collisionbas(self,group_col):
        i = 0
        res = False
        while not res and i < len(group_col):
            block = group_col[i].get_rect()
            if self.rect.collidepoint(block.topleft) or self.rect.collidepoint(block.topright):#(self.rect.bottom >= block.top and not self.rect.bottom > block.bottom) and not( self.rect.right < block.left or self.rect.left > block.right):
                res = True
                self.rect.bottom = block.top
            i+=1
        self.blocked[self.BOTTOM] = res
        
    def move(self,sens:str):
        assert sens in ('j','l','r','d'), "Doit appartenir à un mouvement connu"
        match sens:
            case 'r':
                if not self.blocked[self.RIGHT]:#s'il n'y a pas de block à droite
                    self.rect.x += self.vitesse.x
            case 'l':
                if not self.blocked[self.LEFT]:#s'il n'y a pas de block à droite
                    self.rect.x -= self.vitesse.x
            case 'j':
                if not self.blocked[self.TOP]:
                    self.rect.y -= self.vitesse.y
            case 'd':
                    if not self.blocked[self.TOP]:
                        self.rect.y += self.vitesse.y
       
    #ne pas oublier d'importer la classe File_mouv dans le dossier                 
    def move_from_File(self, File):
        sens = File.get_mouv()["mouvement"]
        if File.est_ecoule():#si le temps du premier mouvement est terminé passe au suivant
            File.defiler_mouv()
            if File.est_vide():
                return File
            sens = File.get_mouv()["mouvement"]
        File.defiler_temps()
        self.move(sens)
        return File

def add_list(list1,list2):
    assert len(list1) == len(list2), "les deux tableaux ne s'additionnent pas"
    res = []
    for i in range(len(list1)):
        res = list1[i] + list2[i]
    return res

def creer_tuile(tuiles, size_tileset, sprite_group, block_group, attribut:str=''):
    for x ,y ,surf in tuiles: #creer une tuile
        pos = (x * size_tileset +800, y * size_tileset)
        match attribut:
            case 'block':
                block = Solid_Block(pos = pos, surf = surf, groups = sprite_group)
                block_group.add(block)
            case 'fatal':
                Fatal_Block(pos = pos, surf = surf, groups = sprite_group)
            case _:
                Tile(pos = pos, surf = surf, groups = sprite_group)