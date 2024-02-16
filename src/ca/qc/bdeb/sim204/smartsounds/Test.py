import mingus.core.value as valeur
import mingus.core.chords as chords
import random
class Accord:
    nom = ""
    pulsation = (4, 4) #meter 4/4, 3/4...
    durationStr = valeur.whole
    durationChiffre = 4

    def __init__(self, nom, pusation, durationStr, durationChiffre):
        self.nom = nom
        self.pulsation = pusation
        self.durationStr = durationStr
        self.durationChiffre = durationChiffre

    def __repr__(self): #for changing
        return "<{0}>".format(self.nom)

class AccordDefinition:
    tonalite = "C"
    def __init__(self, tonalite):
        self.tonalite = tonalite

    tonique = chords.tonic(tonalite)
    progression_accord_debut = [tonique, chords.first_inversion(tonique), chords.second_inversion(tonique)]

    print(progression_accord_debut)
class ProgressionAccords:
    progressionAccords = []
    nombreMesure = 8 #possible de changer
    def __init__(self, nombreMesure):

        self.nombreMesure = nombreMesure

    def genererAccords(self):
        numeroMesure = 1

      #  while (numeroMesure < self.nombreMesure - 2): #2 dernière mesures -> cadance
           # if numeroMesure == 1:
               # self.progressionAccords.append(random.sample())


accords_C_majeur_tonique = AccordDefinition("C")
print(accords_C_majeur_tonique)




