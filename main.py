# Importe random et combinaisons

import random

from itertools import combinations

# Classe Carte définie par 2 attribus (couleur et valeur) et 3 méthodes (__init__, __str__ et __lt__ )
class Carte:
    """Représente une carte à jouer standard."""
    #trèfle' : 0, 'carreau': 1, 'coeur': 2, 'pique':3, ordre de comparaison des couleurs
    
    # Méthode qui onstruit une carte à partir de 2 entiers couleur et valeur (couleur entre 0 et 3 et valeur entre 2 et 14)
    def __init__(self, couleur = 0, valeur = 2):
        self.couleur = couleur
        self.valeur = valeur
    
    # tableaux de couleurs et de valeurs
    noms_couleurs = ['trèfle', 'carreau', 'coeur', 'pique']
    noms_valeurs = [None, None, '2', '3', '4', '5', '6', '7','8', '9', '10', 'valet', 'dame', 'roi','as']

    # Méthode qui retourne un string représentant la carte sous forme "valeur de couleur"
    def __str__(self):
        if self.valeur==-1 or self.couleur==-1:
          return ("Carte non Valide")
        return Carte.noms_valeurs[self.valeur]+' de '+Carte.noms_couleurs[self.couleur]

    # Méthode qui teste si la carte est bien inférieure à une autre en comparant leurs valeurs puis leurs couleurs si les valeurs sont égales
    def __lt__(self, other):
    # teste si self est strictement inférieur à other
        if self.valeur < other.valeur:
            return True
        elif self.valeur > other.valeur:
            return False
        else :
            if self.couleur < other.couleur:
                return True
            else:
                return False

# Classe Paquet définie par 1 attribut (cartes qui est une liste d'objets de la classe Carte, constituée de 52 cartes) et 5 méthodes (__init__,__str__,ajouter_carte, battre et distribuer_cartes)  
class Paquet:
    """Initialise un paquet puis définit les méthodes pour le manipuler"""

    # Méthode qui construit un paquet constitué de 52 cartes : Elle utilise une boucle for pour rajouter à chaque itération, une carte à sa liste de cartes 
    def __init__(self):
        self.cartes = []
        for couleur in range(4):
            for valeur in range(2, 15):
                carte = Carte(couleur, valeur)
                self.cartes.append(carte)

    # Méthode qui retourne un string représentant toutes les cartes du Paquet: Elle utilise une boucle for pour construire une liste de strings représentant les cartes du Paquet et la convertit ensuite en string de cartes séparées par des virgules
    def __str__(self):
        res = []
        for carte in self.cartes:
            res.append(str(carte))
        return ', '.join(res)

    # Méthode qui ajoute une carte à un Paquet : Elle ajoute une carte à la liste de cartes du Paquet
    def ajouter_carte(self, carte):
        self.cartes.append(carte)

    # Méthode qui mélange les cartes du Paquet : Elle utilise la méthode shuffle de random pour mélanger aléatoirement les termes de la liste du Paquet.
    def battre(self):
        random.shuffle(self.cartes)

    # Méthode qui distribue un nombre de cartes et les attribue à une main : Elle utilise une boucle for pour supprimer à chaque fois, une carte de la liste des cartes du Paquet et la rajouter à une main (une main hérite de la classe Paquet)
    def distribuer_cartes(self, main, nombre):
        for i in range(nombre):
            main.ajouter_carte(self.cartes.pop())
    

# Classe Main qui hérite de la classe Paquet et qui est définie par 2 attributs (cartes et etiquette)  et 8 méthodes (__init__,tri, famille, quinte, couleur, quinteFlush, score et __lt__)
class Main(Paquet):
    """Représente une main au jeu de cartes."""

    # Méthode qui construit une main 
    def __init__(self, etiquette = ''):
        self.etiquette = etiquette
        self.cartes = []
        

    # Méthode qui trie les cartes d'une main : Elle utilise la méthode sort() appliquée à la liste des cartes de la main
    def tri(self):
        self.cartes.sort()

    # Méthode qui retourne le nombre maximum de points obtenus par combinaison des cartes de la main ayant la même valeur 
    def famille(self):

        # On costruit la liste des valeurs des cartes de la main
        listeValeurs=[carte.valeur for carte in self.cartes]
        
        # Liste bilan initialisée à une liste vide 
        bilan=[]
        
        # On utilise une boucle for pour remplir la liste bilan : Pour chaque valeur, on compte son nombre d'occurences et on le rajoute à bilan s'il est supérieur ou égal à 2 
        for i in range(2,15):
            nb=listeValeurs.count(i)
            if nb>=2:
                bilan.append(nb)
        # On retourne 0 (points) si la liste bilan est vide
        if len(bilan)==0:
            return 0
        # Sinon, en appliquant les règles du petit Poker, on retourne le maximum de points en fonction de la valeur max de la liste bilan (c-à-d le nombre d'occurences maximum) et aussi la longueur de la liste bilan si 2 paires de cartes ont la même valeur
        else:
            if max(bilan)==4:           #carré
                return 7
            elif max(bilan)==3:
                if len(bilan)==2:       #full
                    return 6
                else:
                    return 3            #brelan
            else:                       # ici le max de bilan est 2
                if len(bilan)==2:       #double paire
                    return 2
                else:
                    return 1            #paire

    # Méthode qui retourne le nombre de points obtenus si on a une combinaison quinte 
    def quinte(self):

        # On construit la liste des valeurs des cartes et on remplace la 1ère valeur par 1 si elle correspond à un as (c-à-d valeur = 14)
        listeValeurs=[carte.valeur for carte in self.cartes]

        if listeValeurs[0]==14:
            listeValeurs[0]=1

        # On trie ensuite les cartes de la main
        listeValeurs.sort()
        
        # On vérifie si les cartes ont des valeurs dans l'ordre : On utilise une boucle while pour vérifier si chaque valeur est suivie par la valeur qui la succède, si oui le bilan est true.
        i=0
        while i<len(listeValeurs)-1:
            if listeValeurs[i+1]!=listeValeurs[i]+1:
                return 0      #La combinaison n'est pas quinte
            i=i+1

        #On retourne 4 car on a une combinaison quinte puisqu'on n'a pas quitté la boucle avant sa fin
        return 4

    # Méthode qui retourne le nombre de points obtenus si on a une combinaison couleur 
    def couleur(self):

        # On construit la liste des couleurs des cartes
        listeCouleurs=[carte.couleur for carte in self.cartes]

        # On retourne 5 (points) si la même couleur se répète dans la liste c-à-d si le nombre d'occurences de la 1ère couleur est égal à la longueur de la liste, sinon on retourne 0 
        if listeCouleurs.count(listeCouleurs[0])==len(listeCouleurs):
            return 5
        else:
            return 0

    # Méthode qui retourne le nombre de points obtenus si on a une combinaison quinteFlush 
    def quinteFlush(self):

        # On retourne 8 la combinaison est à la fois quinte et couleur, sinon on retourne 0
        if self.quinte()==4 and self.couleur()==5:
            return 8
        else:
            return 0

    # Méthode qui retourne le score d'une main
    def score(self):
        
        # On retourne le maximum de la liste des points obtenus selon que la combinaison des cartes de la main est famille (Paire, Double Paire, Brealn, Full ou carré) ou quinte ou couleur ou quinteFlush
        return max([self.famille(),self.quinte(),self.couleur(),self.quinteFlush()])

    # Méthode qui teste si le score d'une main est inférieur strictement à celui d'une autre : Elle retourne True si oui, False sinon
    def __lt__(self, other):
    # teste si self est strictement inférieur à other
        return self.score() < other.score()

    # Méthode qui vérifie si une carte est membre d'une main c-à-d si la main comporte cette carte : Elle utilise une boucle for pour chercher si au moins l'une des cartes de la main a la même valeur et la même couleur que la carte en question et returme True si oui False sinon.
    def membre(self, carte):
        for c in self.cartes:
          if carte.valeur == c.valeur and carte.couleur == c.couleur:
            return True
        return False

def partie(main1,main2):
    """Compare deux mains et retourne un vainqueur"""
    if main1.score()>main2.score():
        return main1.etiquette+" l'emporte avec "+str(main1.score())+ " points contre "+str(main2.score())
    elif main1.score()<main2.score():
        return main2.etiquette+" l'emporte avec "+str(main2.score())+ " points contre "+str(main1.score())
    else :
        return "égalité avec un score de "+str(main1.score())+" points"

# Fonction qui sélectionne les 5 cartes de la meilleure main possible
def meilleureSelection(main):

    """sélectionne à partir d'une main, 5 cartes constituant la meilleure main possible : Elle retourne la liste constituée de ces 5 cartes"""
  
    # On initialise la liste des mains (de 5 cartes) possibles à la liste vide
    listMainsPossibles=[]

    # On construit la liste des mains possibles :
    # Pour cela, on utilise une boucle for et la fonction combinations à importer from itertools pour avoir toutes les combinaisons (ou tuples) possibles de 5 cartes   
    for tupleCartes in combinations(main.cartes, 5):

      # Pour chaque tuple de 5 cartes, on construit une main possible constituée de ces 5 cartes et on la rajoute à la liste des Mains Possibles
      mainPossible=Main()
      mainPossible.cartes=list(tupleCartes)
      listMainsPossibles.append(mainPossible)

    # On construit la liste des scores de toutes les mains possibles 
    listScores=[main.score() for main in listMainsPossibles]
    
    # On calcule le score maximum 
    scoreMax=max(listScores)

    #Puis, on utilise la méthode index pour connaitre la position du meilleur score dans la liste
    PositionMeilleurScore=listScores.index(scoreMax)

    # Enfin, on retourne les cartes de la meilleure Main Possible située à la position trouvée  
    return(listMainsPossibles[PositionMeilleurScore].cartes)

# Fonction qui convertit un texte représentant une carte en 2 entiers valeur et couleur
def text2ValeurCouleur(text):

  # On convertit le texte en minuscule pour tenir compte de la casse (c-à-d des lettres en majiscule ou minuscule)
  text=text.lower()

  # si la carte (text) commence bien par un numéro de carte, on déduit sa valeur et on la supprime de text, sinon on considère que la valeur est égal à -1  
  if len(text)>=5 and text[0:5]=='valet':
    valeur=11
    text=text[5:len(text)]
  elif len(text)>=4 and text[0:4]=='dame':
    valeur=12
    text=text[4:len(text)]
  elif len(text)>=3 and text[0:3]=='roi':
    valeur=13
    text=text[3:len(text)]
  elif len(text)>=2 and text[0:2]=='as':
    valeur=14
    text=text[2:len(text)]
  elif len(text)>=2 and text[0:2]=='10':
    valeur=10
    text=text[2:len(text)]
  elif len(text)>=1 and text[0].isdigit() and int(text[0])>1:
    valeur=int(text[0])
    text=text[1:len(text)]
  else:
    valeur=-1
  

  # si maintenant le text qui reste commence bien par la chaine " de " et se termine par une couleur, on déduit la valeur de la couleur, sinon on considère qu'elle est égale à -1 
  if len(text)>4 and text[0:4]==" de " and text[4:len(text)]=='trèfle':
    couleur=0
  elif   len(text)>4 and text[0:4]==" de " and text[4:len(text)]=='carreau':
    couleur=1
  elif   len(text)>4 and text[0:4]==" de " and text[4:len(text)]=='coeur':
    couleur=2
  elif   len(text)>4 and text[0:4]==" de " and text[4:len(text)]=='pique':
    couleur=3
  else :
    couleur=-1

  # Enfin, on retourne les 2 entiers valeur et couleur
  return(valeur,couleur)




"""Initialisation du jeu"""

# On construit un paquet
paquet = Paquet()

# On bat les cartes du paquet
paquet.battre()

# On construit la main que le joueur doit recevoir et qui est constituée de 7 cartes
mainReçue=Main('Main_Reçue')
paquet.distribuer_cartes(mainReçue, 7)

# On affiche au joueur la main qu'il reçoit
print("Vous avez reçu la main suivante composée de 7 cartes :\n")
print(mainReçue.etiquette+"\n")
print(mainReçue)

# On demande au joueur d'en sélectionner 5 cartes en les saisissant sous format string
print("\nVous devez maintenant en sélectionner 5 cartes pour définir une partie : ")
print("\nPour sélectionner une carte, il faut taper son nom sous forme : valeur de couleur; Par exemple, as de pique ou 9 de coeur \n")

# On construit une main qui sera constituée des 5 cartes sélectionnées par le joueur
mainJoueur=Main('Main que vous avez sélectionnée')
print("")

#on initialise valeur et couleur à -1 et on en construit une carte qui correpond à une carte non valide
valeur=-1
couleur=-1
carte=Carte(couleur,valeur)

# On utilise une boucle for pour construire la main sélectionnée
for i in range (5):
  # On convertit à chaque fois, la main sélectionnée (saisie) par le joueur en 2 entiers couleur et valeur et on l'oblige à l'aide d'une boucle while, à sélectionner une main de nouveau tant que la carte sélectionnée (saisie) n'est pas valide (c-à-d tant que sa couleur ou sa valeur sont égales à -1 ou elle n'est pas une carte de la main reçue ou elle a été déjà sélectionnée)
  while(carte.valeur==-1 or carte.couleur==-1 or not(mainReçue.membre(carte)) or mainJoueur.membre(carte)):

    print("Introduire Carte "+str(i+1)+ " : ")
    textCarte = input()
    carte.valeur, carte.couleur=text2ValeurCouleur(textCarte)
  
  # On construit ensuite une carte valide à partir de la carte sélectionnée et on la rajoute à la liste des cartes de la main sélectionnée
  
  carteValide=Carte(carte.couleur,carte.valeur)
  mainJoueur.cartes.append(carteValide)

  #on initialise de nouveau carte à une carte non valide pour povoir lire les valeurs de la carte suivante
  carte.valeur=-1
  carte.couleur=-1


# On utilise ensuite, la fonction meilleurSelection pour construire la main de l'ordinateur qui sera constituée automatiquement de la meilleure main possible 
mainOrdinateur=Main('Main Ordinateur')
mainOrdinateur.cartes=meilleureSelection(mainReçue)

# On tri les mains du joueur et de l'ordinateur et on les affiche triées avec leurs scores, puis on utilise la fonction partie pour afficher les résultats de la partie
mainJoueur.tri()
mainOrdinateur.tri()

"""affichage des mains et de leur score"""
print("")
print(mainJoueur.etiquette)
print("")
print(mainJoueur)
print("")
print('score de '+mainJoueur.etiquette+ ' : '+str(mainJoueur.score()))
print("")

print(mainOrdinateur.etiquette)
print("")
print(mainOrdinateur)
print("")
print("score de ",mainOrdinateur.etiquette+" : "+str(mainOrdinateur.score()))
print("")

"""Comparaison des mains"""
print(partie(mainJoueur,mainOrdinateur))


