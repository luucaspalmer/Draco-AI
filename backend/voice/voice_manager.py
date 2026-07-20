"""
Draco AI
Voice Manager

Orquestra todo o pipeline de voz.

Fluxo:

Áudio
    ↓
Speech To Text
    ↓
Brain
    ↓
Text To Speech
"""

from pathlib import Path

from backend.voice.speech_to_text import SpeechToText
from backend.voice.text_to_speech import TextToSpeech

from backend.brain import pensar


class VoiceManager:


    def __init__(self):

        print("\nInicializando VoiceManager...\n")

        self.speech_to_text = SpeechToText()

        self.text_to_speech = TextToSpeech()

        print("VoiceManager carregado.\n")


    def process(self, audio_path):

        """
        Executa todo o pipeline de voz.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():

            raise FileNotFoundError(audio_path)


        # ==========================
        # Speech To Text
        # ==========================

        texto = self.speech_to_text.transcribe(
            audio_path
        )


        # ==========================
        # Brain
        # ==========================

        resposta = pensar(
            texto
        )


        # ==========================
        # Text To Speech
        # ==========================

        audio_saida = self.text_to_speech.speak(
            resposta
        )


        # ==========================
        # Resultado
        # ==========================

        return {

            "success": True,

            "user_text": texto,

            "response": resposta,

            "audio_file": str(audio_saida)

        }