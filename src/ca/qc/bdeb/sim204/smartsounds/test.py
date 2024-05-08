import Melody
import Modulation
from mingus.containers import *
from mingus.midi import fluidsynth
from resources import directory
import mingus.core.chords as chords
import ContrePoint
import pygame
from mingus.containers import *
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out
import ConvertisseurMidi
import ContrePoint
import random
import Rythme

from resources import directory

from_Track_Orig = LilyPond.from_Track
# une méthode pour generer progression pour class Melody

i = Instrument()
t1 = Track()
t2 = Track(instrument=i)

r = random.choice([True, False])
if r:
    contrepoint = ContrePoint.ContrePoint(8, "C")
    cp = contrepoint.en_tout()
    cp1 = cp[0]
    cp2 = cp[1]
    for i in range(len(cp1)):
        b = Bar()
        b.place_notes(cp1[i], 4)
        t1.add_bar(b)
    for i in range(len(cp2)):
        b = Bar()
        b.place_notes(cp2[i], 4)
        t2.add_bar(b)
else:
    melody = Melody.Melody("D", 4, (4, 4))
    n = melody.generer_melodie()
    n1 = n[0]
    n2 = n[1]
    for i in range(len(n1)):
        b = Bar()
        b.place_notes(n1[i][1][0], n1[i][0])
        t1.add_bar(b)

    for i in range(len(n2)):
        b = Bar()
        b.place_notes(n2[i], 1)
        t2.add_bar(b)

c = Composition()

c.add_track(t1)
c.add_track(t2)
print("composition: ", LilyPond.from_Composition(c))
LilyPond.to_png(LilyPond.from_Composition(c), "contrepoint ou  mélodie-accord")
