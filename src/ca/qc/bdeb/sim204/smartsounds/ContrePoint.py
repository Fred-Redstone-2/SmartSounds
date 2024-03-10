import Melody
import ProgressionAccords
import Rythme
import mingus.core.intervals as intervals
#plus l'instant, il n'y a pas de saut plus grand qu'un octave dans cantus firmus généré( limite de'un octave)
'''
1.Pas de notes répétées dans le cantus firmus (une répétition autorisée en première espèce). 
2. Pas de sauts d’une octave ou plus. 
3. Pas de sauts dissonants. 
4. Entre deux et quatre sauts au total. 
5. Possède un point culminant (note la plus haute) qui n’est pas la tonique ou la sensible. 
6. Change de direction au moins deux fois. 
7. Aucune note répétée plus de 3 fois. 
8. La note finale est approchée par un pas (pas un saut)
9.les sauts plus grands que M3 doivent être suivis d'un changement de direction
'''


class ContrePoint:
    P1 = C = I = Tonic = Unison = 0
    m2 = Db = ii = 1
    M2 = D = II = Step = 2
    m3 = Eb = iii = 3
    M3 = E = III = 4
    P4 = F = IV = 5
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

        for i in self.progression.progression:
            self.list_notes.append(i[0])
        print("list_note: ", self.list_notes)

        self.list_intervals = [intervals.measure(self.list_notes[i], self.list_notes[i + 1]) for i in
                               range(len(self.list_notes) - 1)]
        print("list_intervals: ", self.list_intervals)

        self.leaps = [i for i in self.list_intervals if i > self.Step]
        print("leaps: ", self.leaps)

        def pas_de_repetition():
            if 0 not in self.list_intervals: #vérifier s'il y a de répétition
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
            consonants = [self.M3,self.P4,self.P5,self.m6, self.P8] #pour les gammes majeure
            if not any([i not in consonants for i in self.leaps]):
                return True
            else:
                if verbose is False:
                    print("échec: pas d'intervals dissonants")

        pas_de_repetition()
        pas_de_sauts_plus_grand_que_octave()
        pas_intervals_dissonants()


