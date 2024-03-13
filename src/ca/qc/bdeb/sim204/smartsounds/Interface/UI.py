import tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.title('Séquence Sonore')
root.configure(bg="light blue")
width = 0.90*1920
height = 0.90*1020
root.resizable(False, False)
root.geometry("%dx%d" % (width, height))

canvas = tk.Canvas(root, width=(width / 2), height=height - 300, bg='white')
canvas.place(x=50, y=50)


# Tonalité Label
textTonalite = tk.Label(root, text="Tonalité :", font=("Eras Demi ITC", 32), bg="white")
textTonalite.place(x=150, y=150)

# Tonalité Combobox
n = tk.StringVar()
n2 = tk.StringVar()
tonalite = tkinter.ttk.Combobox(
    root,
    width=6,
    textvariable=n,
    font=("Eras Demi ITC", 32)
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
tonalite.place(x=450, y=150)
tonalite.current(0)

majeurOuMineur = tkinter.ttk.Combobox(
    root,
    width=6,
    textvariable=n2,
    font=("Eras Demi ITC", 32)
)
majeurOuMineur['values'] = ('Maj',
                           'Min')
majeurOuMineur['state'] = 'readonly'
majeurOuMineur.place(x=650, y=150)
majeurOuMineur.current(0)

def tonalite_change(event):
    if "Ré♭" in n.get() :
        majeurOuMineur['values'] = 'Maj'
        majeurOuMineur.current(0)

    elif "Fa♯" in n.get() :
        majeurOuMineur['values'] = 'Min'
        majeurOuMineur.current(0)

    elif "Do♯" in n.get() :
        majeurOuMineur['values'] = 'Min'
        majeurOuMineur.current(0)

    elif "Sol♭" in n.get() :
        majeurOuMineur['values'] = 'Maj'
        majeurOuMineur.current(0)


tonalite.bind('<<ComboboxSelected>>', tonalite_change)


# Tempo Label
textTempo = tk.Label(root, text="Tempo :", font=("Eras Demi ITC", 32), bg="white")
textTempo.place(x=150, y=350)

current_value = tk.IntVar()


def get_current_value():
    return '{: .0f}'.format(current_value.get())


value_label = ttk.Label(
    root,
    text=get_current_value(),
    font=("Eras Demi ITC", 32),
    background='white'
)

bpm_label = ttk.Label(
    root,
    text="bpm",
    font=("Eras Demi ITC", 28),
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
    length=440,
    variable=current_value
)
temposlider.grid(
    column=1,
    row=0,
    sticky='we'
)
temposlider.set(30)

value_label.place(x=540, y=325)
bpm_label.place(x=630, y=330)


temposlider.place(x=425, y=375)

# Durée Label
textDuree = tk.Label(root, text="Durée :", font=("Eras Demi ITC", 32), bg="white")
textDuree.place(x=150, y=550)

# Tonalité Combobox
g = tk.StringVar()
duree = ttk.Combobox(root, width=15, textvariable=g, font=("Eras Demi ITC", 32))
duree['values'] = ('4 mesures', '8 mesures', '16 mesures', '32 mesures', '64 mesures')
duree['state'] = 'readonly'
duree.place(x=450, y=550)
duree.current(0)

# Bouton GENERER

imgGen = PhotoImage(file = "U+266B_a.svg (1).png")

btnGenerer = tk.Button(
    root,
    text="Générer",
    width = 500,
    height = 150,
    font=("Informal Roman", 60, 'bold'),
    foreground = 'black',
    image = imgGen,
    compound=tk.LEFT
)
btnGenerer.place(x = 150, y = 700)

# Button Exporter

imgExpo = PhotoImage(file= "expo-ezgif.com-webp-to-png-converter.png")

btnExporter = tk.Button(
    root,
    image= imgExpo,
    width = 150,
    height=150
)
btnExporter.place(x = 700, y = 700)

# Affichage de la partition
partition = PhotoImage(file = "O_Canada_sheet_music.png")
imgPart = ttk.Label(
    root,
    image=partition,
    padding=5
)
imgPart.place(x = 1100, y = 25)

# Bouton Jouer
jouer = PhotoImage(file="play-button-6 (1).png")
btnJouer = Button(
    root,
    image=jouer,
    height = 100,
    width= 100
)
btnJouer.place(x = 1300, y = 785)

root.mainloop()
