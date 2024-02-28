import tkinter as tk
from tkinter import ttk, GROOVE, TOP, X
from tkinter.messagebox import showinfo

root = tk.Tk()
root.title('Séquence Sonore')
root.configure(bg="light blue")
width= root.winfo_screenwidth()
height= root.winfo_screenheight() - 100
root.geometry("%dx%d" % (width, height))

canvas = tk.Canvas(root, width=(width/2), height=height-300, bg='white')
canvas.place(x = 50, y = 50)


#Tonalité Label
textTonalite = tk.Label(root, text="Tonalité :", font=("Eras Demi ITC", 32), bg= "white")
textTonalite.place(x = 150, y =150)

# Tonalité Combobox
n = tk.StringVar()
tonalite = ttk.Combobox(root, width=15, textvariable=n, font=("Eras Demi ITC", 32))
tonalite['values'] = ('Do Maj',
                          'Ré Maj',
                          'Mi Maj',
                          'Fa Maj',
                          'Sol Maj',
                          'La Maj',
                          'Si Maj',
                          'Do# Maj',
                          'Mib Maj',
                          'Fa# Maj',
                          'Lab Maj',
                      'Sib Maj')
tonalite['state'] = 'readonly'
tonalite.place(x =  450, y =150)

tonalite.current(0)


#Tempo Label
textTempo = tk.Label(root, text="Tempo :", font=("Eras Demi ITC", 32), bg= "white")
textTempo.place(x = 150, y =350)

current_value = tk.IntVar()
def get_current_value():
    return '{: .0f}'.format(current_value.get())

value_label = ttk.Label(
    root,
    text=get_current_value(),
    font=("Eras Demi ITC", 32),
    background= 'white'
)

bpm_label = ttk.Label(
    root,
    text="bpm",
    font=("Eras Demi ITC", 28),
    background= 'white'
)

def slider_changed(event):
    value_label.configure(text=get_current_value())

temposlider =ttk.Scale(
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

value_label.place(x=540, y = 325)
bpm_label.place(x= 630, y= 330)
temposlider.place(x = 425, y = 375)



#Durée Label
textDuree = tk.Label(root, text="Durée :", font=("Eras Demi ITC", 32), bg= "white")
textDuree.place(x = 150, y =550)

# Tonalité Combobox
g = tk.StringVar()
duree = ttk.Combobox(root, width=15, textvariable=g, font=("Eras Demi ITC", 32))
duree['values'] = ('4 mesures', '8 mesures', '16 mesures', '32 mesures', '64 mesures')
duree['state'] = 'readonly'
duree.place(x =  450, y =550)

duree.current(0)

root.mainloop()