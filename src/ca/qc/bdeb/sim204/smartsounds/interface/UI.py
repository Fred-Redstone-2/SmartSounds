import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
from mingus.containers import Composition

from PIL import Image, ImageTk

from resources import directory
from src.ca.qc.bdeb.sim204.smartsounds.generationMusique import GenerateurPartition

composition = Composition()
partitionGeneree = False
partition_raw = Image

base_width = 1728
base_height = 918

root = tk.Tk()
root.title('Séquence Sonore')
root.configure(bg="light blue")

multiplicateurX = root.winfo_screenwidth() / base_width
multiplicateurY = root.winfo_screenheight() / base_height
espacementX = 50 * multiplicateurX
taille_texte = int(35 * multiplicateurX)

width = (base_width - 100) * multiplicateurX
height = (base_height - 100) * multiplicateurY
root.resizable(False, False)
root.geometry("%dx%d" % (width, height))

canvas = tk.Canvas(root, width=(width / 2), height=height - 325 * multiplicateurY, bg='white')
canvas.place(x=espacementX, y=50 * multiplicateurY)
root.update()
canvas.pos_fin = canvas.winfo_x() + canvas.winfo_width()

# Tonalité Label
textTonalite = tk.Label(root, text="Tonalité :", font=("Eras Demi ITC", taille_texte), bg="white")
textTonalite.place(x=canvas.winfo_x() + espacementX, y=canvas.winfo_y() + 50 * multiplicateurY)
root.update()

# Tempo Label
textTempo = tk.Label(root, text="Tempo :", font=("Eras Demi ITC", taille_texte), bg="white")
textTempo.place(x=textTonalite.winfo_x(),
                y=textTonalite.winfo_y() + textTonalite.winfo_height() + 100 * multiplicateurY)
root.update()

# Durée Label
textDuree = tk.Label(root, text="Durée :", font=("Eras Demi ITC", taille_texte), bg="white")
textDuree.place(x=textTonalite.winfo_x(), y=textTempo.winfo_y() + textTempo.winfo_height() + 100 * multiplicateurY)

# Tonalité Combobox
n = tk.StringVar()
n2 = tk.StringVar()
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
tonalite.place(x=textTonalite.winfo_x() + textTonalite.winfo_width() + espacementX,
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

# Mesures Combobox
g = tk.StringVar()
duree = ttk.Combobox(root, width=15, textvariable=g, font=("Eras Demi ITC", taille_texte))
duree['values'] = ('4 mesures', '8 mesures', '16 mesures', '32 mesures', '64 mesures')
duree['state'] = 'readonly'
duree.place(x=tonalite.winfo_x(), y=textDuree.winfo_y())
duree.current(0)
root.update()

# Ajuster Majeur/Mineur combobox
majeurOuMineur.place(x=duree.winfo_x() + duree.winfo_width() - majeurOuMineur.winfo_width(),
                     y=textTonalite.winfo_y())

# BPM Slider
current_value = tk.IntVar()


def get_current_value():
    return '{: .0f}'.format(current_value.get())


value_label = ttk.Label(
    root,
    text=get_current_value(),
    font=("Eras Demi ITC", taille_texte),
    background='white'
)

bpm_label = ttk.Label(
    root,
    text="bpm",
    font=("Eras Demi ITC", taille_texte - int(1 * multiplicateurX)),
    background='white'
)


def slider_changed(event):
    value_label.configure(text=get_current_value())


temposlider = ttk.Scale(
    root,
    from_=30,
    to=220,
    orient='horizontal',  # vertical
    command=slider_changed,
    length=duree.winfo_width(),
    variable=current_value
)
temposlider.grid(
    column=1,
    row=0,
    sticky='we'
)
temposlider.set(100)
root.update()

temposlider.place(x=tonalite.winfo_x(), y=textTempo.winfo_y() + textTempo.winfo_height() - temposlider.winfo_height())

value_label.place(x=-100, y=-100)
bpm_label.place(x=-100, y=-100)
root.update()

value_label.place(x=temposlider.winfo_x() + temposlider.winfo_width() / 2 - value_label.winfo_width(),
                  y=temposlider.winfo_y() - value_label.winfo_height())
bpm_label.place(x=temposlider.winfo_x() + temposlider.winfo_width() / 2,
                y=temposlider.winfo_y() - value_label.winfo_height())
temposlider.set(30)


# Bouton GENERER
def generer():
    global composition, partitionGeneree, partition_raw
    composition = GenerateurPartition.generer_partition()
    GenerateurPartition.generer_png(composition)
    partitionGeneree = True
    rafraichir_image()


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
    command=generer
)
btnGenerer.place(x=canvas.winfo_x(), y=canvas.winfo_y() + canvas.winfo_height() + 60 * multiplicateurY)


# Bouton Exporter
def exporter():
    if partitionGeneree:
        GenerateurPartition.exporter(composition)


imgExpo = PhotoImage(file=f"{directory.ROOT_DIR}/Icone_Partager.png")

btnExporter = tk.Button(
    root,
    image=imgExpo,
    width=150 * multiplicateurX,
    height=150 * multiplicateurY,
    command=exporter
)
btnExporter.place(x=-100, y=-100)


# Bouton Jouer
def commande_jouer():
    if partitionGeneree:
        GenerateurPartition.jouer_partition(composition)


jouer = PhotoImage(file=f"{directory.ROOT_DIR}/Icone_Jouer.png")
btnJouer = Button(
    root,
    image=jouer,
    height=150 * multiplicateurY,
    width=150 * multiplicateurX,
    command=commande_jouer
)
btnJouer.place(x=-100, y=-100)
root.update()
btnGenerer.pos_fin = btnGenerer.winfo_x() + btnGenerer.winfo_width()

# Ajustement boutons Jouer et Exporter
btnJouer.place(x=canvas.pos_fin - btnExporter.winfo_width(),
               y=btnGenerer.winfo_y())
root.update()
btnExporter.place(x=btnGenerer.pos_fin / 2 + btnJouer.winfo_x() / 2 - btnExporter.winfo_width() / 2,
                  y=btnGenerer.winfo_y())

# Affichage de la partition
def rafraichir_image():
    global partition_raw, label, largeur_part
    partition_raw = Image.open("Composition1.png")
    hauteur_part = int(height - 50 * multiplicateurY)
    largeur_part = int(partition_raw.width / partition_raw.height * hauteur_part)
    partition_raw = partition_raw.resize((largeur_part, hauteur_part))
    partition = ImageTk.PhotoImage(partition_raw)
    label.configure(image=partition)
    label.image = partition
    label.place(x=canvas.pos_fin / 2 + root.winfo_width() / 2 - partition.width() / 2, y=(height - hauteur_part) / 2 - 10 * multiplicateurY)

largeur_part = 0
label = ttk.Label(root, image=None, padding=5)
root.mainloop()
