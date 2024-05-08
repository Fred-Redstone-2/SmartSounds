from copy import deepcopy
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *

from mingus.containers import Composition, Bar, Note

var = Bar()
index = 0
indexMesure = 0
indexPortee = 0
composition = Composition()
composition_changee = False


def reinitialiser(comp):
    global composition, index, composition_changee, indexPortee, indexMesure, var
    composition = deepcopy(comp)
    index = 0
    indexPortee = 0
    indexMesure = 0
    var = composition[indexPortee][indexMesure]
    composition_changee = True
    ajuster_infos_notes()


def ajuster_infos_notes():
    portee.configure(text="Portée : " + str(indexPortee + 1))
    mesure.configure(text="Mesure : " + str(indexMesure + 1))
    note.configure(text="Note : " + str(var[index][2][0]).replace("\'", ""))
    no_note.configure(text="Position : " + str(index + 1))
    type_note.configure(text="Type : " + str(chiffre_a_type(var[index][1])))
    composition[indexPortee][indexMesure] = var


def augmenter():
    global var
    note_augmentee = Note(var[index][2][0])
    note_augmentee.augment()
    if note_augmentee == Note("C#-8"):
        tkinter.messagebox.showinfo("Attention!", "Vous avez atteint la limite du clavier!")
    else:
        var[index][2][0] = note_augmentee
        verifier_note()
        ajuster_infos_notes()


def diminuer():
    global var
    note_diminuee = Note(var[index][2][0])
    note_diminuee.diminish()
    if note_diminuee == Note("Ab-0"):
        tkinter.messagebox.showinfo("Attention!", "Vous avez atteint la limite du clavier!")
    else:
        var[index][2][0] = note_diminuee
        verifier_note()
        ajuster_infos_notes()


def reduire():
    global var
    duree = int(var[index][1])
    if duree < 8:
        var[index][1] = var[index][1] * 2
        position = var[index][0] + 1 / var[index][1]
        mesure_en_list = []
        for x in var:
            mesure_en_list.append(x)
        nouvelle_mesure = [position, var[index][1], var[index][2]]
        mesure_en_list.insert(index + 1, nouvelle_mesure)
        var = Bar(mesure_en_list)
        for x in mesure_en_list:
            var.place_notes(x[2][0], x[1])
        ajuster_infos_notes()
    else:
        tkinter.messagebox.showinfo("Attention!", "La note ne peut pas être plus courte qu'une croche!")


def convertir_croches():
    mesure_croche = []
    for i in var:
        duree_note = i[1]
        if duree_note == 1:
            for j in range(8):
                mesure_croche.append([i[2], 8])
        if duree_note == 2:
            for j in range(4):
                mesure_croche.append([i[2], 8])
        if duree_note == 4:
            for j in range(2):
                mesure_croche.append([i[2], 8])
        if duree_note == 8:
            mesure_croche.append([i[2], 8])
    return mesure_croche


def allonger():
    global var, index
    duree_init = var[index][1]
    if duree_init == 1:
        tkinter.messagebox.showinfo("Attention", "La note ne peut pas être plus longue qu'une ronde!")
    else:
        mesure_finale = Bar()
        mesure_croches = convertir_croches()
        note_allongee = [var[index][2], duree_init / 2]

        # Blanches --> Rondes
        if 1 / note_allongee[1] == 1:
            index = 0
            mesure_finale.place_notes(note_allongee[0], 1)

        # Reste : 2 autres cas - Croche --> Noire, Noire --> Blanche
        # Combinaison vers l'avant
        # Var = [Note1 :[position (0.25), durée (1/2/4/8), [Notes]], Note2 :[position (0.25), durée (1/2/4/8), [Notes]]]
        else:
            combinaison_avant = var[index][0] + 1 / note_allongee[1] <= 1
            mesure_a_arranger = []
            liste_notes_orig = []
            notes_a_placer = []
            duree_totale = 0

            # Configuration des éléments selon le type de combinaison
            if combinaison_avant:
                for pos in range(index):
                    mesure_finale.place_notes(var[pos][2], var[pos][1])
                for element in var:
                    mesure_a_arranger.append(element)
                index_placer = index + 1
            else:
                temp = []
                for x in range(len(mesure_croches)):
                    temp.append(mesure_croches[len(mesure_croches) - x - 1])
                mesure_croches = temp
                for x in range(len(var)):
                    mesure_a_arranger.append(var[len(var) - x - 1])
                index_placer = 1

            for note_finale in range(index_placer - 1):
                duree_totale += 1 / mesure_a_arranger[note_finale][1]

            # Détermination de l'endroit où commencer à sélectionner les notes à recombiner
            if mesure_a_arranger[index_placer - 1][1] == mesure_a_arranger[index_placer][1]:
                index_placer += 1
            elif mesure_a_arranger[index_placer - 1][1] < mesure_a_arranger[index_placer][1]:
                k = index_placer
                while mesure_a_arranger[index_placer - 1][1] < mesure_a_arranger[k][1] or k == len(mesure_a_arranger):
                    index_placer += 1
                    k += 1
            if not combinaison_avant and index != len(var) - 1:
                index_placer += 1
            while index_placer < len(mesure_a_arranger):
                liste_notes_orig.append([mesure_a_arranger[index_placer][2], mesure_a_arranger[index_placer][1]])
                index_placer += 1

            # Remplissage des notes à placer
            mesure_finale.place_notes(note_allongee[0], note_allongee[1])
            position = duree_totale + 1 / note_allongee[1]
            while position < 1:
                notes_a_placer.append([mesure_croches[int(position * 8)][0], mesure_croches[int(position * 8)][1]])
                position += 0.125

            # Recombinaison des notes à placer
            x = 0
            index_croche = 0
            while x < len(liste_notes_orig):
                nb_croches = 0
                if liste_notes_orig[x][1] == 8:
                    mesure_finale.place_notes(liste_notes_orig[x][0], liste_notes_orig[x][1])
                    index_croche += 1
                else:
                    j = index_croche
                    while j < len(notes_a_placer):
                        if notes_a_placer[j][0] == liste_notes_orig[x][0]:
                            nb_croches += 1
                            index_croche += 1
                        else:
                            break
                        j += 1

                    if nb_croches != 0:
                        if nb_croches == 5:
                            mesure_finale.place_notes(liste_notes_orig[x][0], 8)
                            mesure_finale.place_notes((liste_notes_orig[x][0]), 4)
                            mesure_finale.place_notes((liste_notes_orig[x][0]), 4)
                            if liste_notes_orig[x][1] == liste_notes_orig[x + 1][1]:
                                x += 2
                            else:
                                x += 1
                        elif nb_croches == 3:
                            mesure_finale.place_notes(liste_notes_orig[x][0], 8)
                            mesure_finale.place_notes(liste_notes_orig[x][0], 4)
                            if liste_notes_orig[x][1] != 2:
                                x += 1
                        # 1 / liste_notes_orig[x][1] = 1 / 2 = 0.5
                        # nb_croches / 8 = 2 / 8 = 0.25
                        else:
                            mesure_finale.place_notes(liste_notes_orig[x][0],
                                                      1 / min(1 / liste_notes_orig[x][1], nb_croches / 8))
                x += 1

            # Inversement de la mesure si combinaison vers l'arrière
            if not combinaison_avant:
                temp = Bar()
                for x in range(len(mesure_finale)):
                    temp.place_notes(mesure_finale[len(mesure_finale) - x - 1][2],
                                     mesure_finale[len(mesure_finale) - x - 1][1])
                mesure_finale = temp
                index = len(mesure_finale) - 1

        var = mesure_finale
        ajuster_infos_notes()


def note_suivante():
    global index
    global var
    global indexMesure

    index = index + 1

    if index > len(composition[indexPortee][indexMesure]) - 1:
        index = 0
        indexMesure = indexMesure + 1

        if indexMesure > len(composition[indexPortee]) - 1:
            indexMesure = len(composition[indexPortee]) - 1
            index = len(composition[indexPortee][indexMesure]) - 1
            tkinter.messagebox.showinfo("Attention!",
                                        "Vous êtes à la limite de votre composition. On ne peut pas aller plus loin.")
        else:
            var = composition[indexPortee][indexMesure]
    ajuster_infos_notes()


def note_precedente():
    global index
    global var
    global indexMesure

    index = index - 1

    if index < 0:
        index = len(composition[indexPortee][indexMesure]) - 1
        indexMesure = indexMesure - 1

        if indexMesure < 0:
            indexMesure = 0
            index = 0
            tkinter.messagebox.showinfo("Attention!",
                                        "Vous êtes à la limite de votre composition. On ne peut pas aller plus loin.")
        else:
            var = composition[indexPortee][indexMesure]
    ajuster_infos_notes()


def verifier_note():
    global index
    note_verifier = str(var[index][2][0])
    octave = int(note_verifier[-2:-1])
    if "C##" in note_verifier:
        var[index][2][0] = 'D-' + str(octave)
    elif "D##" in note_verifier:
        var[index][2][0] = 'E-' + str(octave)
    elif "E#" in note_verifier:
        var[index][2][0] = 'F-' + str(octave)
    elif "F##" in note_verifier:
        var[index][2][0] = 'G-' + str(octave)
    elif "G##" in note_verifier:
        var[index][2][0] = 'A-' + str(octave)
    elif "A##" in note_verifier:
        var[index][2][0] = 'B-' + str(octave)
    elif "B#" in note_verifier:
        octave = octave + 1
        var[index][2][0] = 'C-' + str(octave)
    elif "Cb" in note_verifier:
        octave = octave - 1
        var[index][2][0] = 'B-' + str(octave)
    elif "Dbb" in note_verifier:
        var[index][2][0] = 'C-' + str(octave)
    elif "Ebb" in note_verifier:
        var[index][2][0] = 'D-' + str(octave)
    elif "Fb" in note_verifier:
        var[index][2][0] = 'E-' + str(octave)
    elif "Gbb" in note_verifier:
        var[index][2][0] = 'F-' + str(octave)
    elif "Abb" in note_verifier:
        var[index][2][0] = 'G-' + str(octave)
    elif "Bbb" in note_verifier:
        var[index][2][0] = 'A-' + str(octave)


def chiffre_a_type(chiffre):
    duree = ""
    if chiffre == 1:
        duree = "Ronde (4 temps)"
    elif chiffre == 2:
        duree = "Blanche (2 temps)"
    elif chiffre == 4:
        duree = "Noire (1 temps)"
    elif chiffre == 8:
        duree = "Croche (½ temps)"
    return duree


def changer_portee():
    global indexPortee, var
    if indexPortee == 0:
        indexPortee = 1
    else:
        indexPortee = 0
    var = composition[indexPortee][indexMesure]
    ajuster_infos_notes()


def confirmer():
    global composition_changee
    composition_changee = True


def launch(root, x, y, taille_texte, comp, base_comp):
    global portee, mesure, note, no_note, type_note
    top = Toplevel(root)
    top.geometry("%dx%d" % (x, y))
    top.title("Modification de partition")

    btn = Button(
        top,
        text="Augmenter",
        command=lambda: augmenter()
    )
    btn2 = Button(
        top,
        text="Diminuer",
        command=lambda: diminuer()
    )
    btn3 = Button(
        top,
        text="Allonger",
        command=lambda: allonger()
    )
    btn4 = Button(
        top,
        text="Réduire",
        command=lambda: reduire()
    )
    btn5 = Button(
        top,
        text="Suivante",
        command=lambda: note_suivante()
    )
    btn6 = Button(
        top,
        text="Précédente",
        command=lambda: note_precedente()
    )
    btn7 = Button(
        top,
        text="Changer de portée",
        width=24,
        command=lambda: changer_portee()
    )
    btn8 = Button(
        top,
        text="Réinitialiser",
        width=24,
        command=lambda: reinitialiser(base_comp)
    )
    btn9 = Button(
        top,
        text="Confirmer",
        width=24,
        command=lambda: confirmer()
    )
    portee = Label(
        top,
        font=("Eras Demi ITC", taille_texte)
    )
    mesure = Label(
        top,
        font=("Eras Demi ITC", taille_texte)
    )
    note = Label(
        top,
        font=("Eras Demi ITC", taille_texte)
    )
    no_note = Label(
        top,
        font=("Eras Demi ITC", taille_texte)
    )
    type_note = Label(
        top,
        font=("Eras Demi ITC", taille_texte)
    )
    reinitialiser(comp)
    text_x = 30
    base_text_y = 10
    base_x_btn = 420
    base_y_btn = 30
    btn.place(x=base_x_btn, y=base_y_btn)
    btn2.place(x=base_x_btn + 80, y=base_y_btn)
    btn3.place(x=base_x_btn, y=base_y_btn + 40)
    btn4.place(x=base_x_btn + 80, y=base_y_btn + 40)
    btn5.place(x=base_x_btn, y=base_y_btn + 80)
    btn6.place(x=base_x_btn + 80, y=base_y_btn + 80)
    btn7.place(x=base_x_btn + 1, y=base_y_btn + 120)
    btn8.place(x=base_x_btn + 1, y=base_y_btn + 160)
    btn9.place(x=base_x_btn + 1, y=base_y_btn + 200)
    portee.place(x=text_x, y=base_text_y)
    mesure.place(x=text_x, y=base_text_y + 50)
    note.place(x=text_x, y=base_text_y + 100)
    no_note.place(x=text_x, y=base_text_y + 150)
    type_note.place(x=text_x, y=base_text_y + 200)


def get_composition_changee():
    return composition_changee


def get_composition():
    global composition_changee
    composition_changee = False
    return composition
