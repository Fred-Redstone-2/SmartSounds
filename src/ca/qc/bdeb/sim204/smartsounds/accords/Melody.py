import random
import ProgressionAccords
import Rythme


class Melody:
    progression: ProgressionAccords
    nombre_notes_par_mesure: int
    list_notes = []
    rythme: Rythme
    mesure:tuple
    list_bass: list
    propabilite = [3/10, 3/10, 1/5, 1/5]

    def __init__(self, nombre_mesure, tonalite, mesure_utilisateur):
        self.progression = ProgressionAccords.ProgressionAccords(nombre_mesure, tonalite)
        self.rythme = Rythme.Rythme(mesure_utilisateur)
        self.rythme.generer_rythme()
        self.nombre_notes_par_mesure = len(self.rythme.list_duree_note)

        print("nombre de note par mesure: ", self.nombre_notes_par_mesure)

    def generer_melodie(self):

        self.progression.genererProgressionAccords()
        for x in range(len(self.progression.progression)):
            loi_de_probabilite = []
            accord = self.progression.progression[x]

            for a in range(len(accord)):
                note_probabilite = [accord[a], self.propabilite[a]]
                loi_de_probabilite.append(note_probabilite)
            print("probabilité: ", loi_de_probabilite)

            for i in range(self.nombre_notes_par_mesure):
                resultat = random.choices(loi_de_probabilite, weights=[p for _, p in loi_de_probabilite])[0]

                self.list_notes.append(resultat[0])

        self.list_notes[-1] = self.progression.progression[-1][0]
        print("class Melody : ", self.list_notes)
        print("nb de notes totales : ", len(self.list_notes))
'''
    def generer_base_une_note(self):
        #"root" a plus chance d'être choisi que "third", "fifth" should be avoided
        for i in self.progression.progression:
            
            note = random.choice
'''


