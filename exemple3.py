from tkinter import *

app = Tk()

app.geometry("640x480+20+20")
app.title("Titre de la fenêtre")
app.minsize(600, 400)
app.maxsize(1024, 768)

mainFrame = LabelFrame(app, text="titre frame", borderwidth=2, padx=10, pady=10)

mes_labels = []
mes_labels.append(Label(mainFrame, text="Mon label 1"))
mes_labels.append(Label(mainFrame, text="Mon label 2"))

mes_saisies = []
mes_saisies.append(Entry(mainFrame))
mes_saisies.append(Entry(mainFrame))

mes_boutons = []
mes_boutons.append(Button(mainFrame, text=" Oui "))
mes_boutons.append(Button(mainFrame, text=" Non "))

mainFrame.grid(padx=2)

for i, l in enumerate(mes_labels): l.grid(column=i, row=0)
for i, e in enumerate(mes_saisies): e.grid(column=i, row=1, padx=5)
for i, b in enumerate(mes_boutons): b.grid(column=i, row=2, pady=10)

app.mainloop()
print("Fin du code")