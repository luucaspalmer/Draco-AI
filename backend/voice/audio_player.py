"""
Draco AI
Audio Player

Responsável por reproduzir arquivos de áudio.
"""

from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioPlayer:


    def play(self, audio_file):

        """
        Reproduz um arquivo WAV.
        """

        audio_file = Path(audio_file)


        if not audio_file.exists():

            raise FileNotFoundError(
                f"Arquivo não encontrado:\n{audio_file}"
            )


        print("\nReproduzindo áudio...\n")


        data, samplerate = sf.read(
            audio_file
        )


        sd.play(
            data,
            samplerate
        )


        sd.wait()


        print(
            "Reprodução finalizada."
        )