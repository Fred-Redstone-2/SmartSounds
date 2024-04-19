import mingus.core.intervals as Intervals
import ContrePoint
import ProgressionAccords
'''
create another contructor in ContrePoint for Modulation, 
with chords progression alresdy done,
progression should start with pivot chord
or 
usd directly fonctions in ContrePoint
'''
class modulation:
    tonalite_principale = ""
    tonalite_apparentee: ""
    pivot = ""
    def __init__(self,nombre_mesure, tonalite):
        self.tonalite_principale = tonalite

    def modulation_en_cours(self):

        tonalite_apparentee = ""
        if self.tonalite_principale.isupper():  # majeure
            self.tonalite_apparentee = Intervals.perfect_fifth(self.tonalite_principale)
            # to major. related key: dominant, pivote chord: forth (tonique in principal key  = fourth in related key)
            print(self.tonalite_apparentee, " = tonalité apparentée")
        elif self.tonalite_principale.islower():  # mineure
            self.tonalite_apparentee = Intervals.minor_third(self.tonalite_principale)
            # to major. related key: third, pivote chord: major third (third in principal key = tonique in related key)
