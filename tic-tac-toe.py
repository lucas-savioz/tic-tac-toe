# Erreurs lors du 1 vs ordi (l'ordinateur joue deux fois)



# Importation des Modules
from tkinter import *
from tkinter import messagebox
import random  # Ajout pour générer des mouvements de l'ordinateur

# Définition des Variables globales
cases = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
drapeau = True  # True pour les croix, False pour les ronds
n = 1  # Numéro du tour de jeu


# -------------- Définition des Fonctions -------------- #

# Entrées : Un événement de la souris
# Sortie : Affiche en temps réel les coordonnées de la case du clic de souris
def afficher(event):
    global drapeau, cases, n
    o = (event.y - 2) // 100
    a = (event.x - 2) // 100

    if (n < 10) and (cases[o][a] == 0):
        if drapeau:
            dessin.create_line(100 * a + 8, 100 * o + 8, 100 * a + 96, 100 * o + 96, width=5, fill="blue")
            dessin.create_line(100 * a + 8, 100 * o + 96, 100 * a + 96, 100 * o + 8, width=5, fill="blue")
            cases[o][a] = 1
            message.configure(text="Aux ronds de jouer")
        else:
            dessin.create_oval(100 * a + 8, 100 * o + 8, 100 * a + 96, 100 * o + 96, width=5, outline="red")
            cases[o][a] = -1
            message.configure(text="Aux croix de jouer")

        drapeau = not (drapeau)
        if (n >= 5) and (n <= 9):
            somme = verif(cases)
            if somme == 1 or somme == -1:
                n = gagner(somme)
            elif n == 9:
                n = gagner(0)
        n += 1

        # Après que le joueur a joué, vérifiez si c'est le tour de l'ordinateur
        if mode_jeu.get() == "1 vs ordi" and drapeau:
            # Implémentez ici votre logique pour le mouvement de l'ordinateur
            jouer_ordi()


# Entrées : un tableau "carré"
# Sorties : Calcule les sommes de chaque ligne/colonne/diagonale
# et vérifie l"alignement
def verif(tableau):
    # -------------- Champs d'actions possibles -------------- #
    # Il y a 8 sommes à vérifier
    sommes = [0, 0, 0, 0, 0, 0, 0, 0]
    # Les lignes (abscisse)
    sommes[0] = sum(tableau[0])
    sommes[1] = sum(tableau[1])
    sommes[2] = sum(tableau[2])
    # Les colonnes (ordonnée)
    sommes[3] = tableau[0][0] + tableau[1][0] + tableau[2][0]
    sommes[4] = tableau[0][1] + tableau[1][1] + tableau[2][1]
    sommes[5] = tableau[0][2] + tableau[1][2] + tableau[2][2]
    # Les diagonales
    sommes[6] = tableau[0][0] + tableau[1][1] + tableau[2][2]
    sommes[7] = tableau[0][2] + tableau[1][1] + tableau[2][0]
    # Parcours des sommes
    for i in range(8):
        if sommes[i] == 3:
            return 1
        elif sommes[i] == -3:
            return -1
    return 0


# -------------- Gagnant -------------- #

def gagner(a):
    # Indique le gagnant en modifiant le message et affiche une boîte de dialogue
    message = " "
    if a == 1:
        message = "Les croix ont gagné !"
    elif a == -1:
        message = "Les ronds ont gagné !"
    elif a == 0:
        message = "Match nul !"

    messagebox.showinfo("Fin du jeu", message)

    return 9


# Cette fonction ré-initialise les variables globales
def reinit():
    global drapeau, cases, n
    cases = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    # True pour les croix, False pour les ronds
    drapeau = True
    n = 1
    message.configure(text="Aux croix de jouer")
    # Efface toutes les figures
    dessin.delete(ALL)
    lignes = []
    for i in range(4):
        lignes.append(dessin.create_line(0, 100 * i + 2, 303, 100 * i + 2, width=3))
        lignes.append(dessin.create_line(100 * i + 2, 0, 100 * i + 2, 303, width=3))
    if mode_jeu.get() == "1 vs ordi":
        jouer_ordi()


# Fonction pour changer le mode de jeu
def changer_mode():
    if mode_jeu.get() == "1 vs ordi":
        reinit()
    else:
        reinit()


# Nouvelles fonctions pour le mode "1 vs ordi"
def jouer_ordi():
    global drapeau
    if not drapeau:  # Vérifier si c'est le tour du joueur (croix)
        return
    # Implémentez ici votre logique pour le mouvement de l'ordinateur
    mouvement_ordi()


# Implémentez ici votre logique pour le mouvement de l'ordinateur
def mouvement_ordi():
    global cases, n

    # Priorité à la victoire
    victoire = mouvement_gagnant(cases, -1)
    if victoire:
        a, o = victoire
    else:
        # Bloquer le joueur
        blocage = mouvement_gagnant(cases, 1)
        if blocage:
            a, o = blocage
        else:
            # Occuper le centre
            if cases[1][1] == 0:
                a, o = 1, 1
            else:
                # Occupation aléatoire
                mouvement_possible = [(i, j) for i in range(3) for j in range(3) if cases[i][j] == 0]
                if mouvement_possible:
                    a, o = random.choice(mouvement_possible)
                else:
                    # Le plateau est plein, aucune action possible
                    return

    dessin.create_oval(100 * o + 8, 100 * a + 8, 100 * o + 96, 100 * a + 96, width=5, outline='red')
    cases[a][o] = -1
    n += 1
    verifier_et_finir()  # Vérifier si le jeu est terminé après le mouvement de l'ordinateur
    message.configure(text='Aux croix de jouer')


def verifier_et_finir():
    global n
    if n >= 5:  # Ne vérifiez le gagnant qu'à partir du tour 5
        somme = verif(cases)
        if somme == 1 or somme == -1:
            n = gagner(somme)
        elif n == 9:
            n = gagner(0)


def mouvement_gagnant(tableau, symbole):
    # Vérifie si le mouvement peut conduire à la victoire
    for i in range(3):
        for j in range(3):
            if tableau[i][j] == 0:
                # Simuler le mouvement pour vérifier si c'est un mouvement gagnant
                tableau[i][j] = symbole
                if verif(tableau) == symbole:
                    tableau[i][j] = 0  # Annuler le mouvement simulé
                    return i, j
                tableau[i][j] = 0  # Annuler le mouvement simulé
    return None


# -------------- Création de la fenêtre principale -------------- #

# Création de la fenêtre principale
fen_ppale = Tk()
fen_ppale.title("Morpion")

# Création des zones de texte
message = Label(fen_ppale, text="Aux croix de jouer")
message.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky=W + E)

# Création des boutons
bouton_quitter = Button(fen_ppale, text="Quitter", command=fen_ppale.destroy)
bouton_quitter.grid(row=2, column=1, padx=3, pady=3, sticky=S + W + E)

bouton_reload = Button(fen_ppale, text="Recommencer", command=reinit)
bouton_reload.grid(row=2, column=0, padx=3, pady=3, sticky=S + W + E)

# Création du canevas
dessin = Canvas(fen_ppale, bg="white", width=301, height=301)
dessin.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# La grille
lignes = []

# Evenements
dessin.bind("<Button-1>", afficher)

# Menu de sélection du mode de jeu
mode_jeu = StringVar()
mode_jeu.set("1 vs 1")  # Par défaut, le mode est "1 vs 1"
menu_jeu = OptionMenu(fen_ppale, mode_jeu, "1 vs 1", "1 vs ordi")
menu_jeu.grid(row=3, column=0, columnspan=2, pady=5)

# Programme principal
reinit()
fen_ppale.mainloop()