import time

from mingus.midi import fluidsynth
import mingus.core.notes as notes
from mingus.containers import *
import mingus.core.keys as diatonic
import mingus.core.intervals as intervals
import mingus.core.chords as chords
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out
from ConvertisseurMidi import ConvertisseurMidi

from resources import directory

class Main:
    soundFont = directory.ROOT_DIR + "\\FluidR3_GM.SF2"
    print(notes.is_valid_note('C'))
    note = diatonic.get_notes("C")
    print(intervals.third("C", "C"))
    print(intervals.determine("E", "A", True))
    print(chords.triad("C", "A"))
    print(chords.dominant("C"))

    fluidsynth.init(soundFont, "dsound")

    n = Note("C-3")
    chord = NoteContainer(["C-2", "C-3", "C-4", "E-4", "G-4", "C-5"])
    n.channel = 5
    n.velocity = 50
    fluidsynth.play_NoteContainer(chord)

    b = Bar()
    b + "C"
    bar = LilyPond.from_Bar(b)
    midi = "song.midi"
    midi_file_out.write_Bar(midi, b)
    ConvertisseurMidi.convertir_midi(midi, soundFont, "song.wav")

