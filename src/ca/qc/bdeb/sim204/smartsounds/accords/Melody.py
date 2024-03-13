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

    def __init__(self, nombre_mesure, tonalite, mesure_utilisateur):
        self.progression = ProgressionAccords.ProgressionAccords(nombre_mesure, tonalite)
        self.rythme = Rythme.Rythme(mesure_utilisateur)
        self.rythme.generer_rythme()
        self.nombre_notes_par_mesure = len(self.rythme.list_duree_note)

        print("nombre de note par mesure: ", self.nombre_notes_par_mesure)

    def generer_melodie(self):
        self.progression.genererProgressionAccords()
        for x in range(len(self.progression.progression)):

            for i in range(self.nombre_notes_par_mesure):
                self.list_notes.append(random.choice(self.progression.progression[x]))

        print("class Melody : ", self.list_notes)
        print("nb de notes totales : ", len(self.list_notes))

    def generer_base_une_note(self):
        #"root" a plus chance d'être choisi que "third", "fifth" should be avoided
        for i in self.progression.progression:
            
            note = random.choice



