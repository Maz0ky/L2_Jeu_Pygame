       
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
    
    def clear(self):
        self.file = []

# Generation de la liste des éléments déplaçables

def generer_liste_elements(elements_deplacables):
    """Trie et génère la liste d'éléments déplaçables"""
    groupes = {
        "groupe_1": [],  # y < 180
        "groupe_2": [],  # 180 <= y < 360
        "groupe_3": [],  # 360 <= y < 540
        "groupe_4": []   # y >= 540
    }
    for elem in elements_deplacables:
        y = elem[1].y  # Position y de l'élément
        if y < 155:
            groupes["groupe_1"].append(elem)
        elif 155 <= y and y < 340:
            groupes["groupe_2"].append(elem)
        elif 335 <= y and y < 530:
            groupes["groupe_3"].append(elem)

    for groupe in groupes:
        groupes[groupe].sort(key=lambda elem: elem[1].x)

    liste_elements = []
    for groupe in ["groupe_1", "groupe_2", "groupe_3"]:
        for elem in groupes[groupe]:
            if elem[2] == "Real_Game/elem/up-arrow.png":
                mouv = "j"
            elif elem[2] == "Real_Game/elem/right-arrow.png":
                mouv = "r"
            elif elem[2] == "Real_Game/elem/left-arrow.png":
                mouv = "l"
            elif elem[2] == "Real_Game/elem/pause.png":
                mouv = "p"
            elif elem[2] == "Real_Game/elem/up-right-arrow.png":
                mouv = "j_r"
            elif elem[2] == "Real_Game/elem/up-left-arrow.png":
                mouv = "j_l"
        
            liste_elements.append({"mouvement": mouv, "temps": elem[3], "element":elem})
    return liste_elements

def traiter_envoie(genere_liste_elements, elements_deplacables, click_again, file_mouvement, Joueur):
    """Gère l'envoi d'une liste d'éléments"""
    if not file_mouvement.est_vide():
        elem_actuel = Joueur.move_from_File(file_mouvement)
    else:
        elem_actuel = None
        click_again = True # Réactive envoie
    
    if genere_liste_elements:
        liste_mouvements = generer_liste_elements(elements_deplacables)  # Retourne la liste des mouvements pour l'utiliser dans Code 3
        for mouvement in liste_mouvements:
            file_mouvement.enfiler_mouv(mouvement)  # Ajoute à la file des mouvements
        genere_liste_elements = False

    return genere_liste_elements, click_again, elem_actuel