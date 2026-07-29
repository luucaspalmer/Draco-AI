"""
Draco AI
Voice - Wake Word Detector

Responsável por identificar a palavra de ativação "Draco"
a partir de um buffer contínuo de áudio.

Estratégia:

Reaproveita o mesmo motor Faster-Whisper já utilizado pelo
Draco (voice/speech_to_text.py) para transcrever pequenas
janelas de áudio (~1.5s) e verificar se a palavra "draco"
foi pronunciada.

Alternativas para uma solução dedicada e mais eficiente:

- openWakeWord (gratuito, offline, open source), mas exige
  treinar um modelo customizado para a palavra "Draco".
- Porcupine (Picovoice), permite criar wake word customizada
  facilmente, porém depende de uma AccessKey gratuita.

Esta implementação foi escolhida por reaproveitar 100% da
infraestrutura já existente no projeto, sem novas
dependências pesadas. Pode ser substituída no futuro sem
alterar o restante do sistema, bastando manter o método
`detectar()`.
"""

import difflib
import re

import numpy as np


class WakeWordDetector:

    def __init__(
        self,
        speech_to_text,
        wake_word="draco",
        similarity_threshold=0.5,
    ):

        # Reaproveita o modelo já carregado em SpeechToText
        self.model = speech_to_text.model

        self.wake_word = wake_word.lower()
        self.similarity_threshold = similarity_threshold

    def _normalizar(self, texto):

        texto = texto.lower().strip()

        texto = re.sub(r"[^a-zà-ú0-9\s]", "", texto)

        return texto

    def _contem_wake_word(self, texto):

        texto = self._normalizar(texto)

        if not texto:

            return False

        if self.wake_word in texto:

            return True

        for palavra in texto.split():

            similaridade = difflib.SequenceMatcher(
                None, palavra, self.wake_word
            ).ratio()

            if similaridade >= self.similarity_threshold:

                return True

        return False

    def detectar(self, audio_bytes, sample_rate=16000):
        """
        Recebe um buffer de áudio (bytes int16 mono) e
        verifica se a wake word foi pronunciada.
        """

        audio_np = (
            np.frombuffer(audio_bytes, dtype=np.int16)
            .astype(np.float32)
            / 32768.0
        )

        if audio_np.size == 0:

            return False

        segments, _ = self.model.transcribe(
            audio_np,
            language="pt",
            beam_size=1,
            without_timestamps=True,
        )

        texto = " ".join(segment.text for segment in segments)

        if texto.strip():

            print(f"[WakeWord] Ouvido: {texto.strip()}")

        return self._contem_wake_word(texto)