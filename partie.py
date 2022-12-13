from grille import Grille

# On creer notre classe Partie
class Partie():
  def __init__(self, c=4):
    """
    On initialise la grille avec la taille d'un de ses cotés
    """
    self.grille = Grille(c)

  @property
  def score(self):
    """
    Pour récupérer le score
    """
    return self.grille.score

  @property
  def historique(self):
    """
    Correspond à l'historique stocké dans la classe Grille
    (Cela a mené à un bug car en redéfinissant la grille, on réinitialisait l'historique)
    """
    return self.grille.historique

  @property
  def go(self):
    """
    Variable determinant si l'état de la partie (arrété, gagné...)
    """
    return self.grille.go

  def __str__(self):
    """
    Imprimer la classe
    """
    return str(self.grille)

  def move_up(self):
    """
    Les cases de la grille font un mouvement vers le haut
    """
    self.grille.move_up()

  def move_down(self):
    """
    Les cases de la grille font un mouvement vers le bas
    """
    self.grille.move_down()

  def move_left(self):
    """
    Les cases de la grille font un mouvement vers la gauche
    """
    self.grille.move_left()

  def move_right(self):
    """
    Les cases de la grille font un mouvement vers la droite
    """
    self.grille.move_right()

  def export(self):
    """
    On export la grille
    """
    return self.grille.export()