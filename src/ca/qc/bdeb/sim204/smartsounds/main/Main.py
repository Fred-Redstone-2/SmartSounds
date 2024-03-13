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

from_Track_Orig = LilyPond.from_Track

#Cette méthode est tirée de Stack Overflow : https://stackoverflow.com/questions/66215400/how-to-change-the-clef-of-a-container-in-mingus
def from_track(track):
    global from_Track_Orig
    result = from_Track_Orig(track)
    if isinstance(result,str) and track.instrument is not None and isinstance(track.instrument.clef,str):
        result = r"%s \clef %s %s" % (result[:1], track.instrument.clef.split()[0], result[1:])
    return result

class Main:
    soundFont = directory.ROOT_DIR + "\\FluidR3_GM.SF2"
    print(notes.is_valid_note('C'))
    note = diatonic.get_notes("C")
    print(intervals.third("C", "C"))
    print(intervals.determine("E", "A", True))
    print(chords.triad("C", "A"))
    print(chords.dominant("C"))

    fluidsynth.init(soundFont, "dsound")

    LilyPond.from_Track = from_track

    n = Note("C-3")
    chord = NoteContainer(["C-4", "E-4", "G-4", "C-5"])
    chord2 = NoteContainer(["C-2", "C-3"])
    n.channel = 5
    n.velocity = 50
    fluidsynth.play_NoteContainer(chord)
    time.sleep(3)

    i = Instrument()

    b = Bar()
    b.place_notes(chord, 2)
    b2 = Bar()
    b2.place_notes(chord2, 2)

    t1 = Track()
    t2 = Track(i)
    t1.add_bar(b)
    t2.add_bar(b2)

    c = Composition()
    c.set_author('Frederic Mac Conaill')
    title = 'Composition1'
    c.set_title(title)
    c.add_track(t1)
    c.add_track(t2)
    composition = LilyPond.from_Composition(c)
    print(composition)

    LilyPond.to_pdf(composition, title)

    midi = title + ".midi"
    midi_file_out.write_Composition(midi, c)
    ConvertisseurMidi.convertir_midi(midi, soundFont, title + ".wav")


