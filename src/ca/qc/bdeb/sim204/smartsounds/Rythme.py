import mingus.core.value as valeur
import random


class Rythme:
    choix_notes = [4 / valeur.whole, 4 / valeur.half, 4 / valeur.quarter, 4 / valeur.eighth]
    # [4.0, 2.0, 1.0, 0.5]
    choix_mesure = [(3, 4), (4, 4), (5, 4)]
    list_duree_note = []
    mesure = ()

    def __init__(self, mesure_utilisateur):
        if mesure_utilisateur not in self.choix_mesure:
            self.mesure = random.choice(self.choix_mesure)
        else:
            self.mesure = mesure_utilisateur

    # generer durée des notes par mesure
    def generer_rythme(self):
        Rythme.vider_list(self)
        i = 0
        while i < self.mesure[0]:
            choix = random.choice(self.choix_notes)
            i += choix

            if i > self.mesure[0]:
                i -= choix
            else:
                self.list_duree_note.append(choix)

    def vider_list(self):
        if len(self.list_duree_note) != 0:
            self.list_duree_note = []
