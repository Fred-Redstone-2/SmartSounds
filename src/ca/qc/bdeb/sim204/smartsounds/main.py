import time

from mingus.midi import fluidsynth
import mingus.core.notes as notes
from mingus.containers import *
import mingus.core.keys as diatonic
import mingus.core.intervals as intervals
import mingus.core.chords as chords

from resources import directory

print(notes.is_valid_note('C'))

note = diatonic.get_notes("C")


print(intervals.third("C", "C"))

print(intervals.determine("E", "A", True))

print(chords.triad("C", "A"))

print(chords.dominant("C"))

fluidsynth.init(directory.ROOT_DIR + "\\FluidR3_GM.SF2", "dsound")

n = Note("C-3")
chord = NoteContainer(["C-2", "C-3", "C-4", "E-4", "G-4", "C-5"])
n.channel = 5
n.velocity = 50
fluidsynth.play_NoteContainer(chord)
time.sleep(3)
