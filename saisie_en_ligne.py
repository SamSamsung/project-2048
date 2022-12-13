# FONCTIONS DE SAISIE EN LIGNE (sans validation)
# Version pour tout systèmes (de type Windows ou Unix)

# Test déjà si le module python windows msvcrt, et sa fonction getch (pour "Get Character") existe, et sinon, implante une fonction getch avec les librairies Unix


# Importation / création de la fonction getch (pour getch pour "Get Character")
try:
    from msvcrt import getch    # la librairie msvcrt n'existe que sous windows et contient la fonction getch de saisie clavier d'un caractère
except ImportError:             # si la librairie n'existe pas (cas de systèmes UNIX), on crée la fonction getch
    def getch():
        """
        Fonction de détection et de récupération d'une seule touche clavier depuis l'entrée standard (STDIO)
        """
        import sys          # module de fonctions système
        import tty          # module (nécessitant le module termios) de fonctions de gestion du terminal
        import termios      # module de fonctions bas niveau et d'interface UNIX pour le terminal
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def saisir_caractere_en_ligne():
    """
    Fonction de détection et de récupération d'une touche clavier frappée, à partir des deux cas possibles (système windows ou système UNIX)
    """
    caractere_saisi = getch()
    if isinstance(caractere_saisi, bytes):  # si caractere_saisi est de type bytes (cas du getch windows) :
        caractere_saisi = getch().decode()  # il faut utiliser decode() pour en faire une chaine de un caractère
    return caractere_saisi                  # sinon (cas UNIX) : caractere_saisi est déjà de type string


def saisir(L_choix):
    """
    Fonction de saisie en ligne d'un caractère figurant dans la liste des choix autorisés
    Attention : ne permet de saisir qu'un seul caractère, sans appuyer sur entrée
    """
    while True:
        caractere_saisi = saisir_caractere_en_ligne()   # ne permet de saisir qu'un seul caractère, sans valider avec la touche entrée
        try :
            assert caractere_saisi in L_choix           # le caractère saisi doit être dans la liste des caractères autorisés donnée en argument
#            assert condition                            # possibilité de rajouter d'autres assertions : entier dans une plage de valeurs, booléen, etc
            break
        except ValueError:         # exception en cas de mauvaise valeur (utile dans le cas ou on attend un entier, un booléen ou un autre type en particulier)
            pass
        except AssertionError:     # exception si le caractère saisi n'est pas dans la liste (exception provenant de l'instruction assert)
            pass
    return caractere_saisi


def saisir_entree(L_choix):
    """
    Fonction de saisie protégée classique (avec validation par la touche entrée) d'une entrée parmi une liste de choix autorisés
    """
    while True:
        saisie = input("Saisir un mot parmi la liste " + str(L_choix) + " : ")
        try:
            assert saisie in L_choix
            break
        except ValueError:
            print("Entrée non valide. Veuillez recommencer.")
        except AssertionError:
            print("Entrée non valide. Veuillez recommencer.")
    return saisie



# TESTS

if __name__ == '__main__':

    saisir_entree(["oui", "non", "autre"])

    print("\n(appuyer sur entrée pour continuer)")
    input()


    liste_caracteres_autorises = ["a", "b", "f"]    # CHANGER LA LISTE DES CARACTERES AUTORISES
    print("\nVRAI TEST EN STREAM : ATTENTION, SAISIR 'f' EN MINUSCULE POUR SORTIR DU PROGRAMME")
    print("RIEN NE S'AFFICHERA SAUF SI VOUS TAPEZ LES TOUCHES CORRESPONDANTES AUX CARACTERES 'a', 'b' ou 'f' POUR FINIR")
    char = saisir(liste_caracteres_autorises)
    while char != 'f':
        if char == "a":
            print("Vous avez saisi 'a'")
        elif char == "b":
            print("Vous avez saisi 'b'")
        char = saisir(liste_caracteres_autorises)
    print("Vous avez saisi 'f', et c est la fin du test de saisie en ligne")