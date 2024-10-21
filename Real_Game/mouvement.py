

class Player:
    def __init__(self,coo,hp) -> None:
        self.coo = coo
        self.hp = hp
        self.surf = pygame.image.load(path_for_files + '/graphics/Player/player_walk_1.png').convert_alpha()
        self.rect = self.surf.get_rect(bottomleft = self.coo )
        
    def kill(self):
        self.hp -= 1
        
    def move_of(self, vect):
        self.rect.move(vect)
        
        
class File:
    
    def __init__(self,file=[]):
        """ Instancie une file vide """
        self.file = file #un tableau
		
    def enfiler(self, element):
        """ Enfile un élément en queue de file """
        self.file.append(element)
		
    def defiler(self):
        """ Défile ( si la file n'est pas vide ! ) un élément en tête de file, et le renvoie """
        if not self.est_vide():
            return self.file.pop(0)
        
    def est_vide(self):
        """ Renvoie True si la file est vide, False sinon """
        return len(self.file) == 0
    
    def affiche(self):
        return self.file

