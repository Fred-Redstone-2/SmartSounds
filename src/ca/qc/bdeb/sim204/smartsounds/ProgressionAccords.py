import random
import Accord
class ProgressionAccords:
    progressionAccords = []
    nombreMesure = 8  # possible de changer
    tonalite = "C"
    #ambiance = "majeur"
    Accord: Accord


    def __init__(self, nombreMesure, tonalite):
        self.nombreMesure = nombreMesure
        self.tonalite = tonalite

        self.Accord = Accord.Accord(tonalite)
        self.Accord.genererAccord()



    def genererProgressionAccords(self):
    #1 accord au début, 5 au milieu, 2 à la fin
            self.progressionAccords.append(random.choice(self.Accord.progression_accord_debut))
            for i in range(5):
                self.progressionAccords.append(random.choice(self.Accord.progression_accord_milieu))
            for i in self.Accord.progression_accord_fin:
                self.progressionAccords.append(i)
'''
        elif self.ambiance == "mineur":
            gh = Accord.progression_accord_debut_min
            self.progressionAccords.append(random.choice())
            for i in range(5):
                 self.progressionAccords.append(random.choice(Accord.progression_accord_milieu_min))
            for i in Accord.progression_accord_fin_min:
                self.progressionAccords.append(i)

        print("progression des accords", self.progressionAccords)
        print(len(self.progressionAccords))
'''