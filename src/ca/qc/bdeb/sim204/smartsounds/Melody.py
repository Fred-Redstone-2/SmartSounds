import random
import ProgressionAccords
import Rythme


class Melody:
    progression: ProgressionAccords
    nombre_notes_par_mesure: int
    list_notes = []
    rythme: Rythme
    mesure: tuple
    list_bass: list
    propabilite = [3 / 10, 3 / 10, 1 / 5, 1 / 5]
    combinaison_duree_note = []

    def __init__(self, tonalite, nombre_mesure, mesure_utilisateur):
        self.progression = ProgressionAccords.ProgressionAccords(tonalite, nombre_mesure)

        self.rythme = Rythme.Rythme(mesure_utilisateur)
        self.rythme.generer_rythme()
        self.nombre_notes_par_mesure = len(self.rythme.list_duree_note)

    def generer_melodie(self):
        Melody.vider_list(self)
        self.progression.generer_preogression_melodie()
        for x in range(len(self.progression.progression)):
            loi_de_probabilite = []
            accord = self.progression.progression[x]

            for a in range(len(accord)):
                note_probabilite = [accord[a], self.propabilite[a]]
                loi_de_probabilite.append(note_probabilite)

            for i in range(self.nombre_notes_par_mesure):
                resultat = random.choices(loi_de_probabilite, weights=[p for _, p in loi_de_probabilite])[0]

                self.list_notes.append(resultat[0])

        self.list_notes[-1] = self.progression.progression[-1][0]

        melodie_temps = Melody.combinaison_melodie_temps(self)
        return melodie_temps, self.progression.progression

    def combinaison_melodie_temps(self):
        combinaison = []
        j = 0
        for i in range(len(self.rythme.list_duree_note)):
            self.rythme.list_duree_note[i] = int(4 / self.rythme.list_duree_note[i])
        for i in range(len(self.list_notes)):
            if j >= len(self.rythme.list_duree_note):
                j = 0
            temp = [self.list_notes[i]]
            note_duree = [self.rythme.list_duree_note[j], temp]
            combinaison.append(note_duree)
        return combinaison

    def diviser_mesure(self):
        self.combinaison_duree_note = Melody.combinaison_melodie_temps(self)
        combinaison_mesure = []
        nb_notes_par_mesure = len(self.rythme.list_duree_note)

        a = 0
        temp = []
        for i in range(len(self.combinaison_duree_note)):

            if a < nb_notes_par_mesure:
                temp.append(self.combinaison_duree_note[i])

                a += 1
                if a == nb_notes_par_mesure:
                    a = 0
                    combinaison_mesure.append(temp)

                    temp = []

    def vider_list(self):
        if len(self.list_notes) != 0:
            self.list_notes = []
