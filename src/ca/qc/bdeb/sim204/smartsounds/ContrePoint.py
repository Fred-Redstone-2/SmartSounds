import mingus.containers.note as notes
from src.ca.qc.bdeb.sim204.smartsounds import ProgressionAccords
import Rythme
import random
from mingus.core import notes as Core_Notes
from src.ca.qc.bdeb.sim204.smartsounds import Modulation

'''
1.Pas de notes répétées dans le cantus firmus (accepter 2 répétition). 
2. Pas de sauts d’une octave ou plus. 
3. Pas de sauts dissonants. 
4. Entre deux et quatre sauts au total. 
/5. Possède un point culminant (note la plus haute) qui n’est pas la tonique ou la sensible. 
/6. Change de direction au moins deux fois. 
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
Pas de motifs de trois notes répétés. 
'''

cantus_firmus = []
contrepoint = []


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
    s_cf = "-4"  # initialiser octave au centre pour cantus_firmus
    s_cp = "-3"  # initialiser octave plus bas que cantus_firmus pour contrepoint
    progression: ProgressionAccords
    nombre_notes_par_mesure: int
    cantus_firmus = []
    contre_point = []
    rythme: Rythme
    leaps = []
    list_intervals = []
    directions = []
    modulation: Modulation
    m_cf = []  # cantus_firmus en tonalité apparentée
    m_cp = []  # contrepoint en tonalité apparentée
    cf_somme = []  # cantus_firmus en somme
    cp_somme = []  # contrepoint en somme
    en_modulation = False

    def __init__(self, nombre_mesure, tonalite, progression: ProgressionAccords = None):
        if progression is not None:
            self.progression = progression
        else:
            self.progression = ProgressionAccords.ProgressionAccords(tonalite, nombre_mesure)
            if not self.progression.progression is None:
                self.progression.generer_progression_accords()

    def creer_list_notes(self, type):
        if type == "cantus_firmus":
            s = self.s_cf
        if type == "contre_point":
            s = self.s_cp

        list_notes = []

        for i in self.progression.progression:
            list_notes.append(random.choice(i) + s)
        elements = [self.progression.progression[-2][-1], self.progression.progression[-2][0]]
        list_notes[-2] = random.choice(elements) + s
        list_notes[-1] = self.progression.progression[-1][0] + s  # tonique

        return list_notes

    def verifier_melodie(self):

        verifiee = False
        while not verifiee:
            self.cantus_firmus = ContrePoint.creer_list_notes(self, "cantus_firmus")
            self.contre_point = ContrePoint.creer_list_notes(self, "contre_point")
            intervals = [notes.Note(self.cantus_firmus[i]).measure(notes.Note(self.cantus_firmus[i + 1])) for i in
                         range(len(self.cantus_firmus) - 1)]
            print("list_intervals: ", intervals)

            leaps = [i for i in intervals if abs(i) > self.Leap]
            print("leaps: ", leaps)

            def pas_de_repetition():
                if self.cantus_firmus:
                    if intervals.count(0) <= 2:  # accepter 2 répétition
                        return True
                    else:
                        print("échec: trop de répétition dans cantus-firmus")
                        return False
                if self.contre_point:
                    if intervals.count(0) <= 3:
                        return True
                    else:
                        print("échec: trop de répétition dans contrepoint")
                        return False

            def pas_intervals_dissonants():
                intervals_acceptes = [self.M3, self.m3, self.P5, self.M6, self.m6, self.P8, self.M2, self.m2,
                                      self.P1]
                for i in range(len(intervals)):
                    intervals[i] = abs(intervals[i])

                if not any([i not in intervals_acceptes for i in intervals]):
                    return True
                else:

                    print("échec: pas d'intervals dissonants")
                    return False

            def entre_deux_et_quatre_sauts():
                if len(leaps) in [2, 3, 4]:
                    return True
                else:
                    print("échec: trop ou pas assez de sauts")

            def note_finale_aprochee_par_pas():
                if self.en_modulation:
                    return True  # pas cette méthode pour vérifier la modulation
                if self.cantus_firmus:
                    if notes.Note(self.cantus_firmus[-1]).measure(notes.Note(self.cantus_firmus[-2])) >= self.Step:
                        return True
                    else:
                        self.cantus_firmus[-2] = self.progression.progression[-2][2] + self.s_cf
                        print("échec: la note finale approchée par saut")
                        return False
                if self.contre_point:
                    self.contre_point[-2] = self.progression.progression[-2][0] + self.s_cf
                    return True

            # M7, m7 --> m2, M2
            # -10 --> +2, -11 --> +1

            def sauts_trop_large_changer_de_direction():
                tout_verifie = False
                while tout_verifie is False:
                    intervals = [notes.Note(self.cantus_firmus[i]).measure(notes.Note(self.cantus_firmus[i + 1])) for i
                                 in
                                 range(len(self.cantus_firmus) - 1)]
                    self.leaps = [i for i in intervals if abs(i) > self.Leap]
                    if not 10 in leaps and not -10 in self.leaps and not 11 in leaps and not -11 in leaps:
                        tout_verifie = True
                    else:

                        for i in range(len(intervals) - 1):

                            if intervals[i] == -self.m7:  # augementer un M2 au lieu de diminuer un m7
                                n = self.cantus_firmus[i]
                                temp = n[0]
                                temp = Core_Notes.augment(temp)
                                temp = Core_Notes.augment(temp)
                                apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) + 1)
                                self.cantus_firmus[i + 1] = apres_n

                            elif intervals[i] == -self.M7:  # augementer un m2 au lieu de diminuer un M7
                                n = self.cantus_firmus[i]
                                temp = Core_Notes.augment(n[0])
                                apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) + 1)
                                self.cantus_firmus[i + 1] = apres_n

                            elif intervals[i] == self.m7:
                                n = self.cantus_firmus[i]
                                temp = Core_Notes.diminish(n[0])
                                temp = Core_Notes.diminish(temp)
                                apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) - 1)
                                self.cantus_firmus[i + 1] = apres_n

                            elif intervals[i] == self.M7:
                                n = self.cantus_firmus[i]
                                temp = Core_Notes.diminish(n[0])
                                apres_n = Core_Notes.reduce_accidentals(temp) + "-" + str(int(n[-1]) - 1)
                                self.cantus_firmus[i + 1] = apres_n

                            else:
                                print("échec d'analyse")
                                tout_verifie = True
                return tout_verifie

            def pas_de_sauts_plus_grand_que_octave():
                intervals = [notes.Note(self.cantus_firmus[i]).measure(notes.Note(self.cantus_firmus[i + 1])) for i in
                             range(len(self.cantus_firmus) - 1)]
                for i in range(len(intervals)):
                    if intervals[i] >= self.P8:
                        return False
                return True

            def pas_de_mouvement_repete():
                note_repetee = ""
                compteur = 0
                for i in range(len(self.cantus_firmus) - 1):

                    if self.cantus_firmus[i + 1] == self.cantus_firmus[i]:
                        note_repetee = self.cantus_firmus[i]
                        compteur += 1
                        if compteur >= 3:
                            return False
                    else:
                        note_repetee = self.cantus_firmus[i + 1]
                        compteur = 0
                return True

            verifiee = (pas_de_repetition() and entre_deux_et_quatre_sauts()
                        and note_finale_aprochee_par_pas() and sauts_trop_large_changer_de_direction()
                        and pas_de_sauts_plus_grand_que_octave() and pas_de_mouvement_repete()
                        and pas_intervals_dissonants()
                        )

        print("cantus_firmus après changé: ", self.cantus_firmus)
        print("contrepoint après changé: ", self.contre_point)
        return self.cantus_firmus, self.contre_point

    '''
No dissonant vertical intervals.
No vertical intervals larger than a 12th (P8 + P5).
No parallel fifths or octaves.
No parallel three-note chains.
    '''

    def verifier_first_specie(self):

        verifiee = False
        while not verifiee:
            tout = ContrePoint.verifier_melodie(self)
            self.cantus_firmus = tout[0]
            self.contre_point = tout[1]
            print(self.cantus_firmus, " cantus_firmu")
            interval_vertical = [notes.Note(self.contre_point[i]).measure(notes.Note(self.cantus_firmus[i])) for i in
                                 range(len(self.cantus_firmus) - 1)]
            i_v = interval_vertical

            def check_voice_cross():  # traduction
                for i in range(len(interval_vertical)):
                    if interval_vertical[i] < 0:
                        temp = self.cantus_firmus[i]
                        self.cantus_firmus[i] = self.contre_point[i]
                        self.contre_point[i] = temp

            def pas_interval_superieur_a_12():
                for i in range(len(interval_vertical)):
                    if interval_vertical[i] >= (self.P8 + self.P5):
                        print("contient interval plus grand que maj12")
                        return False
                return True

            def pas_interval_parfait_paralle():  # traduction
                for i in range(len(interval_vertical) - 1):
                    if (interval_vertical[i] == self.P5 and interval_vertical[i + 1] == self.P5) or (
                            interval_vertical[i] == self.P8 and interval_vertical[i + 1] == self.P8):
                        print("contient p5 ou p8")
                        return False
                return True

            def pas_de_motifs_de_trois_intervals_repetes():
                for i in range(len(interval_vertical) - 2):
                    if interval_vertical[i] == interval_vertical[i + 1] and interval_vertical[i + 1] == \
                            interval_vertical[i + 2] and interval_vertical[i + 2] == interval_vertical[i + 3]:
                        print("plus que trois intervals répétés et consécutifs")
                        return False
                return True

            def pas_de_dissonance_verticale():
                dissonance = [self.m2, self.M2, self.d5, self.m7, self.M7]
                if any(i in interval_vertical for i in dissonance):
                    print("contient interval dissonant")
                    return False
                return True

            check_voice_cross()
            print("interval_vertical = ", interval_vertical)
            verifiee = (
                    pas_de_dissonance_verticale() and pas_interval_superieur_a_12() and pas_interval_parfait_paralle() and pas_de_motifs_de_trois_intervals_repetes())
        print("verifiee=", verifiee)

        return self.cantus_firmus, self.contre_point

    def modulation(self):
        tonalite = self.progression.tonalite[0] + ""
        self.modulation = Modulation.Modulation(tonalite)
        mod = self.modulation.modulation_en_cours()
        self.m_cf = mod[0]
        self.m_cp = mod[1]
        return self.m_cf, self.m_cp

    def en_tout(self):
        c1 = ContrePoint.verifier_melodie(self)
        c2 = ContrePoint.modulation(self)
        c3 = ContrePoint.verifier_melodie(self)
        self.cf_somme = c1[0] + c2[0] + c3[0]
        self.cp_somme = c1[1] + c2[1] + c3[1]
        print(self.cf_somme)
        print(self.cp_somme)
        return self.cf_somme, self.cp_somme

'''
        if verifiee:
            global cantus_firmus, contrepoint
            cantus_firmus = self.cantus_firmus
            contrepoint = self.contre_point


def retourne_cantus_firmus():
    return cantus_firmus


def retourne_contrepoint():
    return contrepoint
'''
