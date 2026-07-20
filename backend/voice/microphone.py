"""
Draco AI
Microphone

Responsável por capturar áudio do microfone
e salvar em formato WAV.
"""

from pathlib import Path

import sounddevice as sd
import soundfile as sf


class Microphone:

    SAMPLE_RATE = 16000
    CHANNELS = 1

    def __init__(self):

        self.audio_dir = Path(__file__).parent / "audio"
        self.audio_dir.mkdir(exist_ok=True)

    def list_devices(self):

        """
        Lista todos os dispositivos de áudio.
        """

        print(sd.query_devices())

    def record(self, seconds=5, filename="input.wav"):

        """
        Grava áudio do microfone.
        """

        output_file = self.audio_dir / filename

        print(f"\nGravando por {seconds} segundos...\n")

        audio = sd.rec(
            int(seconds * self.SAMPLE_RATE),
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            dtype="float32"
        )

        sd.wait()

        sf.write(output_file, audio, self.SAMPLE_RATE)

        print(f"Áudio salvo em:\n{output_file}")

        return output_file