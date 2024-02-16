import mingus.core.value as value
class Accord:
    nom = ""
    pulsation = (4, 4) #meter 4/4, 3/4...
    durationStr = value.whole
    durationChiffre = 4

    def __init__(self, nom, pusation, durationStr, durationChiffre):
        self.nom = nom
        self.pulsation = pusation
        self.durationStr = durationStr
        self.durationChiffre = durationChiffre

