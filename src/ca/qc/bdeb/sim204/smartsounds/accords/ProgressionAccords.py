import random
import Accord


class ProgressionAccords:
    progression = []
    nombreMesure = 8  # possible de changer
    tonalite = "C"
    Accord: Accord

    def __init__(self, nombreMesure, tonalite):
        self.nombreMesure = nombreMesure
        self.tonalite = tonalite

        self.Accord = Accord.Accord(tonalite)
        self.Accord.genererAccord()

    def genererProgressionAccords(self):
    #1 accord au début, 5 au milieu, 2 à la fin
         self.progression.append(self.Accord.progression_accord_debut[0])
         for i in range(5):
            accord = random.choice(self.Accord.progression_accord_milieu)
            self.progression.append(accord)

         for i in self.Accord.progression_accord_fin:
            self.progression.append(i)
         print("class ProgressionAccord: ", self.progression)



