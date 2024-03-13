import mingus.core.value as valeur
'''
note

'''
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

