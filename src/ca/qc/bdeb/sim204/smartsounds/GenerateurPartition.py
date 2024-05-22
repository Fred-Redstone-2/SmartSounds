import pygame
import random
from mingus.containers import *
import mingus.extra.lilypond as LilyPond
from mingus.midi import midi_file_out

import ConvertisseurMidi
import ContrePoint
import Melody
from resources import directory

from_Track_Orig = LilyPond.from_Track


# Cette méthode est tirée de Stack Overflow : https://stackoverflow.com/questions/66215400/how-to-change-the-clef-of-a-container-in-mingus
def from_track(track):
    global from_Track_Orig
    result = from_Track_Orig(track)
    if isinstance(result, str) and track.instrument is not None and isinstance(track.instrument.clef, str):
        result = r"%s \clef %s %s" % (result[:1], track.instrument.clef.split()[0], result[1:])
    return result


# Génère la partition et la retourne en format mingus
def generer_partition(titre, nombre_mesures, tonalite):
    LilyPond.from_Track = from_track

    i = Instrument()
    t1 = Track()
    t2 = Track(instrument=i)

    r = random.choice([True, False])
    if r:
        contrepoint = ContrePoint.ContrePoint(nombre_mesures, tonalite)
        cp = contrepoint.en_tout()
        cp1 = cp[0]
        cp2 = cp[1]
        for i in range(len(cp1)):
            t1.add_notes(cp1[i], 4)
        for i in range(len(cp2)):
            t2.add_notes(cp2[i], 4)
    else:
        melody = Melody.Melody(tonalite, nombre_mesures, (4, 4))
        n = melody.generer_melodie()
        n1 = n[0]
        n2 = n[1]
        for i in range(len(n1)):
            t1.add_notes(n1[i][1][0], int(n1[i][0]))
        for i in range(len(n2)):
            t2.add_notes(n2[i], 1)

    c = Composition()
    c.set_author("Generated by SmartSounds")
    c.title = titre
    c.set_title(c.title)
    c.add_track(t1)
    c.add_track(t2)
    return c


# Joue le fichier MIDI donné
def play_music(music_file):
    # Cette méthode est tirée de https://www.daniweb.com/programming/software-development/code/216979/embed-and-play-midi-music-in-your-code-python
    clock = pygame.time.Clock()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


# Prépare la composition donnée à être jouée
def jouer_partition(partition):
    midi = exporter_midi(partition)
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    play_music(midi)


# Convertit la partition dans le bon format pour LilyPond
def convertir_partition(partition):
    c = LilyPond.from_Composition(partition)
    header = c.split("}")[0] + "}"
    accompagnement = c.split("\\clef bass")[1]
    melodie = c.split("{ {")[1].split("} }")[0].strip()

    upper = melodie.replace("{", "").strip().replace("}", "")
    lower = accompagnement.replace("{", "").strip().replace("}", "")

    staff = " {\n\\new PianoStaff << \n"
    staff += "  \\new Staff { \\clef treble " + upper + " }\n"
    staff += "  \\new Staff { \\clef bass " + lower + "}\n"
    staff += ">>\n}\n"

    resultat = '\\version "2.25.10"\n' + header + staff
    return resultat


# Convertit la composition en image PNG avec LilyPond
def generer_png(partition):
    LilyPond.to_png(convertir_partition(partition), partition.title)


# Prépare la composition donnée à être convertie en WAV
def exporter_wav(partition):
    sf = directory.ROOT_DIR + "\\FluidR3_GM.SF2"
    midi = exporter_midi(partition)
    ConvertisseurMidi.convertir_wav(midi, sf, partition.title + ".wav")


# Convertit la composition donnée en midi
def exporter_midi(partition):
    midi = partition.title + ".midi"
    midi_file_out.write_Composition(midi, partition)
    return midi


# Convertit la composition donnée en PDF par LilyPond
def exporter_pdf(partition):
    LilyPond.to_pdf(convertir_partition(partition), partition.title)
