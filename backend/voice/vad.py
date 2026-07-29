"""
Draco AI
Voice - Voice Activity Detection (VAD)

Responsável por detectar quando o usuário está falando
e quando termina de falar.

Solução escolhida: webrtcvad
- Gratuita
- Offline
- Leve (não requer download de modelo)
- Amplamente utilizada em sistemas de voz

Alternativa mais robusta (não utilizada por padrão, mas
compatível com esta mesma interface): Silero VAD, baseado
em rede neural, mais preciso em ambientes ruidosos, porém
mais pesado.
"""

import webrtcvad


class VoiceActivityDetector:

    def __init__(self, sample_rate=16000, aggressiveness=2):
        """
        aggressiveness: 0 (mais permissivo) a 3 (mais agressivo
        em filtrar ruído/silêncio).
        """

        if sample_rate not in (8000, 16000, 32000, 48000):

            raise ValueError(
                "webrtcvad só aceita 8000, 16000, 32000 ou 48000 Hz"
            )

        self.sample_rate = sample_rate
        self.vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, frame_bytes):
        """
        Verifica se um frame de áudio contém fala.
        O frame deve ter duração de 10, 20 ou 30ms.
        """

        try:

            return self.vad.is_speech(frame_bytes, self.sample_rate)

        except Exception:

            return False