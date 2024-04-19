import random
import Accord


class ProgressionAccords:
    progression = []
    nombreMesure = 8  # possible de changer
    Accord: Accord
    pivot = ""  # initialiser

    def __init__(self, tonalite, nombre_mesure, pivot: str = None):
        if pivot is not None:
            self.nombreMesure = nombre_mesure
            self.tonalite = tonalite
            self.pivot = pivot

            self.Accord = Accord.Accord(self.tonalite)
            self.Accord.generer_acoords_modulation(self.pivot)
            print("constructeur pour modulation")
        elif pivot is None:
            self.nombreMesure = nombre_mesure
            self.tonalite = tonalite

            self.Accord = Accord.Accord(self.tonalite)
            self.Accord.genererAccord()

    def genererProgressionAccords(self):
        ProgressionAccords.vider_list(self)
        # 1 accord au début, 5 au milieu, 2 à la fin
        self.progression.append(self.Accord.progression_accord_debut[0])
        for i in range(5):
            accord = random.choice(self.Accord.progression_accord_milieu)
            self.progression.append(accord)

        for i in self.Accord.progression_accord_fin:
            self.progression.append(i)
        print("class ProgressionAccord: generer progression ", self.progression)

    def generer_progression_accords_modulation(self):
        ProgressionAccords.vider_list(self)

        # 1 accord au début, 6 au milieu, 1 à la fin
        self.progression.append(self.Accord.progression_accord_debut)
        for i in range(6):
            accord = random.choice(self.Accord.progression_accord_milieu)
            self.progression.append(accord)

        self.progression.append(self.Accord.progression_accord_fin)

        print("class ProgressionAccord: progression modulation ", self.progression)

    def vider_list(self):
        if len(self.progression) != 0:
            self.progression = []
