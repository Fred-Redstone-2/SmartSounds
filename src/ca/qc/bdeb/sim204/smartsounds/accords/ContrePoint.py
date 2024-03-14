import mingus.containers.note as notes
import ProgressionAccords
import Rythme
import random
from mingus.core import notes as Core_Notes

# plus l'instant, il n'y a pas de saut plus grand qu'un octave dans cantus firmus généré( limite d'un octave)
# revoir tranpose() in #10
'''
1.Pas de notes répétées dans le cantus firmus (accepter 2 répétition). 
2. Pas de sauts d’une octave ou plus. 
3. Pas de sauts dissonants. 
4. Entre deux et quatre sauts au total. 
/5. Possède un point culminant (note la plus haute) qui n’est pas la tonique ou la sensible. 
/6. Change de direction au moins deux fois. 
/7. Aucune note répétée plus de 3 fois. 
8. La note finale est approchée par un pas (pas un saut)
/9.les sauts plus grands que M3 doivent être suivis d'un changement de direction 
        *** si a note après et M2/m2 dans la même direction, changer après cela,
         sinon, changer de direction. 
         si c'est M3/m3, pas obligé de changer direction 
10. ( ++ M7/m7 --> M2/m2)
/La sensible(leadingTone) doit toujours être suivie de la tonique.
/Pas plus de deux sauts consécutifs dans la même direction.   ***
/Le même intervalle ne peut pas se produire deux fois de suite.
/Pas de “noodling” (c’est-à-dire des motifs tels que N1 N2 N1 N2, pour certaines notes N1 et N2). ***
/Pas de séquences de plus de quatre notes consécutives.
/Pas de tension mélodique non résolue (c’est-à-dire que la note de départ et la note de fin de chaque séquence doivent être consonantes ensemble).
/Pas de motifs de trois notes répétés. 
'''


class ContrePoint:
    P1 = C = I = Tonic = Unison = 0
    m2 = Db = ii = 1
    M2 = D = II = Step = 2
    m3 = Eb = iii = Skip = 3
    M3 = E = III = 4
    P4 = F = IV = Leap = 5  # leap = P4, d5, P5, m6, M6
    d5 = Gb = Vo = Tritone = 6
    P5 = G = V = 7
    m6 = Ab = vi = 8
    M6 = A = VI = 9
    m7 = Bb = vii = 10
    M7 = Bb = VII = LeadingTone = 11
    P8 = O = Octave = 12
    progression: ProgressionAccords
    nombre_notes_par_mesure: int
    list_notes = []
    rythme: Rythme
    leaps = []
    list_intervals = []
    directions = []

    def __init__(self, nombre_mesure, tonalite):
        self.progression = ProgressionAccords.ProgressionAccords(nombre_mesure, tonalite)

    def verifier_melodie(self, verbose=False):
        print("class ContrePoint, method verifier_melodie: ", self.progression.progression)

        s = "-3"  # initialiser octave au centre
        for i in self.progression.progression:
            self.list_notes.append(random.choice(i) + s)
        self.list_notes[-2] = self.progression.progression[-2][1] + s or self.progression.progression[-2][2] + s
        self.list_notes[-1] = self.progression.progression[-1][0] + s  # tonique
        print("list_note: ", self.list_notes)

        self.list_intervals = [notes.Note(self.list_notes[i]).measure(notes.Note(self.list_notes[i + 1])) for i in
                               range(len(self.list_notes) - 1)]
        print("list_intervals: ", self.list_intervals)

        self.leaps = [i for i in self.list_intervals if abs(i) > self.Leap]
        print("leaps: ", self.leaps)

        def pas_de_repetition():
            if self.list_intervals.count(0) <= 2:  # accepter 2 répétition
                return True
            else:
                if verbose is False:
                    print("échec: pas de répétition dans cantus firmus")

        def pas_de_sauts_plus_grand_que_octave():
            if not any(i >= self.P8 for i in self.leaps):
                return True
            else:
                if verbose is False:
                    print("échec: pas de saut plus grand qu'un octave")

        def pas_intervals_dissonants():
            consonants = [self.M3, self.P4, self.P5, self.m6, self.P8]  # pour les gammes majeure
            if not any([i not in consonants for i in self.leaps]):
                return True
            else:
                if verbose is False:
                    print("échec: pas d'intervals dissonants")

        def entre_deux_et_quatre_sauts():
            if len(self.leaps) in [2, 3, 4]:
                return True
            else:
                if verbose is False:
                    print("échec: trop ou pas assez de sauts")

        def note_finale_aprochee_par_pas():
            if notes.Note(self.list_notes[-1]).measure(notes.Note(self.list_notes[-2])) >= self.Step:
                return True
            else:
                if verbose is False:
                    print("échec: la note finale approchée par saut")

        # M7, m7 --> m2, M2
        # -10 --> +2, -11 --> +1

        def sauts_trop_large_changer_de_direction():
            tout_verifie = False
            while tout_verifie is False:
                self.list_intervals = [notes.Note(self.list_notes[i]).measure(notes.Note(self.list_notes[i + 1])) for i
                                       in
                                       range(len(self.list_notes) - 1)]
                self.leaps = [i for i in self.list_intervals if abs(i) > self.Leap]
                if not 10 in self.leaps and not -10 in self.leaps and not 11 in self.leaps and not -11 in self.leaps:
                    tout_verifie = True
                    print("tout-verifié: ", tout_verifie, "leaps: ", self.leaps)

                else:
                    print("tout-verifie: ", tout_verifie, "leap: ", self.leaps)
                    for i in range(len(self.list_intervals) - 1):
                        print(self.list_intervals[i])
                        if self.list_intervals[i] == -self.m7:  # augementer un M2 au lieu de diminuer un m7
                            n = self.list_notes[i]
                            temp = n[0]
                            temp = Core_Notes.augment(temp)
                            temp = Core_Notes.augment(temp)
                            apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) + 1)
                            self.list_notes[i + 1] = apres_n
                            print("apres_n: ", apres_n)

                        elif self.list_intervals[i] == -self.M7:  # augementer un m2 au lieu de diminuer un M7
                            n = self.list_notes[i]
                            temp = Core_Notes.augment(n[0])
                            apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) + 1)
                            self.list_notes[i + 1] = apres_n
                            print("apres_n: ", apres_n)
                        elif self.list_intervals[i] == self.m7:
                            n = self.list_notes[i]
                            temp = Core_Notes.diminish(n[0])
                            temp = Core_Notes.diminish(temp)
                            apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) - 1)
                            self.list_notes[i + 1] = apres_n
                            print("apres_n: ", apres_n)
                        elif self.list_intervals[i] == self.M7:
                            n = self.list_notes[i]
                            temp = Core_Notes.diminish(n[0])
                            apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) - 1)
                            self.list_notes[i + 1] = apres_n
                            print("apres_n: ", apres_n)
                        else:
                            print("échec d'analyse")
                            tout_verifie = True
                print("list_note après changé: ", self.list_notes)


        pas_de_repetition()
        pas_de_sauts_plus_grand_que_octave()
        pas_intervals_dissonants()
        entre_deux_et_quatre_sauts()
        note_finale_aprochee_par_pas()
        sauts_trop_large_changer_de_direction()
