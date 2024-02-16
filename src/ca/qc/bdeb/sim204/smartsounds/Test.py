import mingus.core.value as valeur
import mingus.core.chords as chords
import random
import mingus.core.scales as gamme
import mingus.core.keys as keys

#changement de tonalité plus tard
class Note:
    nom = ""
    durationStr = valeur.whole
    durationChiffre = 4

    def __init__(self, nom, duration_str, duration_chiffre):
        self.nom = nom
        self.durationStr = duration_str
        self.durationChiffre = duration_chiffre

    def __repr__(self):  # pour changer
        return "<{0}>".format(self.nom)


class Accord:
    tonalite_majeure = "C"
    tonalite_mineure = "c"

    tonalite_majeure_list = keys.major_keys
    # ['Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    tonalite_mineure_list = keys.minor_keys
    # ['ab', 'eb', 'bb', 'f', 'c', 'g', 'd', 'a', 'e', 'b', 'f#', 'c#', 'g#', 'd#', 'a#']

    # majeur
    tonique = chords.I(tonalite_majeure)
    progression_accord_debut_maj = [tonique, chords.first_inversion(tonique), chords.second_inversion(tonique)]
    progression_accord_milieu_maj = []
    for i in chords.triads(tonalite_majeure):
        progression_accord_milieu_maj.append(i)
    progression_accord_fin_maj = [chords.V7(tonalite_majeure), tonique]

    # mineur
    tonique = chords.I(tonalite_mineure)
    print("tonique, mineure", tonique)
    progression_accord_debut_min = [tonique, chords.first_inversion(tonique), chords.first_inversion(tonique),
                                    chords.second_inversion(tonique)]
    progression_accord_milieu_min = []
    for i in chords.triads(tonalite_mineure):
        progression_accord_milieu_min.append(i)
    progression_accord_fin_min = [chords.V7(tonalite_mineure), tonique]

    progression_accord_fin_min = [chords.V7(tonalite_mineure), tonique]
    print(progression_accord_debut_min)


class ProgressionAccords:
    progressionAccords = []
    nombreMesure = 8  # possible de changer
    tonalite = "C"
    ambiance = "majeur"

    def __init__(self, nombreMesure, tonalite, ambiance):

        self.nombreMesure = nombreMesure
        self.tonalite = tonalite
        self.ambiance = ambiance

    def genererProgressionAccords(self):
        numeroMesure = 1


        if self.ambiance == "majeur":
            self.progressionAccords.append(random.choice(Accord.progression_accord_debut_maj))
            for i in range(5):
                self.progressionAccords.append(random.choice(Accord.progression_accord_milieu_maj))
            for i in Accord.progression_accord_fin_min:
                self.progressionAccords.append(i)

        elif self.ambiance == "mineur":
            self.progressionAccords.append(random.choice(Accord.progression_accord_debut_min))
            for i in range(5):
                 self.progressionAccords.append(random.choice(Accord.progression_accord_milieu_min))
            for i in Accord.progression_accord_fin_min:
                self.progressionAccords.append(i)
        print("progression des accords", self.progressionAccords)
        print(len(self.progressionAccords))


test = ProgressionAccords(8, "C", "mineur")
print(test.genererProgressionAccords())
