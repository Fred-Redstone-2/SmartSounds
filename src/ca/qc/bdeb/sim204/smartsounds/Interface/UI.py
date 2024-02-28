import tkinter as tk
from tkinter import ttk, GROOVE, TOP, X

root = tk.Tk()
root.title('Canvas Demo')
root.configure(bg="light blue")
width= root.winfo_screenwidth()
height= root.winfo_screenheight() - 100
root.geometry("%dx%d" % (width, height))

canvas = tk.Canvas(root, width=(width/2), height=height-100, bg='white')
canvas.place(x = 50, y = 50)

#Label
title = tk.Label(root, text="Tonalité",
                 font=("times new roman", 50, "bold"), bg="white", fg="green")
title.pack(side=TOP, fill=X)

# Combobox creation
n = tk.StringVar()
tonalite = ttk.Combobox(root, width=20, textvariable=n, font="Verdana 16 bold")

# Adding combobox drop down list
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
tonalite.place(x =  600, y =200)




tonalite.current(0)
tonalite.bind('<<ComboboxSelected>>')


root.mainloop()