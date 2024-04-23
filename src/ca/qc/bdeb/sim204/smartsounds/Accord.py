import mingus.core.chords as chords
import mingus.core.keys as tonalites


class Accord:
    tonalite = "C"
    progression_accord_debut = []
    progression_accord_milieu = []
    progression_accord_fin = []

    tonalite_majeure_list = tonalites.major_keys
    # ['Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    tonalite_mineure_list = tonalites.minor_keys

    # ['ab', 'eb', 'bb', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#']
    def __init__(self, tonalite):
        self.tonalite = tonalite

    def genererAccord(self):
        print("class Accords: accords: ")
        # majeur
        tonique = chords.tonic(self.tonalite)
        self.progression_accord_debut = [tonique]
        for i in chords.triads(self.tonalite):
            self.progression_accord_milieu.append(i)
        self.progression_accord_fin = [chords.V7(self.tonalite), tonique]

    def generer_acoords_modulation(self, pivot, accords):
        n = []
        if pivot == "4":  # tonalité associé en dominant, majeure
            n = accords[3]

        elif pivot == "6":
            n = accords[4]

        # begin and end with pivot
        self.progression_accord_debut = n

        accords_milieu = chords.triads(self.tonalite)

        for i in accords_milieu:
            self.progression_accord_milieu.append(i)
        self.progression_accord_fin = n
