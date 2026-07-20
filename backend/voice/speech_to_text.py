"""
Draco AI
Speech To Text

Responsável por transformar áudio
em texto utilizando Faster-Whisper.
"""

from pathlib import Path

from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(
        self,
        model_size="base",
        device="cpu",
        compute_type="int8"
    ):

        print("Carregando modelo Whisper...")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

        print("Whisper carregado.")

    def transcribe(self, audio_file):

        audio_file = Path(audio_file)

        if not audio_file.exists():
            raise FileNotFoundError(audio_file)

        print("\nTranscrevendo áudio...\n")

        segments, info = self.model.transcribe(
            str(audio_file),
            language="pt",
            beam_size=5
        )

        texto = ""

        for segment in segments:
            texto += segment.text + " "

        texto = texto.strip()

        print("Texto reconhecido:")
        print(texto)

        return texto