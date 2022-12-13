import params
from grille import Grille


def scores():
    """
    Utilisation du tri a bulle pour retourner la liste des scores triés
    """
    # On ouvre le fichier et on place les scores dans une liste L
    with open("highscores.txt", "r") as file:
        L = [x.split(";") for x in file.read().split("\n") if x != ""]
    # On utilise le tri à bulle vu en classe
    for i in range(len(L)):
        for j in range(len(L) - 1):
            if int(L[j][1]) < int(L[j + 1][1]):
                aux = L[j]
                L[j] = L[j + 1]
                L[j + 1] = aux
    return L


def print_highscores():
    """
    On affiche les meilleurs scores
    """

    print("Rang   Nom          Score")
    print("-------------------------")
    lines = scores()
    # On borne la liste des meilleurs scores de 0 au, minimum entre le nombre de scores a afficher et la taille du fichier pour ne pas avoir de problème si on il n'y a pas assez de score affiché
    lines = lines[:min(params.RANKN, len(lines))]
    for line in range(len(lines)):
        # On affiche le rank; le nom, le score
        print(line + 1, " "*format_rank(line, lines), lines[line][0],
                " " * (11 - len(lines[line][0])), lines[line][1])


def format_rank(line, lines):
  """
  Fonction permettant d'avoir un entier pour avoir des espaces en moins pour aligner les rangs avec les noms et les scores
  """
  return len(str(len(lines)))-len(str(line+1))+2# On soustrait à la longueur du plus grand classement la longueur du classement actuel et on ajoute 2 pour aligner les noms avec le header "Nom"


def get_pot_rank(score):
    """
    On obtient le rang du joueur
    """
    highscores = scores()
    # On fait une boucle avec comme taille tous les meilleurs scores
    for i in range(len(highscores)):
        # Si le score du joueur est supérieur on retourne son index + 1 pour ne pas commencer à zéro
        if score > int(highscores[i][1]):
            return i + 1
    # On retourne 1 si le fichier est vide
    return 1


def historique_meilleur_score():
    """
    Enregistrer l'historique du meilleur score
    """
    # On ouvre le fichier
    with open("historique_meilleur_score.txt", "r") as file:
      text = file.read().split(";")
    # On convertit la chaine de caractère en liste pour pouvoir l'utiliser
    grilles = eval(text[0])
    # On fait une boucle
    for grille in grilles:
        # On définit g comme le cote de la grille
        g = Grille(int(text[1]))
        # on définit la grille comme la grille du fichier
        g.grille = grille[0]
        # On print le score
        print("Score:", grille[1])
        # On print la grille
        print(g)
        