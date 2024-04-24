import subprocess


def convertir_wav(midi_file, soundfont, wav_file):
    subprocess.Popen(f'fluidsynth -ni {soundfont} {midi_file} -F {wav_file} -r 44100', shell=True).wait()
