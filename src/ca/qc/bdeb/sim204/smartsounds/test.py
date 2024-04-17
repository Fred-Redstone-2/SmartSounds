import Melody

from mingus.containers import *
from mingus.midi import fluidsynth
from resources import directory

'''
rythme = Rythme.Rythme((0,0))
rythme.generer_rythme()
progression = ProgressionAccords.ProgressionAccords(8,"D")
progression.genererProgressionAccords()
'''

melody = Melody.Melody(8, "D", (3, 4))
melody.generer_melodie()

#contrepoint = ContrePoint.ContrePoint(8, "D")
#contrepoint.verifier_melodie()
#contrepoint.verifier_first_specie()
#print(ContrePoint.retourne_cantus_firmus())
#print(ContrePoint.retourne_contrepoint())

# melody.diviser_mesure()
# test
cf = ['F#-3', 'A-3', 'F#-3', 'D-3', 'B-3', 'C#-3', 'A-3', 'D-3']
cf1 = ['D-3', 'C#-3', 'A-3', 'D-3', 'G-3', 'E-3', 'E-3', 'D-3']
cp = ['F#-2', 'A-2', 'A-2', 'D-2', 'B-2', 'C#-2', 'G-2', 'D-2']

sf = directory.ROOT_DIR + r"\FluidR3_GM.sf2"
track = Track()
for note in cf:
    track.add_notes([str(note)])

fluidsynth.init(sf, "dsound")
fluidsynth.play_Track(track)


'''
print("tritone", Core_intervals.measure("C", "F#"))

tout_verifie = False
lst = [10, 8, 7, 4]
if not (10 or -10 or 11 or -11) in lst:
    tout_verifie = True
    print("tout-verifié:    ", tout_verifie)
else:
    print("tout_verifier:    ", tout_verifie)

print(notes_container.Note("C", 3).measure(notes_container.Note("D", 4)))

a = 'B-3'
temp = a[0]
temp = Notes.augment(temp)
temp = Notes.augment(temp)
apres_a = Notes.reduce_accidentals(temp)+"-"+str(int(a[-1])-1)
print(apres_a)

tout_verifie = False
lst = [1, -11, 9]

if not 10 in lst and not -10 in lst and not 11 in lst and not -11 in lst:
    tout_verifie = True
    print("tout-verifié:    ", tout_verifie)
else:
    print("tout_verifier:    ", tout_verifie)



print("--------")
note_cf = "D"
chord = ["D", "F#", "A"]
note_ctp = "F#"
ctp = []
ctp.append(note_ctp)
interval = Core_intervals.determine(note_cf, note_ctp, True)

#print(interval is ("5" or "8" or "1"))
#print(interval is "5" or interval is "8" or interval is "1")
regenere = True
while regenere is True:

    if interval == "5" or interval == "8" or interval == "1":
        regenere = False

    else:
        ctp[0] = random.choice(chord)
        interval = Core_intervals.determine(note_cf, ctp[0], True)
    print(regenere)

print("ctp:  ", ctp[0], "nf: ", note_cf)
print("interval:  ", interval)
'''
