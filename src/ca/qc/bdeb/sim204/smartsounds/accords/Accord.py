
import mingus.core.chords as chords
import random
import mingus.core.scales as gamme
import mingus.core.keys as keys
import Note
#changement de tonalité plus tard
#iter

class Accord:
    tonalite = "C"
    tonalite_majeure = "C#"
    tonalite_mineure = "c#"
    progression_accord_debut = []
    progression_accord_milieu = []
    progression_accord_fin = []

    tonalite_majeure_list = keys.major_keys
    # ['Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    tonalite_mineure_list = keys.minor_keys
    # ['ab', 'eb', 'bb', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#']
    def __init__(self, tonalite):
        self.tonalite = tonalite

    def genererAccord (self):
        # majeur
        tonique = chords.I(self.tonalite)
        self.progression_accord_debut = [tonique]
        for i in chords.triads(self.tonalite):
            self.progression_accord_milieu.append(i)
        self.progression_accord_fin= [chords.V7(self.tonalite), tonique]
'''
        # mineur
        tonique = chords.I(tonalite_mineure)
        print("tonique, mineure", tonique)
        progression_accord_debut_min = [tonique, chords.first_inversion(tonique), chords.first_inversion(tonique),
                                        chords.second_inversion(tonique)]
        progression_accord_milieu_min = []
        for i in chords.triads(tonalite_mineure):
            progression_accord_milieu_min.append(i)
        progression_accord_fin_min = [chords.V7(tonalite_mineure), tonique]
        print(progression_accord_debut_min)
'''




