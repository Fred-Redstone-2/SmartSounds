import random
class Melody:
    progression_accords: list
    nombre_notes_par_mesure: int
    list_notes = []
    def __init__(self, progression_acords: list):
        self.progression_accords = progression_acords
        self.nombre_notes_par_mesure = random.randint(1,8)
        print("nombre de note par mesure: " ,self.nombre_notes_par_mesure )


    def generer_melodie(self):
        for x in range(len(self.progression_accords)):

            for i in range(self.nombre_notes_par_mesure):
                self.list_notes.append(random.choice(self.progression_accords[x]))

        print(self.list_notes)

