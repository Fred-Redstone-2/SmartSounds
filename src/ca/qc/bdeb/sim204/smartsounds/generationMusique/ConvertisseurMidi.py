import subprocess


class ConvertisseurMidi:
    @staticmethod
    def convertir_wav(midi_file, soundfont, wav_file):
        subprocess.Popen(f'fluidsynth -ni "%s" {midi_file} -F {wav_file} -r 44100' % soundfont, shell=True).wait()
