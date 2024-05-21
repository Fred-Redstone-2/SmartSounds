import os
from threading import *
from copy import deepcopy

import tkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from mingus.containers import Composition

from PIL import Image, ImageTk

from resources import directory
import GenerateurPartition
import ModificationPartition

## VARIABLES GÉNÉRALES
composition = Composition()
partitionGeneree = False
midi_genere = False
en_gen = False
partition_raw = Image
titreComposition = ""

## FENÊTRE DE BASE
base_width = 1728
base_height = 918

root = tk.Tk()
root.title('Séquence Sonore')
root.configure(bg="light blue")

multiplicateurX = root.winfo_screenwidth() / base_width
multiplicateurY = root.winfo_screenheight() / base_height
taille_texte = int(35 * multiplicateurX)

width = (base_width - 100) * multiplicateurX
height = (base_height - 100) * multiplicateurY
root.resizable(False, False)
root.geometry("%dx%d" % (width, height))


# Supprime le fichier donné
def supprimer(fichier):
    try:
        os.remove(fichier)
    except FileNotFoundError:
        ""


## COMPOSANTS DE LA FENÊTRE
canvas = tk.Canvas(root, width=(width / 2), height=height - 290 * multiplicateurY, bg='white')
canvas.place(x=40 * multiplicateurX, y=30 * multiplicateurY)
root.update()
canvas.pos_fin = canvas.winfo_x() + canvas.winfo_width()

# Tonalité Label
textTonalite = tk.Label(root, text="Tonalité :", font=("Eras Demi ITC", taille_texte), bg="white")
textTonalite.place(x=canvas.winfo_x() + 50 * multiplicateurX, y=canvas.winfo_y() + 50 * multiplicateurY)
root.update()

# Durée Label
textDuree = tk.Label(root, text="Durée :", font=("Eras Demi ITC", taille_texte), bg="white")
textDuree.place(x=textTonalite.winfo_x(),
                y=textTonalite.winfo_y() + textTonalite.winfo_height() + 75 * multiplicateurY)

# Tonalité Combobox
n = tk.StringVar()
n2 = tk.StringVar()
n3 = tk.StringVar()
tonalite = tkinter.ttk.Combobox(
    root,
    width=6,
    textvariable=n,
    font=("Eras Demi ITC", taille_texte)
)

tonalite['values'] = ('Do',
                      'Ré',
                      'Mi',
                      'Fa',
                      'Sol',
                      'La',
                      'Si',
                      'Do♯',
                      'Ré♭',
                      'Mi♭',
                      'Fa♯',
                      'Sol♭',
                      'La♭',
                      'Si♭'
                      )
tonalite['state'] = 'readonly'
tonalite.place(x=textTonalite.winfo_x() + textTonalite.winfo_width() + 50 * multiplicateurX,
               y=textTonalite.winfo_y())
tonalite.current(0)
root.update()

# Majeur/Mineur Combobox
majeurOuMineur = tkinter.ttk.Combobox(
    root,
    width=6,
    textvariable=n2,
    font=("Eras Demi ITC", taille_texte)
)
majeurOuMineur['values'] = ('Maj',
                            'Min')
majeurOuMineur['state'] = 'readonly'
majeurOuMineur.place(x=-100, y=-100)
majeurOuMineur.current(0)


# Force "Majeur" ou "Mineur" selon certaines tonalités
def tonalite_change(event):
    if "Ré♭" in n.get():
        majeurOuMineur['values'] = 'Maj'
        majeurOuMineur.current(0)

    elif "Fa♯" in n.get():
        majeurOuMineur['values'] = 'Min'
        majeurOuMineur.current(0)

    elif "Do♯" in n.get():
        majeurOuMineur['values'] = 'Min'
        majeurOuMineur.current(0)

    elif "Sol♭" in n.get():
        majeurOuMineur['values'] = 'Maj'
        majeurOuMineur.current(0)
    else:
        majeurOuMineur['values'] = ('Maj', 'Min')
        majeurOuMineur.current(0)


tonalite.bind('<<ComboboxSelected>>', tonalite_change)

# Durée Combobox
g = tk.StringVar()
duree = ttk.Combobox(
    root,
    width=15,
    textvariable=g,
    font=("Eras Demi ITC", taille_texte)
)
duree['values'] = ('4 mesures', '8 mesures', '16 mesures', '32 mesures')
duree['state'] = 'readonly'
duree.place(x=tonalite.winfo_x(), y=textDuree.winfo_y())
duree.current(0)
root.update()

# Ajuster Majeur/Mineur combobox
majeurOuMineur.place(x=duree.winfo_x() + duree.winfo_width() - majeurOuMineur.winfo_width(),
                     y=textTonalite.winfo_y())

# Titre de la partition
textTitre = tk.Label(root, text="Titre :", font=("Eras Demi ITC", taille_texte), bg="white")
textTitre.place(x=textTonalite.winfo_x(),
                y=textDuree.winfo_y() + textDuree.winfo_height() + 75 * multiplicateurY)
titre = tk.Text(root,
                bg="white",
                font=("Eras Demi ITC", taille_texte),
                width=20,
                height=1)
titre.place(x=-100, y=-100)
root.update()
titre.place(x=duree.winfo_x() + duree.winfo_width() - titre.winfo_width(),
            y=textTitre.winfo_y())


## GÉNÉRATION DE PARTITION
# Assigne un Thread à la génération de partition, pour que l'interface ne gèle pas
def commande_generer():
    if not en_gen:
        t = Thread(target=generer)
        t.start()


# Génère la partition à partir de la composition générée
def generer():
    global partitionGeneree, titreComposition, en_gen
    if titre.get("1.0", "end-1c") == "":
        tk.messagebox.showinfo("Attention!", "Le titre ne peut pas être vide!")
    else:
        en_gen = True
        titreComposition = titre.get("1.0", "end-1c")
        generer_composition()
        GenerateurPartition.generer_png(composition)
        partitionGeneree = True
        rafraichir_image()
        en_gen = False


# Convertit la tonalité en format international, puis appelle la génération de partition
def generer_composition():
    global composition
    ton = ""
    if 'Do♯' in n.get():
        ton = "C#"
    elif 'Ré♭' in n.get():
        ton = "Db"
    elif 'Mi♭' in n.get():
        ton = "Eb"
    elif 'Fa♯' in n.get():
        ton = "F#"
    elif 'Sol♭' in n.get():
        ton = "Gb"
    elif 'La♭' in n.get():
        ton = "Ab"
    elif 'Si♭' in n.get():
        ton = "Bb"
    elif 'Do' in n.get():
        ton = "C"
    elif 'Ré' in n.get():
        ton = "D"
    elif 'Mi' in n.get():
        ton = "E"
    elif 'Fa' in n.get():
        ton = "F"
    elif 'Sol' in n.get():
        ton = "G"
    elif 'La' in n.get():
        ton = "A"
    elif 'Si' in n.get():
        ton = "B"

    if "Min" in n2.get():
        ton = ton.lower()

    nombre_mesures = int(g.get().removesuffix(' mesures'))
    composition = GenerateurPartition.generer_partition(titreComposition, nombre_mesures, ton)


imgGen = PhotoImage(file=f"{directory.ROOT_DIR}/Note_Musique.png")

btnGenerer = tk.Button(
    root,
    text="Générer",
    width=400 * multiplicateurX,
    height=150 * multiplicateurY,
    font=("Informal Roman", int(63 * multiplicateurX), 'bold'),
    foreground='black',
    image=imgGen,
    compound=tk.LEFT,
    command=commande_generer
)
btnGenerer.place(x=-100, y=-100)

# Combobox de sélection du format d'exportation
format_export = tkinter.ttk.Combobox(
    root,
    width=5,
    textvariable=n3,
    font=("Eras Demi ITC", taille_texte)
)
format_export['values'] = ('PNG',
                           'PDF',
                           'WAV',
                           'MIDI',
                           'MSCZ')
format_export['state'] = 'readonly'
format_export.place(x=-100, y=-100)
format_export.current(0)
root.update()


## EXPORTATION
# Assigne un Thread à l'exportation, pour que l'interface ne gèle pas
def commande_exporter():
    t = Thread(target=exporter)
    t.start()


# Déplace le fichier exporté vers l'endroit sélectionné
def deplacer(path_location):
    format_exp = n3.get().lower()
    if 'MSCZ' in n3.get():
        format_exp = "midi"
    try:
        os.replace("%s.%s" % (composition.title, format_exp), path_location +
                   "\\%s.%s" % (composition.title, format_exp))
        message = ("Exportation en %s réussie!" % format_exp.upper())
    except PermissionError:
        message = "Erreur lors de l'exportation!"
    tk.messagebox.showinfo("Statut de l'exportation", message)


# Choisit, selon le format sélectionné, quelle méthode exécuter pour exporter la partition dans le bon format
def exporter():
    if partitionGeneree:
        if 'MSCZ' in n3.get():
            tk.messagebox.showinfo("Instruction Fichier Musecore",
                                   "Vous n'avez qu'à importer le fichier midi dans MuseScore, et tout fonctionnera parfaitement!")
        path_location = filedialog.askdirectory()
        if 'PNG' in n3.get():
            GenerateurPartition.generer_png(composition)
        elif 'PDF' in n3.get():
            GenerateurPartition.exporter_pdf(composition)
        elif 'WAV' in n3.get():
            GenerateurPartition.exporter_wav(composition)
            supprimer(composition.title + ".midi")
        elif 'MIDI' or 'MSCZ' in n3.get():
            GenerateurPartition.exporter_midi(composition)
        deplacer(path_location)


imgExpo = PhotoImage(file=f"{directory.ROOT_DIR}/Icone_Partager.png")

btnExporter = tk.Button(
    root,
    image=imgExpo,
    width=format_export.winfo_width() - 9 * multiplicateurX,
    height=90 * multiplicateurY,
    command=commande_exporter
)
btnExporter.place(x=-100, y=-100)


## MODIFICATION DE LA PARTITION
def verifier_composition():
    global composition
    if ModificationPartition.composition_changee:
        composition = ModificationPartition.get_composition()
        GenerateurPartition.generer_png(composition)
        rafraichir_image()
    root.after(2000, verifier_composition)


def modifier_partition():
    if partitionGeneree:
        ModificationPartition.launch(root, multiplicateurX, multiplicateurY, taille_texte, composition,
                                     deepcopy(composition))
        root.after(5000, verifier_composition)


imgModif = PhotoImage(f"{directory.ROOT_DIR}/1x1.png")

modifier = Button(
    root,
    text="Modifier la partition",
    font=("Eras Demi ITC", taille_texte),
    width=(majeurOuMineur.winfo_x() + majeurOuMineur.winfo_width() - textTonalite.winfo_x()),
    height=55 * multiplicateurY,
    image=imgModif,
    compound=tk.LEFT,
    command=modifier_partition
)
modifier.place(x=-100, y=-100)


## JOUER LA PARTITION CRÉÉE
# Crée un Thread pour jouer la partition, afin de ne pas faire geler l'interface
def commande_jouer():
    t = Thread(target=jouer)
    t.start()


# Joue la partition générée, puis supprime le fichier utilisé pour la faire jouer
def jouer():
    if partitionGeneree:
        GenerateurPartition.jouer_partition(composition)
        supprimer(composition.title + ".midi")


imgJouer = PhotoImage(file=f"{directory.ROOT_DIR}/Icone_Jouer.png")
btnJouer = tk.Button(
    root,
    image=imgJouer,
    width=210 * multiplicateurX,
    height=150 * multiplicateurY,
    command=commande_jouer
)
btnJouer.place(x=-100, y=-100)

# Ajustement boutons Générer, Jouer et Exporter
btnGenerer.place(x=canvas.winfo_x(),
                 y=(canvas.winfo_y() + canvas.winfo_height()) / 2 + root.winfo_height() / 2 -
                   btnGenerer.winfo_height() / 2)
root.update()
btnJouer.place(x=canvas.pos_fin - btnJouer.winfo_width(),
               y=btnGenerer.winfo_y())
root.update()
btnExporter.place(x=(btnGenerer.winfo_x() + btnGenerer.winfo_width()) / 2 +
                    btnJouer.winfo_x() / 2 - btnExporter.winfo_width() / 2,
                  y=btnGenerer.winfo_y())
root.update()
format_export.place(x=btnExporter.winfo_x(),
                    y=btnGenerer.winfo_y() + btnGenerer.winfo_height() - format_export.winfo_height())
modifier.place(x=textTitre.winfo_x(),
               y=textTitre.winfo_y() + textTitre.winfo_height() + 75 * multiplicateurY)


## AFFICHAGE DE LA PARTITION
# Change l'image de la partition affichée dans l'interface. Cette méthode est en partie tirée de
#   https://python-forum.io/thread-7807.html
def rafraichir_image():
    global partition_raw, label
    nom_image = titreComposition + ".png"
    partition_raw = Image.open(nom_image)
    hauteur_part = int(height - 25 * multiplicateurY)
    largeur_part = int(partition_raw.width / partition_raw.height * hauteur_part)
    partition_raw = partition_raw.resize((largeur_part, hauteur_part))
    partition = ImageTk.PhotoImage(partition_raw)
    label.configure(image=partition)
    label.image = partition
    label.place(x=canvas.pos_fin / 2 + root.winfo_width() / 2 - partition.width() / 2,
                y=(height - hauteur_part) / 2 - 10 * multiplicateurY)
    supprimer(nom_image)


label = ttk.Label(root, image=None, padding=5)

imgIcon = PhotoImage(file=f"{directory.ROOT_DIR}/IconApp.png")
photo = imgIcon
root.wm_iconphoto(False, photo)
root.mainloop()
