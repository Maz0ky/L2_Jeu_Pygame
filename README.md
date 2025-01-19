# L2_Jeu_Pygame -> Projet L2 CMI Visi301
Il s'agit d'un projet de création d'un jeu sur pygame fait par des étudiants en L2 CMI Info à L'USMB (2024-2025)
Atteindrez vous la mystique page de fin du jeu?

## Le jeu

### Introduction au jeu
Il s'agit d'un jeu de plateforme qui semble être comme les autres mais qui ne l'est pas !!
Vous n'allez pas manipuler votre personnage avec un quelconque appui sur une touche !

Ici, vous faites face à une double interface.
- La première est dédiée à la création d'une suite de mouvement. Il s'agira de générer une séquences de mouvements (gauche, droite, pause ou encore saut droits et diagonaux) avec un temps d'execution choisit.
- La seconde est dédiée au terrain sur lequel votre personnage va évoluer en executant la séquence fournie.


### But du jeu

Vous devrez guider votre personnage jusqu'au portes de 5 niveaux tous plus durs les uns que les autres afin terminer le jeu.

### Les commandes du jeu

-> Sur la première page, cliquez sur Start pour accéder à la page de choix de niveaux.

-> Sur la page de choix de niveaux cliquez sur l'un des 5 niveaux disponible (en blanc donc) pour le lancer. Le niveau 5 s'illustre du sigle de dragon.

-> Sur les pages de niveaux:
- Sur l'interface de gauche :
  - Pour revenir au menu de choix des niveaux, appuyez sur le bouton **Retour menu choix level** (Attention, appuyez bien sur le texte et non sur sa bulle).
  - Les éléments en bas (flèches directionnelles et pauses) sont des éléments fixes.
  - Votre nombre de tentative figure en haut à droite. Essayez de réaliser le niveaux avec réalisant le moins d'actions possible !
  - Cliquez gauche sur un élément fixe, maintenez enfoncé et déplacez la sourie pour créer un élément déplaçable.
  - Cliquez gauche sur un élément déplaçable, maintenez enfoncé et déplacez la souris pour déplacer un élément déplaçable.
  - Placez un élément sur une des troies lignes de l'interface pour le placer dans la zone dédiée. Tout élément ailleur sera supprimé ou non lu lors de la lecture de la séquence.
  - Les éléments déplaçable figurant dans la zone dédiée sont lu de gauche à droite et de bas en haut lors de la lecture de la séquence.
  - Evitez de placer un élément entre deux lignes pour éviter tout ordre de lecture indésirable.
  - Interchanger la position de deux éléments interchange donc leur ordre de lecture.
  - Pour lire la séquence, appuyez sur le bouton **envoie** (Attention, appuyez bien sur le texte et non sur sa bulle). *Notez que le double clique peut résulter sur un bug. Essayer de ne cliquer qu'une fois sur le bouton envoie à chaque fois*.
  - Pour écraser toute la séquence, appuyez sur le bouton **effacer** (Attention, appuyez bien sur le texte et non sur sa bulle).
  - Vous pouvez effectuer deux actions en clickant droit sur un élément déplaçable.
     - Supprimer l'élément en appuyant sur le bouton **Supprimer**.
     - Modifier le temps de l'élément en appuyant sur le bouton **Modifier temps**.
       - Vous visualisez alors le temps de l'élément.
       - Cliquez sur - et + pour réduire et augmenter ce temps de 1.
       - Cliquez sur -- et ++ pour réduire et augmenter ce temps de 10.
       - N'oubliez pas de fermer ce menu à l'aide du bouton **Fermer**.
  - Lors de la lecture d'une liste de mouvement, vous visualisez la lecture en temps réel à l'aide du grossissement de l'élément qui est lu.
  

- Sur l'interface de droite
  - Vous pouvez visualiser le résultat de votre séquence d'instruction.
  - Votre personnage est replacé au départ à chaque lecture de séquence.
  - S'il touche un pic, votre personnage meurt et sa position est réinitialisée.
  - S'il atteint une porte (ressemble à des guirlandes verticales), le niveau est réussi et vous basculez sur la pâge de choix de niveaux.

-> Lorsque les 5 niveaux sont terminés, vous arrivez sur la page de fin. Vous pouvez alors revenir sur la page de choix de niveaux. *Pourquoi ne pas tenter de terminer les niveaux avec le moins de tentatives possibles ??? Arriverez vous à tous les terminer en un seul essai !?*

### Installation du jeu
#### Windows
Il suffit de télécharger le code et de l'ouvrir sur un IDE tel que Visual Studio Code ou PyCharm par exemple. Pour une problématique de chemins, il faut ouvrir le code à partir du dossier "Visi301_Mathieu_Teva".

Il faut ensuite s'assurer d'avoir bien installé python.

Enfin, il faut installer les deux dépendances suivantes (à l'aide d'un **pip install** par exemple):
- pygame
- pytmx

### Linux
En fonction de votre distribution linux, la manipulation n'est pas la même. En premier lieu, essayez la manipulation windows.

Si cela ne fonctionne pas à cause du blocage du pip install (comme c'est le cas sur Ubuntu à partir d'une certaine version), il faudra créer un environnement virtuel.

Pour ce faire, executez les commandes suivantes dans un terminal: 

- **1 : Se placer dans le bon répertoire :**

cd ~blabla/L2_Jeu_Pygame (bien penser à modifier le chemin pour que cela fonctionne)

- **2 : Créer l'environnement virtuel :**

python3 -m venv venv

- **3 : Activer l'environnement virtuel :**

source venv/bin/activate

- **4 : Mettre à jour pip :**

pip install --upgrade pip

- **5 : Installer les dépendances :**

pip install pygame pytmx

- **6 : Lancer le script python :**

python Real_Game/run.py

Notez que si vous souhaitez désactiver l'environnement virtuel, il suffit d'utiliser la commande "**deactivate**"

## Crédits
- PHILIPPE Teva
- BRUNOT Mathieu
