from random import randint
from copy import deepcopy
import params


class Pile:
  """
  Creation de la classe Pile pour sauvegarder toute une partie 
  """
  def __init__(self):
    # On initialise la taille et la pile vide
    self.taille = 0
    self.memoire = []

  @property
  def est_vide(self):
    # Verifier si la pile est vide    
    return self.taille == 0

  @property
  def sommet(self):
    # Permet de récupérer le sommet de la pile
    s = self.depiler()
    self.empiler(s)
    return s

  def empiler(self, x):
    # Rajouter un élément dans la pile
    self.memoire.append(x)
    # On change la taille vu qu'on rajoute un element
    self.taille += 1

  def depiler(self):
    # On recupere le dernier élément de la pile étant dans une LIFO
    if not self.est_vide:
        self.taille -= 1
        return self.memoire.pop()

  @property
  def as_list(self):
    """
    On creer une liste dans laquelle on met la grille pour pouvoir l'exporter dans l'historique
    """
    # On creer une liste vide
    res = []
    for i in range(self.taille):
        # On dépile chaque élément de la pile
        a = self.depiler()
        # On met la grille et le score dans la liste
        res.append([a[0], a[1]])
    # On reverse la liste
    res = res[::-1]
    # On le rempile pour ne pas toucher à la pile
    for i in range(len(res)):
        self.empiler(res[i])
    return res


class Grille:
    """
    On creer la classe Grille dans laquelle on va creer la grille et effectuer les changements
    """

    def __init__(self, c=4):
        
        
        # La grille est simplement la grille utilisée pour jouer, la première valeure est le numero de la case et la deuxieme est soit 0, soit 1, utilisée si la fusion avec une autre case a deja eu lieu.
        self.grille = [[[0, 0] for j in range(c)] for i in range(c)]

        # L'historique de la grille, générée grace à la pile est stocké dans cette variable
        self.historique = Pile()

        # On innitialise la classe avec c, comme un cote du carré
        self.c = c
        self.continued = False
        
        # Le score est le score de la partie (A chaque fusion des nombres, on les addition au score)
        self.score = 0
        # On fait cette boucle pour ajouter les deux premiers chiffres.
        for i in range(2):
            self.add_new_block()

    def __str__(self):
        """
        Fonction appellée lors de l'utilisation de print()
        C'est elle qui va afficher la grille.
        """
        max = 6
        for i in self.grille:
            for j in i:
                if len(str(j)) > max:
                    max = len(str(j))
        c = self.c
        # On affiche les lignes horizontales en fonction de la val max et de la taille de la grille
        sep = "-" * ((max + 1) * c + 1) + "\n"
        res = sep
        for i in range(len(self.grille)):
            # On rajoute ici les valeurs en dessous et au dessus de la valeure
            res += ("|" + " " * max) * c + "|\n"
            for j in range(len(self.grille[i])):
                # On met ici la valeure de la case
                res += "|" + format_n(self.grille[i][j][0], max)
            res += "|\n" + ("|" + " " * max) * c + "|\n"
            res += sep
        return res

    def add_new_block(self):
        """Rajoute un 2 ou un 4 dans une position random"""
        # On prend deux cases random
        x = randint(0, self.c - 1)
        y = randint(0, self.c - 1)
        # On utilise val pour gérer le pourcentage
        val = randint(1, 100)
        while self.grille[y][x][0] != 0:  # Tant que la case n'est pas vide, on trouve une autre case random
            x = randint(0, self.c - 1)
            y = randint(0, self.c - 1)
        # En fonction du pourcentage, on génère soit 2, soit 4
        self.grille[y][x][0] = 2 if val <= params.CASE_2_PROBA else 4

    @property
    def go(self):  #go = game over
        if self.continued:
          return 3
        won = False
        full = True
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if self.grille[i][j][0] == 0:
                    full = False
                if self.grille[i][j][0] == params.OBJECTIVE:
                    # On verifie si l'utilisateur n'a pas gagné en trouvant 2048
                      won = True

        res = 0
        if won:
            # Si l'on a trouvé 2048, res prend comme valeure 1, l'utilisateur a gagné.
            res = 1
        elif full:
          """
          On simule un mouvements dans toutes les directions et si rien ne change dans aucune direction on peut dire que la grille est pleine.  
          """ 
          # On utilise un compteur pour vérifier que les quatres mouvements sont bien vérifiés
          cpt = 0
          temp = deepcopy(self)
          # On simule le mouvement vers le haut
          temp.move_up()
          if self.grille == temp.grille:
            cpt += 1
        
          temp = deepcopy(self)
          # On simule le mouvement vers le bas
          temp.move_down()
          if self.grille == temp.grille:
            cpt += 1
        
          temp = deepcopy(self)
          # On simule le mouvement vers la gauche
          temp.move_left()
          if self.grille == temp.grille:
            cpt += 1
        
          temp = deepcopy(self)
          # On simule le mouvement vers la droite
          temp.move_right()
          if self.grille == temp.grille:
            cpt += 1
          # On vérifie bien que les quatres mouvements on été vérifiés  
          if cpt == 4:
            # res prend donc comme valeure 2, l'utilisateur a perdu
            res = 2
        return res

    def mvup(self):
        """La fonction bouge chaque case avec un nombre en accord avec les regles du jeu 2048 
        Séparée de move_up car il fallait enregistrer l'historique avant chaque mouvement, et comme on transposait la liste pour certains mouvements, on ne pouvait pas mettre l'historique à jour depuis cette fonction"""
        # On sauvegarde la grille pour l'utiliser en tant que grille précédente
        for y in range(self.c):
            for x in range(self.c):
                yb = y
                # Tant que la case n'est pas vide et que la ligne de la case n'est pas la première
                while yb > 0 and self.grille[yb][x][0] != 0:
                    # Si la case d'avant est égale a 0 ou que la case d'au dessus et la case sont les memes et que la case et la case d'avant n'ont pas déja été fusionné dans le meme mouvement 
                    if (self.grille[yb - 1][x][0] == 0 or self.grille[yb - 1][x][0] == self.grille[yb][x][0] and self.grille[yb - 1][x][1] == 0 and self.grille[yb][x][1] == 0):
                        if self.grille[yb - 1][x][0] != 0:
                            self.grille[yb - 1][x][1] = 1
                        self.score += self.grille[yb - 1][x][0] * 2
                        self.grille[yb - 1][x][0] += self.grille[yb][x][0]
                        # On initialise la case a 0 car elle a fusionnée et n'est donc plus a sa place
                        self.grille[yb][x][0] = 0
                        # On dit qu'elle a déja fusionnée et donc ne peut plus etre refusionée dans le meme tour
                        self.grille[yb][x][1] = 0
                    # On monte de ligne
                    yb -= 1
        # On réinitialise à la fin du mouvement les possibilités de fusion pour que les cases puissent fusionner au tour d'après
        for i in range(self.c):
            for j in range(self.c):
                self.grille[i][j][1] = 0

    def move_up(self):
        # On sauvegarde l'état de la grille avant le mouvement
        self.historique.empiler((deepcopy(self.grille), self.score))
        self.mvup()
        # On ne fait le mouvement que si la grille d'avant et celle d'après le mouvement sont différentes pour éviter de générer un nombre.
        if not self.historique.sommet[0] == self.grille:
            self.add_new_block()
        else:
            # On dépile a chaque mouvement pour éviter de creer des grilles pareils.
            self.historique.depiler()

    def move_down(self):
        """
        Pour eviter de coder une fonction move_down, on transpose la liste de liste vers le haut, on utilise mvup puis on la remet dans sa position d'origine
        """
        # On sauvegarde l'état de la grille avant le mouvement
        self.historique.empiler((deepcopy(self.grille), self.score))
        self.transpose()
        self.transpose()
        self.mvup()
        self.transpose()
        self.transpose()
        # On ne fait le mouvement que si la grille d'avant et celle d'après le mouvement sont différentes pour éviter de générer un nombre.
        if not self.historique.sommet[0] == self.grille:
            self.add_new_block()
        else:
            # On dépile a chaque mouvement pour éviter de creer des grilles pareils.
            self.historique.depiler()


    def move_left(self):
        """
        Pour eviter de coder une fonction move_left, on transpose la liste de liste vers le haut, on utilise mvup puis on la remet dans sa position d'origine
        """
        # On sauvegarde l'état de la grille avant le mouvement
        self.historique.empiler((deepcopy(self.grille), self.score))
        self.transpose()
        self.mvup()
        self.transpose()
        self.transpose()
        self.transpose()
        # On ne fait le mouvement que si la grille d'avant et celle d'après le mouvement sont différentes pour éviter de générer un nombre.
        if not self.historique.sommet[0] == self.grille:
            self.add_new_block()
        else:
            # On dépile a chaque mouvement pour éviter de creer des grilles pareils.
            self.historique.depiler()


    def move_right(self):
        """
        Pour eviter de coder une fonction move_right, on transpose la liste de liste vers le haut, on utilise mvup puis on la remet dans sa position d'origine
        """
        # On sauvegarde l'état de la grille avant le mouvement
        self.historique.empiler((deepcopy(self.grille), self.score))
        self.transpose()
        self.transpose()
        self.transpose()
        self.mvup()
        self.transpose()
        # On ne fait le mouvement que si la grille d'avant et celle d'après le mouvement sont différentes pour éviter de générer un nombre.
        if not self.historique.sommet[0] == self.grille:
            self.add_new_block()
        else:
            # On dépile a chaque mouvement pour éviter de creer des grilles pareils.
            self.historique.depiler()


    def transpose(self):
        """On transpose la grille vers la droite"""
        # On initialise une liste vide
        newGrille = [[[0, 0] for j in range(self.c)] for i in range(self.c)]
        for x in range(self.c):
            for y in range(self.c - 1, -1, -1):
                newGrille[x][self.c - 1 - y] = self.grille[y][x]
        self.grille = newGrille

    def export(self):
        # Fonction export pour retourner la gille a sauvegarder
        return str(deepcopy(self.historique.as_list)) + ";" + str(
            self.c) + ";" + str(self.score)


def format_n(number, n):
    """Retourne un nombre avec des espaces avant et après pour qu'il soit centré dans la case


    Args:
        nombre (int): Le nombre a formater 
        n (int): La largeur en caractères de la case


    Retourne:
        str: La case formaté e
"""

    if number == 0:
        number = ""
    l = len(str(number))
    left = " " * ((n - l) // 2)
    return left + str(number) + " " * (n - l - len(left))
