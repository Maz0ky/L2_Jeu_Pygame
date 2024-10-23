path_for_files = "Visi301_Mathieu_Teva/First_Steps"

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
        
        
class File_mouv:
    
    def __init__(self,file=[]):
        """ Instancie une file vide """
        self.file = file #un tableau
		
    def enfiler_mouv(self, element):
        """ Enfile un élément en queue de file """
        self.file.append(element)
		
    def defiler_mouv(self):
        """ Défile ( si la file n'est pas vide ! ) un élément en tête de file, et le renvoie """
        if not self.est_vide():
            return self.file.pop(0)
        
    def defiler_temps(self):
        """ Permet de decrementer le temps d'un cran pour le premier mouvement"""
        if not self.est_ecoule() and not self.est_vide():
            self.file[0]["temps"] -= 1
        
    def est_vide(self):
        """ Renvoie True si la file est vide, False sinon """
        return len(self.file) == 0
    
    def est_ecoule(self):
        """ Verifie que le premier mouvement de la file n'est pas finie"""
        if not self.est_vide():
            return self.file[0]["temps"] == 0

    def affiche(self):
        print(self.file)
    
    def get_mouv(self):
        if not self.est_vide():
            return self.file[0]

