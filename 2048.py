from partie import Partie
import params
import saisie
from os import system as cmd
from copy import deepcopy
import saisie_en_ligne
import classement

def print_grid(partie):
      cmd("clear")
      print(f"""
***** Bienvenue au 2048 *****

Le jeu 2048 est sufisamment célèbre pour ne pas à présenter les règles et le but du jeu

Rappels de touches de direction :
- {saisie.HAUT} : haut
- {saisie.BAS} : bas
- {saisie.DROITE} : droite
- {saisie.GAUCHE} : gauche
- {saisie.QUITTER} : quitter la partie en cours
- {saisie.ANNULER} : annuler le dernier coup
""")
      print("Score:", partie.score)
      print(partie)

# On regarde si le fichier highscores.txt existe
try:
  open("highscores.txt", "r")
except FileNotFoundError:
    # Sinon on le créer en écrivant rien dedans
     with open("highscores.txt", "w") as file:
        file.write("")

# On regarde si le fichier historique_meilleur_score.txt existe
try:
  open("historique_meilleur_score.txt", "r")
except FileNotFoundError:
  # Sinon on le créer en écrivant rien dedans
  with open("historique_meilleur_score.txt", "w") as file:
    file.write("")


# On creer la boucle rejouer qui contient tout le code principal, pour pouvoir rejouer
rejouer = True
while rejouer:
    jouer = True
    # On initionalise la partie en appelant la classe partie
    partie = Partie(params.SIDE)
    cmd("clear")
    
    print(f"""
***** Bienvenue au 2048 *****

Le jeu 2048 est sufisamment célèbre pour ne pas à présenter les règles et le but du jeu

Rappels de touches de direction :
- {saisie.HAUT} : haut
- {saisie.BAS} : bas
- {saisie.DROITE} : droite
- {saisie.GAUCHE} : gauche
- {saisie.QUITTER} : quitter la partie en cours
- {saisie.ANNULER} : annuler le dernier coup
""")
    # On ouvre le fichier last_games.bk pour utiliser la sauvegarde
    with open("last_games.bk", "r") as file:
        bck = file.read().split(";")

    # On regarde si le fichier existe
    if len(bck) == 3:
        print(
            "Une sauvegarde a été trouvée, voulez-vous tenter de la restaurer ? (O/N)"
        )
        # Si l'utilisateur le veut.
        if "o" in input().lower():
          # Aucune garantie que la liste est bien formatée
            try:
                partie = Partie(int(bck[1]))
                plt = eval(bck[0])
                for y in range(len(plt)):
                    partie.historique.empiler([plt[y][0], int(plt[y][1])])
                a = partie.historique.depiler()
                partie.grille.grille = a[0]
                partie.grille.score = a[1]
            # Si erreur tout le code a une erreur donc on met except
            except Exception as e:
                partie = Partie(params.SIDE)
    
    # On utilise la liste_caracteres_autorises pour la saisie en ligne
    liste_caracteres_autorises = [
        saisie.HAUT, saisie.BAS, saisie.DROITE, saisie.GAUCHE, saisie.QUITTER,
        saisie.ANNULER
    ]
    
    # On initialise la variable qui permet de sauvegarder la grille
    save = False
      
    # On creer la boucle de jeu principale
    while jouer:
        print_grid(partie)
        # On utilise la saisie en ligne
        move = saisie_en_ligne.saisir(liste_caracteres_autorises)
    
        # On regarde quelle touche l'utilisateur utilise et agit en consequence
        if move == saisie.HAUT:
            partie.move_up()
        elif move == saisie.BAS:
            partie.move_down()
        elif move == saisie.DROITE:
            partie.move_right()
        elif move == saisie.GAUCHE:
            partie.move_left()
        elif move == saisie.QUITTER:
            # Si l'utilisateur le souhaite, il peut arreter la partie
            jouer = False
            # On ajoute à la pile l'historique de la partie
            partie.historique.empiler((deepcopy(partie.grille.grille), partie.grille.score))
            print("Voulez-vous pouvoir reprendre la partie plus tard ? (O/N)")
            # On sauvegarde la partie si l'utilisateur le souhaite
            if "o" in input().lower():
                save = True
        elif move == saisie.ANNULER:
            # Si l'utilisateur le souhaite, il peut aller un mouvement en arriere; on vérifie que la pile de l'historique n'est pas vide
            if not partie.historique.est_vide:
                # On dépile le dernier mouvement dans la valeure a 
                a = partie.historique.depiler()
                partie.grille.grille = a[0]
                partie.grille.score = a[1]
        # Si la partie n'est pas en cours et que l'utilisateur n'a pas choisi de continuer la partie
        if partie.go != 0 and partie.go != 3:
            # On arrete la partie
            jouer = False
            # Si l'utilisateur a gagné
            if partie.go == 1:
                # On lui dit en affichant la dernière grille    
                print_grid(partie)
                print("Vous avez gagné!")
                # On lui propose de continuer a jouer malgres sa victoire
                if "o" in input("Voulez-vous continuer la partie ? (O/N):").lower():
                    partie.grille.continued = True
                    # On empeche donc pas la boucle de continuer
                    jouer = True
    
    print_grid(partie)
    
    if jouer == False and partie.go == 0 and save:
        # Quand l'utilisateur a decidé d'arrêter de jouer, on enregistre sa partie
        with open("last_games.bk", "w") as file:
            file.write(str(partie.export()))
    else:
        # Si l'utilisateur a perdu, on affiche un message.
        if partie.go == 2:
            print("Vous avez perdu...")
    
    highscores = classement.scores()
    pot_rank = classement.get_pot_rank(partie.score)
    # On affiche son rang
    print("Vous êtes classé {} sur {}".format(
        pot_rank, len(highscores)+1))
    with open("highscores.txt", "a") as file:
        # On demande le pseudo du joueur
        pseudo = input("Choisissez un pseudo inférieur à 9 caractères:")
        # On vérifie que le pseudo est bien écrit sinon il est redemandé
        while "\n" in pseudo or ";" in pseudo or len(pseudo) > 8 or len(pseudo)*" " == pseudo or pseudo in [x[0] for x in highscores]:
            pseudo = input("Choisissez un pseudo valide et qui n'a pas été déjà utilisé:")
        # On note son pseudo et son score dans le fichier
        file.write("\n" + pseudo + ";" + str(partie.score))
    
    # Si l'utilisateur a le meilleur score
    if pot_rank == 1:
        # On enregistre sa partie comme celle du meilleur score
        with open("historique_meilleur_score.txt", "w") as file:
            file.write(str(partie.export()))
    
    boucle = True
    rejouer = False
    # On propose a l'utilisateur plusieurs choix après la fin de la partie
    while boucle:
        print("Que voulez-vous faire ?")
        print("1) Rejouer")
        print("2) Afficher le classement des meilleurs scores")
        print("3) Afficher l'historique de la partie ayant eu le meilleur score")
        print("4) Quitter")
        choix = int(input("Saisir une option parmi 1/2/3/4:"))
        if choix == 1:
            # On fait rejouer l'utilisateur en relançant la boucle du début
            rejouer = True
            # On sort de cette boucle
            boucle = False
        elif choix == 2:
            # On affiche les meilleurs scores 
            classement.print_highscores()
        elif choix == 3:
          cmd("clear")
          # On affiche l'historique de la partie ayant eu le meilleur score
          classement.historique_meilleur_score()
        else:
            # On ne fait rien et on sort de la boucle, le programme est terminé
          boucle = False
