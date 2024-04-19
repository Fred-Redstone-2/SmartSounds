import mingus.core.intervals as Intervals
import ContrePoint
import ProgressionAccords
import Accord

'''
create another contructor in ContrePoint for Modulation, 
with chords progression alresdy done,
progression should start with pivot chord
or 
usd directly fonctions in ContrePoint
'''


class Modulation:
    tonalite_principale = ""
    tonalite_apparentee = ""
    pivot = "4" #initialiser
    progression: ProgressionAccords
    accords: Accord
    mod: ContrePoint  # pour utiliser les méthodes dans class ContrePoint
    nombre_mesure = 8

    def __init__(self, tonalite):
        self.tonalite_principale = tonalite

    def trouver_pivot(self):  # méthode privée

        if self.tonalite_principale.isupper():  # majeure
            self.tonalite_apparentee = Intervals.perfect_fifth(self.tonalite_principale)
            # to major. related key: dominant, pivot chord: forth (tonic in principal key  = fourth in related key)
            return "4"
        elif self.tonalite_principale.islower():  # mineure
            self.tonalite_apparentee = Intervals.major_sixth(self.tonalite_principale)
            # to major. related key: sixth, pivot chord: major sixth (tonic in principal key = sixth in related key)
            return "6"

    def modulation_en_cours(self):
        self.pivot = self.trouver_pivot()
        self.progression = ProgressionAccords.ProgressionAccords(self.tonalite_apparentee, self.nombre_mesure, self.pivot)
        if not self.progression.progression is None:
            self.progression.generer_progression_accords_modulation()

        mod = ContrePoint.ContrePoint(self.nombre_mesure, self.tonalite_apparentee, self.progression)
        temp = mod.verifier_first_specie()  # cantus_firmus et contrepoint en tonalité apparentée

        return temp[0], temp[1]
