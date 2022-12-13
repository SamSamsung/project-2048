# Fonctionnement du code
## Informations sur le code
- Créateurs : **Samuel** et **Noé**
- Date due du projet : **07/10/2022**
- Contexte :
```
2048 est un jeu vidéo de type puzzle conçu en mars 2014 par le développeur indépendant italien Gabriele Cirulli et publié en ligne sous licence libre via Github le 9 mars 2014.

Le but du jeu est de faire glisser des tuiles sur une grille, pour combiner les tuiles de mêmes valeurs et créer ainsi une tuile portant le nombre 2048. Le joueur peut toutefois continuer à jouer après cet objectif atteint pour faire le meilleur score possible.
```
## Jouer au 2048
Afin de jouer au célèbre jeu du 2048, il vous suffit d'éxécuter le fichier `2048.py`. 
## Fichiers
- `grille.py`: Implantation de la classe Grille qui représente en objet une grille du 2048. Cette classe contient le score et l'historique de la grille. L'historique est stocké sous forme de pile (structure LIFO) grâce à la classe Pile.
- `partie.py`: Implantation de la classe Partie qui représente en objet une partie de 2048. Cette classe contient une grille de classe Grille et contient des références aux attributs de l'objet grille comme le score et l'historique de cette dernière.
- `classement.py`: Implantation des fonctions permettant de gérer le classement des meilleurs joueurs.
- `saisie_en_ligne.py`: Fonction donnée par Mr.Senot. Nous ne sommes donc pas responsables de son fonctionnement. 
- `saisie.py`: Définition des touches pour contrôler le jeu. 
- `params.py`: Définition des paramètres pour personnaliser le jeu.
## Paramètres et saisies
Nom | Impact
--- | ---
`SIDE` | Définit la taille du côté de la grille (carré)
`CASE_2_PROBA` | Définit la probabilité (en %) que le nouveau chiffre soit un `2` lors de l'ajout d'un chiffre
`OBJECTIVE` | Définit l'objectif de la partie (on a par défaut 2048)
`RANKN` | Définit le nombre de joueurs à afficher lors de l'affichage des meilleurs scores
`HAUT` | Définit la touche qui commande le mouvement de la grille vers le haut
`BAS` | Définit la touche qui commande le mouvement de la grille vers le bas
`GAUCHE` | Définit la touche qui commande le mouvement de la grille vers le gauche
`DROITE` | Définit la touche qui commande le mouvement de la grille vers le droite
`QUITTER` | Définit la touche qui commande l'arrêt de la partie
`ANNULER` | Définit la touche qui permet d'annuler le mouvement qui vient d'être fait
# Répartition du travail
## Temps
Nous avons créé le jeu en lui-même dans la semaine où nous avons reçu le projet. Le reste a été fait dans les deux dernières semaines avant l'échéance. 
## Ressources humaines
Samuel | Noé
--- | ---
Structure Pile | `partie.py`
`classement.scores()` + `classement.get_pot_rank()` | `classement.historique_meilleur_score()` + `classement.print_highscores()` + `classement.format_rank()`
`main.py` | `main.py`
Début structure Grille + détection de fin de partie| `mvup()` + méthodes directionnelles
`params.py`&`saisie.py` | `params.py`&`saisie.py`
# Arborescence du projet
```shell
Structure du dossier
D:.
|   2048.py
|   classement.py
|   grille.py
|   highscores.txt
|   historique_meilleur_score.txt
|   last_games.bk 
|   params.py
|   partie.py
|   saisie.py
|   saisie_en_ligne.py
```
# Arborescence des appels
- Module principal:
  - `2048.py`
- Modules secondaires:
  - `partie.py`
    - `grille.py`
      - `params.py`
  - `classement.py`
    - `grille.py`
    - `params.py`
  - `saisie.py`
  - `params.py`
  - `saisie_en_ligne.py`
- Modules externes:
  - `os`
  - `copy`
  - `random`
  - `msvcrt`
  - `sys`
  - `tty`
  - `termios`