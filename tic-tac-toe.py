from tkinter import *

#  Définition des Variables
blocks = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
drapeau = True


#  Définition des Fonctions 
def afficher(event):
    global drapeau, blocks
    l = (event.y-2)//100                    # Ligne du clic
    c = (event.x-2)//100                    # Colonne du clic

    if blocks[l][c] == 0:
        if drapeau:
            draw.create_line(100*c+8, 100*l+8, 100*c+96, 100*l+96, width=5, fill='blue')
            draw.create_line(100*c+8, 100*l+96, 100*c+96, 100*l+8, width=5, fill='blue')
            blocks[l][c] = 1
            message.configure(text='Aux ronds de jouer')
        else:
            draw.create_oval(100*c+8, 100*l+8, 100*c+96, 100*l+96, width=5, outline='red')
            blocks[l][c] = -1
            message.configure(text='Aux croix de jouer')

        drapeau = not(drapeau)
        somme = verif(blocks)
        if somme == 1:
            message.configure(text='Les croix ont gagné !')
        elif somme == -1:
            message.configure(text='Les croix ont gagné !')


def verif(tableau):
    sommes = [0, 0, 0, 0, 0, 0, 0, 0]
    sommes[0] = sum(tableau[0])
    sommes[1] = sum(tableau[1])
    sommes[2] = sum(tableau[2])
    sommes[3] = tableau[0][0]+tableau[1][0]+tableau[2][0]
    sommes[4] = tableau[0][1]+tableau[1][1]+tableau[2][1]
    sommes[5] = tableau[0][2]+tableau[1][2]+tableau[2][2]
    sommes[6] = tableau[0][0]+tableau[1][1]+tableau[2][2]
    sommes[7] = tableau[0][2]+tableau[1][1]+tableau[2][0]

    for i in range(8):
        if sommes[i] == 3:
            return 1
        elif sommes[i] == -3:
            return -1
    return 0


def recommencer():
    global drapeau, blocks
    drapeau = True
    blocks = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    draw.delete("all")  # Efface tout le contenu du canevas
    message.configure(text='Aux croix de jouer')


# Création de la fenêtre principale
main_window = Tk()
main_window.title('Morpion')

# Création des zones de texte et des boutons
message = Label(main_window, text='Aux croix de jouer')
message.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky=W+E)

bouton_quitter = Button(main_window, text='Quitter', command=main_window.destroy)
bouton_quitter.grid(row=2, column=1, padx=3, pady=3, sticky=S+W+E)

bouton_reload = Button(main_window, text='Recommencer', command=recommencer)
bouton_reload.grid(row=2, column=0, padx=3, pady=3, sticky=S+W+E)

# Création du canevas
draw = Canvas(main_window, bg="white", width=301, height=301)
draw.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# La grille
lignes = []
for i in range(4):
    lignes.append(draw.create_line(0, 100*i+2, 303, 100*i+2, width=3))
    lignes.append(draw.create_line(100*i+2, 0, 100*i+2, 303, width=3))

# Evenements
draw.bind('<Button-1>', afficher)

# Programme principal
main_window.mainloop()
