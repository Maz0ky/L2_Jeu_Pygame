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
        self.mask = pygame.mask.from_surface(self.image)#rajoute un masque aux blocs pour avoir une collision précise

class Finish_Block(Tile):
    #classe des blocks fatals
    def __init__(self, pos, surf, groups):
        super().__init__(pos = pos, surf = surf, groups = groups)

class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        self.image = pygame.image.load("Real_Game/Tuile/Image/Player_Sprite/Shrek-1.png")
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.rect.bottomleft = start_pos
        self.game_over = False
        self.on_ground = False
        self.win = False
        self.mask = pygame.mask.from_surface(self.image)

        self.vitesse = pygame.math.Vector2(0,0)
    
    def show(self,screen):
        screen.blit(self.image, self.rect)
        
    def get_rect(self):
        return self.rect
        
    def update(self,b_grp,fatal_grp,finish_grp):
        self.collisionx(b_grp)
        self.collisiony(b_grp)
        self.check_border_map()
        self.applique_vitesse(b_grp)
        self.touch_hurting_block(fatal_grp)
        self.touch_end(finish_grp)
           
    def applique_vitesse(self,b_grp):
        self.rect.x  += self.vitesse.x
        self.check_on_ground(b_grp)
        self.rect.y  += self.vitesse.y
        self.vitesse.x = 0
        self.gravity()
    
    def check_on_ground(self,b_grp): 
        collision = self.get_hit(b_grp)
        cheat_fly = True
        i = 0
        while cheat_fly and i < len(collision):# tant que le joueur n'est pas detecté au sol
            if self.rect.clipline((collision[i].rect.left+2,collision[i].rect.top),(collision[i].rect.right-2,collision[i].rect.top)):
                cheat_fly = False
            i += 1
        if cheat_fly:
            self.on_ground = False
        
    ########## DEPLACEMENTS ##########

    def jump(self):
        if self.on_ground :
            self.on_ground = False
            self.vitesse.y = -10
    
    def jump_right(self):
        if self.on_ground :
            self.on_ground = False
            self.vitesse.y = -10
        self.vitesse.x = 5
    
    def jump_left(self):
        if self.on_ground :
            self.on_ground = False
            self.vitesse.y = -10
        self.vitesse.x = -5
    
    def gravity(self):
        if (not(self.on_ground) and self.vitesse.y < 10) :
            self.vitesse.y += 0.5
    
    ########## COLLISIONS ##########
    
    def check_border_map(self)->None:
        if self.rect.x + self.vitesse.x < 800:
            self.vitesse.x, self.rect.x = 0, 800
        elif self.rect.right + self.vitesse.x > 1600:
            self.vitesse.x, self.rect.right = 0, 1600
    
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
            if (self.vitesse.y > 0 and self.rect.clipline((block.rect.left+2,block.rect.top),(block.rect.right-2,block.rect.top))):#si touche un block du bas
                self.on_ground = True
                self.vitesse.y = 0
                self.rect.bottom = block.rect.y + 1
            elif (self.vitesse.y < 0 and self.rect.clipline((block.rect.left+2,block.rect.bottom),(block.rect.right-2,block.rect.bottom))):#si touche un block du haut
                self.vitesse.y = 0
                self.rect.y = block.rect.bottom
            
    ########## GESTION_MOUVEMENTS ##########
        
    def move(self,sens:str):
        match sens:
            case 'r':
                self.vitesse.x = 5
            case 'l':
                self.vitesse.x = -5
            case 'j':
                self.jump()
            case 'j_r':
                self.jump_right()
            case 'j_l':
                self.jump_left()
                        
    def move_from_File(self, File):
        #ne pas oublier d'importer la classe FileMouv
        sens = File.get_mouv()["mouvement"]
        elem_actuel = File.get_mouv()["element"]
        if File.est_ecoule():#si le temps du premier mouvement est terminé passe au suivant
            File.defiler_mouv()
            sens = File.get_mouv()
        File.defiler_temps()
        self.move(sens)
        return File, elem_actuel
    
    ########## MORT ET RESTART ##########
    def touch_hurting_block(self,sprite_grp):
        collision = self.get_hit(sprite_grp)
        for block in collision:
            if self.mask.overlap(block.mask,(block.rect.x - self.rect.x, block.rect.y - self.rect.y)):
                self.game_over = True
    
    def respawn(self):
        self.game_over = False
        self.rect.bottomleft = self.start_pos
    
    def touch_hurting_block(self,sprite_grp):
        if self.get_hit(sprite_grp):
            self.game_over = True
            
    def is_dead(self):
        return self.game_over

    ########## LEVEL UP ##########

    def touch_end(self,sprite_grp):
        if self.get_hit(sprite_grp):
            self.win = True
            
    def is_finish(self):
        return self.win
    
    def reset(self):
        self.win = False

